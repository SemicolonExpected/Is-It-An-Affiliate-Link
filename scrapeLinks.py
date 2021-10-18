# -*- coding: utf-8 -*-
"""
Created on Thu Oct 14 15:44:23 2021

@author: SemicolonExpected
"""
"""

curl "https://astrosnout.com/images/uploads/game1/10200/fortnite.png" ^
  -H "sec-ch-ua: ^\^"Chromium^\^";v=^\^"94^\^", ^\^"Google Chrome^\^";v=^\^"94^\^", ^\^";Not A Brand^\^";v=^\^"99^\^"" ^
  -H "Referer: https://astrosnout.com/action/fortnite?utm_content=target2&gclid=EAIaIQobChMIvprwt93h8QIVxrpRCh1BRgQ1EAEYASAAEgJO9_D_BwE" ^
  -H "sec-ch-ua-mobile: ?0" ^
  -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36" ^
  -H "sec-ch-ua-platform: ^\^"Windows^\^"" ^
  --compressed
  
"""
# get list of links and referer (main site)
# use getquerystrings to split
# merge sites to referer

import requests
from requests.structures import CaseInsensitiveDict
from bs4 import BeautifulSoup

import argparse
import pandas as pd
import sys
import json
import re

    
def scrape(urls, ifFilter = False):
    
    headers = CaseInsensitiveDict()
    headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81   Safari/537.36"

    #in future grab all the script and maybe see if can find urls in that
    #grab all the a tags and li tags
    ignorePatterns = ["", "#", None, "javascript:void(0)"]
    urldict = {}
    domainNum = 1
    for domain in urls:
        print("Domain ", domainNum, " ", domain)
        urldict[domain] = {}
        for url in urls[domain]:
            urldict[domain][url] = {"links" : []}
            try:
                response = requests.get(url, headers=headers, timeout=10)
            except:
                print(url, "would not connect")
                urldict[domain][url]["links"].append("dead")
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'lxml')
                for line in soup.find_all('a'):
                    if line.get('href') not in ignorePatterns:
                        urldict[domain][url]["links"].append(line.get('href'))
                    #print(line.get('href'))
            else:
                urldict[domain][url]["Status Code"] = response.status_code
        domainNum = domainNum + 1
    return urldict
        #r = re.compile(r"(http://[^ ]+)")
        #r = re.compile(r"(http://[^ ]+)")
        #print( re.search("(?P<url>https?://[^\s]+)", response).group("url") )
        

    #grab anything http:// and anything js

    #if https:// or .js in text
    #{url: url affiliate: true/false, links: []}

    
    #url = ""
    #resp = requests.get(url, headers=headers)
    




#if resp.status_code == 200 then get response text