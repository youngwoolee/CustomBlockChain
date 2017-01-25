'''
Created on 2017. 1. 20.

@author: joeylee
'''

class ValueData(object):
    '''
        need to change sender_ip  -> sender address
    '''
    def __init__(self, receiver, coin):
        self.receiver_address = receiver
        self.coin = coin