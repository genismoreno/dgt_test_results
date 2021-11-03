# DGT Test results scraper

## Basic scraper for DGT test results

Providing the body and the headers with the user credentials 
(DNI, fecha examen, tipo permiso, fecha de nacimiento), 
results request is automatized. 

Useful if integrated in an iterative environment.

### How to run
1. `git clone git@github.com:genismoreno/dgt_test_results.git`
2. `cd dgt_test_results`
3. `pip install -r requirements.txt`
4. Create _body.txt_ and _headers.txt_ files
5. `python main.py`

### Requirements
1. requests
2. lxml (html)

### Files to be provided
All info could be provided from the browser console when accessing via web (recommended way).

1. `body.txt` Text content
2. `headers.txt` Text content in raw format. Code is capable of converting it to a dictionary.

### Lxml documentation
1. https://www.kite.com/python/examples/5724/lxml-find-all-html-elements-with-a-given-class-name
2. https://lxml.de/lxmlhtml.html#parsing-html-fragments
