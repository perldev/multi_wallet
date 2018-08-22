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
import signal
import pickle
import django
import random
from datetime import datetime, timedelta as dt
import time
reload(sys)
sys.setdefaultencoding('utf-8')
from django.core.management import call_command

parent_dir = os.path.abspath(os.path.dirname(__file__)) # get parent_dir path
sys.path.append(parent_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "crypton.settings")
from sdk.crypto_settings import Settings as CryptoSettings
from main.global_check import check_lock_user

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


commands = {
 "100":("process_complexity_trans",),
 "101":("incomin_btc_blockchaint_tx",),
 "102":("process_monero",),
# "103":("process_fonero",),
 "104":("thread_etc",),
 "105":("thread_eth",),
 "106":("thread_blockchain",),
}
index = 107
for Name in CryptoSettings.keys():
      print "add default  %s" % Name
      commands[str(index)] = ("incoming_crypto", Name)
      index +=1


to_start_command = None

signal_ending = 100

# this worker actully is working
def default_worker(signum):
   print "="*64
   current_workers_tasks =  getmemorystate()
   to_start_command = current_workers_tasks["to_start"]
   print "command %s" % (str(commands[to_start_command]))
   print "index %s" % (to_start_command)
   args = commands[to_start_command]
   if not check_lock_user("_".join(args)):
     try:
       call_command(*args)       
     except:
      traceback.print_exc() 
   else:
     print "="*64
     print "Ooops the processes if blocked"
     print "="*64
   # signal that telling that first worker that this worker is finishing

   uwsgi.signal(signum+signal_ending)


# register signal for workers
worker_number =  uwsgi.numproc
workers_signal = []
for i in range(2, worker_number+1):
  print "register signal %i for worker%i" % (10+i, i)
  uwsgi.register_signal(10+i, "worker%i" % i, default_worker)
  workers_signal.append(10+i)


# this worker check free workers and decide what command to start
# simple round roubine working strategy

INT_ORDS = {48, 49, 50, 51, 52, 53, 54, 55, 56, 57}

def getmemorystuff():
    v = uwsgi.sharedarea_memoryview(0)
    data = v.tobytes()
    int_string = ''
    # convert hex char to int  string 
    for char in data[:3]:
        char_ord = ord(char)
        if char_ord not in INT_ORDS:
            break
        else:
            int_string += char

    return int_string

def getmemorystate():
    v = uwsgi.sharedarea_memoryview(0)
    data = v.tobytes()
    return pickle.loads(data)


def setmemorystate(state):
    data = pickle.dumps(state)
    uwsgi.sharedarea_write(0, 0, data)
    return True


def memorystuff(state):
    uwsgi.sharedarea_write(0, 0, state)
    return True


def gracefull_stop(signum):
    state =  getmemorystate()
    state["stop"]  = True  
    setmemorystate(state)

def gracefull_reload(signum):
    state =  getmemorystate()
    state["stoping"]  = True  
    setmemorystate(state)


def routing(signum):
     state =  getmemorystate()
     current_workers_tasks = state["current_workers_tasks"]
     workers_tasks = state["workers_tasks"]
     # reload
     if state.has_key("stoping"):
        print "seems we are reload"
        print "let's start"
        if not len(current_workers_tasks.keys()):
           print "oo there is no tasks"
           print uwsgi.workers()
           del state["stoping"]
           setmemorystate(state)
           uwsgi.reload()
        return

     # stop
     if state.has_key("stop"):
        print "seems we are stoping"
        print "let's start"
        if not len(current_workers_tasks.keys()):
           print "oo there is not tasks"
           print uwsgi.workers()
           uwsgi.stop()
        return
  

     # choose command to start
     tmp_commands = commands.copy()
     for  working_task  in  current_workers_tasks.keys():
         print "delete %s " % current_workers_tasks[working_task]["comand_key"]
         del tmp_commands[current_workers_tasks[working_task]["comand_key"]] # there is no possible exception here 
     
     # if comman is existed in past half of length also do not start
     cmds = tmp_commands.keys()
     past_length = len(cmds)/2
     for past_work in  workers_tasks[-1*past_length:]:
        try:  
           del tmp_commands[past_work]#but here it seems to be 
        except KeyError:
           print "%s is already deleted  from possible executin" % past_work  
           
     cmds = tmp_commands.keys()
     to_start_command = None
     if len(cmds):
       to_start_command = random.choice(cmds)   
     else:
       print "it's seems that everything is working recently, do not let workers to be lazy"
       to_start_command = random.choice(commands.keys())   
       

     workers_signal_tmp = workers_signal[:] 
     for busy_worker in current_workers_tasks.keys():
       print "delete from choice busy worker %i" % busy_worker
       workers_signal_tmp.remove(busy_worker) 

     if len(workers_signal_tmp)>0:
       print "choosing from the workers"
       print workers_signal_tmp
       number_of_signal = random.choice(workers_signal_tmp)   
       workers_tasks.append(to_start_command)

       # write to shard memory index of  command
       state["to_start"] = to_start_command     
       current_workers_tasks[number_of_signal] = {"started": datetime.now(), "comand_key": to_start_command, "command": commands[to_start_command]}
       state["workers_tasks"] = workers_tasks[-300:] # only 300 save in history
       state["current_workers_tasks"] = current_workers_tasks
       setmemorystate(state)
       
       try: 
        print "ok sending signal %i" % number_of_signal
        print "and going start %s" % str(commands[to_start_command])
        print "and going start %s" % to_start_command
        uwsgi.signal(number_of_signal)
        print workers_tasks
       except:
        traceback.print_exc()
        print "oh no %i busy" % number_of_signal
     else:
        print "="*64
        print "there is no free workers ?!"
        print "="*64

     print "busy workers "
     nw = datetime.now()
     for working_id in current_workers_tasks.keys():
        print "%i -> %s" % (working_id, str(current_workers_tasks[working_id]))
        working_delta = nw - current_workers_tasks[working_id]["started"]
        if working_delta>dt(minutes=5):
           print "this process seems to be stuck"
           print "%i -> %s" % (working_id, str(current_workers_tasks[working_id]["command"]))
              


          
def worker_end(signum):
    workerfinsihed = signum - signal_ending
    print "task is finished  of signal %i" % (workerfinsihed)
    state =  getmemorystate()    
    del state["current_workers_tasks"][workerfinsihed]
    print state 
    setmemorystate(state)

      

# main signal of routing
uwsgi.register_signal(10, "worker1", routing)
# gracefull reload
uwsgi.register_signal(99,  "worker1", gracefull_stop)
uwsgi.register_signal(98,  "worker1", gracefull_reload)


# register for all workers signal of finishing
for i in workers_signal:
  uwsgi.register_signal(signal_ending+i, "worker1", worker_end)
  


##every 2 seconds
uwsgi.add_timer(10, 2)


## initilize state
state = {"workers_tasks":[], "current_workers_tasks": {}}
setmemorystate(state)










#uwsgi.add_timer(99, 45)
#uwsgi.add_timer(95, 50)
#uwsgi.add_timer(98, 60)
#uwsgi.add_timer(97, 90)


#uwsgi.add_timer(98, 300)
# Apply WSGI middleware here.
# from helloworld.wsgi import HelloWorldApplication
# application = HelloWorldApplication(application)
