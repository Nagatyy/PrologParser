import os

#   global variables
lexeme = []

#   character classes
lowercase_char, uppercase_char, digit, special = 0, 1, 2, 3
unknown = 99

#   token codes
character = 10
string = 11
numeral = 12
alphanumeric = 13
character_list = 14
variable = 15
small_atom, atom = 16, 17
structure = 18
term, term_list = 19, 20
predicate, predicate_list = 21, 22
query = 23, 24
clause, clause_list = 25, 26

period = 30
colon = 31
dash = 32
question_mark = 33
comma = 34
open_parenthesis, close_parenthesis = 35, 36
quotation = 37

list_of_specials = ["+", "-", "*", "/", "\\", "^", "~", ":", ".", "?", " ", "#", "$", "&"]

def lookup(character):
    pass

def add_char():
    pass

def get_char():
    pass

def getNonBlank():
    pass

def lex():
    pass


def file_handler():
    # a list holding the names of all the txt files in the current directory
    list_of_files = sorted([file for file in os.listdir() if file[-4::] == ".txt"])

    for file in list_of_files:
        pass


########### start of script ###########
file_handler()