import random
import string

LETTERS = string.ascii_letters
DIGITS = string.digits
SYMBOLS = string.punctuation


def generateRandomPassword(pass_len = 25, num_symbols = 2, num_digits = 3):
    if num_symbols + num_digits > pass_len:
        raise Exception("Number of symbols plus number of digits is greater than the length of password.")

    password = ""

    for i in range(num_symbols):
        password += random.choice(SYMBOLS)

    for i in range(num_digits):
        password += random.choice(DIGITS)

    for i in range(pass_len - num_digits - num_symbols):
        password += random.choice(LETTERS)

    password = password[:pass_len]

    # Shuffling the password
    password = ''.join(random.sample(password, len(password)))

    return password