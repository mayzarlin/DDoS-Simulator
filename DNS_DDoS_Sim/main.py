# -*- coding: utf-8 -*-
"""
Created on Fri Jun 15 16:25:45 2018

@author: May Lin
"""

import DNS_DDoS

def main():
    ## There are three domain generator
    # DNS_DDoS.randomsundomain
    # DNS_DDoS.valid_domain()
    # DNS_DDoS.randomdomain()
    #DNS_DDoS.Matsnu()
    DNS_DDoS.Attack(domain_generator=DNS_DDoS.Matsnu())
if __name__ == "__main__": main()