"""
WSGI config for crypton project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""
import os


# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
#from django.core.wsgi import get_wsgi_application
#application = get_wsgi_application()

import uwsgi
import traceback 
import sys
import django
reload(sys)
sys.setdefaultencoding('utf-8')
from django.core.management import call_command

parent_dir = os.path.abspath(os.path.dirname(__file__)) # get parent_dir path
sys.path.append(parent_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "crypton.settings")


#django.setup()

#*/15 *  *  *   *         cd crypton;python ./manage_lock.py out_crypto_block BTC 0 1>> out_btc.log 2>>out_btc.log
#*/15 *  *  *   *         cd crypton;python ./manage_lock.py out_crypto_eth 1>> out_eth.log 2>>out_eth.log
#*/5    *  *   *   *     cd crypton;python ./manage_lock.py out_crypto_merger 1>> out_crypto_merged.log 2>> out_crypto_merged.log
#*/3    *  *   *   *       cd crypton; python  ./manage_lock.py  incomin_btc_blockchaint_tx 1>>  incomin_btc_blockchaint_tx.log 2>>incomin_btc_blockchaint_tx.log
#*/4    *  *   *   *       cd crypton; python  ./manage_lock.py  process_complexity_trans 1>> process_complexity_trans.log 2>>process_complexity_trans.log
#*/5  *  *   *   *       cd crypton; python ./manage_lock.py  incoming_crypto_merger 1489820322  1>> incoming_crypto_merger.log 2>>incoming_crypto_merger.log
#*/10  *  *   *   *       cd crypton;  python ./manage_lock.py check_out_tx 1>> check_out_tx.log 2>> check_out_tx.log
#*/4  *  *   *   *     cd crypton;python ./manage_lock.py global_crypto_check 1>> global_check.log 2>>global_check.log
#*  *  *   *   *     cd crypton;python ./manage_lock.py encrypt_pin 1>> pin_encrypting.log 2>>pin_encrypting.log
#10  2  *   *   *     cd crypton;python ./manage_lock.py backup_wallets 2>>result_back.log 2>>result_back.log



def worker(signum):

    try:
      call_command('btc_fee')
    except:
      traceback.print_exc()


    try:
      call_command('wallets_new')
    except:
      traceback.print_exc()

    try:
      call_command('encrypt_pin')
    except:
      traceback.print_exc()



def out_eth(signum):
    try:
      call_command('out_crypto_eth')
    except:
      traceback.print_exc()
    try:
      call_command('out_crypto_etc')
    except:
      traceback.print_exc()
 

 

def out_trans(signum):
    uwsgi.lock()
    try:
      call_command('out_crypto_merger')
    except:
      traceback.print_exc()
    
    try:
      call_command('out_monero')
    except:
      traceback.print_exc()
    
   # try:
   #   call_command('out_fonero')
   # except:
   #   traceback.print_exc()
    



    try:
      call_command('out_crypto_block', "BTC", "0")
    except:
      traceback.print_exc()

    uwsgi.unlock()


def sweep(signum):

    try:
      call_command('sweep_etc')
    except:
      traceback.print_exc()
    
    try:
      call_command('sweep_eth')
    except:
      traceback.print_exc()
    



uwsgi.register_signal(96, "", out_trans)
uwsgi.add_timer(96, 300)

uwsgi.register_signal(97, "", out_eth)
uwsgi.add_timer(97, 30)

uwsgi.register_signal(98, "", sweep)
uwsgi.add_timer(98, 600)

uwsgi.register_signal(99, "", worker)
uwsgi.add_timer(99, 60)

#uwsgi.add_timer(98, 300)
# Apply WSGI middleware here.
# from helloworld.wsgi import HelloWorldApplication
# application = HelloWorldApplication(application)
