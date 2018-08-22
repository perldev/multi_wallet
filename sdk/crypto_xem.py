import requests
from sdk.crypto_settings import Settings
import hashlib
import json
PREC = 1000000
from decimal import Decimal
from nem.NemConnect import NemConnect
from nem.Account import Account
#import BasicUi
import traceback
import json
import sys
import re
from binascii import hexlify, unhexlify






class CryptoAccountXem:
        def __init__(self, currency="XEM", account=None):
           self.__currency =  currency
           self.__account = account
           self.__host = Settings[currency]["host"]
           self.__port = Settings[currency]["port"]
           self.__rpc_user = Settings[currency]["rpc_user"]
           self.__rpc_pwd = Settings[currency]["rpc_pwd"]
           self.__access = "http://%s:%s/" % (self.__host, self.__port)
           self.__connect  = NemConnect(self.__host, int(self.__port))

        def walletpassphrase(self, time=20):
            raise Exception("Is not implemented")

        def keypoolrefill(self, size=None):
            raise Exception("Is not implemented")

        def getrawmempool(self):          
            raise Exception("Is not implemented")

        def getrawtransaction(self, txid):          
            raise Exception("Is not implemented")
             
      
        def decoderawtransaction(self, hex_data):
            raise Exception("Is not implemented")

        def listaddressgroupings(self):
            raise Exception("Is not implemented")

        def walletlock(self):
            raise Exception("Is not implemented")

        def dumpwallet(self, filename):
            raise Exception("Is not implemented")

        def backupwallet(self, filename):
            raise Exception("Is not implemented")

   	def dumpprivkey(self, Addr):
            raise Exception("Is not implemented")

        def getstatus(self):
            
             resp = requests.get(self.__access + "node/extended-info")
             respJson = resp.json()
             return  respJson["node"]

        def getheight(self):
                
             resp = requests.get(self.__access + "chain/height")
             respJson = resp.json()
             return  respJson["height"]



        def getbalance(self, address):
            
             resp = requests.get(self.__access +"account/get?address=" + address )
             respJson = resp.json()
             print respJson 
             return  float(respJson["account"]["balance"])/PREC #  + float(respJson["account"]["vestedBalance"])/PREC
            

        def getnewaddress(self):
            raise Exception("Is not implemented")
            

        def listunspent(self):
            raise Exception("Is not implemented")
       
        def sendtoaddress(self, priv, to_addr, amnt, message, multisig=None):
                privkey =priv
                recipient = to_addr
                amount = int(amnt*PREC)
                fee = 0


                a = Account(priv)
                print " [+] PREPARING TRANSACTION"
                ok, j = self.__connect.prepareTransfer(a.getHexPublicKey(), multisig, recipient, amount, message, fee, None)
                print j
                if ok and ('data' in j):
                   return  self.signAndAnnounceTransaction(a, j)
                else:
                   print " [!] prepare failed: "
                   return j

        def signAndAnnounceTransaction(self, a, jsonData):
               connector =  self.__connect
               print " [+] TRYING TO SIGN PREPARED DATA"
               data = unhexlify(jsonData['data'])
               sig = a.sign(data)

               ok, j = connector.transferAnnounce(jsonData['data'], hexlify(sig))
               if ok:
                print " [+] ANNOUNCED"
               else:
                print " [!] announce failed"
               return j

 
        def listtransactionsin(self, address, from_block_hash=None, count=25, verbose=False):

             """
                http://127.0.0.1:7890/account/transfers/incoming?address=TALICELCD3XPH4FFI5STGGNSNSWPOTG5E4DS2TOS&hash=949583a20ebdfdcb58277eb42fef3e66e9e6bbfc47304d8741a82c68f7c53a2

             """
             """
                      {u'data': [{u'meta': {u'innerHash': {}, u'hash': {u'data': u'015e761752e7ed8fc20728ed6916a9bf7c03885319d9e5a58a8daf3e46af0484'}, u'id': 1823429, u'height': 1555392}, u'transaction': {u'fee': 100000, u'timeStamp': 94165304, u'signature': u'9290bcff1d878ac31ad0fe1be7747d441cd95fa57b162b4374748b1120b5b00985500d8b8ace871f711abeff0870acf95daa303c0a112af6fda0f85bd7e9c509', u'amount': 5000000, u'version': 1744830465, u'deadline': 94251704, u'type': 257, u'signer': u'75c5cc65090a104526aafccf7b88363a27e82ed10b1950cd792acd88e3829f66', u'message': {u'type': 1, u'payload': u'336530303839626361663766356263'}, u'recipient': u'NDQ6SBYGMEUZMZOBKJTQAKXQREA55SVLF7QUYPEU'}}, {u'meta': {u'innerHash': {}, u'hash': {u'data': u'3175202ed9e0601911779f6961343d0e76d2ece33505db7f59352e918d232bed'}, u'id': 1823419, u'height': 1555385}, u'transaction': {u'fee': 100000, u'timeStamp': 94164757, u'signature': u'e219c15c7a469065b32dad55220768c949470a67605f78ecffb74523ab63b53deee53365ad1d7c2b4cf832a29fbec6040bc9e90f7046e8911bf724a0d339a80e', u'amount': 5000000, u'version': 1744830465, u'deadline': 94251157, u'type': 257, u'signer': u'75c5cc65090a104526aafccf7b88363a27e82ed10b1950cd792acd88e3829f66', u'message': {u'type': 1, u'payload': u'336530303839626361663766356263'}, u'recipient': u'NDQ6SBYGMEUZMZOBKJTQAKXQREA55SVLF7QUYPEU'}}]}


             """
             """
                    {u'meta': {u'innerHash': {}, u'hash': {u'data': u'015e761752e7ed8fc20728ed6916a9bf7c03885319d9e5a58a8daf3e46af0484'}, u'id': 1823429, u'height': 1555392}, u'transaction': {u'fee': 100000, u'timeStamp': 94165304, u'signature': u'9290bcff1d878ac31ad0fe1be7747d441cd95fa57b162b4374748b1120b5b00985500d8b8ace871f711abeff0870acf95daa303c0a112af6fda0f85bd7e9c509', u'amount': 5000000, u'version': 1744830465, u'deadline': 94251704, u'type': 257, u'signer': u'75c5cc65090a104526aafccf7b88363a27e82ed10b1950cd792acd88e3829f66', u'message': {u'type': 1, u'payload': u'336530303839626361663766356263'}, u'recipient': u'NDQ6SBYGMEUZMZOBKJTQAKXQREA55SVLF7QUYPEU'}}

             """
 
             req_str = "account/transfers/incoming?address="+address
              
             if from_block_hash:
                req_str +="&hash=" + from_block_hash

             resp = requests.get(self.__access + req_str)
             respJson = resp.json()
            # if verbose :
             current = self.getheight()
             print respJson
             result = []
             for i in respJson["data"]:
                 it = i["transaction"]
                 try:
                    it["address"] = i["transaction"]["recipient"]
                 except :
                    print "cant parse trans"
                    print i
                    continue
                 it["category"] = "receive"
                 it["amount"] = Decimal(str(i["transaction"]["amount"]))/PREC
                 if "mosaics" in it:
                   for mosaic in it["mosaics"]:
                     if mosaic["mosaicId"]["name"] == "xem" and mosaic["mosaicId"]["namespaceId"] == "nem":
                           it["amount"] = (mosaic["quantity"]*it["amount"])/PREC
                           break

                 if "payload" in i["transaction"]["message"]:
                     try:
                        it["paymentId"]= bytearray.fromhex( i["transaction"]["message"]["payload"]).decode()
                     except :
                        traceback.print_exc()
                        print i["transaction"]["message"]["payload"]
                        it["paymentId"] = ""
                 it["txid"] = i["meta"]["hash"]["data"]# + "_" +  str(i["meta"]["id"])
                 it["confirmations"] = current - i["meta"]["height"]
                 result.append(it)

             return  result
              
    
        def sendmany(self, addrs, changeto=None, fee=0.005, payment_id=None):       
             return  respJson["result"]["transactionHash"]
           
 

              
