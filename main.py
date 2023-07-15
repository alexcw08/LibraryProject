import inquirer

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Library:
    """ 
    Library class to represent users library collection. Can hold three 
    types of items. Add methods available to add to dictionary.
    """
    def __init__(self) -> None:
        self.books = []
        self.movies = []
        self.videoGames = []

    def getSummary(self):
        """ Prints a summary of the librarys current holdings. """
        print('')
        print(f'{bcolors.OKCYAN}{bcolors.UNDERLINE}My Collection has: {bcolors.ENDC}')
        print(f'{len(self.books)} Books \n{len(self.movies)} Movies \n{len(self.videoGames)} Video Games \n')
        print('')
    
    def getLength(self):
        return len(self.books) + len(self.movies) + len(self.videoGames)

    def getBooks(self):
        """ Returns the dictionary of books. """
        return self.books

    def getMovies(self):
        """ Returns the dictionary of movies. """
        return self.movies

    def getVideoGames(self):
        """ Returns the dictionary of video games. """
        return self.videoGames

    def addBook(self, book):
        """ Takes in a book and adds it to the librarys dictionary. """
        # self.books[book.name] = book
        self.books.append(book)
        print(f'{bcolors.OKGREEN}[Success]Book successfully added.')

    def addMovie(self, movie):
        """ Takes in a movie and adds it to the librarys dictionary. """
        self.movies.append(movie)
        print(f'{bcolors.OKGREEN}[Success]Movie successfully added.')

    def addVideoGame(self, videoGame):
        """ Takes in a video game and adds it to the librarys dictionary. """
        self.videoGames.append(videoGame)
        print(f'{bcolors.OKGREEN}[Success]Video Game successfully added.')

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
    userChoices = [inquirer.List('choice', message=f'{bcolors.UNDERLINE}What would you like to do? {bcolors.ENDC}', choices=['[Form]Add a book', '[Form]Add a movie', '[Form]Add a video game', 'View Collection' ,'Quit'])]
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

    printLibraryQ = [
        inquirer.List('choice', message=f'{bcolors.UNDERLINE}View options{bcolors.ENDC}', choices=['Basic', 'Detailed', 'Go Back'])
    ]

    userLibrary = Library()
    # book1 = Book('My Favorite Book', 'Jane Doe', 'Action')
    # book2 = Book('My Other Book', 'Jane Doe', 'Horror')
    # book3 = Book('Not So Book', 'Bob Mall', 'Romance')

    # movie1 = Movie('First Movie', 'Bob Lob', 'Action')
    # videoGame1 = VideoGame('First Game', 'Bob Lob', 'RPG')

    # userLibrary.addBook(book1)
    # userLibrary.addBook(book2)
    # userLibrary.addBook(book3)
    # userLibrary.addMovie(movie1)
    # userLibrary.addVideoGame(videoGame1)

    print('')

    print(f'{bcolors.OKGREEN}Use < arrow > to scroll | use < enter > to select')
    while True:
        userLibrary.getSummary()
        userRes = inquirer.prompt(userChoices)
        if userRes['choice'] == '[Form]Add a book':
            newBook = inquirer.prompt(bookForm)
            if newBook['continue'] is True:
                addBook = Book(newBook['title'], newBook['author'], newBook['genre'])
                userLibrary.addBook(addBook)
            else:
                print(f'{bcolors.FAIL}[Cancelled]Book was not added.')
        elif userRes['choice'] == '[Form]Add a movie':
            newMovie = inquirer.prompt(movieForm)
            if newMovie['continue'] is True:
                addMovie = Movie(newMovie['title'], newMovie['director'], newMovie['genre'])
                userLibrary.addMovie(addMovie)
            else:
                print(f'{bcolors.FAIL}[Cancelled]Movie was not added.')
        elif userRes['choice'] == '[Form]Add a video game':
            newVideoGame = inquirer.prompt(videoGameForm)
            if newVideoGame['continue'] is True:
                addVideoGame = VideoGame(newVideoGame['title'], newVideoGame['publisher'], newVideoGame['genre'])
                userLibrary.addVideoGame(addVideoGame)
            else:
                print(f'{bcolors.FAIL}[Cancelled]Video game was not added.')
        elif userRes['choice'] == 'View Collection':
            if userLibrary.getLength() == 0:
                print(f'{bcolors.FAIL}[Error] Sorry, the library is empty.')
            else:
                res = inquirer.prompt(printLibraryQ)
                books = userLibrary.getBooks()
                movies = userLibrary.getMovies()
                videoGames = userLibrary.getVideoGames()
                if res['choice'] == 'Basic':
                    print('')
                    print('')
                    for book in books:
                        print(f'{book.name}, {book.author}')
                    for movie in movies:
                        print(f'{movie.name}, {movie.director}')
                    for videoGame in videoGames:
                        print(f'{videoGame.name}, {videoGame.publisher}')
                    print('')
                    print('')

                elif res['choice'] == 'Detailed':
                    print('')
                    print('')
                    # print by category and above
                    print(f'{bcolors.OKCYAN}{bcolors.UNDERLINE}Books{bcolors.ENDC}')
                    for book in books:
                        print(f'{book.name}, {book.author}')
                    print(f'{bcolors.OKCYAN}{bcolors.UNDERLINE}Movies{bcolors.ENDC}')
                    for movie in movies:
                        print(f'{movie.name}, {movie.director}')
                    print(f'{bcolors.OKCYAN}{bcolors.UNDERLINE}Video Games{bcolors.ENDC}')
                    for videoGame in videoGames:
                        print(f'{videoGame.name}, {videoGame.publisher}')
                    print('')
                    print('')
        else:
            break
