import pandas as pd
import random
import re
from colorama import Fore, Back, Style



wiki_tables = pd.read_html("https://en.wikipedia.org/wiki/List_of_national_capitals")
source_table = wiki_tables[1]
main_table = source_table[['City/Town', 'Country/Territory']].rename(columns = {'City/Town' : 'Capital', 'Country/Territory' : 'Country'})
max_row = max(source_table.index)

#exclude indexes with correct answere
exclude_guessed_countries = []
exclude_list_length = len(exclude_guessed_countries)

tries_counter = 0
right_guess_points = 0
wrong_guess_points = 0
capital_correct_answeres = 0
total_countries = max_row + 1

is_end = False

while not is_end:
    
    if tries_counter == 0:
        start_command = input('Are you ready to start?   ( [Y]es, [N]o ):  ')
    else:
        pass
    start_command = start_command.lower()
    tries_counter += 1
    
    #selection of the pair Country-Capital based on the random index
    auto_index = random.randint(0, max_row)
    
    for length in range(exclude_list_length + 1):
    
        if auto_index in exclude_guessed_countries:
            auto_index = random.randint(0, max_row)
        else:
            exclude_guessed_countries.append(auto_index)
    
    auto_selection = main_table[(main_table.index == auto_index)].iloc[:,:] 
    auto_country = main_table[(main_table.index == auto_index)][['Country']]
    auto_capital = main_table[(main_table.index == auto_index)][['Capital']]
    country = auto_country.iloc[0]['Country']
    capital = auto_capital.iloc[0]['Capital']
    capital = re.sub(r'\([^)]*\)','',capital)
    
    #validation of chars in the capital string
    char_replacement = {
    'é': 'e',
    'ă': 'a',
    '-': ' ',
    'ú': 'u',
    'ș': 's',
    '`': "'",
    'ñ': 'n',
    'ʻ': "'",
    'í': 'i',
    'ã': 'a'
    }
    capital_check_string = ''
    length = len(capital)

    for x in range(length):
        char = capital[x]

        if x == length - 1 and char == " ":
            char = ""
            capital_check_string += char
        elif ord(char) in range(97, 122) or ord(char) in range(65, 90) or ord(char) == 32 or ord(char) == 39:
            capital_check_string += char
        else:
            if char in char_replacement:
                char = char_replacement[char]
                capital_check_string += char
    capital = capital_check_string

#start of the game
    if start_command == 'y':
        print(Fore.WHITE)
        print(Back.BLACK)
        guess_the_capital = input(f"What is the capital of {country}?: ")
        print(Style.RESET_ALL)

        if guess_the_capital.lower() == capital.lower():
            print(Fore.GREEN + f"Bravo! The capital of {country} is {capital}!")
            print(Style.RESET_ALL)
            capital_correct_answeres += 1
            right_guess_points += 100
            want_more = input("Do you want to continue?  y/n: ")
            if want_more == "y":
                # exclude_guessed_countries.append(country)
                continue
            else:
                is_end = True
            
        else:
            wrong_guess_points += 100
            
            print(Fore.RED + 'Wrong!')
            print(Style.RESET_ALL)
            want_more = input("Do you want to continue?  y/n: ")
            if want_more == "y":
                continue
            elif want_more == "n":
                is_end = True
            else:
                print(Fore.RED + "Wrong input! Let's try again...")
                print(Style.RESET_ALL)
    elif start_command == 'n':
        is_end = True
    else:
        print(Fore.RED + "Wrong input! Let's try again...")
        print(Style.RESET_ALL)
        start_command = input('Are you ready to start?   ( [Y]es, [N]o ):  ')
        continue

diff = right_guess_points - wrong_guess_points
countries_left = total_countries - capital_correct_answeres
    
if right_guess_points > wrong_guess_points:
    print(Back.WHITE)
    print(Fore.BLUE + f"Not bad! You successfully guessed {capital_correct_answeres} countries.")
    print(f"Your points for correct answers are: {right_guess_points} and your negative score for wrong answers is: {wrong_guess_points}. \
          In total you've {diff} points")
    print(f"You started with a list of {total_countries} countries from which you've guessed corectly {capital_correct_answeres} of them!")
    print(Style.RESET_ALL)
elif wrong_guess_points > right_guess_points:
    print(Back.WHITE)
    print(Fore.RED + f"Not a good result! You successfully guessed {capital_correct_answeres} countries.")
    print(f"Your points for correct answers are: {right_guess_points} and your negative score for wrong answers is: {wrong_guess_points}. \
          In total you've left with {diff} points")
    print(f"You started with a list of {total_countries} countries from which you've guessed corectly {capital_correct_answeres} of them!")
    print(Style.RESET_ALL)
else:
    print("You don't even started but OKAY... Good Bye")
