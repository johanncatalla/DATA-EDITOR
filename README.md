# DATA-EDITOR-v1.2.0
* Local CRUD for CSV Editor
* CRUD in MySQL database
* Editable cells
* Case Insensitive Search
* Bug fixes

# PROJECT DESCRIPTION:

A Text Editor and CSV Editor using Tkinter utilizing MVC architecture of the Object-Oriented Programming approach. The user can search records and perform CRUD operations locally and on MySQL database on both applications. 

# CSV Editor with Search
![CSV Viewer](https://github.com/johanncatalla/DATA-EDITOR/blob/main/images/csv-1.png)

# Text Editor with Search
![Text Editor](https://github.com/johanncatalla/DATA-EDITOR/blob/main/images/Txt-editor-1.2.0.png)

# PROPERTIES
The search functionality of the Text Editor has the following properties:
* It can be case-sensitive or case-insensitive
* Multiple Words in the search bar are considered separate.
* The keywords are matched to the sentences that contain them, regardless of the keyword's position in the sentence.
* Statements with new lines separating them and having no punctuation are considered one sentence.
* It does not match words with prefixes or suffixes that are digits or alphabets. 
* It matches words with prefixes or suffixes that are special characters or punctuations.
* The search function returns the following to the text editor in the display frame:
    1. The number of sentence matches
    2. the number of matches per keyword in the text
    3. the sentence matches

The record searching of the CSV Editor has the following properties:
* To search records the input format should be: column1=value,column2=value
* The user can search a column only once.
    * In cases that the user inputs the same column multiple times (i.e. column1=value,column1=value), the last value will be searched.
* The user can specify whether they want to display all columns or just the inputted column names in the entry box.
    * In cases that the user wants to display a column but does not want to match a value, they can input their entry without the value (i.e. column1=,column2=)
* The column name is case insensitive but should be the exact string in the header (e.g. Total Household Income).
* The column value is case insensitive but can be not the entire value (e.g. "Ca" matches cat, Camel...).
* The user can search only with the "=" operator. 

