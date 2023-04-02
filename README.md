# DATA-PROJECT-v1.0.1

Editable cells, case-insensitive search, and CRUD functions for CSV Editor

# CSV Editor with Search
![CSV Viewer](https://github.com/johanncatalla/DATA-PROJECT/blob/main/images/csv_editor.png)

# Text Editor with Search
![Text Editor](https://github.com/johanncatalla/DATA-PROJECT-v1.0/blob/main/images/text_editor_new.png)

# PROJECT DESCRIPTION:

A Text Editor and CSV Viewer using Tkinter utilizing MVC architecture of the Object-Oriented Programming approach. The user can search records and perform CRUD operations on both applications. 

# IMPROVEMENTS

Editable cells

Case Insensitive Search

Bug fixes

# PROPERTIES
The search functionality has the following properties:
1. It can be case-sensitive or case-insensitive
2. Multiple Words in the search bar are considered separate.
3. The keywords are matched to the sentences that contain them, regardless of the keyword's position in the sentence.
4. Statements with new lines separating them and having no punctuation are considered one sentence.
5. It does not match words with prefixes or suffixes that are digits or alphabets. 
6. It matches words with prefixes or suffixes that are special characters or punctuations.
7. The search function returns the following to the text editor in the display frame:
  1. the number of sentence matches
  2. the number of matches per keyword in the text
  3. the sentence matches

