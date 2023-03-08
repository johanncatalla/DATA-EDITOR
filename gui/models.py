import os
import re

class Model():
    def __init__(self):
        """where the text in the editor will be stored"""
        self.text = ''

    def open(self, filename: str):
        """opens the file in read mode

        Args:
            filename (str): file path string of the text that will be opened
        """
        file = open(filename, 'r') 
        self.text = file.read()
        file.close()

    def save(self, filename: str):
        """opens the file in write mode for saving

        Args:
            filename (_type_): file path string of the text that will be opened
        """
        file = open(filename, 'w')
        file.write(self.text)
        file.close()

    def delete(self, filename: str):
        """deletes the file from directory

        Args:
            filename (str): file path string of the text that will be opened
        """
        os.remove(filename)
        self.text = ''

    def export_searches(self, text: str, filename: str):
        """exports the search results

        Args:
            text (str): text in the display widget
            filename (str): file path string of the text that will be opened for writing
        """
        file = open(filename, 'w')
        file.write(text)
        file.close()

    def str_to_list(self, text: str) -> list:
        """Convert text input to list split on space"""
        return text.split(' ')

    def entry_list(self, text_entry: str) -> list:
        """cleans the text input and converts it to list

        Args:
            text_entry (str): string in the search entry

        Returns:
            list: list of words in the search entry
        """
        clean_entry = re.sub(' +', ' ', text_entry)
        lst_entry = self.str_to_list(clean_entry)
        return lst_entry
    
    def search_sentence(self, text_input: str, text_entry: str, option_value: str) -> list:
        """processes the entry text and editor text to search sentences using the keywords

        Args:
            text_input (str): string in the text editor
            text_entry (str): string in the search entry
            option_value (str): value in the option menu wheter ignore case or case sensitive

        Returns:
            list: list of words in the search entry
        """   
        clean_editor = re.sub('[ \n]+', ' ', text_input) # clean text editor content to remove extra lines/spaces
        lst_entry = self.entry_list(text_entry) # creates the list keywords
        
        # Adding "|" between each keyword on list to search more than one keyword
        # Regex that allows special char/punctuations before and after keyword but disallows alphanum chars 
        keywords = r'\b[^.?!\w]*(?:' + '|'.join(lst_entry) + r')(?=[\s@*&^%$#.,;:\/\'-\?!]|$)'

        # change behavior of the search based on ignore case/case sensitive option
        if option_value == "Ignore Case":
                # compile keyword pattern with sentence pattern to create main regex pattern 
                pattern = re.compile(r'\b[^.?!]*\b{0}\b[^.?!]*[ .?!]'.format(keywords), re.IGNORECASE) # Regex that formats the keywords to be in a sentence/standalone
        else:
                pattern = re.compile(r'\b[^.?!]*\b{0}\b[^.?!]*[ .?!]'.format(keywords))

        # Execute findall with the main regex pattern
        lst_searches = pattern.findall(clean_editor)

        return lst_searches
    