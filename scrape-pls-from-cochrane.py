#!/usr/bin/python3
# Getting some dozens of multilingual parallel Cochrane PLSs from Wiley's site 
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
import re
import datetime

try:
    from bs4 import BeautifulSoup
except ImportError:
    raise ImportError('Please install Beautiful Soup 4')

try:   
    import requests
except ImportError:
    raise ImportError('Please install requests')


# Google query minus the language word
partialquery="site:onlinelibrary.wiley.com/doi/10.1002 14651858 plain language summary abstract"


if len(sys.argv)<3 :
   print ("Usage: scrape-pls-from-cochrane.py languagecode1 languagecode2 [ languagecode ]*")
   exit()

else :
# Read languages and filename prefix from command line
   nlangs=len(sys.argv)
   lang = []
   for k in range(1,nlangs) :
       lang.append(sys.argv[k])

# Language words (list from web, may be incomplete )
   langnames = {"de" : "german" , 
                "pl" : "polish" ,
                "ms" : "malay" ,  
                "fr" : "french" ,
                "en" : "english",
                "hr" : "croatian", 
                "ru" : "russian",
                "jp" : "japanese", 
                "pt" : "portuguese" ,
                "ta" : "tamil" }

# get results page for selected languages (100 results)

# build language string
   langstring = ""
   for k in range(0,nlangs-1) :
       langstring = langstring + " " + langnames[lang[k]] 

   page = requests.get("https://www.google.cat/search?q=" + partialquery + langstring + "&num=100")

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



# Now process the pages in the URL list

# start writing a results file 

# build filename
results_filename = "results"
for k in range(0,nlangs-1) :
    results_filename = results_filename + "_" + lang[k]
results_filename = results_filename + ".html"

# minimum preamble
results_file = open(results_filename, "w", encoding="utf-8") 
results_file.write("<html>") # will be tidy-ed later
results_file.write("<body>") 
now=datetime.datetime.now()
results_file.write("<h1>Results:" + now.ctime() + "</h1>")


for url in urllist :

     pattern=re.compile("CD[0-9][0-9][0-9][0-9][0-9][0-9][.]pub[0-9]?")
     fileprefix = pattern.search(url).group(0)

# get page and parse it into a tag soup
     page = requests.get(url)
     soup = BeautifulSoup(page.content,"html.parser")

# cut out the Plain Language Summary parts that are in the selected languages
     snippet = []
     for k in range(0,nlangs-1) :
         snippet.append(soup.find("div",id=lang[k] + "_short_abstract"))

        
# If all snippets for the URL are not empty, write them to conveniently named files, and tidy them using command-line tidy
     print("Processing " + fileprefix)
     condition = True 
     for k in range(0,nlangs-1) :
         condition = condition and snippet[k]
     if condition :
        results_file.write("<p>" + fileprefix + ": ")
        results_file.write('<a href="' + url + '">original file</a> ') 
        for k in range(0,nlangs-1) :
            filename = fileprefix +  "_PLS_" + lang[k] + ".html"
            with open(filename, "w", encoding="utf-8") as text_file :
               for tagg in snippet[k] :
                   text_file.write(str(tagg))
            results_file.write('<a href="' + filename + '">' + lang[k] + "</a> ")
            text_file.close() 
            os.system("tidy -m -utf8 -asxml " + filename + " >/dev/null 2>/dev/null")
        results_file.write("</p>")
# And that's all folks	

results_file.write("</body></html>")
results_file.close()
os.system("tidy -m -utf8 -asxml " + results_filename + " >/dev/null 2>/dev/null")

