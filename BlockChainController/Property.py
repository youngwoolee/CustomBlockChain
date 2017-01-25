'''
Created on 2017. 1. 20.

@author: joeylee
'''
import os


myNode = None #node entity
my_node_json = None   #node entity written in json
nodeList = None   #all peer(node) list of se-chain
trust_node_ip = '192.168.22.72'
my_ip_address = "192.168.22.72"
node_sync = False
alive_nodes = dict() # key value ['alive'] is currently connected nodes
check_flag = False
block_sync = False
port = 10654
ui_frame = None
node_started = False
NODE_IDX = 0

max_transaction = 0
CONTRACT_DEPLOY_PATH = os.path.dirname(os.path.dirname(__file__)) + '\_ContractStorage'+ '\\'
DB_PATH = os.path.dirname(os.path.dirname(__file__)) + '\StorageManager'+ '\\'