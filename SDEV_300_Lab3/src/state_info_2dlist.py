'''Menu-driven application to allow user to display info about US states
and update state populations'''
import sys
import os
import csv
import matplotlib.pyplot as plt
from PIL import Image

# Info sources:
# https://www.census.gov/data/tables/2020/dec/2020-apportionment-data.html
# https://www.crestcapital.com/tax/us_states_and_capitals
# List of lists to hold U.S. States sorted alphabetically, capital, state population, and flower

# import csv containing needed values as 2d list
with open("state_data.csv", "r", encoding="utf-8") as state_file:
    datareader = csv.reader(state_file, delimiter=",")
state_data = []
for row in datareader:
    state_data.append(row)
# create list containing valid state names for validation purposes
valid_states = []
for row in state_data:
    if row != []:
        valid_states.append(row[0])
# create sorted list of paths of flower images
# images are already named 001.jpg-050.jpg in alphabetical order by corresponding state
FLOWERS_PATH = "flowerimg/"
# 001.jpg is now flowers_list[0], 002.jpg is flowers_list[1], etc.
flowers_list = sorted(os.listdir(FLOWERS_PATH))

def display_all_states():
    '''prints table in tabular form'''
    # gets overall max length of any singular value in the state_data table
    lns = [len(str(s)) for state in state_data for s in state]
    max_len = max(lns)
    # iterate over each element of the list
    # for each row, get a string that's left-justified based on the overall max_len
    # print each row string
    for state in state_data:
        print("".join(str(s).ljust(max_len+2) for s in state))

def search_for_state():
    '''searches for a state and displays capital name, state population, and image of state flower
    Images from: https://www.flowerglossary.com/state-flowers/'''
    while True:
        try:
            state = input("Please enter a state name to search\n")
            if state in valid_states:
                # finds index of row where state matches input
                state_index = valid_states.index(state)
                # prints state info
                print(state_data[state_index])
                # opens and displays correct image
                state_flower = Image.open(FLOWERS_PATH + flowers_list[state_index])
                state_flower.show()
                break
            print("Invalid input, please enter a valid state name\n")
        except ValueError:
            pass

def graph_top5_pop():
    '''displays bar graph of top 5 state populations'''
    # sort state data by population in descending order
    sorted_by_pop = sorted(state_data, key=lambda x:int(x[2]), reverse=True)
    # take first 5 rows of sorted 2D list and desired columns
    top_5_pops = sorted_by_pop[:5]
    # create and show bar graph
    # names of states as categories for bar graph
    state_names = [row[0] for row in top_5_pops]
    # parse populations as integers for plotting
    state_pops = [int(row[2]) for row in top_5_pops]
    plt.bar(state_names, state_pops)
    plt.show()

def update_pop():
    '''Update specified state's population to user-entered value'''    
    while True:
        try:
            state = input("Please enter the name of the state to update its population\n")
            # if state exists
            if state in valid_states:
                new_pop = int(input("Please enter the new population of the state\n"))
                if new_pop >= 0:
                    # retrieves index of state
                    state_index = valid_states.index(state)
                    # updates corresponding population entry in master table
                    state_data[state_index][2] = new_pop
                    # finds row where state matches input
                    us_state = state_data[state_index]
                    # prints state info
                    print(us_state)
                    break
                print("Population must be larger than 0, please try again")
            # prompts for new state and population if state does not exist
            else:
                print("State does not exist, please enter a valid state name\n")
        except ValueError:
            print("Please enter a String for the state and an integer for the population")

def handle_menu():
    '''function to handle user input'''
    while True:
        try:
            print("Welcome to the U.S. State Information application.")
            print("Please select from the following choices:")
            print("1. Display all US States in alphabetical order with capital, \
            state population, and flower")
            print("2. Search for a state and display its capital name, state population, \
            and an image of the associated state flower.")
            print("3. Provide a bar graph of the top 5 populated states showing their populations.")
            print("4. Update the overall state population for a specific state.")
            print("5. Exit the program")
            user_input = int(input("Please enter a choice to run\n"))
            if user_input == 1:
                display_all_states()
            elif user_input == 2:
                search_for_state()
            elif user_input == 3:
                graph_top5_pop()
            elif user_input == 4:
                update_pop()
            elif user_input == 5:
                print("You've indicated that you want to exit. Thanks and goodbye\n")
                sys.exit()
            else:
                print("Invalid number, please enter a number 1-5\n")
        except ValueError:
            print("Please enter an integer\n")

handle_menu()
