from html.parser import HTMLParser
import re
import requests

with open('sample.html', mode='r') as f:
    html = ''

print('File: sample.html')
print('Date: 2018-11-26')

# Variable to check how many H1 inside section or article
h1AppearancesSectionorArticle = 0
# Variables to check how many H1 OUTSIDE Section or article.
h1AppearancesOther = 0
# count sitemap
countsitemap = 0
countjss = 0
countcss = 0


class Stack:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def incluir(self, item):
        self.items.append(item)

    def extraer(self):
        return self.items.pop()

    def inspeccionar(self):
        return self.items[len(self.items) - 1]

    def inspeccionarplus(self, n):
        return self.items[len(self.items) - n]

    def tamano(self):
        return len(self.items)


class Parser(HTMLParser):

    def handle_starttag(self, tag, attrs):
        global h1AppearancesOther
        global h1AppearancesSectionorArticle
        global countsitemap
        global countcss
        global countjss
        error2 = ""
        error6 = ""
        error9 = ""
        error7 = ""
        error8 = ""
        # H1 restriction
        if (pila.isEmpty() == False):
            if tag == "h1" and pila.inspeccionar() != "article" and pila.inspeccionar() != "section":
                h1AppearancesOther += 1
                if h1AppearancesOther > 1:
                    error2 = " 2"
            elif tag == "h1" and pila.inspeccionar() == "article" or pila.inspeccionar() == "section":
                h1AppearancesSectionorArticle += 1
                if h1AppearancesSectionorArticle > 1:
                    error2 = " 2"
            # countsitemaps xml
            if attrs != []:
                if "href" in attrs[0] or "src" in attrs[0] or "link" in attrs[0]:
                    if "sitemap.xml" in attrs[0]:
                        countsitemap += 1
            # blank for a href outside the websiet
            if tag == "a":
                haveblank = False
                try:
                    for i in range(len(attrs)):
                        if ("https://www.semic.es" in attrs[0]) == False and ("_blank" in attrs[i]) == True:
                            haveblank = True
                    if (haveblank == False):
                        error6 = " 6"
                except IndexError:
                    error6 = " 6"
                if "href" in attrs[0][0]:
                    try:
                        if requests.get(attrs[0][1]).status_code == 404:
                            error9 = " 9"
                    except Exception:
                        pass
            if tag == "script":
                if attrs != []:
                    if "text/javascript" in attrs[0]:
                        countjss += 1
                        if countjss > 5:
                            error7 = " 7"
            if tag == "link":
                if "stylesheet" in attrs[0]:
                    countcss += 1
                    if countcss > 5:
                        error8 = " 8"
        if error2 == " 2" or error6 == " 6" or error9 == " 9" or error7 == " 7" or error8 == " 8":
            print("Line " + str(self.getpos()[0]) + ":" + str(error2) + str(error6) + str(error9) + str(error7) + str(
                error8))
        pila.incluir(tag)

    def handle_endtag(self, tag):
        global errorHTML
        global h1AppearancesSectionorArticle
        if pila.isEmpty() == False:
            # HTML errors
            if pila.inspeccionar() != tag:
                print("Line " + str(self.getpos()[0]) + ":" + str(" 1"))
            # H1 errors
            if tag == "article" or tag == "section":
                h1AppearancesSectionorArticle = 0
            pila.extraer()
        else:
            print("Line " + str(self.getpos()[0]) + ":" + str(" 1"))

    def handle_data(self, data):
        global countsitemap
        error3 = ""
        error5 = ""
        if "GTM" in data:
            if ('GTM-XXXXXX' in data):
                error3 = " 3"
            if re.match(r'GTM-[0-9A-Za-z]{6}', data) == False:
                error3 = "3"
        if "UA-" in data:
            if re.match(r'UA-[0-9]-1{7}', data) == False:
                error3 = "3"
        if "TODO:" in data:
            error5 = " 5"
        if error3 == " 3" or error5 == " 5":
            print("Line " + str(self.getpos()[0]) + ":" + str(error3) + str(error5))

    def handle_comment(self, data):
        if "TODO:" in data:
            print("Line " + str(self.getpos()[0]) + ":" + str(" 5") + str(data[6:]))


pila = Stack()
parser = Parser()
parser.feed(html)
parser.close()
if (countsitemap < 1):
    print("Line 0" + str(": 6"))
