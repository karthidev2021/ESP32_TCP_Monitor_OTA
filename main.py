import socket,subprocess,threading
from datetime import datetime
import msvcrt

class Monitor:
    def __init__(self):
        ip=subprocess.check_output("netsh interface ipv4 show ipaddresses Wi-Fi")
        self.ip=ip.decode('utf-8').split(" ")[1]
        self.port=2002

        self.server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server.bind((self.ip,self.port))
        self.server.settimeout(0.1)

        self.clients=[]

        self.timeLogFlag=True

    def start(self):
        self.server.listen()
        print("Monitor(TCP_Server) Listening on {}:{}".format(self.ip,self.port))
        
        try:
            while True:
                try:
                    client,address=self.server.accept()
                    if client not in self.clients:
                        self.clients.append(client)
                        print("New connection established from {}:{}".format(address[0],address[1]))

                        client_thread=threading.Thread(target=self.handle_receive_message,args=(client,address))
                        client_thread.start()
                
                except socket.timeout:
                    continue    #server.accept() blocks the code..so even keyboardInterrupt won't work
                                #so we are setting timeout so it will raise timeError
        except KeyboardInterrupt:
            for client in self.clients:
                client.close()
            self.server.close()
            print("Server listening on {}:{} is closed.".format(self.ip,self.port))
            
            


    def handle_receive_message(self,client,address):

        while True:
            try:
                printdata=""
                data=client.recv(1024)
                if not data:
                    raise Exception("client may be disconnected")

                data=data.decode("utf-8")
                data=data.split("\r\n")

                for str_element_index in range(len(data)):
                    str_element=data[str_element_index]

                    if str_element !="":
                        str_element=str_element.split("\n")
                        for index in range(len(str_element)):
                            # if str_element[index] != "":
                            print(datetime.now().strftime('%H:%M:%S.%f -> ')+str_element[index],end="")
                            if index!=len(str_element)-1:
                                print("\n",end="")

                    if str_element_index!=len(data)-1:
                        print("\n",end="")

            except Exception as e:
                print("{}:{} ---> Connection error : {}".format(address[0],address[1],e))
                self.clients.remove(client)
                client.close()
                break
    
print("A simple TCP-based Monitor, similar to serial monitor in Arduino IDE")
print("Developed by : Karthikeeyan_S_M")
print("To close the server click ctrl+c...\n")
m=Monitor()
m.start()

print("Press any key to exit")
while msvcrt.kbhit():  #to clear the buffer that get stored if any key is pressed during the server
    msvcrt.getch()
msvcrt.getch()



#datetime.now().strftime('%H:%M:%S.%f -> ')