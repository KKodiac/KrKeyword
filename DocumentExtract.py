"""
    Scrapes keyword topics from Wikipidia or Naver Dictionary
    list of possible urls
    {
        naverdict : "https://dict.naver.com"
        naverterm : "https://terms.naver.com"
        wikipedia_kr : "https://ko.wikipedia.org/wiki/"
    }
"""
from bs4 import BeautifulSoup as bs4
import nltk
from os import path
import requests
from rake_nltk import Rake
from argparse import ArgumentParser
import sys
class Scrape:
    def __init__(self, topic: str, doc_type: str):
        hangul_ranges = (
            range(0xAC00, 0xD7A4),  # Hangul Syllables (AC00–D7A3)
            range(0x1100, 0x1200),  # Hangul Jamo (1100–11FF)
            range(0x3130, 0x3190),  # Hangul Compatibility Jamo (3130-318F)
            range(0xA960, 0xA980),  # Hangul Jamo Extended-A (A960-A97F)
            range(0xD7B0, 0xD800),  # Hangul Jamo Extended-B (D7B0-D7FF)
        )
        is_hangul = lambda c: any(ord(c) in r for r in hangul_ranges)
        if(is_hangul(topic[0])):
            self.topic = topic
        else:
            raise Exception("Topic input must be in Korean. {}" % topic)
        
        if(int(doc_type) >= 1 and int(doc_type) <= 3):
            self.doc_type = int(doc_type)
        else:
            raise Exception("Doc_type input must be an integer within 1 to 3. {} " % doc_type)

        self.legit_url = {
            "naver_dict" : "https://dict.naver.com/",
            "naver_term" : "https://terms.naver.com/",
            "wikipedia_kr" : "https://ko.wikipedia.org/wiki/"
        }

        self.topic_url = ""

        
    # doc_type : 1: naver_dict, 2: naver-term, 3: wikipedia korea
    def setURL(self):        
        naver_query = {
            "dict"  : "search.nhn?query={}&searchType=text&dicType=&subject=",
            "terms" : "search.nhn?dicQuery={}&query={}&target=dic&ie=utf8&query_utf=&isOnlyViewEE="
        }
        if(self.doc_type==1):
            self.topic_url = path.join(self.legit_url['naver_dict'], naver_query["dict"].format(self.topic))
        elif(self.doc_type==2):
            self.topic_url = path.join(self.legit_url["naver_term"], naver_query["terms"].format(self.topic,self.topic))
        else:
            self.topic_url = path.join(self.legit_url["wikipedia_kr"], self.topic)
        print(self.doc_type)
        print(self.topic_url)
        return self.topic_url
    
    def soupifyDoc(self):
        html = requests.get(self.topic_url)
        return bs4(html.text, 'html.parser')

    # Has similar layout for html as Naver Dictionary. However will be working to diverge from it
    def termsNaver(self):
        soup = self.soupifyDoc()
        document = soup.find(class_='search_result_area')
        text_doc = document.text

        return text_doc

    # Returns only the english language result
    def dictNaver(self):
        soup = self.soupifyDoc()
        document = soup.find(class_='search_result_area')
        text_doc = document.text

        return text_doc        

    def wikiKorea(self):
        soup = self.soupifyDoc()
        document = soup.find(id="mw-content-text").find(class_="mw-parser-output")
        text_doc = document.text
        
        return text_doc        

    def getDoc(self):
        if(self.doc_type==1):
            return self.termsNaver()
        elif(self.doc_type==2):
            return self.dictNaver()
        else:
            return self.wikiKorea()

    def rakeResult(self):
        text_doc = self.getDoc()
        r = Rake()
        r.extract_keywords_from_text(text_doc)
        ranked_w_score = r.get_ranked_phrases_with_scores()
        ranked = r.get_ranked_phrases()
        word_degree = r.get_word_degrees()
        word_freq_dist = r.get_word_frequency_distribution()

        return ranked_w_score, ranked, word_degree, word_freq_dist


if __name__=="__main__":
    topic_param = sys.argv[1]
    doc_type_param = sys.argv[2]
    s = Scrape(topic_param, doc_type_param)
    s.setURL()
    print(s.rakeResult())
    
