# import required modules
from bs4 import BeautifulSoup
import requests
import urllib.parse

def scrape(search):
    """
    input:
    search:string | topic_to_search
    """
    #the base url of wikipedia
    base_URl="https://en.wikipedia.org/wiki/"

    url=base_URl+urllib.parse.quote(search)
    page = requests.get(url)

    # scrape webpage
    soup = BeautifulSoup(page.content, 'html.parser')

    #scrape the title
    title_element = soup.find(class_='firstHeading mw-first-heading')
    title = title_element.get_text()

    #scrape the remaining data(text)
    content_div = soup.find('div', class_='mw-content-ltr mw-parser-output')
    content_text= content_div.getText()
    
    return(title,content_text)