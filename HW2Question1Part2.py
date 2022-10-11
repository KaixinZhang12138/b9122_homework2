from bs4 import BeautifulSoup
import urllib.request
#from urllib.request import Request

seed_url = "https://www.sec.gov/news/pressreleases"
match_url = "https://www.sec.gov/news/press-release"
word = "charges"
urls = [seed_url]    #queue of urls to crawl
seen = [seed_url]    #stack of urls seen so far
contain_charges = []
text_list = ["seed"]
result_text = []
opened = []          #we keep track of seen urls so that we don't revisit them

maxNumUrl = 20; #set the maximum number of urls to visit
print("Starting with url="+str(urls))
while len(urls) > 0 and len(contain_charges) < maxNumUrl:
    # DEQUEUE A URL FROM urls AND TRY TO OPEN AND READ IT
    try:
        curr_url=urls.pop(0)
        curr_text = text_list.pop(0)
        print("num. of URLs in stack: %d " % len(urls))
        print("Trying to access= "+curr_url)
        req = urllib.request.Request(curr_url,headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urllib.request.urlopen(req).read()
        opened.append(curr_url)

    except Exception as ex:
        print("Unable to access= "+curr_url)
        print(ex)
        continue    #skip code below

    # IF URL OPENS, CHECK WHICH URLS THE PAGE CONTAINS
    # ADD THE URLS FOUND TO THE QUEUE url AND seen
    soup = BeautifulSoup(webpage)  #creates object soup
    # Put child URLs into the stack

    print("***Check whether contain charges ***")

    if word in soup.get_text().lower():
        print("word found in " + curr_url)
        if match_url in curr_url:
            contain_charges.append(curr_url)
            result_text.append(curr_text)



    for tag in soup.find_all('a', href = True): #find tags with links
        childUrl = tag['href'] #extract just the link
        childText = tag.get_text()
        o_childurl = childUrl
        childUrl = urllib.parse.urljoin(seed_url, childUrl)
        print("childurl=" + childUrl)
        print("match_url in childUrl=" + str(match_url in childUrl))
        print("Have we seen this childUrl=" + str(childUrl in seen))
        if match_url in childUrl and childUrl not in seen:
            print("***urls.append and seen.append***")
            urls.append(childUrl)
            text_list.append(childText)
            seen.append(childUrl)


        else:
            print("######")

print("num. of URLs seen = %d, and scanned = %d" % (len(seen), len(opened)))
print("num. of URLs output contained charges = %d" % (len(contain_charges)))

print("List of URLs contain charges:")

for i in range(len(contain_charges)):
    print(contain_charges[i] + '\t ' + result_text[i])
