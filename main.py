import inquirer

if __name__ == "__main__":
    # Ask user what they want to do
    userChoices = [inquirer.List('choice', message='What would you like to do?', choices=['[Form]Add a book', '[Form]Add a movie', '[Form]Add a video game', 'Quit'])]

    while True:
        userRes = inquirer.prompt(userChoices)
        if userRes['choice'] == '[Form]Add a book':
            print('You chose to add a book')
        elif userRes['choice'] == '[Form]Add a movie':
            print('You chose to add a movie')
        elif userRes['choice'] == '[Form]Add a video game':
            print('You chose to add a video game')
        else:
            break
