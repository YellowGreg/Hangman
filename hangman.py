import requests


# get a word from the API and return it
def get_word():
    # API - Application Programming Interface
    url = "https://random-word-api.herokuapp.com/word"
    result = requests.get(url)
    # JSON - JavaScript Object Notation
    return result.json()[0].upper()


# to display the current hint, we need three pieces of
# information: actual word, guessed letters, placeholder
def get_display(word, guessed_letters, placeholder):
    result = ""
    for letter in word:
        if letter in guessed_letters:
            result += letter
        else:
            result += placeholder
    return result


# get a guess from the user; keep asking
# until a valid guess is made
def get_guess(guessed_letters):
    while True:
        guess = input("Guess a letter: ").upper()
        if len(guess) != 1 or not guess.isalpha():
            print("A guess must be exactly one letter.")
        elif guess in guessed_letters:
            print(guess + " was already guessed.")
        else:
            return guess


# take a turn in the game
def take_turn(word, guessed_letters):
    guess = get_guess(guessed_letters)
    guessed_letters.append(guess)
    if guess in word:
        print("Yes, good guess!")
    else:
        print("No, sorry.")


# check if the game is won by making sure that
# all letters in word are in guessed_letters
def game_won(word, guessed_letters):
    for letter in word:
        if letter not in guessed_letters:
            return False
    return True


def play_game():
    word = get_word()
    if len(word) <= 8:
        guesses_remaining = len(word) * 2
    elif len(word) <= 10:
        guesses_remaining = len(word) + 6
    else:
        guesses_remaining = len(word) + 2
    guessed_letters = []
    while True:
        print("You have " + str(guesses_remaining) + " guesses remaining.")
        print("Guessed letters: " + ", ".join(sorted(guessed_letters)))
        print(get_display(word, guessed_letters, "-"))
        take_turn(word, guessed_letters)
        guesses_remaining -= 1
        print()
        if game_won(word, guessed_letters):
            end_game(word, True)
            return
        elif guesses_remaining == 0:
            end_game(word, False)
            return


def end_game(word, won):
    if won:
        desc = "won!"
    else:
        desc = "lost."
    print("You " + desc)
    print("The word was " + word + ".")
    get_definition(word)


def play_games():
    again = "Y"
    while again == "Y":
        play_game()
        print()
        again = input("Play again? (Y/N)").upper()
        print()
    print("Thanks for playing!")


def get_definition(word):
    key = "3c2907f0-f79c-45a3-9872-4a17da2fa433"
    url = "https://dictionaryapi.com/api/v3/references/collegiate/json/" + word + "?key=" + key
    result = requests.get(url).json()
    try:
        print("Word: " + result[0]["meta"]["id"])
        print("Definition: " + result[0]["shortdef"][0])
    except:
        print(
            "Something went wrong in looking up the word. Maybe it's not a real word?"
        )


play_games()
