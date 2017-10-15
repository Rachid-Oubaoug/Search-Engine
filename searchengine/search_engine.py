import urllib2
import os
import BeautifulSoup
import json
import re
import datetime

def get_page(url):
    try:
        return urllib2.urlopen(url).read()
    except:
        return ""
    
def get_next_target(page,racine_page):
    start_link = page.find('<a href=')
    if start_link == -1:
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1:end_quote]
    url = racine_page + url
    return url, end_quote

def get_all_links(page,racine_page):
    links = []
    while True:
        url, endpos = get_next_target(page,racine_page)
        if url:
            links.append(url)
            page = page[endpos:]
        else:
            break
    return links

def get_keywords(content):
    soup = BeautifulSoup.BeautifulSoup(content)
    try:
        x = soup.head.find('meta', attrs={'name' : 'keywords'})['content']
        x = x.encode(soup.originalEncoding)
        x = re.split(",| ",x)
        return x
    except:
        return ""
    
def union(a, b):
    for e in b:
        if e not in a:
            a.append(e)

def charge_stop_words():
    sw=[]
    f = open('static/stopwords.txt', 'r')
    x = f.readlines()
    for l in x:
        sw.append(l)
    return sw

def add_page_to_index(index, url, content):
    sw=charge_stop_words()
    for word in content:
    	word = word.lower()
        if word not in sw:
            add_to_index(index, word, url)

def add_to_index(index, keyword, url):
    if keyword in index:
        if url not in index[keyword]:
            index[keyword].append(url)
    else:
        index[keyword] = [url]

def compute_ranks(graph):#Computing ranks for a given graph -> for all the links in it
    d=0.8
    numloops=10
    ranks={}
    npages=len(graph)
    for page in graph:
        ranks[page]=1.0/npages
    for i in range(0,numloops):
        newranks={}
        for page in graph:
            newrank=(1-d)/npages
            for node in graph:
                if page in graph[node]:
                    newrank=newrank+d*ranks[node]/len(graph[node])
            newranks[page]=newrank
        ranks=newranks
    return ranks

def crawl_web(): # returns index, graph of inlinks
    seed_pages = ['https://www.dmoz.org','https://botw.org','http://www.pegasusdirectory.com','http://attracta.org','http://shveaa.com']
    crawled = []
    graph = {}  # <url>, [list of pages it links to]
    index = {}
    ranks = {}
    for j in xrange(0,5):
		tocrawl = [seed_pages[j]]
		for i in xrange(1,20):
			page = tocrawl.pop(0)
			print page
			if page not in crawled:
				content = get_page(page)
				keywords = get_keywords(content)
				add_page_to_index(index, page, keywords)
				outlinks = get_all_links(content,seed_pages[j])
				graph[page] = outlinks
				union(tocrawl, outlinks)
				crawled.append(page)
	        	ranks = compute_ranks(graph)
	        	d = datetime.datetime.utcnow()
    fi = open("static/Search_Engine_indexes", 'a')
    fr = open("static/Search_Engine_rankes", 'a')
    del index[""]
    json.dump(index, fi)
    json.dump(ranks, fr)
    fi.close()
    fr.close() 
    print os.path.getsize("static/Search_Engine_indexes") + os.path.getsize("static/Search_Engine_rankes")
    return index,graph

crawl_web()
