import requests
import urllib
import time
from bs4 import BeautifulSoup

def remove_first_link_if_in_parens(p,links):
    if len(links) == 0:
        return links
    #print (str(p))
    open_index = p.find("(")
    closed_index = p.find(")")
    if open_index == -1 or closed_index == -1:
        return links

    link_index = p.find("href")
    if open_index < link_index and link_index < closed_index:
        return links[1:]
    return links

def find_nth_link(url,n):
    response = requests.get(url)
    print(response.url)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    content_div = soup.find("div",{"id":"mw-content-text"})
    content_div_new = content_div.find("div",{"class":"mw-parser-output"})
    current_link = None
    #print (content_div_new)

    links_seen = 0
    elem_list = content_div_new.find_all("p",recursive = False)
    for elem in elem_list:
        elem_links = elem.find_all("a", recursive = False)
        elem_links = remove_first_link_if_in_parens(str(elem), elem_links)
        num_links = len(elem_links)
        if num_links >= n-links_seen:
            current_link = elem_links[n-1-links_seen].get("href")
            break
        else:
            links_seen += num_links

    if not current_link:
        return

    second_link = urllib.parse.urljoin('https://en.wikipedia.org/',current_link)
    return second_link

MAX_LINKS = 100

visited_links = []

#current_page = "https://en.wikipedia.org/wiki/Attention"
#current_page = "https://en.wikipedia.org/wiki/Phallodrilus"
#current_page = requests.get("https://en.wikipedia.org/wiki/Philosophy").url
current_page = requests.get("https://en.wikipedia.org/wiki/Special:Random").url

while len(visited_links) <= MAX_LINKS and not (current_page in visited_links):
    visited_links.append(current_page)
    current_page = find_nth_link(current_page,2)
    if current_page is None:
        break
print("Looped on: " + current_page)