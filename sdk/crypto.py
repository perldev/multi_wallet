from jsonrpc import ServiceProxy
from sdk.crypto_settings import Settings




class CryptoAccount(object):
        def __init__(self, currency="BTC", account=None, path=None):
           self.__currency =  currency
           self.__host = Settings[currency]["host"]
           self.__port = Settings[currency]["port"]
           self.__rpc_user = Settings[currency]["rpc_user"]
           self.__rpc_pwd = Settings[currency]["rpc_pwd"]
           self.__path = ""
           if "rpc_path" in Settings[currency]:
              self.__path = Settings[currency]["rpc_path"]
          
           if path is not None:
              self.__path = path
           self.__account = account
           self.__access = ServiceProxy("http://%s:%s@%s:%s%s" % (self.__rpc_user,
                                                             self.__rpc_pwd,
                                                             self.__host,
                                                             self.__port, self.__path))
        def walletpassphrase(self, time=20):
            return self.__access.walletpassphrase(Settings[self.__currency]["pwd2"],time)

        def keypoolrefill(self, size=None):
           if size is None:
              return self.__access.keypoolrefill()
           else:
              return self.__access.keypoolrefill(size)

        def getrawmempool(self):          
            return self.__access.getrawmempool()

        def getrawtransaction(self, txid):          
            return self.__access.getrawtransaction(txid)

        def gettransaction(self, txid):          
            return self.__access.gettransaction(txid)
      
        def decoderawtransaction(self, hex_data):
            return self.__access.decoderawtransaction(hex_data)

        def listaddressgroupings(self):
           return self.__access.listaddressgroupings()
 
        def validateaddress(self, address):
           return self.__access.validateaddress(address)
    
        def settxfee(self, amnt):
           return self.__access.settxfee(amnt)
        
        def listsinceblock(self, hashblcok):
           return self.__access.listsinceblock(hashblcok)

        def getblockcount(self):
           return self.__access.getblockcount()

        def getblockhash(self, hs):
           return self.__access.getblockhash(hs)

        def getblock(self, hs):
           return self.__access.getblock(hs)


        def walletlock(self):
           return self.__access.walletlock()

        def dumpwallet(self, filename):
           return self.__access.dumpwallet(filename)

        def backupwallet(self, filename):
           return self.__access.backupwallet(filename)

   	def dumpprivkey(self, Addr):
		return self.__access.dumpprivkey(Addr)
        
        def getinfo(self):
                return self.__access.getinfo()

        def getbalance(self, path=None):
            if path is None:
                 return self.__access.getbalance()
            else:
                 old_access = self.__access
                 self.__access = ServiceProxy("http://%s:%s@%s:%s%s" % (self.__rpc_user,
                                                             self.__rpc_pwd,
                                                             self.__host,
                                                             self.__port, path))

                 balance = self.__access.getbalance()
                 self.__access = old_access
                 return balance 
                
 

        def getnewaddress(self):
           if self.__account:
                return self.__access.getnewaddress(self.__account)
           else:
                return self.__access.getnewaddress()

        def listunspent(self):
                return self.__access.listunspent()      
       
        def sendmany(self, to_addr):
            print self.__account
            return self.__access.sendmany(self.__account, to_addr)
 
        def listtransactions(self):
                if self.__account is None :
                         return []
                return self.__access.listtransactions(self.__account,10000,0)  
    
        def sendtoaddress(self, addr, amnt):       
                return  self.__access.sendtoaddress(addr, amnt)

        def sendto(self, to_addr, amnt, minconf = 3, comment = None ):  
                if comment is not None :
                      return  self.__access.sendfrom(self.__account, to_addr, amnt, minconf, comment)
                else: 
                      return  self.__access.sendfrom(self.__account, to_addr, amnt, minconf)


        def access(self):
            return self.__access
          


class CryptoAccountOmni(CryptoAccount):
    
    
        def __init__(self, *args, **kwargs):
            property_id = int(kwargs.pop('property_id', None))
            super(CryptoAccountOmni, self).__init__(*args, **kwargs)
            self.__property_id = int(property_id)
            self.__access = self.access()
            
        
        def sendtoaddress(self, from_address,  addr, amnt):       
            return  self.__access.omni_send(from_address, addr, self.__property_id, amnt, from_address)
        
        
        def getbalance_omni(self, address):

            return  self.__access.omni_getbalance(address, self.__property_id )
        
        
        def omni_listblocktransactions(self, blockindex):
            return  self.__access.omni_listblocktransactions(int(blockindex))
            
        
        def omni_gettransaction(self, txid):
            return  self.__access.omni_gettransaction(txid) 
             

 
