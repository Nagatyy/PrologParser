import os
import re
#   global variables
lexeme = []
next_token = -100
number_of_lines = 1
char_index = -1     # to track the character we are currently on
next_char = ""
iFile = None
char_class = -100
num_of_errors = 0
list_of_errors = []

#   character classes
lowercase_char, uppercase_char, digit, special = 0, 1, 2, 3
unknown = 99
new = 98

#   token codes
numeral = 12
variable = 15
small_atom = 16


dash = 32
comma = 34
open_parenthesis, close_parenthesis = 35, 36
quotation = 37
addition_op, subtraction_op, multiplication_op, division_op = 101, 102, 103, 104
backslash, floating_triangle_without_a_bottom = 105, 106    # \ and ^
tilda, colon, period, question_mark = 107, 108, 109, 110
hashtag, dollar_sign, ampersand = 111, 112, 113
space = 114
EOF = -99

# whitespace ??
list_of_specials = ["+", "-", "*", "/", "\\", "^", "~", ":", ".", "?", "#", "$", "&", " "]

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
    return num + 101
def decrypt_hash(hsh):
    return hsh - 101

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
        if char_class == uppercase_char or char_class == lowercase_char or char_class == digit:
            while char_class == uppercase_char or char_class == lowercase_char or char_class == digit:
                add_char()
                get_char()
            next_token = variable
        # else:
        next_token = uppercase_char
    elif char_class == lowercase_char:
        add_char()
        get_char()
        if char_class == uppercase_char or char_class == lowercase_char or char_class == digit:
            while char_class == uppercase_char or char_class == lowercase_char or char_class == digit:
                add_char()
                get_char()
            next_token = small_atom
        # else:
        next_token = lowercase_char
    elif char_class == digit:
        add_char()
        get_char()
        if char_class == digit:
            while char_class == digit:
                add_char()
                get_char()
            next_token = numeral
        # else:
        next_token = digit
    elif char_class == unknown:
        lookup(next_char)
        get_char()
    elif char_class == EOF:
        lexeme.append("EOF")

    #print("Next token is: " + str(next_token) + " Next Lexeme is: " + str(lexeme))

    return next_token

############## End of Lexical Analysis ###############
# syntax analysis

# a special is a character in the list list_of_specials
def special_func():
    #print("Enter <special>")
    global num_of_errors, list_of_errors
    if next_token in [hash_special(x) for x in range(len(list_of_specials))]:
        lex()
    else:
        list_of_errors.append(("Invalid Special Character", number_of_lines, char_index))
        num_of_errors += 1
        lex()

# an alphanumeric or a lowercase char or an uppercase char or a digit
def alphanumeric_func():
    #print("Enter <alphanumeric>")
    global num_of_errors, list_of_errors

    if next_token == lowercase_char or next_token == uppercase_char or next_token == digit:
        lex()
    else:
        num_of_errors += 1
        list_of_errors.append(("Invalid Alphanumeric Character", number_of_lines, char_index))
        lex()

# a character is an alphanumeric or a special
def character_func():
    #print("Enter <character>")
    global num_of_errors, list_of_errors

    if next_token == lowercase_char or next_token == uppercase_char or next_token == digit:  # an alphanumeric
        alphanumeric_func()
    elif next_token in [hash_special(x) for x in range(len(list_of_specials))]:  # or a special
        special_func()
    else:
        num_of_errors += 1
        list_of_errors.append(("Invalid Character", number_of_lines, char_index))
        lex()
# a string is a character followed optionally by a string (rec)
def string_func():
   # print("Enter <string>")

    character_func()        # a character
    if next_token == uppercase_char or next_token == lowercase_char or next_token == digit\
            or next_token in [hash_special(x) for x in range(len(list_of_specials))]:
        lex()
        string_func()

# a numeral is a digit followed by 0 or more numerals
def numeral_func():
   # print("Enter <numeral>")
    global num_of_errors, list_of_errors

    if next_token == digit:     # a digit
        lex()
        if next_token == digit:  # followed optionally by more digits
            numeral_func()
    else:
        num_of_errors += 1
        list_of_errors.append(("Invalid Numeral", number_of_lines, char_index))
        lex()
# a character-list is an alphanumeric followed by 0 or more character-lists
def character_list_func():
   # print("Enter <character-list>")

    alphanumeric_func()     # an alphanumeric
    if next_token == uppercase_char or next_token == lowercase_char or next_token == digit:
        # followed by 0 or more character-lists
        lex()
        character_list_func()

# a variable is an uppercase character followed by 0 or more character-lists
def variable_func():
  #  print("Enter <variable>")
    global num_of_errors, list_of_errors

    if next_token == uppercase_char:        # uppercase character
        lex()
        if next_token == uppercase_char or next_token == lowercase_char or next_token == digit:
            # followed optionally by a character-list
            character_list_func()
    else:
        num_of_errors += 1
        list_of_errors.append(("Invalid Variable. Must begin with uppercase", number_of_lines, char_index))
        lex()

# a small atom is a lowercase character followed by 0 or more character-lists
def small_atom_func():
  #  print("Enter <small-atom>")
    global num_of_errors, list_of_errors

    if next_token == lowercase_char:        # lowercase character
        lex()
        if next_token == lowercase_char or next_token == uppercase_char or next_token == digit:
            # followed optionally by a character-list
            character_list_func()
    else:
        num_of_errors += 1
        list_of_errors.append(("Invalid small-atom. Must begin with lowercase", number_of_lines, char_index))
        lex()

# an atom is small atom or a ' <string> '
def atom_func():
   # print("Enter <atom>")
    global num_of_errors, list_of_errors

    if next_token == lowercase_char:    # a small atom
        small_atom_func()
    elif next_token == quotation:       # or a '
        lex()
        string_func()                   # followed by a <string>
        if next_token == quotation:     # followed by a '
            lex()
        else:
            num_of_errors += 1
            list_of_errors.append(("String missing a ' ", number_of_lines, char_index))
            lex()
    else:
        num_of_errors += 1
        list_of_errors.append(("Invalid atom", number_of_lines, char_index))
        lex()

# a term is a numeral or a variable or a structure or a atom
# but a structure is just an atom followed by ( <term-list> )
def term_func():
   # print("Enter <term>")
    global num_of_errors, list_of_errors
    if next_token == digit:     # a numeral
        numeral_func()
    elif next_token == uppercase_char:      # or a variable
        variable_func()
    elif next_token == lowercase_char or next_token == quotation:  # or a structure
        structure_func()

    else:
        num_of_errors += 1
        list_of_errors.append(("Invalid term", number_of_lines, char_index))
        lex()

# a term-list is a term followed by 0 or more ,<term-list>
def term_list_func():
  #  print("Enter <term-list>")
    global num_of_errors, list_of_errors

    term_func()

    if next_token == comma:
        lex()
        term_list_func()


# a predicate is an atom followed by 0 or more ( <term-list> )
def predicate_func():
  #  print("Enter <predicate>")
    global num_of_errors, list_of_errors

    atom_func()

    if next_token == open_parenthesis:
        lex()
        term_list_func()
        if next_token == close_parenthesis:
            lex()
        else:
            num_of_errors += 1
            list_of_errors.append(("Missing Close Parenthesis in Predicate", number_of_lines, char_index))
            lex()

# a predicate-list consists of a predicate followed by 0 or more , <predicate-lists>
def predicate_list_func():
  #  print("Enter <predicate-list>")
    global num_of_errors, list_of_errors

    predicate_func()            # a predicate
    if next_token == comma:     # followed by 0 or more commas and predicate-lists
        lex()
        predicate_list_func()

# a query consists of a ? then a - then a predicate-list then a .
def query_func():
  #  print("Enter <query>")
    global num_of_errors, list_of_errors

    if next_token == question_mark:     # question mark
        lex()
        if next_token == dash:          # then a dash
            lex()
            predicate_list_func()       # then a predicate list
            if next_token == period:    # then a period
                lex()
            else:
                num_of_errors += 1
                list_of_errors.append(("Missing period in query", number_of_lines, char_index))
                lex()
        else:
            num_of_errors += 1
            list_of_errors.append(("Missing - in query", number_of_lines, char_index))
            lex()
    else:
        num_of_errors += 1
        list_of_errors.append(("Missing ? in query", number_of_lines, char_index))
        lex()

# a structure consists of an atom followed by '(' followed by a term-list followed by ')'
def structure_func():
  #  print("Enter <structure>")
    global num_of_errors, list_of_errors

    atom_func()         # an atom
    if next_token == open_parenthesis:      # followed by an open parenthesis
        lex()
        term_list_func()                    # followed by a term-list
        if next_token == close_parenthesis: # followed by close parenthesis
            lex()
        else:
            num_of_errors += 1
            list_of_errors.append(("Missing Close Parenthesis", number_of_lines, char_index))
            lex()


#   a clause consists of either 1. a predicate followed by a period
#                            or 2. a predicate followed by a :- followed
#                                  by a predicate-list followed by a period
def clause_func():
  #  print("Enter <clause>")
    global num_of_errors, list_of_errors

    predicate_func()                # a predicate
    if next_token == period:        # followed by a period
        lex()
    elif next_token == colon:       # or followed by a :
        lex()
        if next_token == dash:      # and a -
            lex()
            predicate_list_func()   # followed by a predicate-list
            if next_token == period:  # and finally a period
                lex()
            else:
                num_of_errors += 1
                list_of_errors.append(("Missing period at the end of clause", number_of_lines, char_index))
                lex()
        else:
            num_of_errors += 1
            list_of_errors.append(("Missing colon in clause", number_of_lines, char_index))
            lex()

    else:
        num_of_errors += 1
        list_of_errors.append(("Invalid clause", number_of_lines, char_index))
        lex()

#   a clause-list consists of a clause followed by 0 or more clause-lists
def clause_list_func():
   # print("Enter <clause-list>")
    global num_of_errors, list_of_errors

    clause_func()   # a clause
    if next_token == lowercase_char or next_token == quotation:     # followed by 0 or more clause-lists
        clause_list_func()

# a program consists of a query, or a clause-list followed by a query
def program_func():
   # print("Enter <program>")
    global num_of_errors, list_of_errors

    if next_token == question_mark:    # a query
        query_func()
    elif next_token == lowercase_char:  # or a clause-list
        clause_list_func()
        if next_token == question_mark:    # followed by a query
            query_func()
        else:
            num_of_errors += 1
            list_of_errors.append(("Invalid program. Clause list must be followed by query", number_of_lines, char_index))
            lex()


def driver():
    # a list holding the names of all the txt files in the current directory
    list_of_files = sorted([file for file in os.listdir(os.getcwd()) if file[-4::] == ".txt"])

    global iFile, next_token, number_of_lines, char_index, next_char, char_class, num_of_errors, list_of_errors

    if len(list_of_files) == 0:
        print("No txt files found in the directory")

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
                program_func()

            display_errors() if len(list_of_errors) != 0 else print("No errors found...")
            #   resetting for next file
            next_token = -100 if file != list_of_files[-1] else EOF
            number_of_lines = 1
            num_of_errors = 0
            char_index = -1
            list_of_errors = []

        except FileNotFoundError:
            print("Could not open the file: " + file)

    iFile.close()

def display_errors():
    global list_of_errors
    print( str(len(list_of_errors)) +" errors found:")
    for error in list_of_errors:
        print("Error: " + error[0] + " line: " + str(error[1]) + " character: " + str(error[2]))


########### start of script ###########
driver()
