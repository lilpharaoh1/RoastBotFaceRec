import requests
from bs4 import BeautifulSoup
import random

class Insults(): 
    def __init__(self):
        # Loading in Insult Names
        insult_names_source = requests.get('https://www.insult.wiki/list-of-insults')
        insult_names_html = insult_names_source.text
        insult_names_soup = BeautifulSoup(insult_names_html, features="html.parser")
        insult_names_ol = insult_names_soup.find_all('ol')
        insult_names_raw = []
        for i in insult_names_ol:
            insult_names_raw.append(i.text)
        self.insult_names = insult_names_raw[0].split("\n")

        # Loading Thought Catalogue Insults
        tc_insults_source = requests.get(
            'https://thoughtcatalog.com/lorenzo-jensen-iii/2016/11/sick-burns-the-100-greatest-insults-of-all-time/')
        tc_insults_html = tc_insults_source.text
        tc_insults_soup = BeautifulSoup(tc_insults_html, features="html.parser")
        tc_insults_ol = tc_insults_soup.find_all('p')
        self.long_insults = []
        for i in tc_insults_ol:
            self.long_insults.append(i.text)

        # Insults need to be written...
        self.personal_insults = {
            'aaron' : ["aaron insult"],
            'alex' : ["alex insult"],
            'cian' : ["Cian insult"],
            'david' : ["David insult"],
            'emran' : ["Emran insult"],
            'jp' : ["JP insult"],
            'raf' : ["Raf Insult"],
            'sean' : ["Sean Clarke Insult"],
            'simon' : ["Simon Insult"]
        }

    def known_short_setups(self, name):
        setups = [
            #setups with name
        ]
        chosen_insult = [random.randint(0, len(setups) - 1)]

        return chosen_insult
    
    def unknown_short_setups(self):
        setups = [
            #setups without name
        ]
        chosen_insult = [random.randint(0, len(setups) - 1)]

        return chosen_insult