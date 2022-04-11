"""
Timothy Queva
CS3130 Lab2
Jan. 31, 2021

This program will display 
"""

import argparse

#reveals send/recv ip's
def ip():
    with open('converted_w_name.pcap') as data:
        print("Sender              Receiver")
        for elemnt in data:
            elemnt  = elemnt.strip()
            elemnt = elemnt.split()
            
            #skips processing of IP6 packets
            if elemnt[1] != "IP6" and elemnt[1] != "ARP,":
                #This processes the sender part
                sender = elemnt[2]
                sender = sender.split(".")
                sender.pop()
                sender = ".".join(sender)
                
                #This processes the receiver part
                receiver = elemnt[4]
                receiver = receiver.split(".")
                receiver.pop()
                receiver = ".".join(receiver)
                
                print('{:<20}'.format(sender) + '{:<15}'.format(receiver))
            
#reveals send/recv ip's with ports
def udp():
    with open('converted_w_name.pcap') as data:
        print()
        print("UDP packets are as follows:")
        
        print("Sender            Port     :     Receiver          Port")
        for elemnt in data:
            elemnt  = elemnt.strip()
            elemnt = elemnt.split()
                
            if elemnt[5] == "UDP," and elemnt[1] != "IP6":
                sender = elemnt[2]
                sender = sender.split(".")
                s_port = sender[4]
                sender.pop()
                sender = ".".join(sender)
                s_port = s_port.strip(":")
                
                #This processes the receiver part
                receiver = elemnt[4]
                receiver = receiver.split(".")
                r_port = receiver[4]
                receiver.pop()
                receiver = ".".join(receiver)
                r_port = r_port.strip(":")
                
                print('{:<18}'.format(sender) + '{:<15}'.format(s_port) +
                      '{:<18}'.format(receiver) + '{:<8}'.format(r_port))
            
def arp(choice):
    with open('converted_w_name.pcap') as data:
        print()
        print(str(choice) + " ARP packets are as follows:")
        
        print("Sender              Receiver")
        for elemnt in data:
            elemnt  = elemnt.strip()
            elemnt = elemnt.split()
            
            if elemnt[1] == "ARP," and choice == "REQUEST":
                if elemnt[2] == "Request":
                    if elemnt[6] == "tell":
                        elemnt[7] = elemnt[7].strip(",")
                        print('{:<20}'.format(elemnt[7]) +
                              '{:<22}'.format("All - (ARP broadcast)"))
                    else:    
                        elemnt[6] = elemnt[6].strip(",")
                        print('{:<20}'.format(elemnt[6]) +
                              '{:<22}'.format("All - (ARP broadcast)"))
            elif elemnt[1] == "ARP," and choice == "REPLY":
                if elemnt[2] == "Reply":
                    elemnt[3] = elemnt[3].strip(",")
                    print('{:<20}'.format(elemnt[3]) +
                          '{:<22}'.format("All - (ARP broadcast)"))

def source(port):
    with open('converted_w_name.pcap') as data:
        print()
        print("Senders from port " + str(port) + " are as follows: ")
        
        for elemnt in data:
            elemnt  = elemnt.strip()
            elemnt = elemnt.split()
            
            if elemnt[1] != "IP6" and elemnt[1] != "ARP,":
                receiver = elemnt[4]
                receiver = receiver.split(".")
                try:
                    r_port = receiver[4]
                    receiver.pop()
                except:
                    pass
                receiver = ".".join(receiver)
                r_port = r_port.strip(":")
                
                if r_port == port:
                    print('{:<18}'.format(receiver))

def dest(port):
    with open('converted_w_name.pcap') as data:
        print()
        print("Receivers from port " + str(port) + " are as follows: ")
        
        for elemnt in data:
            elemnt  = elemnt.strip()
            elemnt = elemnt.split()
            
            if elemnt[1] != "IP6" and elemnt[1] != "ARP,":
                sender = elemnt[2]
                sender = sender.split(".")
                try:
                    s_port = sender[4]
                    sender.pop()
                except:
                    pass
                sender = ".".join(sender)
                s_port = s_port.strip(":")
                
                if s_port == port:
                    print('{:<18}'.format(sender))
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--IP',help='displays sender/receivers of all IP ' +
                        'packets',action='store_true')
    parser.add_argument('--UDP',help='displays sender/receiver + port #\'s ' +
                        'for all UDP packets',action='store_true')
    parser.add_argument('--ARP',help='displays request/display ARP packets' +
                        ' (User specifies)',choices=['REQ','REPLY'])
    parser.add_argument('--SRC',help='displays all IP packets associated ' +
                        ' with specified source port',nargs =1)
    parser.add_argument('--DEST',help='displays all IP packets asscoiated ' +
                        'with specified destination port',nargs =1)
    parser.add_argument('FILENAME',help="tcpdump file")
    args = parser.parse_args()
    
    option = {args.IP: ip, args.UDP: udp, args.ARP: arp}
    if args.IP == True:
        function = option[args.IP]
        function()
    elif args.UDP == True:
        function = option[args.UDP]
        function()
    elif args.ARP == "REPLY":
        function = option[args.ARP]
        function("REPLY")
    elif args.ARP == "REQ":
        function = option[args.ARP]
        function("REQUEST")
    elif args.SRC: 
        if args.SRC[0].isdigit():
            source(args.SRC[0])
    elif args.DEST:
        if args.DEST[0].isdigit():
            dest(args.DEST[0])