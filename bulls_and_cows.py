
print("""
projekt_2.py:druhý projekt do Engeto akademie 

Author: Robert Prima
email: x.zidy@seznam.cz
discord: robert.prima
""")
print("""  Bulls 🐂 and Cows 🐄
#                            _.-^-._    .--.
#                         .-'   _   '-. |__|
#                        /     |_|     \|  |
#                       /               \  |
#                      /|     _____     |\ |
#                       |    |==|==|    |  |
#   |---|---|---|---|---|    |--|--|    |  |
#   |---|---|---|---|---|    |==|==|    |  |
#  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"""
) 

import random

def create_line(lenght):
    """
    Returns the underline
    
    """
    return lenght * "_"
line = create_line(47)   


def opening_text():
    print("Hi there!")
    print(line)
    print("""
I've generated a random 4 digit number for you.
Let's play a bulls and cows game.""")
    print(line)


def generate_secret_number():
    """
    Returns a randomly generated secret four-digit number from 0 to 9
    
    """
    number = ''.join(random.sample('0123456789', 4))
    return number


def valid_input(guess, secret_number):
    """
    input must be a four-digit number
    >>> 123 >>> False
    >>> 1234 >>> True

    input must not start with zero
    >>>0123 >>> False
    >>>1234 >>> True

    input cannot contain duplicates
    >>> 1123 >>> False
    >>> 1234 >>> True
    
    """
    if not guess.isdigit() or len(guess) != 4 or guess[0] == '0' or len(set(guess)) < 4:
        return False
    return True


def evaluate(secret_number, guess):
    """
    Returns the response from the input
    
    cow/cows = returns guessed number of numbers
    
    example:
    Randomly generated number: 1234
    input: 5476
    returns : 0 bull, 1 cow
    
    bull/bulls = returns the guessed number of numbers in the correct place
    
    example:
    Randomly generated number: 1234
    input: 5674
    returns : 1 bull, 0 cow
    """
    
    bulls = 0
    cows = 0

    for s, g in zip(secret_number, guess):
        if s == g:
            bulls += 1
        elif g in secret_number:
            cows += 1

    return bulls, cows


def print_evaluation(bulls, cows):
    """
    returns singular or plural bull/cow
    
    """
    print(f"{bulls} {'bull' if bulls == 1 else 'bulls'}, {cows} {'cow' if cows == 1 else 'cows'}")
    print(line)


def play_game():
    opening_text()
    secret_number = generate_secret_number()
    guess_attempts = 0

    
    while True:
        user_guess = input("Enter a 4-digit number:\n>>>")

        if not valid_input(user_guess, secret_number):
            print("Invalid input. Please enter a valid 4-digit number with unique digits.")
            continue

        guess_attempts += 1

        bulls, cows = evaluate(secret_number, user_guess)
        print_evaluation(bulls, cows)

        if bulls == 4:
            print(f"Correct, you've guessed the right number in {guess_attempts} {'guess' if guess_attempts == 1 else 'guesses'}!")
            break

if __name__ == "__main__":
    play_game()