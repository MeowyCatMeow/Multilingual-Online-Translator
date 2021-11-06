"""
Multilingual Online Translator
https://hyperskill.org/projects/99
https://imgur.com/a/FtrTyhd
"""
import requests
from bs4 import BeautifulSoup
import sys
import argparse


class OnlineTranslator:
    def __init__(self):
        self.languages = {
            '1': 'arabic',
            '2': 'german',
            '3': 'english',
            '4': 'spanish',
            '5': 'french',
            '6': 'hebrew',
            '7': 'japanese',
            '8': 'dutch',
            '9': 'polish',
            '10': 'portuguese',
            '11': 'romanian',
            '12': 'russian',
            '13': 'turkish'
        }
        self.log = []
        self.language_1 = ''
        self.language_2 = ''
        self.word = ''
        self.temp_lang2 = ''
        self.s = requests.Session()
        self.example_num = 1

    def ask_languages(self):
        print("Hello, you're welcome to the translator. Translator supports:")
        for k, v in self.languages.items():
            print(f'{k}. {v.capitalize()}')
        self.language_1 = input('Type the number of your language:\n')
        self.language_2 = input(
            "Type the number of a language you want to translate to or '0' or all to translate to all languages:\n")
        self.temp_lang2 = self.language_2
        self.word = input('Type the word you want to translate:\n')

    def print(self, *strings):
        for string in strings:
            self.log.append(string + '\n')
            print(string)

    def input(self, message=''):
        if message != '':
            self.print(message)
        term = input()
        self.log.append(term + '\n')
        return term

    def translate(self, l2):
        if self.language_1 == l2:
            return
        url = f'https://context.reverso.net/translation/{self.language_1}-{l2}/{self.word}'
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = self.s.get(url, headers=headers)
        soup = BeautifulSoup(r.content, 'html.parser')
        words = soup.find('div', {'id': 'translations-content'})
        words_list = [w.text.strip() for w in words if len(w.text.strip()) > 0]
        self.print(f'{l2.capitalize()} Translations:')
        for w in range(self.example_num):
            self.print(words_list[w])
        self.print(f'\n{l2.capitalize()} Examples:')
        lan1_examples = soup.find('section', {'id': 'examples-content'}).find_all('div', {'class': 'src'})
        lan2_examples = soup.find('section', {'id': 'examples-content'}).find_all('div', {'class': 'trg'})
        lan1_list = [e.text.strip() for e in lan1_examples if len(e.text.strip()) > 0]
        lan2_list = [e.text.strip() for e in lan2_examples if len(e.text.strip()) > 0]
        for x in range(self.example_num):
            self.print(lan1_list[x])
            self.print(lan2_list[x] + '\n')

    def find_key(self, value):
        for _k in self.languages.keys():
            if value == self.languages[_k]:
                return _k

    def args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('language1')
        parser.add_argument('language2')
        parser.add_argument('word')
        args = parser.parse_args()
        self.temp_lang2 = args.language2
        self.language_1 = self.find_key(args.language1)
        self.language_2 = self.find_key(args.language2) if args.language2 != 'all' and args.language2 != '0' else '0'
        self.word = args.word

    def operate(self):
        try:
            self.language_1 = self.languages[self.language_1]
            if self.language_2 != 'all' and self.language_2 != '0':
                self.language_2 = self.languages[self.language_2]
                self.translate(self.language_2)
            else:
                for x in range(len(self.languages)):
                    self.translate(self.languages[f'{x + 1}'])
            with open(f'{self.word}.txt', 'w', encoding='utf-8') as file:
                for x in self.log:
                    file.write(x)
        except requests.exceptions.ConnectionError:
            print('Something wrong with your internet connection')
        except KeyError:
            print(f"Sorry, the program doesn't support {self.temp_lang2}")
        except TypeError:
            print(f'Sorry, unable to find {self.word}')

    def start(self):
        if len(sys.argv) == 4:
            self.args()
            self.operate()
        else:
            self.ask_languages()
            self.operate()


translator = OnlineTranslator()
translator.start()
