import asyncio
from pyppeteer import launch
from bs4 import BeautifulSoup


def parse_lukol_result(result):
    title = result.find('a',attrs={"class":"gs-title"}).text
    url = result.find('a',attrs={"class":"gs-title"})['href']
    try:
        description = result.find(attrs={"class":"gs-bidi-start-align gs-snippet"}).text.split(" ... ")[1]
    except Exception as e:
        print(e)
        description = result.find(attrs={"class":"gs-bidi-start-align gs-snippet"}).text
    image_url = result.find('img',attrs={"class":"gs-image"})
    try:
        image_url = image_url["src"]
    except Exception as e:
        print(e)
        image_url = None
    return {
        "title":title,
        "url":url,
        "description":description,
        "image_url":image_url
    }

def parse_lukol_html(html):
    soup = BeautifulSoup(html, 'lxml')
    results = soup.findAll(attrs={"class":"gsc-webResult gsc-result"})
    return [parse_lukol_result(result) for result in results]




async def main():
    browser = await launch({'headless': True, "browserWSEndpoint": 'ws://browser:3000' })
    page = await browser.newPage()
    urls = ["https://www.lukol.com/s.php?q=protect+plants#gsc.tab=0&gsc.q=protect%20plants&gsc.page={i+1}" for i in range(10)]
    htmls = []
    for e,i in enumerate(urls):
        print(e)
        await page.goto(i)
        html = await asyncio.create_task(page.evaluate("() =>  document.documentElement.outerHTML"))
        htmls.append(html)
    await browser.close()
    results = sum([parse_lukol_html(html) for html in htmls], [])
    print(f"results are {results}")
    return results


if __name__ == "__main__":
    results = asyncio.run(main())
    print("hi")
    print(results)


# text = soup.findAll(attrs={"class":"gsc-webResult gsc-result"})[0].find('a',attrs={"class":"gs-title"}).text
# url = soup.findAll(attrs={"class":"gsc-webResult gsc-result"})[0].find('a',attrs={"class":"gs-title"})["href"]
# description = soup.findAll(attrs={"class":"gsc-webResult gsc-result"})[0].find(attrs={"class":"gs-bidi-start-align gs-snippet"}).text.split(" ... ")[1]
# image = soup.findAll(attrs={"class":"gsc-webResult gsc-result"})[0].find('img',attrs={"class":"gs-image"})["src"]