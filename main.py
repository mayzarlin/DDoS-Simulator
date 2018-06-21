# -*- coding: utf-8 -*-
"""
Created on Wed Jun 13 17:31:07 2018

@author: May Lin
"""
import dns.resolver
from imp import reload
from datetime import datetime
from datetime import timedelta
import DGA.Matsnu
import logging
import time
import random
import string

def main():
    reload(dns.resolver)
    logging.basicConfig(filename='log/attack06_20.log', level=logging.INFO)
    
    attacktime = 480# in second
    dlay = 1 # 0 no delay
    tdelta =  15 # minutes for round time (for example 15 minutes)
    offsetsleeptime = 120 # in second
    #maxrate = 10# maximum query rate per second
    #diff = 2 # rate increase between each attack.
    rate = (1,5) # in query per second
    attackrate,i = 0,0
    #domain_generator = (DGA.Matsnu.Matsnu,randomdomain,randomsubdomain,valid_domain)
    domain_generator = (randomsubdomain,randomdomain,DGA.Matsnu.Matsnu) # valid_domain)
    for func in domain_generator:
        i=0
        while True:
                attackrate = rate[i]
                #SEED = attacktime*attackrate
                # attackrate number of query per second
                logging.info('%s Started with Kids and Parental Control %s. ',datetime.now(),'#'*20)
                logging.info('attackrate = %d qps, attacktime = %d s, Domain Generator = %s',attackrate,attacktime,func.__name__)
                now = datetime.now()
                while True:
                    ###### DGA
                    if datetime.now()>= now+timedelta(seconds = attacktime):
                        break
                    domain = func.domain()
                    #domain = randondomain()
                    #domain = DGA.lockyDGA.lockyDGA(z, SEED, now)
                    #domain = DGA.Tinba.Tinba(count = 1)
                    ##### Random sub domain domainname , TLD = com (default), subdomainlen = 8(default)
                    #domain = randomsubdomain(domainname = 'amazon')
                    ##### regular query
                    #domain = 'www.google.com'
                    sendtime = datetime.now()
                    #print(domain)
                    logging.info('%s %s',datetime.now(),domain)
                    dnsquery(domain,'A')
                    while True: # to adjust qps.
                        if datetime.now() >= sendtime + timedelta(seconds = 1/attackrate):
                            break
                    
                logging.info('%s Finish %s. \n',datetime.now(),'#'*30)
                if dlay == 1:
                    nextattacktime = datetime.now()+timedelta(minutes = tdelta)
                    nextattacktime -= timedelta(minutes = nextattacktime.minute%tdelta)
                    d = nextattacktime-datetime.now()
                    timetosleep = d.seconds+offsetsleeptime
                else:
                    timetosleep = 1
                i+=1
                # sleep till next round time 
                time.sleep(timetosleep)
                if i == len(rate):
                    break
           
            #print('Waiting')
    logging.shutdown()
        
##########################  Sending out DNS Query
def dnsquery(qname,rdtype=dns.rdatatype.NS, rdclass=dns.rdataclass.IN,
             source=None,source_port = random.randint(0,1024),
             timeout = 1):
        request = dns.message.make_query(qname,rdtype)
        default = dns.resolver.get_default_resolver()
        #random.randint(0,65535)
       # while response is None:
        #dns.resolver.Timeout.msg = None
        for nameserver in default.nameservers:
            dns.query.udp(request,nameserver,
                          timeout = timeout,
                          source_port = source_port) 
########  ### Random Subdomain Generation

class randomsubdomain():
        def domain(domainname = 'google',TLD ='com',subdomainlen = 8):
            subdomain = ''
            for i in range(subdomainlen):
                subdomain +=random.choice(string.ascii_letters+string.digits)
            return subdomain+'.'+domainname+'.'+TLD    
class valid_domain():
    def domain():
        return 'netflix.com'
##############
class randomdomain():
    def domain():
        domain= ''.join((random.choice(string.ascii_letters+string.digits) for i in range(random.randint(8,15))))
        return domain+'.'+''.join((random.choice(string.ascii_lowercase) for i in range(2)))

if __name__ == "__main__": main()
