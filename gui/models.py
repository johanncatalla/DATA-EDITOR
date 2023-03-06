import os
import re

class Model():
    def __init__(self):
        self.text = ''

    def open(self, filename):
        file = open(filename, 'r') 
        self.text = file.read()
        file.close()

    def save(self, filename):
        file = open(filename, 'w')
        file.write(self.text)
        file.close()

    def delete(self, filename):
        os.remove(filename)
        self.text = ''

    def export_searches(self, text, filename):
        file = open(filename, 'w')
        file.write(text)
        file.close()

    def str_to_list(self, text):
        return text.split(' ')

    def entry_list(self, text_entry: str):
        clean_entry = re.sub(' +', ' ', text_entry)

        lst_entry = self.str_to_list(clean_entry)
        return lst_entry
    
    def search_sentence(self, text_input: str, text_entry: str, option_value: str):
    
        clean_editor = re.sub('[ \n]+', ' ', text_input)

        lst_entry = self.entry_list(text_entry)
        
        keywords = r'\b[^.?!\w]*(?:' + '|'.join(lst_entry) + r')(?=[\s@*&^%$#.,;:\/\'-\?!]|$)'

        if option_value == "Ignore Case":
                pattern = re.compile(r'\b[^.?!]*\b{0}\b[^.?!]*[ .?!]'.format(keywords), re.IGNORECASE)
        else:
                pattern = re.compile(r'\b[^.?!]*\b{0}\b[^.?!]*[ .?!]'.format(keywords))

        lst_searches = pattern.findall(clean_editor)

        return lst_searches
    