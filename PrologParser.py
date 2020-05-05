import os
import re
#   global variables
lexeme = []
next_token = -100
number_of_lines = 0
char_index = -1     # to track the character we are currently on
next_char = ""
iFile = None
char_class = -100
num_of_errors = 0

#   character classes
lowercase_char, uppercase_char, digit, special = 0, 1, 2, 3
unknown = 99
new = 98

#   token codes
charact = 10
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
addition_op, subtraction_op, multiplication_op, division_op = 101, 102, 103, 104
backslash, floating_triangle_without_a_bottom = 105, 106    # \ and ^
hashtag, dollar_sign, ampersand = 107, 108, 109
EOF = -99

# whitespace ??
list_of_specials = ["+", "-", "*", "/", "\\", "^", "~", ":", ".", "?", " ", "#", "$", "&"]


def lookup(character):

    global next_token, number_of_lines, char_index

    if character == '(':
        add_char()
        next_token = open_parenthesis
    elif character == ')':
        add_char()
        next_token = close_parenthesis
    elif character == '.':
        add_char()
        next_token = period
    elif character == '?':
        add_char()
        next_token = question_mark
    elif character == '-':
        add_char()
        next_token = dash
    elif character == '\'':
        add_char()
        next_token = quotation
    elif character == ',':
        add_char()
        next_token = comma
    elif character == ':':
        add_char()
        next_token = colon
    elif character in list_of_specials:
        add_char()
        next_token = hash_special(list_of_specials.index(character))
    elif character == "\n":
        number_of_lines += 1
        char_index = -1
    elif character != '':
        add_char()
        next_token = unknown
    else:
        add_char()
        next_token = EOF

    return next_token



# used for generating ints from special characters
def hash_special(num):
    return (num + 1) * 100
def decrypt_hash(hash):
    return hash/100 - 1

def add_char():
    lexeme.append(next_char)

def get_char():
    global next_char, char_class, char_index, number_of_lines

    next_char = iFile.read(1)   # to read one character

    #   once we have reached EOF, len(next_char) will be 0
    if next_char != '':
        while re.match("\s", next_char):     # while the next character is a \s (to skip)
            if next_char == "\n":
                number_of_lines += 1
                char_index = -1
            else:
                char_index += 1
            next_char = iFile.read(1)

        if re.match("[A-Z\_]", next_char):  # uppercase (and _ )
            char_class = uppercase_char
        elif re.match("[a-z]", next_char):  # lowercase
            char_class = lowercase_char
        elif re.match("\d", next_char):     # digit
            char_class = digit
        else:
            char_class = unknown

    else:
        char_class = EOF

    char_index += 1


def getNonBlank():
    pass

def lex():
    global next_token
    global lexeme
    lexeme = []
    if char_class == uppercase_char:
        add_char()
        get_char()
        while char_class == uppercase_char or char_class == lowercase_char or char_class == digit:
            add_char()
            get_char()
        next_token = variable
    elif char_class == lowercase_char:
        add_char()
        get_char()
        while char_class == uppercase_char or char_class == lowercase_char or char_class == digit:
            add_char()
            get_char()
        next_token = small_atom
    elif char_class == digit:
        add_char()
        get_char()
        while char_class == digit:
            add_char()
            get_char()
        next_token = numeral
    elif char_class == unknown:
        lookup(next_char)
        get_char()
    elif char_class == EOF:
        lexeme.append("EOF")

    print("Next token is: " + str(next_token) + " Next Lexeme is: " + str(lexeme))

    return next_token


def driver():
    # a list holding the names of all the txt files in the current directory
    list_of_files = sorted([file for file in os.listdir() if file[-4::] == ".txt"])

    global iFile, next_token, number_of_lines, char_index, next_char, char_class, num_of_errors

    for file in list_of_files:
        try:
            iFile = open(file, "a")
            iFile.write("\n")       # error otherwise
            iFile.close()

            iFile = open(file, "r")
            print("Parsing File: " + file)
            get_char()

            while next_token != EOF:
                lex()

            #   resetting for next file
            next_token = -100 if file != list_of_files[-1] else EOF
            number_of_lines = 0
            num_of_errors = 0
            char_index = -1



        except FileNotFoundError:
            print("Could not open the file: " + file)

    iFile.close()



########### start of script ###########
driver()