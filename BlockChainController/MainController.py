'''
Created on 2017. 1. 20.

@author: joeylee
'''

import json
from NodeManager import NodeController
from BlockChainController import Property
from StorageManager import FileController
from BlockManager import BlockGenerator
from CommunicationManager import Sender


def set_my_node():
    from NodeManager import NodeController
    
    Property.myNode, Property.my_node_json = NodeController.get_node()
    

def commnad_control() :
    
    from TransactionManager import TransactionController
    
    cmd = None
    while cmd != 'q':
        cmd = raw_input('(t : send transaction, v : view transaction buffer, q : quit) >')
        
        if cmd == 't':
            receiver_ip = raw_input('Receiver IP : ')
            amount = raw_input('Amount : ')
            message = raw_input('Message : ')
        
            
            trx_json = TransactionController.create_transaction(Property.myNode['public_key'],Property.myNode['private_key'], cmd,
                                                               receiver_ip, amount, message, '')
            
            if FileController.get_number_of_transactions() >= 0:
                block = BlockGenerator.generate_block(trx_json)
                block_temp = json.dumps(block, indent=4, default=lambda o: o.__dict__, sort_keys=True)
                Sender.send_to_all_node(block_temp)
            else:
                Sender.send_to_all_node(trx_json)
                
        elif cmd =='v':
            TransactionController.print_all_transaction()
            
            

def get_ip_address():
    import socket
    Property.my_ip_address = socket.gethostbyname(socket.gethostname())
    

def node_start():
    from CommunicationManager import ConnectionChecker
    import thread
    from CommunicationManager import Receiver
    set_my_node()
    print("have got node information")
    
    ping = ConnectionChecker.Pinger()
    ping.thread_count =8
    ping.hosts = FileController.get_ip_list()
    
    for host in ping.hosts:
        print('hosts list')
        print(host)
    
    Property.alive_nodes = ping.start()
    print('hi')
    print(Property.alive_nodes)
    
    NodeController.add_new_node(Property.myNode)
    
    if Property.my_ip_address != Property.trust_node_ip:
        NodeController.send_my_node_info(Property.myNode['ip_address'])
        
    
    Property.nodeList = FileController.get_node_list()
    thread.start_new_thread(Receiver.start, ("Listener_Thread", Property.my_ip_address, Property.port))
    
    Property.node_started = True
    
def initial_node():
    from NodeInitializer import NodeListSynchronizer
    from NodeInitializer import BlockSynchronizer

    print("Blocks are synchronizing now")    
    BlockSynchronizer.sync_blocks()

    while(True):
           if(Property.block_sync == True):
                break
            
    print("Blocks are synchronized")   
    
    print("Downloading node list")  
    
    NodeListSynchronizer.download_node_list(Property.my_node_json)
    
    while (True):
            if (Property.node_sync == True):
                break
            
    node_start()
    
    print("Node Start")  



    
get_ip_address()
# node_start()
initial_node()
commnad_control()
