import json

def QuickSort(pages,ranks):#Sorting in descending order
    if len(pages)>1:
        piv=ranks[pages[0]]
        i=1
        j=1
        for j in range(1,len(pages)):
            if ranks[pages[j]]>piv:
                pages[i],pages[j]=pages[j],pages[i]
                i+=1
        pages[i-1],pages[0]=pages[0],pages[i-1]
        QuickSort(pages[1:i],ranks)
        QuickSort(pages[i+1:len(pages)],ranks)


def Look_up(index,keyword):#This function is for given an index, it finds the keyword in the index and returns the list of links
    if keyword in index:
        return index[keyword]
    return []


def Look_up_new(index,ranks,keyword):
    pages=Look_up(index,keyword)
    QuickSort(pages,ranks)
    return pages



def charge_file():
    f = open("/home/pc/Desktop/AI Search Engine/searchengine/ssisearchengine/static/Search_Engine_indexes", 'r')
    index = f.readlines()
    index = index[0].replace("'", "\"")
    iindex = json.loads(index,encoding='ascii')
    f = open("/home/pc/Desktop/AI Search Engine/searchengine/ssisearchengine/static/Search_Engine_rankes", 'r')
    ranks = f.readlines()
    ranks = ranks[0].replace("'", "\"")
    rranks = json.loads(ranks,encoding='ascii')
    return iindex,rranks




