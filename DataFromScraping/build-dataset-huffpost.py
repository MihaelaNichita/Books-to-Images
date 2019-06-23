import requests
from bs4 import BeautifulSoup

def spider(name, found_titles, url, found):
    try:
        from urllib.request import Request, urlopen 
        headers = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        req = Request(url, headers=headers)
        webpage = urlopen(req).read()
        soup = BeautifulSoup(webpage, 'html.parser')

        # result = requests.get(url, headers=headers)
        # soup = BeautifulSoup(result.content.decode(), "lxml")


        title    = soup.title.string.lower()
        # print(title)
        if '|' in title:
            title = title[:title.index('|')]

        keywords = soup.select('meta[name="keywords"]')
        if keywords != []:
            keywords = keywords[0]['content'].lower().split(' ')

        description = soup.select('meta[name="description"]')
        if description != []:
            description = description[0]['content'].lower()


        # print('title = ',title)
        # print('keywords = ',keywords)
        # print('description = ',description)

        if name in keywords:
            keywords.remove(name)

        cleaned_keywords = []
        cleaned_keywords_description = []

        for k in keywords:
            if k in title:
                cleaned_keywords.append(k)
            if k in description:
                cleaned_keywords_description.append(k)

        # print('cleaned_keywords = ',cleaned_keywords)
        # print('cleaned_keywords_description = ',cleaned_keywords_description)

        if len(cleaned_keywords) > 0 and title not in found_titles:
            found_titles.append(title)
            # print(title)
            # print(description)
            # print(cleaned_keywords)

            f = open('keyword-data-huffpost.txt', 'a')
            f.write(
                title + "\t" + ' '.join(
                    k.replace(' ', '_') for k in cleaned_keywords
                ) + "\n"
            )
            f.close()
        if len(cleaned_keywords_description) > 0 and title not in found_titles:
            g = open('keyword-data-descr-huffpost.txt','a')
            g.write(
                description + "\t" + ' '.join(
                    k.replace(' ', '_') for k in cleaned_keywords_description
                ) + "\n"
            )
            g.close()

        #print("soup.select('a[href]')",soup.select('a[href]'))
        for a in soup.select('a[href]'):
            #print('found = ', found)
            b = a['href'].replace('#replies', '')
            # print('b = ',b)

            if 'https://www.' + name + '.com' in b and b not in found:
                if b.index('https') != 0:
                    continue
                # print('b = ',b)
                found.append(b)
                spider(name, found_titles, b, found)

    except:
        pass

def main():
    name      = 'huffpost'
    start_url = 'https://www.huffpost.com/entry/airbnb-wi-fi-dangers_l_5ceebbcfe4b0f078035e3ed4'
    spider(name, [], start_url, [start_url])

if __name__ == "__main__":
    main()
