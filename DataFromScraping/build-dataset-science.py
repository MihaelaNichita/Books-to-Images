import requests
from bs4 import BeautifulSoup
import re
import demjson


def spider(name, found_titles, url, found):
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        keywords = []
        title    = soup.title.string.lower()
        if '|' in title:
            title = title[:title.index('|')]
        # print('title = ',title)

        scripts = soup.find_all('script')
        foundVar = False
        for s in scripts:
            if s.string is None:
                continue
            vars  = s.string.split("var ")  # get each var entry

            for v in vars:
                if 'pageMetricsData' in v:
                    words = v.split('keywords')[1].split('"')[1].split(',')
                    # print(words)
                    for w in words:
                        w = re.sub(r'[^\w\s]', ' ', w).strip()
                        w = re.sub(r'[x20]', '', w).strip()                     
                        w = re.sub(r'[^\s]+[\d]+[^\s]*',r'', w)
                        w = re.sub(r'  ', ' ', w).strip()
                        # w = re.sub(r' ',r'_',w)
                        # print(w)
                        keywords.append(w)
                    foundVar = True
                    break
            if foundVar:
                break

        description1 = soup.select('meta[name="description"]')[0]['content'].lower()
        description2 = soup.select('meta[property="og:description"]')[0]['content'].lower()

        # print('keywords = ',keywords)
        # print('description1 = ',description1)
        # print('description2 = ',description2)

        if name in keywords:
            keywords.remove(name)

        cleaned_keywords = []
        cleaned_keywords_description1 = []
        cleaned_keywords_description2 = []

        for k in keywords:
            if k in title:
                cleaned_keywords.append(k)
            if k in description1:
                cleaned_keywords_description1.append(k)
            if description1 != description2 and k in description2:
                cleaned_keywords_description2.append(k)

        # print('cleaned_keywords = ',cleaned_keywords)
        # print('cleaned_keywords_description1 = ',cleaned_keywords_description1)
        # print('cleaned_keywords_description2 = ',cleaned_keywords_description2)

        if len(cleaned_keywords) > 0 and title not in found_titles:
            found_titles.append(title)

            f = open('keyword-data-vice.txt', 'a')

            f.write(
                title + "\t" + ' '.join(
                    k.replace(' ', '_') for k in cleaned_keywords
                ) + "\n"
            )
            f.close()

        if len(cleaned_keywords_description1) > 0 and title not in found_titles:
            found_titles.append(title)

            g = open('keyword-data-descr-vice.txt','a')
            g.write(
                description1 + "\t" + ' '.join(
                    k.replace(' ', '_') for k in cleaned_keywords_description1
                ) + "\n"
            )
            g.close()

        if len(cleaned_keywords_description2) > 0 and title not in found_titles:
            found_titles.append(title)

            g = open('keyword-data-descr-vice.txt','a')
            g.write(
                description1 + "\t" + ' '.join(
                    k.replace(' ', '_') for k in cleaned_keywords_description2
                ) + "\n"
            )
            g.close()

        # print("soup.select('a[href]')",soup.select('a[href]'))
        for a in soup.select('a[href]'):
            #print('found = ', found)
            b = a['href'].replace('#replies', '')
            # print('b = ',b)
            if 'https://science.' + name + '.com' in b and b not in found:
                #print('b = ',b)
                found.append(b)
                spider(name, found_titles, b, found)

    except:
        pass

def main():
    name      = 'howstuffworks'
    start_url = 'https://animals.howstuffworks.com/animal-facts/chameleons-change-colors.htm'
    spider(name, [], start_url, [start_url])

if __name__ == "__main__":
    main()
