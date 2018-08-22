# -*- coding: utf-8 -*-

from main.models  import Accounts, Currency, TradePairs, sato2Dec, change_volitile_const,VolatileConsts
from blockchain.wallet import Wallet
from sdk.crypto import CryptoAccount
from sdk.crypto_krb import CryptoAccountKrb, PREC as PREC_KRB 
from sdk.crypto_xem import CryptoAccountXem 
from sdk.crypto_xrp import CryptoAccountXrp
import crypton.settings
from sdk.crypto_settings import Settings as CryptoSettings
import json
import requests
import blockchain.util
import urllib2
import main.msgs
import traceback
'''
 <h3>Мы должны: {{item.currency}} <h3>
 <p>На ордерах: {{item.sum}} {{item.currency}} </p>
 <p>Ошибка: {{item.mistake}} {{item.currency}} </p>
 <p>Комиссия: {{item.comission}} {{item.currency}} </p>
 <p>Сальдо ввод - вывод: {{item.saldo}} </p> 
'''
import crypton.settings as settings
from django.db import connection
from decimal import Decimal
from sdk.p24 import p24


from main.models import VolatileConsts

def check_ip(obj):
    try:
        VolatileConsts.objects.get(Name="white_ip_%s" % user.username, Value=ip)
        return True
    except :
        pass
    
    try:
        VolatileConsts.objects.get(Name="white_ip_%s" % user.username, Value="%")
        return True
    except :
        pass 

    print "http://api.db-ip.com/v2/%s/%s" % (settings.GEO_API, obj.description)
    res = requests.get("http://api.db-ip.com/v2/%s/%s" % (settings.GEO_API, obj.description))

    result = res.json()
    print result
    obj.tx_checking = str(result)
    obj.save()
    
    
    
    if not  result["countryCode"] in ("UA", ) :
       try:
          VolatileConsts.objects.get(Name="pin_restore_"+str(obj.order_id))
          print "but we have aproving"
          return True
       except:
          traceback.print_exc()
          return False
    else:
       return True

def save_var(name, value):
    var = VolatileConsts(Name=name,
                          Value=value)
    var.save(using="security")


def change_var(var, new_value, new_name=None):
   if new_name is None:
      var.Value = new_value
      var.save() 
   else:
      var.Value = new_value
      var.Name = new_name
      var.save(using="security")

def get_vars(name):
    return list(VolatileConsts.objects.using("security").filter(Name=name).order_by("id"))

def lock_user(User):
    lock = VolatileConsts(Name="user_lock",
                          Value=User.username)
    lock.save(using="security")

def check_approve(obj):
    try:
        d = VolatileConsts.objects.using("security").filter(Name="approve_trans",
                                    Value=str(obj.id)).count()
        if d>0:
          return True
        else:
          return False
    except:
        return False

def approve_trans(obj):
    approve = VolatileConsts(Name="approve_trans",
                          Value=str(obj.id))
    approve.save(using="security")


def check_lock_user(username):
    try:
        l = list(VolatileConsts.objects.using("security").filter(Name="user_lock", Value=username))
        l2 = list(VolatileConsts.objects.filter(Name="user_lock", Value=username))
        return len(l)>0 or len(l2)>0
    except:
        return False




def check_global_lock():
	try :
		l = list(VolatileConsts.objects.using("security").filter(Name = "global_lock"))
		l2 = list(VolatileConsts.objects.filter(Name = "global_lock"))
		return len(l)>2 or len(l2)>2
	except :
		return False

def lock_global(Desc):
	lock = VolatileConsts(Name = "global_lock", Value = Desc)
	lock.save(using = "security")

def check_uah_balance():
        cursor = connection.cursor()
        cursor.execute("SELECT sum(balance) FROM main_accounts WHERE currency_id=1 AND balance>0 AND balance<1000000 AND id!=353 ");
        s = cursor.fetchone()*1
        if s == (None, ) :
              s = Decimal("0.0")
        else:
           (s, ) = s
        cursor.execute("SELECT sum(amnt)*0.99 FROM main_cardp2ptransfers WHERE status in ('created','processing','processing2','auto') AND pub_date>='2015-05-08' ");

        s1 = cursor.fetchone()*1
        if s1 == (None, ) :
              s1 = Decimal("0.0")
        else:
           (s1, ) = s1

        D = p24("UAH", "https://api.privatbank.ua/", settings.P24_MERCHID2, settings.P24_PASSWD2, settings.P24MERCH_CARD2)
        D1 = p24("UAH", "https://api.privatbank.ua/", settings.P24_MERCHID, settings.P24_PASSWD, settings.P24MERCH_CARD)
        BalanceUAH  = Decimal(D.balance() ) + Decimal(D1.balance())
        return (BalanceUAH - s - s1+16200)>0


def check_btc_balance(verbose=False):
        
        return 1>=0

def get_balance(addr, Confs=0):
    Res = get_adress(addr)
    print int(Res["final_balance"])
    return int(Res["final_balance"])

def get_balance1( Adr, Confs=0 ):
    Url = "https://blockchain.info/q/addressbalance/{0}?confirmations={1}".format(Adr, Confs)

    Decoder = json.JSONDecoder()
    D = urllib2.urlopen(Url)
    Str = D.read()
    print Str
    return  int(Str)

def get_adress( Adr ):
    Url = "https://blockchain.info/address/%s?format=json" % (Adr)

    Decoder = json.JSONDecoder()
    D = urllib2.urlopen(Url)
    Str = D.read()
    Res = Decoder.decode(Str)
    return Res

def check_crypto_balance(Currency, Correction =  "0", check_wallet=True):
        cursor = connection.cursor()
        cursor.execute("SELECT sum(balance) FROM main_accounts WHERE currency_id=%i AND balance>0" % Currency.id);
        s = cursor.fetchone()*1
        if s == (None, ) :
              s = Decimal("0.0")
        else:
           (s, ) = s

        cursor.execute("SELECT sum(amnt) FROM main_cryptotransfers WHERE debit_credit='out' \
			AND status in ('processing','processing2','created') AND pub_date>='2015-05-08' and currency_id=%i " % Currency.id);

        s1 = cursor.fetchone()*1
        if s1 == (None, ) :
              s1 = Decimal("0.0")
        else:
           (s1, ) = s1
        
        cursor.execute("SELECT sum(amnt) FROM main_cryptotransfers WHERE debit_credit='in' \
			AND status in ('processing', 'processing2') AND confirms>0 AND pub_date>='2015-05-08' and currency_id=%i " % Currency.id);

        s2 = cursor.fetchone()*1
        if s2 == (None, ) :
              s2 = Decimal("0.0")
        else:
           (s2, ) = s2

        Crypton = None
        Balance = None
        if check_wallet:
          if Currency.title in ("KRB",):
  
            Crypton = CryptoAccountKrb(Currency.title, "trade_stock")
            Balance  = Crypton.getbalance()

          if Currency.title in ("XMR",):
              rpc_url = CryptoSettings[Currency.title]["host"]
              req =  {"jsonrpc":"2.0","method":"getbalance", "id":1}
              resp = requests.post(rpc_url, data=json.dumps(req) )
              print resp.json() 
              Balance = float(resp.json()["result"]["balance"])/PREC_KRB
              Balance = "%.12f" % ( Balance )
   
          if Currency.title in ("ZEC", "BCH", "DOGE", "TLR", "FNO"):

            Crypton = CryptoAccount(Currency.title, "")
            Balance  = Crypton.getbalance()

          if Currency.title in ("XRP", ):
            Crypton = CryptoAccountXrp(Currency.title, "")
            Balance  = Crypton.getbalance(CryptoSettings[Currency.title]["acc"])
         
          if Currency.title in ("XEM", ):
            Crypton = CryptoAccountXem(Currency.title, "")
            Balance  = Crypton.getbalance(CryptoSettings[Currency.title]["acc"])


          if Currency.title in ("LTC","NVC", "DOGE", "ITI", "DASH", "PPC", "CLR", "SIB" ):
   
            Crypton = CryptoAccount(Currency.title, "trade_stock")
        
            Balance  = Crypton.getbalance()

          change_volitile_const("balance_corr_"+Currency.title, Correction)
          change_volitile_const("balance_out_"+Currency.title, str(Balance))
	print "balance in system %s" % s
	print "balance on wallet " + str(Balance)
	print s1+s
        if check_wallet:
	  Delta = (Decimal(Balance) - s1 - s - s2  + Decimal(Correction))
	  print "Delta is %s " % Delta
          return Delta>0
        return True





def check_crypto_currency(Cur, Eps="0.01"):
       
        Main_Account = Accounts.objects.get(user_id = settings.CRYPTO_USER, currency = Cur)
        cursor = connection.cursor()
        transit_accounts = []
        for pair  in TradePairs.objects.all():
            transit_accounts.append(str(pair.transit_on.id))
            transit_accounts.append(str(pair.transit_from.id))
        
        ComisId = settings.COMISSION_USER
        
        NotId = ",".join(transit_accounts)
        #not Credit and not Mistake and not transit accounts
        Query =  "SELECT sum(balance) FROM main_accounts \
                    WHERE currency_id=%s \
                    AND user_id not in (346, 31, %s) AND id not in (%s) AND balance>0 " % (str(Cur.id), ComisId, NotId)
                    
        cursor.execute(Query, [])
        S1 = cursor.fetchone()
        if S1 == (None, ) :
                S1 = Decimal("0.0")
        else :
                S1 = S1[0]
                
        Query = "SELECT sum(sum1) FROM main_orders \
                        WHERE currency1_id=%s AND currency2_id!=currency1_id \
                        AND status=\"processing\"  \
                        AND user_id not in (346)  " % (str(Cur.id))   
                        
        cursor.execute(Query, [  ])
        
        S2 = cursor.fetchone()*1
        if S2 == (None, ) :
                S2 = Decimal("0.0")
        else :
                S2 = S2[0]
        print S1
        print S2
        CheckSum  = S1 + S2
        print "balance in system "
        print CheckSum
        print "balance on wallet"
        print Main_Account.balance
        print "div between two sums "
        print CheckSum + Main_Account.balance
        if CheckSum <= abs(Main_Account.balance):
            return False
        else :
            return True	


def check_currency_orders(Cur, Eps=0.01):
    
        cursor = connection.cursor()
        transit_accounts = []
        trade_pairs = []
        for pair  in TradePairs.objects.filter(status = "processing", currency_on = Cur):
            transit_accounts.append( str( pair.transit_on.id ) )
            trade_pairs.append( str( pair.id ) )

            
        for pair  in TradePairs.objects.filter(status = "processing", currency_from = Cur):
            transit_accounts.append( str( pair.transit_from.id ) )
            trade_pairs.append( str( pair.id ) )

            
        ComisId =  settings.COMISSION_USER
        InId = ",".join(transit_accounts)
        TradesId = ",".join(trade_pairs)
        Query = "SELECT sum(balance) FROM main_accounts WHERE  id IN (%s)  " % (InId)
        #print Query
        cursor.execute(Query, [])
            
        TransitSum = cursor.fetchone()*1
        if TransitSum == (None, ) :
                TransitSum = Decimal("0.0")
        else :
                TransitSum = TransitSum[0]  
        Query = "SELECT sum(sum1) FROM main_orders \
                        WHERE currency1_id=%s AND currency2_id!=currency1_id \
                        AND status=\"processing\"  \
                        AND user_id not in (346) AND trade_pair_id in (%s) " % ( str(Cur.id), TradesId )        
        #print Query
        cursor.execute(Query, [])
        
        OrdersSum = cursor.fetchone()*1
        if OrdersSum == (None, ) :
                OrdersSum = Decimal("0.0")
        else :
                OrdersSum = OrdersSum[0]
        print "on orders"       
        print OrdersSum
	print "on accounts"
        print TransitSum
   	print "Delta transit sum %s" % (TransitSum-OrdersSum)  
        if TransitSum < OrdersSum  :
	    print "case 1"
            return True
        else :
	    print "case 2"
            if  OrdersSum - TransitSum > Eps :
                return True
            else :
                return False

		

def check_fiat_currency(Cur):
        cursor = connection.cursor()
        pay_in_out = []
        for pair  in TradePairs.objects.filter( currency_on = Cur, currency_from  = Cur):
            pay_in_out.append(str(pair.transit_on.id))
            pay_in_out.append(str(pair.transit_from.id))
            
        ComisId =  settings.COMISSION_USER
        MainIn = ",".join(pay_in_out)
        Query = "SELECT sum(balance) FROM main_accounts WHERE  in (%s) " % (MainIn)
        #not Credit and not Mistake and not transit accounts
        cursor.execute(Query, [])
            
        WholeSum = cursor.fetchone()*1
        if  WholeSum == (None, ) :
                WholeSum = Decimal("0.0")
                
        transit_accounts = []
        for pair  in TradePairs.objects.all():
            transit_accounts.append(str(pair.transit_on.id))
            transit_accounts.append(str(pair.transit_from.id))
            
        ComisId =  settings.COMISSION_USER
        NotId = ",".join(transit_accounts)
        #not Credit and not Mistake and not transit accounts
        Query = "SELECT sum(balance) FROM main_accounts WHERE currency_id=%s \
                            AND user_id not in (346, 31) AND id not in (%s) AND balance>0 " % (str(Cur.id), NotId)
        cursor.execute(Query, [])
            
        S1 = cursor.fetchone()*1
        if S1 == (None, ) :
                S1 = Decimal("0.0")
        
        Query = "SELECT sum(sum1) FROM main_orders WHERE currency1_id=%s AND currency2_id!=currency1_id \
                                                AND status=\"processing\"  \
                            AND user_id not in (346)  " % ( str(Cur.id) )
        cursor.execute(Query, [])
        
        S2 = cursor.fetchone()*1
        if S2 == (None, ) :
                S2 = Decimal("0.0")
        print S1
        print S2
        print Main_Account.balance
        if S1 + S2 < WholeSum:
            return check_currency_orders(Cur)
        else :
            return True 
        
        
        
