import socket
import threading 
from threading import Thread, Lock
import pyfiglet
from queue import Queue 
import requests

queue = Queue()

PortsOpen = []

banner = pyfiglet.figlet_format("CobaltSpider")
print(banner)

Select = int(input('''
             
(1) Port Scanner 
(2) Subdomain Scanner
             
Select mode: '''))

if Select == 1: 
    InputIP = input("Input the IP address: ")

    ScanMode = int(input('''
                
    (1) Ports up to 1024 
    (2) Ports up to 492152
    (3) Most Common ports 
    (4) Custom port amount
                
    Select scanner mode: '''))

    ThreadNumber = int(input("\nSelect number of threads: "))

    target = socket.gethostbyname(InputIP)   

    
    print("-" * 50)
    print("Scanning target: " + target)
    print("-" * 50)

    def portScan(port):
        try: # tests a block of code for errors
               
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((target, port)) # connect.ex returns 0 if connection to port is succesful.
            #banner2 = s.recv(1024).decode()
            
            return True
        except:
            return False        
            
    def selectPorts(mode):
        if mode == 1: 
            for port in range(1,1024):
                queue.put(port)    
        elif mode == 2: 
            for port in range(1, 492152):
                queue.put(port)  
        elif mode == 3:
            ports = [20, 21, 22, 23, 25, 53, 80, 110, 443]
            queue.put(ports)
        elif mode == 4: 
            ports = input("enter the ports to scan (seperate with space): ")
            ports = ports.split() # split takes a string and makes it a list 
            ports = list(map(int, ports)) # lists store multiple items in one variable, map applies int to all ports
            for port in ports: 
                queue.put(ports)
                
    def worker():
        while not queue.empty(): # as long as queue is not empty, the next element is scanned , if that port is open, prints port open. 
            port = queue.get()
            
            if portScan(port): 
                
                print("port {} is open".format(port))
                PortsOpen.append(port)
            
    def Run_scanner(threads, mode):
        
        selectPorts(mode)
        
        ThreadedList = []
        
        for t in range(threads):
            thread = threading.Thread(target = worker)
            ThreadedList.append(thread)
        
        for thread in ThreadedList:
            thread.start() # starts threading 
        
        for thread in ThreadedList:
            thread.join() # waits until thread times out 
            
        print("open ports are:", PortsOpen)
        
    Run_scanner(ThreadNumber, ScanMode)

elif Select == 2:
    
    domain = input("Input the domain to scan: ")
    
    n_threads = int(input("Input number of threads: "))
    
    file = open("subdomains.txt")
    
    q = Queue()
    
    list_lock = Lock()
    
    DiscovoredDomains = []
    
    def SubdomainScan(domain):
        global q 
        
        subdomain = q.get()
        
        url = f"http://{subdomain}.{domain}"
        try: 
            requests.get(url)
        except requests.ConnectionError:
            pass
        else: 
            
            print("[+] Discovered Subdomain", url)
            
            with list_lock:
                DiscovoredDomains.append(url)
                
        q.task_done()
    
    def main(domain, n_threads, subdomains):
        global q
        
        for subdomain in subdomains: 
            q.put(subdomain)
            
        for t in range(n_threads):
            worker = Thread(target = SubdomainScan(domain))
        
            worker.deamon = True
            
            worker.start()
            
    main(domain = domain, n_threads = n_threads, subdomains=file.read().splitlines())
       
    with open("Discovered_subdomain.txt", "w")as f:
        for url in DiscovoredDomains:
            print(url, file=f)

#elif Select == 3:
    
    
         
        
            
            

