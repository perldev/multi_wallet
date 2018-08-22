from django.contrib.auth.models import User
#from  main.finance import   notify_admin_withdraw

from main.models import VolatileConsts, CryptoTransfers, Currency, Accounts, crypton_in, PoolAccounts, BaseCommand, process_in_crypto_low
from sdk.crypto import CryptoAccount
from sdk.crypto_krb import CryptoAccountKrb, PREC as PREC_KRB
import crypton.settings 
from sdk.crypto_settings import Settings as CryptoSettings
import traceback
from main.api import  format_numbers_strong
from django.db import connection
from decimal import getcontext, Decimal
import os
import sys



class Command(BaseCommand):
    args = '<CurrencyTitle ...>'
    help = 'every minute get crypto currency transes from the ledger'
    strict_name = True

    def handle2(self, *args, **options):
        CurrencyTitle = args[0]    
	print "process  currency incoming %s" % (  CurrencyTitle ) 
	try:
		print "start proces %s" % CurrencyTitle
		if not CurrencyTitle in ( "KRB",  "ETH", "ETC", "XMR", "XEM", "XRP",) :
		   try:
			process_in_crypto(CurrencyTitle)
		   except:
		        traceback.print_exc()

		if  CurrencyTitle in ("KRB",) :
		   try:
			process_in_crypto_krb(CurrencyTitle)
		   except:
		        traceback.print_exc()

			    
			    
	except :
		traceback.print_exc()
		print "Unexpected error:", sys.exc_info()[0]	

def process_in_crypto_eth(CurrencyTitle):
        print "processing %s"  % CurrencyTitle
        user_system =   User.objects.get(id = 1)
        CurrencyInstance = Currency.objects.get(title = CurrencyTitle)
        getcontext().prec = crypton.settings.TRANS_PREC
        for Trans in  CryptoTransfers.objects.filter(status="processing", currency=CurrencyInstance):
            if Trans.status == "processing" and Trans.confirms > CryptoSettings[CurrencyTitle]["min_confirmation"]:
                 print "processing it %s" % (str(Trans))
                 Trans.save()
                 crypton_in(Trans, user_system)

           



def process_in_crypto_krb(CurrencyTitle):
        List = None
        getcontext().prec = crypton.settings.TRANS_PREC
        """
        receive transactions {u'fee': 100000000, u'extra': u'01560b938122e67d21d3410ed853300dfd40dc4c77a70acfa5f2c3821f1a8d19c4', u'timestamp': 1498144097, u'blockIndex': 121323, u'state': 0, u'transactionHash': u'573901188114c9331e88e99d4030e1c12f25243e7472154919079ee27582f5e2', u'amount': 30000000000000, u'unlockTime': 0, u'transfers': [{u'amount': 30000000000000, u'type': 0, u'address': u'Kj2pFhj7StvibBAt8ULR3hgJVCX5Gb2RFisvFoviyKoCDbmtg47XWum3BtK9VJCJc4cwEM44zvp8n9iDrMPwXwDs5i8Dk47'}, {u'amount': -35000000000000, u'type': 0, u'address': u''}, {u'amount': 4999900000000, u'type': 0, u'address': u''}], u'paymentId': u'', u'isBase': False}
        """
        
        Crypton = CryptoAccountKrb(CurrencyTitle, "trade_stock")
        print "="*60
        print "process krb"
        TimeLastBlock =  VolatileConsts.objects.get(Name = "last_btc_process_block_krb")
        Time =  int(TimeLastBlock.Value)
        print Time
          
        List = Crypton.listtransactions(100000, Time-200) # process last 100 blocks
        user_system =   User.objects.get(id = 1)
        CurrencyInstance = Currency.objects.get(title = CurrencyTitle)
        getcontext().prec = crypton.settings.TRANS_PREC
        TransResult = []
        status = Crypton.getstatus()
        print "current block"
        CurrentBlock = int(status["blockCount"])
        print CurrentBlock
        for trans in List :
            print "receive transactions %s" % (str(trans))
            if not "blockIndex" in trans:
                  continue
            if trans["amount"]<0:
                  print "it's out transaction %s" % (str(trans))
                  continue
            krb_address=None
            if len(trans["paymentId"]) > 0: 
                
               if True:
                 try:
                   krb_address = PoolAccounts.objects.get(ext_info = trans["paymentId"], currency = CurrencyInstance)
                   print "our transaction"
                 except PoolAccounts.DoesNotExist:
                   print "no paymentID"
                   print trans["paymentId"]
                   continue
            else:
               continue

            for  trans_in in trans["transfers"]:
               print "process it %s" % str(trans_in)
               trans_in["amount"] = Decimal(str(trans_in["amount"]))/PREC_KRB
               if trans_in["amount"]<=0:
                  continue

               if trans_in["address"] == '':
                  continue

               if trans_in["address"]!=krb_address.address:
                  
                  continue  


               TransResult.append({"txid":trans["transactionHash"], 
                                   "category":"receive",
                                   "paymentId": trans["paymentId"],
                                   "address": trans_in["address"],
                                   "amount" : trans_in["amount"], # krb is more complicated than btc
                                    "confirmations": CurrentBlock-trans["blockIndex"]
                                     })
 
        print TransResult
        print "process transes"
        
 
        process_in_crypto_low(TransResult, user_system, CurrencyInstance)
        TimeLastBlock.Value = str(CurrentBlock)
        TimeLastBlock.save()
        for trans in CryptoTransfers.objects.filter(status='processing', currency=CurrencyInstance,confirms__gte=10):
            crypton_in(trans, user_system)
            continue
   

        

def process_in_crypto(CurrencyTitle):
	List = None	 
        crypto_acc = "trade_stock"
        if CurrencyTitle in ("ZEC"):
           crypto_acc = ""
        Crypton = CryptoAccount(CurrencyTitle, crypto_acc)
        print "process %s" % CurrencyTitle
        TimeLastBlock = None
        TopBlock = int(Crypton.getblockcount())
        print "top block %i" % TopBlock
        try :
           TimeLastBlock =  VolatileConsts.objects.get(Name = "last_process_block_%s" % CurrencyTitle)
           TimeLastBlock.Value = int(TimeLastBlock.Value)

        except VolatileConsts.DoesNotExist:
           count = TopBlock - 100
           TimeLastBlock = VolatileConsts(Name = "last_process_block_%s" % CurrencyTitle, Value=str(count))
           TimeLastBlock.save()

        Time =  int(TimeLastBlock.Value) 
        print "start process block %i " % Time

        user_system =   User.objects.get(id = 1)
        CurrencyInstance = Currency.objects.get(title = CurrencyTitle)
        getcontext().prec = crypton.settings.TRANS_PREC
        block_hash = Crypton.getblockhash(Time-200)
        print "block %s" % block_hash
        List = Crypton.listsinceblock(block_hash)
        List = List["transactions"]
        process_in_crypto_low( List, user_system, CurrencyInstance)
        TimeLastBlock.Value = str(TopBlock)
        TimeLastBlock.save()
        
        


