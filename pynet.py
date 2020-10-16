# Author: Sina Tamari 
# Website: sinatamari.pythonanywhere.com
# Telegram: @sina_tamari
# Email: cissp.it@gmail.com
# Python: 2.7
import os
import sys
import threading
import time
import subprocess
import socket
class PyNet:
    def __init__(self):
        # this nmap_threads is verry important in nmap scan speed. If you have a powerfull computer with good 
        # internet bandwidth, try a bigger number, for me the 50 is max
        self.__nmap_threads = 50
        # this masscan_threads will use by masscan tool with --rate command
        self.__masscan_threads = 10
        self.__tor_running_ports = []
        # this will create tor listenner, not tor processes, because we are not going to use Multitor anymore
        self.__number_of_tor_processes = 5
        # true format is: self.__ips = [ IP1 , IP2 ]
        self.__ips = []
        # true format is: self.__masscan_results = { IP1: [ PORT1, PORT2, PORT3, ... ], IP2: [ PORT1, PORT2, PORT3, ... ], ... }
        self.__masscan_results = {}
        self.__nmap_threads_window = []
        self.__nmap_number_of_proccessed_ips = 0
        self.__nmap_is_writing = False
        self.__stop_printing_dots = True
        self.__initialize()
    def __handle_keyboard_interrupt(self):
        self.__stop_printing_dots = True
        time.sleep(1)
        self.__print("Exiting ",dots=True)
        time.sleep(2)
        self.__stop_printing_dots = True
        time.sleep(1)
        sys.exit(0)
    def __initialize(self):
        """
        Initializing program ...
        checking root priviledges, checking installed packages, ...
        """
        self.__introduction()
        self.__check_root_priviledge()
        self.__check_internet_connection()
        self.__check_packages()
    def __print_with_dots(self,message,mtype="n"):
        """message:        => string message
        mtype:      
                    "n" => normal
                    "e" => error
                    "w" => warning   
        """
        try:
            self.__stop_printing_dots = False
            dots = ['.','. .','. . .','                                          ']
            i = 0
            W = '\033[0m'
            R = '\033[31m'
            G = '\033[32m'
            O = '\033[33m'
            P = '\033[35m'
            BOLD = '\033[1m'
            THIN = '\033[1m'
            if mtype == "n":
                while not self.__stop_printing_dots:
                    sys.stderr.write('\r'+BOLD+P+'[ '+G+'+'+P+' ] '+O+message+THIN+ dots[i])
                    i += 1
                    if i == 4:
                        i = 0
                        sys.stderr.write('\r'+BOLD+P+'[ '+G+'+'+P+' ] '+O+message+THIN)
                    time.sleep(0.1)
                sys.stderr.write('\r                                                  \n')
            elif mtype == "e":
                while not self.__stop_printing_dots:
                    sys.stderr.write('\r'+BOLD+P+'[ '+G+'+'+P+' ] '+O+message+THIN+ dots[i])
                    i += 1
                    if i == 4:
                        i = 0
                    time.sleep(0.1)
                sys.stderr.write('\r                                                  \n')
            elif mtype == "w":
                while not self.__stop_printing_dots:
                    sys.stderr.write('\r'+BOLD+P+'[ '+G+'+'+P+' ] '+O+message+THIN+ dots[i])
                    i += 1
                    if i == 4:
                        i = 0
                    time.sleep(0.1)
                sys.stderr.write('\r                                                  \n')
            else:
                while not self.__stop_printing_dots:
                    sys.stderr.write('\r'+BOLD+P+'[ '+G+'+'+P+' ] '+O+message+THIN+ dots[i])
                    i += 1
                    if i == 4:
                        i = 0
                    time.sleep(0.1)
                sys.stderr.write('\r                                                  \n')
        except:
            pass
    def __introduction(self):
        os.system('clear')
        W = '\033[0m'
        R = '\033[31m'
        G = '\033[32m'
        O = '\033[33m'
        P = '\033[35m'
        BOLD = '\033[1m'
        THIN = '\033[1m'
        message = BOLD+"""
     \033[31m        ________  \033[33m          \033[31m       ___        __ \033[33m           \033[33m          
     \033[31m       / ______ \ \033[33m          \033[31m      / _ \      / / \033[33m           \033[33m          
     \033[31m      / /     / / \033[33m_      __ \033[31m     / / \\\     / / \033[33m           \033[33m      __
     \033[31m     / /_____/ /  \033[33m\\\    / /\033[31m     / /  \\\    / / \033[33m    ____   \033[33m   ___/ /__
     \033[31m    / /_______/   \033[33m \\\  / / \033[31m    / /   \\\   / /  \033[33m   / __ \  \033[33m  /__/ /__/
     \033[31m   / /            \033[33m  \\\/ /  \033[31m   / /    \\\  / /   \033[33m  / /__\_| \033[33m    / /
     \033[31m  / /             \033[33m   / /    \033[31m / /     \\\_/ /     \033[33m \ \____   \033[33m  / /_
     \033[31m /_/              \033[33m  /_/     \033[31m/ /      \\___/      \033[33m  \____/   \033[33m /_/_/
                                \033[31m/ /                 
                        \033[33mAuthor \033[31m/ / \033[33mSina Tamari
                      \033[33mWebsite \033[31m/ / \033[33mhttps://sinatamari.pythonanywhere.com
                    \033[33mTelegram \033[31m/ / \033[33mhttps://t.me/sina_tamari
                      \033[33mEmail \033[31m/ / \033[33mcissp.it@gmail.com
                           \033[31m/_/ \033[33m  
 

        """
        print message
    def __print(self,message,mtype="n",dots=False):
        """message:        => string message     
        mtype:      
                    "n" => normal
                    "e" => error
                    "w" => warning   
        """
        W = '\033[0m'
        R = '\033[31m'
        G = '\033[32m'
        O = '\033[33m'
        P = '\033[35m'
        BOLD = '\033[1m'
        THIN = '\033[1m'
        if dots:
            t = threading.Thread(target=self.__print_with_dots,args=(message,mtype))
            t.start()
        else:
            if mtype == "n":
                print BOLD+P+'[ '+G+'+'+P+' ] '+O+message+THIN
            elif mtype == "e":
                print BOLD+P+'[ '+R+'!'+P+' ] '+O+message+THIN
            elif mtype == "w":
                print BOLD+P+'[ '+R+'?'+P+' ] '+O+message+THIN
            else:
                print BOLD+P+'[ '+W+'+'+P+' ] '+O+message+THIN 
    def __check_root_priviledge(self):
        """
        Checking root priviledges using 'whoami' command.
        Exiting if user is not root.
        """
        out,failed_error = self.__execute(['whoami'])
        if out != 'root\n':
            self.__print('Need root priviledges to run.','e')
            sys.exit(1)
    def __check_internet_connection(self):
        host = '8.8.8.8'
        port = 53
        timeout = 3
        try:
            socket.setdefaulttimeout(timeout)
            s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            s.connect((host,port))
            return True
        except:
            self.__print("No internet connections",'e')
            sys.exit(1)
    def __execute(self,commands=[]):
        """
        Running command using subprocess module with Popen.

        commands => list of commands, for example: ['ls'] or ['ping','-c','10','192.168.1.1'] or ...

        returns => results of executing commands as string.
        """
        if len(commands) <= 0:
            return ""
        try:
            out = subprocess.Popen(commands,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            stdout = out.stdout.read()
            stderr = out.stderr.read()
            return stdout,stderr
        except KeyboardInterrupt:
            self.__handle_keyboard_interrupt()
        except:
            return ""
    def __check_packages(self):
        try:
            failed_package = ''
            failed_error = ""
            packages = ['python-pip','ivre','mongodb','python-pymongo','python-crypto','tor','nmap','masscan','proxychains','curl','obfs4proxy']
            self.__print("Checking packages")
            for pkg in packages:
                self.__stop_printing_dots = True
                self.__print('Processing '+pkg)
                # processing each package ...
                if self.__is_installed(pkg):
                    self.__print("Package "+pkg+" DONE")
                elif not self.__is_installed(pkg):
                    self.__stop_printing_dots = True
                    self.__print('Installing '+pkg+' ',dots=True)
                    # installing the package ...
                    if pkg == 'ivre':
                        cmd = ['sudo','pip','install','ivre']
                        out,failed_error = self.__execute(cmd)
                    else:
                        out,failed_error = self.__execute(['sudo','DEBIAN_FRONTEND=noninteractive','apt-get','install',pkg,'--yes'])
                    self.__stop_printing_dots = True
                # checking the installation  of the package ...
                if not self.__is_installed(pkg):
                    # unable to install the package
                    failed_package = pkg
                    self.__stop_printing_dots = True
                    time.sleep(1)
                    break
                self.__stop_printing_dots = True
                time.sleep(1)
            self.__stop_printing_dots = True
            # ckecking if there is an uninstalled package
            if failed_package != '':
                self.__print('Unable to install '+failed_package,'e')
                self.__print(str(failed_error),mtype='w')
                raise KeyboardInterrupt
            else:
                self.__print('Packages are ready')  
        except:
            self.__handle_keyboard_interrupt()
    def __is_installed(self,pkg_name=""):
        """
        returns True if the package was installed, otherwise returns False.
        pkg_name => string package name
        """
        if not pkg_name or pkg_name == "":
            return False
        out,err = self.__execute(['apt-cache','policy',pkg_name])
        if not out or out == "":
            if pkg_name in os.listdir('/usr/local/bin/'):
                return True
            return  False
        out = out.split('\n')[1].split('Installed: ')[1]
        if out == "(none)":
            return False
        return True
    def RUN(self,ips=[]):
        if not isinstance(ips,list):
            self.__print('Error: ip range should be list',mtype='e')
            self.__handle_keyboard_interrupt()
        if len(ips) <= 0 or not self.__ip_range_is_valid(ips):
            self.__print('Error: ip range is not valid',mtype='e')
            self.__handle_keyboard_interrupt()
        self.__run_tor()
        self.__config_proxychains()
        self.__run_masscan()
        self.__extract_masscan_results()
        self.__run_nmap()
        self.__import_nmap_outputs_into_ivre()
        self.__run_ivre_webserver()
    def __ip_range_is_valid(self,ips=[]):
        if len(ips) != 2:
            return False
        import re
        patern = r"^[0-9]{1}[0-9]?[0-9]?\.[0-9]{1}[0-9]?[0-9]?\.[0-9]{1}[0-9]?[0-9]?\.[0-9]{1}[0-9]?[0-9]?$"
        for ip in ips:
            x = re.search(patern,ip)
            if x == None:
                return False
            ip_parts = ip.split(".")
            for part in ip_parts:
                if int(part) > 255:
                    return False
            self.__ips.append(str(int(ip_parts[0]))+'.'+str(int(ip_parts[1]))+'.'+str(int(ip_parts[2]))+'.'+str(int(ip_parts[3])))
        return True
    def __run_tor(self):
        self.__print('Configuring Tor ...')
        cmd = ['sudo','service','tor','stop']
        self.__execute(cmd)
        cfg = ""
        for number in range(self.__number_of_tor_processes):
            cfg += "SOCKSPort 127.0.0.1:"+str(9050+number+1)+"\n"
        cfg += "UseBridges 1\n"
        cfg += "ClientTransportPlugin obfs3,obfs4 exec /usr/bin/obfs4proxy\n"
        cfg += "obfs4 95.28.20.70:443 1CE9D74211CCE7C1BFA7B3502FFB1EAE5C9FBFF7 \
            cert=BENdcUL5pTe/kRKTEN3gV4UtCZXv/wxLoYydIbdjmxqahP0iS935AcbkJ8D9ZOA3PxZwVA iat-mode=0\n"
        cfg += "obfs4 69.51.252.123:46591 D812B795432FCDC3FF23DF40F46BB2E87C0EC041 \
            cert=wKoR0UPiqktiNI9SPm77RNyAIr7AvYCxXBrylT8XcftkC3X3RP06I0UT0dTEI7SwOx2NBA iat-mode=0\n"
        cfg += "obfs4 185.165.171.12:2010 356645B213921D081EF8B67A0DCCDB9882241F4A \
             cert=plxINWIExT/NqVMyoyUBeb9pJ6cbCakgzeYEQ0mmReZvKaS3x5NmttZJZZbPTDfhUJF1Uw iat-mode=0\n"
        try:
            f = open("/etc/tor/torrc",'w')
            f.write(cfg)
            f.close()
        except:
            self.__print('Unable to apply Tor configs','e')
            self.__handle_keyboard_interrupt()
        self.__print("Running Tor ...")
        cmd = ['sudo','service','tor','start']
        self.__execute(cmd)
        self.__stop_printing_dots = True
        self.__print("Waiting for 1 mimute to service Tor gets started ",dots=True)
        time.sleep(60)
        self.__stop_printing_dots = True
        time.sleep(1)
        self.__test_tor()
    def __test_tor(self):
        number_of_failed_ports = 0
        for number in self.__number_of_tor_processes:
            port_number = str(9050+number+1)
            self.__print("Checking port "+port_number+" ...")
            cmd = ['curl', '--socks5', '127.0.0.1:'+port_number, '--socks5-hostname',\
                 '127.0.0.1:'+port_number, '-s', 'https://check.torproject.org/', '|', 'cat', '|',\
                      'grep', '-m', '1' ,'Congratulations' ,'|','xargs']
            while True:
                out, err = self.__execute(cmd)
                if out == None or out == "":
                    self.__print("Port "+port_number+" FAILED",mtype='e')
                    number_of_failed_ports += 1
                    break
                elif "congratulations" in out.lower():
                    self.__tor_running_ports.append(port_number)
                    self.__print("Port "+port_number+" DONE !")
                    break
                time.sleep(1) 
        if number_of_failed_ports == self.__number_of_tor_processes:
            self.__print("No ports are running",mtype='e')
            self.__handle_keyboard_interrupt()   
    def __config_proxychains(self):
        self.__print('Configuring Proxychains ...')
        cfg = "random_chain\n"
        cfg += "proxy_dns\n"
        cfg += "tcp_read_time_out 15000\n"
        cfg += "tcp_connect_time_out 8000\n"
        for i in self.__tor_running_ports:
            cfg += "socks5 127.0.0.1 "+i+'\n'
        try:
            f = open('/etc/proxychains.conf','w')
            f.write(cfg)
            f.close()
        except:
            self.__print('Unable to apply proxychanis configs',mtype='e')
            self.__handle_keyboard_interrupt()
        self.__print('Proxychains has been configured')
    def __run_masscan(self):
        self.__stop_printing_dots = True
        self.__print("Starting MASSCAN on given ips in 10 seconds ",dots=True)
        time.sleep(10)
        self.__stop_printing_dots = True
        time.sleep(1)
        #os.system('clear')
        #os.system('sudo proxychains masscan '+self.__ips[0]+'-'+self.__ips[1]+\
        # ' --ports 0-65535 --rate 0.5 -oX ./masscan_results.xml')
        # saving path is: ./masscan_results.xml
        # executing commands is: sudo proxychains masscan IP1-IP2 --ports 0-65535 --rate 10 -oX ./masscan_results.xml
        cmd = ['sudo','proxychains','masscan',self.__ips[0]+'-'+self.__ips[1],\
            '--ports','21,22,23,80,443,8080,7070,8000,3306,20,7000,9999,9090,6060,5050,883,1212,1111,1010,1515,1414,1616'\
                ,'--rate',str(self.__masscan_threads),'-oX','./masscan_results.xml']
        out,err = self.__execute(cmd)
        time.sleep(2)
        os.system('clear')
    def __extract_masscan_results(self):
        import xml.etree.ElementTree as et
        import xml.dom.minidom as mm
        try:
            self.__print('Reading masscan results')
            tree = et.parse("./masscan_results.xml")
            root = tree.getroot()
            for e in root:
                name = e.tag
                if name == 'host':
                    add_e = e[0].get('addr')
                    port_e,state = e[1][0].get('portid'),e[1][0][0].get('state')
                    if add_e not in self.__masscan_results.keys():
                        if state == "open":
                            self.__masscan_results[add_e] = [port_e]
                    else:
                        if state == "open":
                            self.__masscan_results[add_e].append(port_e)
            self.__print('Found '+str(len(self.__masscan_results.keys()))+" ips with open ports")
        except:
            self.__print("Unable to read masscan results. Maybe the content\
                 of the file is not correct or empty or even it's not exists in this current path",mtype='e')
            self.__handle_keyboard_interrupt()        
    def __run_nmap(self):
        os.mkdir('./nmap_results')
        p = threading.Thread(target=self.__show_nmap_percentage,args=(,))
        p.start()
        for ip in self.__masscan_results.keys():
            if len(self.__nmap_threads_window) > self.__nmap_threads:
                while len(self.__nmap_threads_window) > self.__nmap_threads:
                    time.sleep(0.1)
            t = threading.Thread(target=self.__nmap_in_thread,args=(ip,))
            t.start()
            
    def __nmap_in_thread(self,ip):
        self.__nmap_threads_window.append(ip)
        # nmap commands :
        ports = ""
        for i in self.__masscan_results[ip]:
            ports += str(i)+',' 
        cmd = ['sudo','proxychains','nmap','-sV','-p',ports,ip,'-oX','./nmap_results/'+ip+'.xml']
        self.__execute(cmd)
        # .
        while self.__nmap_is_writing:
            time.sleep(0.1)
        self.__nmap_is_writing = True
        self.__nmap_number_of_proccessed_ips += 1
        self.__nmap_is_writing = False
        self.__nmap_threads_window.remove(ip)
    def __show_nmap_percentage(self):
        W = '\033[0m'
        R = '\033[31m'
        G = '\033[32m'
        O = '\033[33m'
        P = '\033[35m'
        BOLD = '\033[1m'
        THIN = '\033[1m'
        ips = len(self.__masscan_results.keys())
        while self.__nmap_number_of_proccessed_ips < ips:
            sys.stderr.write('\r'+BOLD+P+'[ '+G+'+'+P+' ] '+O+"Scanning "+str(self.__nmap_number_of_proccessed_ips)+'/'+str(ips)+' ips'+THIN)
            time.sleep(0.1)
        time.sleep(1)
        sys.stderr.write('\r'+BOLD+P+'[ '+G+'+'+P+' ] '+O+"Scanning "+str(self.__nmap_number_of_proccessed_ips)+'/'+str(ips)+' ips\n'+THIN)
        time.sleep(1)
    def __import_nmap_outputs_into_ivre(self):
        self.__print("Initializing ivre ...")
        self.__execute(['yes','|','ivre','ipinfo','--init'])
        self.__execute(['yes','|','ivre','scancli','--init'])
        self.__execute(['yes','|','ivre','view','--init'])
        self.__execute(['yes','|','ivre','flowcli','--init'])
        self.__execute(['yes','|','sudo','ivre','runscansagentdb','--init'])
        self.__print("Importing into ivre database ...")
        self.__execute(['ivre','scan2db','-c','ROUTABLE',',','ROUTABLE-CAMPAIGN-001','-s','MySource','-r','./nmap_results'])
        self.__execute(['ivre','db2view','nmap'])
        self.__print("Imported")
    def __run_ivre_webserver(self):
        self.__print("Running Ivre WebServer on 0.0.0.0:8080 ...")
        os.system('ivre httpd -b 0.0.0.0 -p 8080')
        os.system('clear')
        self.__print("Ivre WebServer closed.")
        

