from bs4 import BeautifulSoup
import urllib.request


seed_url = "https://www.federalreserve.gov/newsevents/pressreleases.htm"
match_url = "https://www.federalreserve.gov/newsevents/pressreleases"
word = "covid"
urls = [seed_url]    #queue of urls to crawl
seen = [seed_url]    #stack of urls seen so far
contain_covid = []
opened = []          #we keep track of seen urls so that we don't revisit them

maxNumUrl = 10; #set the maximum number of urls we want to output
print("Starting with url="+str(urls))
while len(urls) > 0 and len(contain_covid) < maxNumUrl:
    # DEQUEUE A URL FROM urls AND TRY TO OPEN AND READ IT
    try:
        curr_url=urls.pop(0)
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

    if word in soup.get_text().lower():
        print("word found in " + curr_url)
        contain_covid.append(curr_url)


    for tag in soup.find_all('a', href = True): #find tags with links
        childUrl = tag['href'] #extract just the link
        o_childurl = childUrl
        childUrl = urllib.parse.urljoin(seed_url, childUrl)

        if match_url in childUrl and childUrl not in seen:
            urls.append(childUrl)
            seen.append(childUrl)


print("num. of URLs seen = %d, and scanned = %d" % (len(seen), len(opened)))
print("num. of URLs output contained covid = %d" % (len(contain_covid)))
print("List of URLs contain covid:")
for contain_covid_url in contain_covid:
    print(contain_covid_url);