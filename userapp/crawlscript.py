# Libraries
from urllib.parse import urlencode, urlunparse
from htmldate import find_date
from bs4 import BeautifulSoup
import nltk, requests
import validators

#Crawler
class Crawler:

    def remove_tags(self,html):

        # parse html content
        soup = BeautifulSoup(html, "html.parser")
        for data in soup(['style', 'script']):
            # Remove tags
            data.decompose()

        # return data by retrieving the tag content
        return ' '.join(soup.stripped_strings)

    # Group text in tokens of 2000
    def token_batches(self, article):
        final_text = []
        final_articles = []
        all_articles = []

        text = ""
        number = 0
        avoid_words = ["signup", "cookies", "login", "password", "username"]
        tokens = nltk.tokenize.sent_tokenize(article)
        if number < len(tokens):

            for number in range(number, len(tokens)):
                sentence = tokens[number]
                sentence_splits = sentence.lower().split(" ")
                any_word = self.similar_element(
                    sentence_splits, avoid_words)
                if any_word != True:
                    if len(text) < 2000:
                        text += "".join(sentence)

                        final_text.append(text)

                        for index in range(len(final_text)):
                            try:
                                if final_text[index] in final_text[index + 1]:
                                    final_text[index] = final_text[index + 1]
                            except Exception as error:
                                pass

                    else:
                        number += number
                        text = ""

        # Remove duplicates
        for index, item in enumerate(final_text):
            if item not in final_articles[:index]:
                final_articles.append(item)

        # Remove persistent duplicates
        for index in range(len(final_articles)):
            items_ = final_articles[-index]
            items = final_articles[-index-1]
            if items not in items_:
                if items not in all_articles:
                    all_articles.append(items)

        all_articles.reverse()
        return all_articles

    # Get text
    def scraper(self,url):
        session = requests.Session()
        request = session.get(url, headers={"User-Agent": "python-requests/2.31.0"})

        soup = BeautifulSoup(request.content,features="lxml")
        text = soup.find('body').text
        request.close()

        return text

    #any similar elemnts in lists
    def similar_element(self,list_a, list_b):
        if (set(list_a) & set(list_b)):
            return True
        else:
            return False

    def search(self, query):
        all_links = []

        for search in query:
            url = f'https://en.wikipedia.org/wiki/{search}'
            all_links.append(url)

        
        return all_links



    # All information needed from a link
    def link_info(self,url):
        # url validator
        validurl = validators.url(url)
        if validurl == True:
            try:
                
                session = requests.Session()
                request = session.get(url, headers={"User-Agent": "python-requests/2.31.0"})

                soup = BeautifulSoup(request.content, features="lxml")
                request.close()

                date = find_date(url)
                source = url.split(".")[-2]
                title = soup.title.text
                if title == '':
                    title = "None"

                title_split = title.lower().split(" ")
                avoid_words = ["sign", "sign-in", "login", "account"]
                any_element = self.similar_element(title_split, avoid_words)

                if any_element != True:
                    text = self.scraper(url)
                    batches = '\n\n'.join(self.token_batches(text))

                    if len(batches) > 4:
                        dictionary = {"title": title,
                                    "source": source,
                                    "text": self.remove_tags(batches),
                                    "tokens": len(batches),
                                    "date": date,
                                    "url": url}

                        return dictionary
            except:
                pass