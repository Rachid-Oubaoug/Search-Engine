from django.shortcuts import render
from django.http import HttpResponse
from ssisearchengine.forms import SearchForm
from out import *
from ssisearchengine.models import Search
import BeautifulSoup
import urllib2

#def search(request):
	
	#return render(request, 'search.html')

#def search(request, query):
#	return render(request, 'search.html',{'query': query})

#def search_index(request):
#    return render(request, 'se.html',)


def search(request):
	x = {}
	c = {}
	pgs,i = [],[]
	if request.method == 'POST': # S'il s'agit d'une requete POST
		form = SearchForm(request.POST)
		query = request.POST.get('query')
		index,ranks = charge_file()
		if query != None:
			query = query.split()
			for q in query:
				#print q
				q = q.lower()
				look_up = Look_up_new(index,ranks,q)
				#print look_up
				for l in look_up:
					if l not in pgs:
						pgs.append(l)
						#print pgs 
		#print pgs
			for i in pgs:
				soup = BeautifulSoup.BeautifulSoup(urllib2.urlopen(i))
				x[i] = soup.title.string
				x[i] = x[i].encode(soup.originalEncoding)
				c[i] = soup.head.find('meta', attrs={'name' : 'description'})['content']
        		#c[i] = c[i].encode(soup.originalEncoding)
        	#result = zip(c, x)
	return render(request, 'search.html', locals())