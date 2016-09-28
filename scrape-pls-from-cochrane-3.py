#!/usr/bin/python3
# Getting some dozens of trilingual Cochrane PLSs from Wiley's site 
# (from the first Google 100 hits)
# Copyright (c) Mikel L. Forcada 2016
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 3 of the License, or
#   (at your option) any later version.
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software Foundation,
#   Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301  USA


import sys
import os
from bs4 import BeautifulSoup
import requests
import re


# Google query minus the language word
partialquery="site:onlinelibrary.wiley.com/doi/10.1002 14651858 plain language summary abstract"


if len(sys.argv)!=4 :
   print ("Usage: scrape-pls-from-cochrane.py languagecode1 languagecode2 languagecode3")
   exit()

else :
# Read languages and filename prefix from command line
   lang1=sys.argv[1]
   lang2=sys.argv[2]
   lang3=sys.argv[3]
# Language words
   langnames = {"de" : "german" , 
                "pl" : "polish" ,
                "cs" : "czech"  ,
                "ro" : "romanian" , 
                "es" : "spanish" , 
                "fr" : "french" ,
                "en" : "english" }
# get results page for selected languages (100 results)

   page = requests.get("https://www.google.cat/search?q=" + partialquery + " " + langnames[lang1] + " " + langnames[lang2] + " " + langnames[lang3] + "&num=100")

# parse the page into a tag soup
   soup = BeautifulSoup(page.content,"html.parser")

# get all links in the page
   links = soup.findAll("a")

# The list of relevant URLs is empty
   urllist = set()    

# Files will be numbered in this version
# Ideally, they should contain part of the URL: later

# Get all links, and turn them into direct URLs not going through Google
# Stole this code snippet from http://stackoverflow.com/questions/25471450/python-getting-all-links-from-a-google-search-result-page
   for link in  soup.find_all("a",href=re.compile("(?<=/url\?q=)(htt.*://.*)")):
       url=(re.split("&",link["href"])[0]).replace("/url?q=","")
# Compile the pattern that the really interesting result URLs follow
       pattern=re.compile("^http[:]//onlinelibrary[.]wiley[.]com/doi/10[.]1002/14651858[.]CD[0-9][0-9][0-9][0-9][0-9][0-9][.]pub[0-9]?/abstract$")
 
# If URLs match the pattern, add them to the URL list
       if pattern.match(url) : 
          urllist.add(url)


# debug
# for url in urllist :
#   print(url)

# Now process the pages in the URL list
for url in urllist :

     pattern=re.compile("CD[0-9][0-9][0-9][0-9][0-9][0-9][.]pub[0-9]?")
     fileprefix = pattern.search(url).group(0)

# get page and parse it into a tag soup
     page = requests.get(url)
     soup = BeautifulSoup(page.content,"html.parser")

# cut out the Plain Language Summary parts that are in the selected languages
     snippet1=soup.find("div",id=lang1 + "_short_abstract")
     snippet2=soup.find("div",id=lang2 + "_short_abstract")
     snippet3=soup.find("div",id=lang2 + "_short_abstract")

        
# If all three snippets are not empty, write them to conveniently named files, and tidy them using command-line tidy
     print("Processing " + fileprefix)
     if snippet1 and snippet2 and snippet3 :
        filename1 = fileprefix +  "_PLS_" + lang1 + ".html"
        filename2 = fileprefix +  "_PLS_" + lang2 + ".html"
        filename3 = fileprefix +  "_PLS_" + lang3 + ".html"
      
        with open(filename1, "w", encoding="utf-8") as text_file :
            for tagg in snippet1 :
                text_file.write(str(tagg))
#        os.system("tidy -m -utf8 -asxml " + filename1 + " >/dev/null 2>/dev/null")
        with open(filename2, "w", encoding="utf-8") as text_file :
            for tagg in snippet2 :
                text_file.write(str(tagg))
#        os.system("tidy -m  -utf8 -asxml" + filename2 + " >/dev/null 2>/dev/null")
        with open(filename3, "w", encoding="utf-8") as text_file :
            for tagg in snippet3 :
                text_file.write(str(tagg))
#        os.system("tidy -m  -utf8 -asxml" + filename3 + " >/dev/null 2>/dev/null")

# And that's all folks	
