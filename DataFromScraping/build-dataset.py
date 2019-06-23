import requests
from bs4 import BeautifulSoup

def spider(name, found_titles, url, found):
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        title    = soup.title.string.lower()

        keywords = soup.select('meta[name="keywords"]')[0]['content'].lower().split(', ')
        description = soup.select('meta[name="description"]')[0]['content'].lower()


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

            f = open('keyword-data.txt', 'a')
            g = open('keyword-data-descr.txt','a')
            f.write(
                title + "\t" + ' '.join(
                    k.replace(' ', '_') for k in cleaned_keywords
                ) + "\n"
            )
            f.close()

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
            if 'https://' + name + '.com' in b and b not in found:

                found.append(b)
                spider(name, found_titles, b, found)

    except:
        pass

def main():
    name      = 'lifehacker'
    start_url = 'https://lifehacker.com/how-to-hack-your-brain-5747213'
    spider(name, [], start_url, [start_url])

if __name__ == "__main__":
    main()
