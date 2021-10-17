# -*- coding: utf-8 -*-
"""
Created on Sat Oct 16 09:50:48 2021

@author: SemicolonExpected
"""

from getQueryStrings import *

import argparse
#import pandas as pd
import sys
import json
import re
from urllib.parse import urlparse

parser = argparse.ArgumentParser(description='Gets the Query Strings from list of urls')
parser.add_argument('--filter', dest = 'iffilter', action='store_true')
parser.add_argument('--noheader', dest = 'ifheader', action='store_false')
parser.add_argument('ifile', type=argparse.FileType('r'), help='input list of urls in txt file without header')
parser.add_argument('--ignore', dest = 'ignorelist', default="none")

args = parser.parse_args()

infile = args.ifile.name

print(args.ignorelist)

try:
    file = open(infile, 'r')
    urls = file.readlines()
except:
    print('Input file not supported')
    sys.exit(1)
    
urldict = splitUrls(urls, args.iffilter)

aggregateReferers(urldict)

domains = aggregateDomains(urldict)

'''
If the ignored file is valid then we use that, otherwise we use the default list
'''
ignorePatterns = ["facebook", "amazon", "walmart", "mikmak", "opera.com", ".edu", "romwe", "pinterest","glossier","mccormick",
                  "oldspice", "mccormick", "peloton", "oracle", "starz", "hbo", "jared", "plarium", "qualtrics", "joinhoney", 
                  "cdw", "statefarm", "verizon", "marriott.com", "okta.com", "zales.com", "leagueoflegends", "sparkfun",
                  "macys", "chase", "zillow", "target", "wendys", "playstation", "americanexpress","cafebustelo", "ugg.com", 
                  "headspace.com", "tiffany.com", "snacks.com", "samsclub.com", "vimeo.com", "tacobell.com", "hillshirefarm.com",
                  "amtrak.com", ".gov", "mubi.com", "bombas.com", "twilio.com", "icananswerthat", "poki", "8fat", "poki", "kola", 
                  "arkcrystals", "gongs-unlimited", "surrogacy", "adblock", "adgone", "adremover", "curology", "https://gop.com",
                  "kingston", "miraclesmanifesterhoodies.com", "slotomania", "covidsecure", "pdftodoc", "lezhinus.com", 
                  "decked.com", "groovyhistory", "edx.org", "entropiauniverse", "contactlensking", "christianfilipina.com", 
                  "birchgold", "typeform.com", "starstable", "filmsupply", "audible", "dixxon", "apexlegends", "xeroshoes", 
                  "disney", "pamperedchef", "groovelife.com", "lumedeodorant", "getlambs.com", "learcapital", "consolidatedcredit"] 
                    #some of these are mainstream while others are just things I know for a fact are not affiliate marketing through labelling
'''
For the ignorelist We need a way to sift the domains that are definitely NOT affiliate marketers from everything else
Because there are obscure companies that are real the Alexa 500/1000/1m doesnt work (it is also overkill)
'''
try:
    file = open(args.ignorelist, 'r')
    lines = set(file.readlines())
    iPatterns = [str.strip(urlparse(line).netloc) for line in lines]
    ignorePatterns.extend(iPatterns)
except:
    print('Ignored file not supported')
    sys.exit(1)

indicatorPatterns = {
        "convertri": {"domainpat": True, "substr": False, 
                      "attributes":{"affiliate": True, "affiliateCertainty":100}},
        "/shop.": {"domainpat": True, "substr": False, 
                      "attributes":{"affiliate": False, "affiliateCertainty":100}},
        "/store.": {"domainpat": True, "substr": False, 
                      "attributes":{"affiliate": False, "affiliateCertainty":100}},
        "/investors.": {"domainpat": True, "substr": False, 
                      "attributes":{"affiliate": False, "affiliateCertainty":100}},
        "search": {"domainpat": True, "substr": False, 
                      "attributes":{"affiliate": True, "fraud": "yes", "affiliateCertainty":100}},
        "question_chains": {"domainpat": True, "substr": False, 
                      "attributes":{"affiliate": False, "affiliateCertainty":100, "You_may_qualify_for": True}},
        "h_ad_id": {"domainpat": False, "substr": False, 
                    "attributes":{"webinar-or-book": True,"webinarCertainty": 90, "tracker": "hyros", "affiliate": False, "affiliateCertainty":50}},
        "wickedid": {"domainpat": False, "substr": False, 
                    "attributes":{"webinar-or-book": True, "webinarCertainty": 90, "tracker": "wickedreports", "affiliate": False, "affiliateCertainty":50}},
        "webinar": {"domainpat": True, "substr": False, 
                    "attributes":{"webinar-or-book": True, "webinarCertainty": 100, "affiliate": False, "affiliateCertainty":50}},
        "ac": {"domainpat": False,"substr": False, 
               "attributes":{"affiliate": True, "fraud": "Ad-hijacker" ,"affiliateCertainty": 100}},
        "adp": {"domainpat": False,"substr": False, 
                "attributes":{"affiliate": False, "affiliateCertainty": 100}},
        "abtf2": {"domainpat": False,"substr": False, 
                  "attributes":{"affiliate": False, "affiliateCertainty": 100, "adware": "MobiGame"}},
        "baexist": {"domainpat": False,"substr": False, 
                    "attributes":{"affiliate": False, "affiliateCertainty": 100, "adware": "MobiGame"}},
        "contract_id": {"domainpat": False,"substr": False, 
               "attributes":{"affiliate": True, "fraud": "Ad-hijacker","affiliateCertainty": 100}},
        "creativeId": {"domainpat": False,"substr": False, 
                "attributes":{"affiliate": True, "affiliateCertainty": 100}},
        "s4": {"domainpat": False,"substr": False, 
                "attributes":{"affiliate": True, "affiliateCertainty": 90}},
        "sub4": {"domainpat": False,"substr": False, 
                "attributes":{"affiliate": True, "affiliateCertainty": 100}},
        "subid": {"domainpat": False,"substr": False, 
                "attributes":{"affiliate": True, "affiliateCertainty": 95}}
        }
                     #"aff": {"substr": True, "attributes": {"affiliate": True}}}
urlsToQuery = []
#print( domains[list(domains.keys())[0]].keys() )
for domain in domains:
    ignore = False
    #to speed things up we just skip past the items that are clearly not affiliates
    host = domains[domain]
    for pat in ignorePatterns:
        if pat in domain.lower():
            ignore = True
            host["affiliate"] = False
    if not ignore:
        host = domains[domain]
        for link in host["links"]:
            #ideally we only need to check one link, but i want to catch outliers
            for indicator in indicatorPatterns:
                if indicatorPatterns[indicator]["domainpat"]==True:
                    if indicator in link:
                        host.update(indicatorPatterns[indicator]["attributes"])
                if indicatorPatterns[indicator]["substr"] == False:
                    if indicator in host["links"][link]:
                        host.update(indicatorPatterns[indicator]["attributes"])
                        #if indicator is "wickedid":
                            #print(domain, link)
                else:
                    for key in host["links"][link]:
                        if indicator in key.lower():
                            print(domain, indicator, key)
'''
Scrape links off remaining domains
'''

numAff = 0
numWebinar = 0
domainsRemaining = {}
for domain in domains:
    if "affiliate" in domains[domain]:
        if domains[domain]["affiliate"] is True:
            numAff = numAff + 1
        else:
            if "webinar-or-book" in domains[domain]:
                numWebinar = numWebinar + 1
    else:
        domainsRemaining[domain] = domains[domain]
            
print("Total Domains: ",len(list(domains.keys())), " # of Affiliates: ", numAff, " # of Possible Webinars: ", numWebinar)
#print(urlparse("https://todays-tech.co/hp/US/x-85/").scheme, urlparse("https://todays-tech.co/hp/US/x-85/").netloc)
print("Domains Remaining", len(list(domainsRemaining.keys())))

out_file = open("lookat.json", "w")
json.dump(domainsRemaining, out_file, indent = 4)
out_file.close()

#out_file = open("organizedUrls.json", "w")
#json.dump(domains, out_file, indent = 4)
#out_file.close()