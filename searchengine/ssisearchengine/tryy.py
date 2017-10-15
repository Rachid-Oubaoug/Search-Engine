import urllib2
import os
import BeautifulSoup
#----------------------------web_crawl--------------------------------
def get_page(url):
    try:
        return urllib2.urlopen(url).read()
    except:
        return ""
    
def get_next_target(page):
    start_link = page.find('<a href=')
    if start_link == -1:
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1:end_quote]
    url = "https://www.dmoz.org" + url
    return url, end_quote

def get_all_links(page):
    links = []
    while True:
        url, endpos = get_next_target(page)
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
    words = content.split()
    sw=charge_stop_words()
    for word in words:
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

def crawl_web(seed): # returns index, graph of inlinks
    tocrawl = [seed]
    crawled = []
    graph = {}  # <url>, [list of pages it links to]
    index = {}
    ranks = {}
    os.mknod("Search_Engine_indexes")
    os.mknod("Search_Engine_rankes")
    while os.path.getsize("Search_Engine_indexes") + os.path.getsize("Search_Engine_rankes") <50*1024*1024: #*1024*5:
        print os.path.getsize("Search_Engine_indexes") + os.path.getsize("Search_Engine_rankes")
        fi = open("Search_Engine_indexes", 'w')
        fr = open("Search_Engine_rankes", 'w')
        page = tocrawl.pop(0)
        if page not in crawled:
            content = get_page(page)
            keywords = get_keywords(content)
            add_page_to_index(index, page, keywords)
            outlinks = get_all_links(content)
            graph[page] = outlinks
            union(tocrawl, outlinks)
            crawled.append(page)
            ranks = compute_ranks(graph) 
            sindex = str(index)
            fi.write(sindex)
            sranks = str(ranks)
            fr.write(sranks)
        fi.close()
        fr.close() 
    return index,graph


crawl_web('https://www.dmoz.org')




#crawl_web('https://www.dmoz.org')
#print "Enter What you want to search"
#search_term=raw_input()
#print lookup(index, search_term)
