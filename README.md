# cochrane-translation-hacks

This contains a experimental script to access Plain Language Summaries of Cochrane reviews.

The file `scrape-pls-from-cochrane.py` takes 2 or more ISO-639-2 language codes and scrapes the corresponding versions of Plain Language Summaries off the first 100 Google search results on the Wiley Library. It returns sets of parallel HTML documents containg the plain language summaries. A timestamped results file in HTML links all of them. All HTML files are tidy-ed. 

Older version of the code may be found in the `dev` directory.

## To do

* One should be able to add some keywords to narrow the search
* Check if all language codes in the website are there

## Requirements

### Python modules

* Beautiful Soup 4.0 (bs4)
* requests 

### Other software

* Command-line HTML tidy

## License

* GPL v3
