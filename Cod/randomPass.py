#! python3 
# Gerador de senhas aleatorias, para não ter que criar uma senha

import random as rd
import string as st

def rd_pass():

    """RETURN A RANDOM PASSWORD WITH LETTER, DIGITS AND PUNCTUATION"""
    
    letters = st.ascii_letters
    digits = st.digits
    punctuation = st.punctuation

    # senhas de 8 a 10 caracter's
    len_letter = rd.randint(10,12)
    len_digits = rd.randint(4,6)
    len_simbol = rd.randint(3,5)
    
    passLetters = [rd.choice(letters) for espaço in range(len_letter)]
    passDigits = [rd.choice(digits) for space in range(len_digits)]
    passSimbolos = [rd.choice(punctuation) for space in range(len_simbol)]

    passwd = passSimbolos + passDigits + passLetters
    rd.shuffle(passwd)
    password = ''.join(passwd)

    return password