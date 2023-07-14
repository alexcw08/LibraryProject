import inquirer

class Library:
    """ 
    Library class to represent users library collection. Can hold three 
    types of items. Add methods available to add to dictionary.
    """
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
        print(f'[Success]Book successfully added.')

    def addMovie(self, movie):
        """ Takes in a movie and adds it to the librarys dictionary. """
        self.movies[movie.name] = movie
        print(f'[Success]Movie successfully added.')

    def addVideoGame(self, videoGame):
        """ Takes in a video game and adds it to the librarys dictionary. """
        self.videoGames[videoGame.name] = videoGame
        print(f'[Success]Video Game successfully added.')

class Book:
    """ Class representing a book item. """
    def __init__(self, title, author, genre) -> None:
        self.name = title
        self.author = author
        self.genre = genre

class Movie:
    """ Class representing a movie item. """
    def __init__(self, title, director, genre) -> None:
        self.name = title
        self.director = director
        self.genre = genre

class VideoGame:
    """ Class representing a video game item. """
    def __init__(self, title, publisher, genre) -> None:
        self.name = title
        self.publisher = publisher
        self.genre = genre


if __name__ == "__main__":
    # Array holding user choice question / choices
    userChoices = [inquirer.List('choice', message='What would you like to do?', choices=['[Form]Add a book', '[Form]Add a movie', '[Form]Add a video game', 'Quit'])]
    # Form arrays
    bookForm = [
        inquirer.Text("title", message="What is the title of the book?"),
        inquirer.Text("author", message="Who is the author of the book?"),
        inquirer.Text("genre", message="What is the genre of the book?"),
        inquirer.Confirm("continue", message="Finish submitting this book?"),]

    movieForm = [
        inquirer.Text("title", message="What is the title of the movie?"),
        inquirer.Text("director", message="Who is the director of the movie?"),
        inquirer.Text("genre", message="What is the genre of the movie?"),
        inquirer.Confirm("continue", message="Finish submitting this movie?"),
    ]

    videoGameForm = [
        inquirer.Text("title", message="What is the title of the video game?"),
        inquirer.Text("publisher", message="Who is the publisher of the video game?"),
        inquirer.Text("genre", message="What is the genre of the video game?"),
        inquirer.Confirm("continue", message="Finish submitting this video game?"),
    ]

    userLibrary = Library()

    while True:
        userLibrary.getSummary()
        userRes = inquirer.prompt(userChoices)
        if userRes['choice'] == '[Form]Add a book':
            newBook = inquirer.prompt(bookForm)
            if newBook['continue'] is True:
                addBook = Book(newBook['title'], newBook['author'], newBook['genre'])
                userLibrary.addBook(addBook)
            else:
                print('[Cancelled]Book was not added.')
        elif userRes['choice'] == '[Form]Add a movie':
            newMovie = inquirer.prompt(movieForm)
            if newMovie['continue'] is True:
                addMovie = Movie(newMovie['title'], newMovie['director'], newMovie['genre'])
                userLibrary.addMovie(addMovie)
            else:
                print('[Cancelled]Movie was not added.')
        elif userRes['choice'] == '[Form]Add a video game':
            newVideoGame = inquirer.prompt(videoGameForm)
            if newVideoGame['continue'] is True:
                addVideoGame = VideoGame(newVideoGame['title'], newVideoGame['publisher'], newVideoGame['genre'])
                userLibrary.addVideoGame(addVideoGame)
            else:
                print('[Cancelled]Video game was not added.')

        else:
            break
