# Simon Dutton
# due April 7, 2023
# PokeAPI Program
# Gets specific info from the PokeAPI in a dictionary.
# Extra Credit: Making a full program that plays around with the PokeAPI

# Note: 
# pokeapi.co/api/v2/pokemon/2 -- can give us pokemon with id2
# pokeapi.co/api/v2/pokemon/pikachu can give us pikachu

import requests as r
from ascii_magic import AsciiArt
from random import randint, choice
import sys

from colorama import init
init(strip=not sys.stdout.isatty()) # strip colors if stdout is redirected
from termcolor import cprint 
from pyfiglet import figlet_format
import os 

class Pokemon ():
    """
        A Pokemon is a pokemon from an entry in the PokeAPI.
        This class contains methods to get/print information about the pokemon,
        and a method to print the image ascii for the pokemon.
    """
    def __init__(self, my_pokemon):
        """
            __init__(my_pokemon:str|int)
            A Pokemon is initialized by a parameter "my_pokemon" which is either
            a string (name) or an int (ID) of the pokemon we are referencing 
            from the PokeAPI. It also initializes the values we want from the info,
            as well as a dictionary that holds the info we get about the pokemon.
        """
        self.my_pokemon = my_pokemon # user inputs the id of the pokemon
        self.name, self.sprite_front_shiny_url = ("",)*2
        self.abilities = []
        self.base_experience, self.hp_base_stat, self.attack_base_stat, self.defense_base_stat = (0,) * 4
        self.pokemon_info = {}

    def get_pokemon_name(self):
        """
            get_pokemon_name()
            Gets the name of the Pokemon
        """
        res = r.get(f'https://pokeapi.co/api/v2/pokemon/{self.my_pokemon}')
        if res.ok:
            data = res.json()
            self.name = data['name'].title()
        # does not need to return anything because it just sets the variable to 
        # the name of the pokemon according to the file

    def get_pokemon_info(self):
        """
            get_pokemon_info()
            Gets the information that we want about a pokemon from the PokeAPI.
            Returns a dictionary of those values.
        """
        res = r.get(f'https://pokeapi.co/api/v2/pokemon/{self.my_pokemon}')
        if res.ok:
            data = res.json()
            self.name = data['name'].title()
            self.abilities = [ability['ability']['name'] for ability in data['abilities']]
            self.base_experience = data['base_experience']
            self.sprite_front_shiny_url = data['sprites']['front_shiny']
            self.hp_base_stat = data['stats'][0]['base_stat']
            self.attack_base_stat = data['stats'][1]['base_stat']
            self.defense_base_stat = data['stats'][2]['base_stat']

            # create dictionary
            self.pokemon_info[self.name] = {
                'abilities' : self.abilities,
                'base_experience' : self.base_experience,
                'sprite_front_shiny_url' : self.sprite_front_shiny_url,
                'hp_base_stat' : self.hp_base_stat,
                'attack_base_stat' : self.attack_base_stat,
                'defense_base_stat' : self.defense_base_stat
            }
            return self.pokemon_info
        else: 
            return 'Invalid pokemon name / ID.'
        
    def print_pokemon_info(self):
        """
            print_pokemon_info()
            Prints out the information about a pokemon.
            Returns nothing
        """
        string = f"Here is the info for {self.name}:\n"
        for item in self.pokemon_info[self.name]:
            string += f"{item}: "
            if isinstance(self.pokemon_info[self.name][item], list): # print off all items in the list separately
                for value in self.pokemon_info[self.name][item]:
                    if value != self.pokemon_info[self.name][item][0]: # get commas between values
                        string += ", "
                    string += f"{value}"
                string += "\n"
            else:
                string += f"{self.pokemon_info[self.name][item]}\n"
        print(string)
        
    def image_ascii (self):
        """
            image_ascii()
            Prints the ascii art for the image of a pokemon.
            Returns nothing
        """
        res = r.get(f'https://pokeapi.co/api/v2/pokemon/{self.my_pokemon}')
        if res.ok:
            data = res.json()
            try:
                # prints the ascii for the image
                my_art = AsciiArt.from_url(data['sprites']['front_shiny'])
                my_art.to_terminal() 
                # gets a random color background and text for the name ascii
                color_list = ['red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white', 'black']
                color_random_text = choice(color_list)
                color_random_background = choice(color_list)
                # prints the name of the pokemon in ascii
                cprint(figlet_format(f'{data["name"].upper()}', font='starwars', width = (os.get_terminal_size())[0], justify="center"), f'{color_random_text}', f'on_{color_random_background}', attrs=['bold'])

            except OSError as e: # if the URL doesn't load
                print(f'Could not load the image, server said: {e.code}, {e.msg}')
        else:
            print('Invalid pokemon name / ID.')

###############

class PokemonInputProgram():
    """
        PokemonInputProgram is a class that deals with all the user input for a 
        program that allows the user to interact with the PokeAPI.
    """
    def __init__(self):
        """
            __init__()
            Initializes values for the PokemonInputProgram
            We have some strings for repeated menu options (main_options and inner_options),
            the initial input/output, and the dictionary which holds the pokemon
            that the user has asked for information about.
        """
        self.main_options = "Type 'info' to get the information for a pokemon, 'image' to see what a pokemon looks like, and 'quit' to quit the program.\n"
        self.inner_options = "Type 'known' for a pokemon whose name/ID number you know, 'random' for a random pokemon, 'birthday' for the pokemon that corresponds to your birthday, and 'main' to get back to the main menu.\n"
        self.output = input(f"Welcome to the Pokemon program.\n{self.main_options}")
        self.pokemon_dict = {
            'pokemon': [],
            'birthday_pokemon' : {} # dictionary so it holds the date and the name
        }

    def get_birthday(self):
        """
            get_birthday()
            Gets a birthday in the form of a list [month, day, year] from the 
            user based on their input.
            Returns the list
        """
        try:
            month = int(input("What month were you born? Type the number using 1-2 digits.\nFor example: January = 1.\n"))
            day = int(input("What day were you born? Type the number using 1-2 digits.\nFor example: 3rd = 3.\n"))
            year = int(input("What year were you born? Type the number using digits.\nFor example: 1994.\n"))
            # make sure proper lengths
            if (len(str(month)) == 1 or len(str(month)) == 2) and (len(str(day)) == 1 or len(str(day)) == 2) and len(str(year)) == 4:
                return [month, day, year]
            else:
                return ""
        except:
            return ""
        
    def get_birthday_pokemon_id(self, birthday_list):
        """
            Gets the (relatively) unique pokemon ID associated with the user's
            inputted birthdate
            Returns the ID for the birthday pokemon
        """
        num = 0
        for item in birthday_list:
            num += item
        return num % 249 # according to the API there are 248 items. We do not want ID=0
    
    def print_info(self, pokemon, image="", birthdate="", birthday=""):
        """
            print_info(pokemon, image="" birthdate="", birthday="")
            Prints the information for the pokemon the user has requested.
            If the user has requested an image, the image is printed, otherwise
            information is printed.
            Also adds the pokemon to the dictionary-> of searched pokemon.
            If the user has requested a birthday pokemon, then it adds the pokemon
            and its associated birthday to the nested dictionary of searched pokemon.
            Returns the user's input from the main menu
        """
        if image:
            pokemon.image_ascii()
            pokemon.get_pokemon_name()
        else:
            print(f"Here is the information for your {birthday}pokemon, in dictionary form.\n{pokemon.get_pokemon_info()}\n")
            pokemon.print_pokemon_info()
        if pokemon.name not in self.pokemon_dict['pokemon'] and (pokemon.get_pokemon_info() != 'Invalid pokemon name / ID.'):
            self.pokemon_dict['pokemon'].append(pokemon.name)# this has to be called after get_pokemon_info to get name
        if birthday:
            if pokemon.name not in self.pokemon_dict['birthday_pokemon']:
                self.pokemon_dict['birthday_pokemon'][pokemon.name] = f"{birthdate[0]}/{birthdate[1]}/{birthdate[2]}"
        return input(f'What else would you like to do?\n{self.main_options}')
                        

    def get_info(self, image=""):
        """
            get_info(image="")
            Handles the submenu retrieval of information if the user has typed that they want 
            to get the info/image of a pokemon. 
            Returns the user's input from the main menu
        """
        info_type = input(f"Which Pokemon would you like to get the information for?\n{self.inner_options}")
        while True:
            if info_type == 'known':
                id = input("What is the Pokemon's name/id?\n")
                pokemon = Pokemon(id)
                return self.print_info(pokemon, image)
            elif info_type == 'random':
                pokemon = Pokemon((randint(1, 248)))
                return self.print_info(pokemon, image)
            elif info_type == 'birthday':
                while True:
                    birthdate = self.get_birthday()
                    birthday_id = self.get_birthday_pokemon_id(birthdate)
                    if birthday_id:
                        birthday_pokemon = Pokemon(birthday_id)
                        return self.print_info(birthday_pokemon, image, birthdate, "special birthday ")
                    else:
                        print("You did not input the proper digits for each month/day/year value. Please try again.")
            elif info_type == 'main':
                return input(f'Taking you back to the main menu.\n{self.main_options}')
            else:
                info_type = input(f"Sorry, I couldn't catch what you wanted.\n{self.inner_options}")

    def quit_program(self):
        """
            quit_program()
            Prints out the dictionary of the pokemon/birthday pokemon the user 
            searched for before the program is quit.
        """
        print("\nThank you for using our program.\nHere are all the pokemon you looked up today.")
        for item in self.pokemon_dict['pokemon']:
            print(item)
        print("\nHere are all the special pokemon we attributed to the birthday(s) you entered:")
        for item in self.pokemon_dict['birthday_pokemon']:
            print(f"{item} : {self.pokemon_dict['birthday_pokemon'][item]}")
        print("\nHave a nice day!")

    def start_program(self):
        """
            start_program()
            Starts the user-input program.
            Handles the information at the main menu.
        """
        while True:
            if self.output == 'info':
                self.output = self.get_info()
            elif self.output == 'image':
                #self.output = self.get_image()
                self.output = self.get_info('image')
            elif self.output == 'quit':
                self.quit_program()
                break
            else:
                self.output = input(f"Sorry, I couldn't catch what you wanted.\n{self.main_options}")


# runs the program
program = PokemonInputProgram()
program.start_program()
