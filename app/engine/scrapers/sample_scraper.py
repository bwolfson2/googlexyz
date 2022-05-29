from bs4 import BeautifulSoup 
import requests 


def get_lycos_soup(session,url):
    req = session.get(url)
    soup = BeautifulSoup(req.text,'lxml')
    return soup

def lycos_soup_to_results(soup):
    results = []
    listings = soup.find_all(class_="result-item")
    for content in listings:
        title = content.find(class_='result-title').text
        description = content.find(class_='result-description').text
        url = content.find(class_='result-url').text
        results.append({
            'title':title,
            'description':description,
            'url':url
        })
    return results

def get_lycos_next_button(soup):
    base_url = "https://search17.lycos.com"
    next = soup.find('a', href=True, text='Next')
    if next:
        next_url = next['href']
        return base_url+next_url
    else:
        return None

def lycos_search(query):
    base_url = "https://search17.lycos.com"
    first_url = f'{base_url}/web?q={query}'
    s = requests.Session()
    soup = get_lycos_soup(s,first_url)
    results = lycos_soup_to_results(soup)
    next_url = get_lycos_next_button(soup)
    for i in range(20):
        print(i)
        if not next_url:
            break
        soup = get_lycos_soup(s,next_url)
        results += lycos_soup_to_results(soup)
        next_url = get_lycos_next_button(soup)
    return results

    


