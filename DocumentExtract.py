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

class Scrape:
    def __init__(self, str : topic, int : doc_type):
        value = ord(topic)
        if(value >= 4352 and value <= 4607):
            self.topic = topic
        else:
            raise Exception("Topic input must be in Korean. {}" % topic)
        
        if(doc_type > 0 and doc_type <= 3):
            self.doc_type = doc_type
        else:
            raise Exception("Doc_type input must be an integer within 1 to 3. {} " % doc_type)

        self.legit_url = {
            "naver_dict" : "https://dict.naver.com/",
            "naver_term" : "https://terms.naver.com/",
            "wikipedia_kr" : "https://ko.wikipedia.org/wiki/"
        }

        

        
    # doc_type : 1: naver_dict, 2: naver-term, 3: wikipedia korea
    def setURL(self):        
        naver_query = {
            "dict"  : "search.nhn?query={}&searchType=text&dicType=&subject=",
            "terms" : "search.nhn?dicQuery={}}&query={}&target=dic&ie=utf8&query_utf=&isOnlyViewEE="
        }
        if(self.doc_type==1):
            return path.join(self.legit_url['naver_dict'], naver_query["dict"].format(self.topic))
        elif(self.doc_type==2):
            return path.join(self.legit_url["naver_term"], naver_query["terms"].format(self.topic))
        else:
            return path.join(self.legit_url["wikipedia_kr"], self.topic)
        