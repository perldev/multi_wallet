from __future__ import print_function
import requests
from sdk.crypto_settings import Settings
import hashlib
import json
PREC = 1000000
from decimal import Decimal
from datetime import datetime, timedelta
#import BasicUi
import argparse
from pygments import highlight, lexers, formatters

from ripple.client import Remote, ResponseError
from ripple.sign import get_ripple_from_secret


import json
import sys
import re
from binascii import hexlify, unhexlify



use_core = False
headers = {'Content-type': 'application/json', 'Accept': 'application/json'}


class CryptoAccountXrp:
        def __init__(self, currency="XRP", account=None):
           self.__currency =  currency
           self.__account = account
           self.__host = Settings[currency]["host"]
           self.__port = Settings[currency]["port"]
           self.__host2 = Settings[currency]["host_ws"]
           self.__port2 = Settings[currency]["port_ws"]
           self.__access = "http://%s:%s/" % (self.__host, self.__port)

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
            
            raise Exception("Is not implemented")

        def getheight(self):
            raise Exception("Is not implemented")

        """
        {
    "method": "account_info",
    "params": [
        {
            "account": "rG1QQv2nh2gr7RCZ1P8YYcBUKCCN633jCn",
            "strict": true,
            "ledger_index": "current",
            "queue": true
        }
       ]
        }
        """

        def getbalance(self, address):
             req  = {"method":"account_info", "params":[{"account":address, "strict": True, "ledger_index":"current", "queue": True}]}
             resp = requests.post(self.__access, data= json.dumps(req), headers=headers)
             respJson = resp.json()
             print(respJson)
             return  Decimal(respJson["result"]["account_data"]["Balance"])/PREC
            

        def getnewaddress(self):
            raise Exception("Is not implemented")
            

        def listunspent(self):
            raise Exception("Is not implemented")
       
        def sendtoaddress(self, priv, to_addr, amnt, message, multisig=None):
            remote = Remote("ws://%s:%s" % (self.__host2, str(self.__port2)), priv )
            if isinstance(amnt, Decimal):
                amnt = int(amnt*PREC)
         
            try : 
              if len(message)>0:
                 message = int(message)
            except:
              raise Exception("Invalid message")

            result_node  = remote.send_payment(
            to_addr, amnt, flags=0,
            destination_tag=message)
            print('TxHash: %s' % result_node.hash)

            try:
               result = result_node.wait()
            except ResponseError as e:
               result = e.response

            if True:
              formatted_json = json.dumps(result, sort_keys=True, indent=4)
              colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.TerminalFormatter())
              print(colorful_json)

            print(result['engine_result_message'])
            return (result_node, result)
   

            
 
        def listtransactionsin(self, address, from_block_hash=None, count=5000, verbose=False):

             """
                http://127.0.0.1:7890/account/transfers/incoming?address=TALICELCD3XPH4FFI5STGGNSNSWPOTG5E4DS2TOS&hash=949583a20ebdfdcb58277eb42fef3e66e9e6bbfc47304d8741a82c68f7c53a2
                 "https://data.ripple.com/v2/accounts/t1Z7o4ME2jgzhfBjYUwhpEcBnZufGG/transactions?type=Payment&result=tesSUCCESS&limit=30000
             """
             """
             {
    "method": "account_tx",
    "params": [
        {
            "account": "r9cZA1mLK5R5Am25ArfXFmqgNwjZgnfk59",
            "binary": false,
            "forward": false,
            "ledger_index_max": -1,
            "ledger_index_min": -1,
            "limit": 2
        }
    ]
            } 

             """
             result = []      

             if use_core:
                req =  {"method":"account_tx", "params":[{"account":address, "binary": False, "forward":"false",      "ledger_index_max": -1,
                        "ledger_index_min": -1, "limit":count }]}
                resp = requests.post(self.__access, data= json.dumps(req), headers=headers)
                respJson = resp.json()
                print(respJson)
                transes = None
                if "result" in respJson and respJson["result"]["status"] == "success":
		  transes = respJson["result"]["transactions"]
                else:
                  return  []
                for i in transes:
                  it = i["tx"]
                  print(it)
                  it["address"] = it["Destination"]
                  if it["address"] == address:
                    it["category"] = "receive"  
                  else:
                    it["category"] = "send"  
                
                  it["amount"] = Decimal(str(it["Amount"]))/PREC
                  if "DestinationTag" in it:
                     it["paymentId"]= str(it["DestinationTag"])

                  it["txid"] = it["hash"]
                  if i["validated"]:
                    it["confirmations"] = 99
                  else:
                    it["confirmations"] = 0
            
                  result.append(it)
             else:
                start = datetime.now() - timedelta(days=7)
                q = "https://data.ripple.com/v2/accounts/%s/transactions/?type=Payment&result=tesSUCCESS&limit=%i&start=%s" % ( address, count, start.date()  )
                print(q)
                resp = requests.get(q , headers=headers)
                respJson = resp.json()
                print("from data ripple")
                #print(respJson)
                transes = None
             
                if "result" in respJson and respJson["result"] == "success":
                  transes = respJson["transactions"]
                else:
                  print(respJson)
                  return  []
                result = []
                print("got %i" % len(transes))
                transes.reverse()
                
                for i in transes:
                  it = i["tx"]
                  print(it)
                  it["address"] = it["Destination"]
                  if it["address"] == address:
                    it["category"] = "receive"  
                  else:
                    it["category"] = "send"  

                  if "meta" in i and "delivered_amount" in i["meta"]:
                    it["amount"] = Decimal(str(i["meta"]["delivered_amount"]))/PREC
                  else:
                    print("="*120)
                    print("Warning! can't find amount")
                    print("="*120) 
                    continue
                  
                  if "DestinationTag" in it:
                     it["paymentId"]= str(it["DestinationTag"])
                  else:
                     it["paymentId"] = ""
                     
                  it["txid"] = i["hash"]
                  it["confirmations"] = 99
                  result.append(it)

                

             return  result
              
    
        def sendmany(self, addrs, changeto=None, fee=0.005, payment_id=None):       
            raise Exception("Is not implemented")
            

              
