# cochrane-translation-hacks

This contains some experimental code to access Plain Language Summaries of Cochrane reviews.

The file scrape-pls-from-cochrane-3.py takes three language codes and scrapes the corresponding versions of Plain Language Summaries off the first 100 Google search results. It usually returns around 30 trios of HTML documents. A timestamped results file in HTML links all of them. All HTML files are tidy-ed. 

There is an older scrape-pls-from-cochrane.py that takes only two language codes and does not clean up HTML so that is valid.

## To do

* Ideally, the scraper could be generalized so it deals with any number of languages between 2 and 3.
* One should be able to add some keywords to narrow the search
* More language codes have to be added

