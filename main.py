import inquirer

class Library:
    def __init__(self) -> None:
        self.books = {}
        self.movies = {}
        self.videoGames = {}

    def getSummary(self):
        """ Prints a summary of the librarys current holdings. """
        print('')
        print(f'My Collection has:')
        print(f'{len(self.books)} Books \n{len(self.movies)} Movies \n{len(self.videoGames)} Video Games \n')
        print('')
        
    def addBook(self, book):
        """ Takes in a book and adds it to the librarys dictionary. """
        self.books[book.name] = book
        print(f'[Success] Book successfully added.')

    def addMovie(self, movie):
        """ Takes in a movie and adds it to the librarys dictionary. """
        self.movies[movie.name] = movie
        print(f'[Success] Movie successfully added.')

    def addVideoGame(self, videoGame):
        """ Takes in a video game and adds it to the librarys dictionary. """
        self.videoGames[videoGame.name] = videoGame
        print(f'[Success] Video Game successfully added.')

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
