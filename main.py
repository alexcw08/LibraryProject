import os
import inquirer
import requests
from dotenv import load_dotenv
import json
import socket as s

load_dotenv()
API_KEY = os.getenv("API_KEY")

class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

class Library:
    """
    Represents a library collection. Has a list for each type of media that can be added and removed.
    Also contains print outs of information for user.
    """

    def __init__(self) -> None:
        self.books: list[object] = []
        self.movies: list[object] = []
        self.videoGames: list[object] = []

    def printWelcome(self):
        print(f'\nPython Media Library v1.0')
        print(f"{bcolors.OKGREEN}Use < arrow > to scroll | use < enter > to select \n")

    def getSummary(self):
        """Prints amount of each type of media collection currently has. """
        print(f"{bcolors.OKCYAN}{bcolors.UNDERLINE}My Collection has: {bcolors.ENDC}")
        print(
            f"{len(self.books)} Books \n{len(self.movies)} Movies \n{len(self.videoGames)} Video Games \n"
        )

    def getLength(self):
        return len(self.books) + len(self.movies) + len(self.videoGames)

    def getBooks(self):
        return self.books

    def getMovies(self):
        return self.movies

    def getVideoGames(self):
        return self.videoGames

    def handleAdd(self):
        """ Prompts user and calls respective function based on answer.  """
        addChoice = inquirer.prompt(addChoices)
        if addChoice['choice'] == '[Form]Book':
            self.addBook()
        elif addChoice['choice'] == '[Advanced]Import Book':
            self.importBook()
        elif addChoice['choice'] == '[Form]Movie':
            self.addMovie()
        elif addChoice['choice'] == '[Form]Video Game':
            self.addVideoGame()

    def handleRemove(self):
        """ Prompts user and calls respective function based on answer.  """
        userChoice = inquirer.prompt(removeChoices)
        if userChoice['choice'] == 'Book':
            self.removeBook()
        elif userChoice['choice'] == 'Movie':
            self.removeMovie()
        elif userChoice['choice'] == 'Video Game':
            self.removeVideoGame()

    def removeBook(self):
        """ Prompts user for title of book to be removed and removes from list. """
        removeChoice = inquirer.prompt(removeTitle)
        for book in self.books:
            if removeChoice['removeTitle'] == book.title:
                self.books.remove(book)
                print(f'{bcolors.OKGREEN}Successfully removed book. \n')
                return
        print(f'{bcolors.FAIL}No matching book found. \n')

    def removeMovie(self):
        """ Prompts user for title of movie to be removed and removes from list. """
        removeChoice = inquirer.prompt(removeTitle)
        for movie in self.movies:
            if removeChoice['removeTitle'] == movie.title:
                self.movies.remove(movie)
                print(f'{bcolors.OKGREEN}Successfully removed movie. \n')
                return
        print(f'{bcolors.FAIL}No matching movie found. \n')

    def removeVideoGame(self):
        """ Prompts user for title of video game to be removed and removes from list. """
        removeChoice = inquirer.prompt(removeTitle)
        for videoGame in self.videoGames:
            if removeChoice['removeTitle'] == videoGame.title:
                self.videoGames.remove(videoGame)
                print(f'{bcolors.OKGREEN}Successfully removed video game. \n')
                return
        print(f'{bcolors.FAIL}No matching video game found. \n')

    def handleView(self):
        """ Prompts user and calls respective function based on answer.  """
        viewChoice =  inquirer.prompt(viewChoices)
        if viewChoice['choice'] == 'Basic':
            self.printBasic()
        elif viewChoice['choice'] == 'Detailed':
            self.printDetailed()
        else:
            return

    def printBasic(self):
        books = userLibrary.getBooks()
        movies = userLibrary.getMovies()
        videoGames = userLibrary.getVideoGames()
        for book in books:
            print(f"{book.title}, {book.author}")
        for movie in movies:
            print(f"{movie.title}, {movie.director}")
        for videoGame in videoGames:
            print(f"{videoGame.title}, {videoGame.publisher}")

    def printDetailed(self):
        books = userLibrary.getBooks()
        movies = userLibrary.getMovies()
        videoGames = userLibrary.getVideoGames()

        print(f"{bcolors.OKCYAN}{bcolors.UNDERLINE}Books{bcolors.ENDC}")
        for book in books:
            print(f"{book.title}, {book.author}")
        print(f"{bcolors.OKCYAN}{bcolors.UNDERLINE}Movies{bcolors.ENDC}")
        for movie in movies:
            print(f"{movie.title}, {movie.director}")
        print(
            f"{bcolors.OKCYAN}{bcolors.UNDERLINE}Video Games{bcolors.ENDC}"
        )
        for videoGame in videoGames:
            print(f"{videoGame.title}, {videoGame.publisher}")

    def addBook(self):
        """Takes in a book and adds it to the librarys dictionary."""
        newBook = inquirer.prompt(bookForm)
        if newBook["continue"] is True:
            book = Book(newBook["title"], newBook["author"])
            self.books.append(book)
            print(f"{bcolors.OKGREEN}[Success]Book successfully added. \n")
        else:
            print(f"{bcolors.FAIL}[Cancelled]Book was not added. \n")

    def addMovie(self):
        """Takes in a movie and adds it to the librarys dictionary."""
        newMovie = inquirer.prompt(movieForm)
        if newMovie["continue"] is True:
            movie = Movie(
                newMovie["title"], newMovie["director"]
            )
            self.movies.append(movie)
            print(f"{bcolors.OKGREEN}[Success]Movie successfully added. \n")
        else:
            print(f"{bcolors.FAIL}[Cancelled]Movie was not added. \n")

    def addVideoGame(self):
        """Takes in a video game and adds it to the librarys dictionary."""
        newVideoGame = inquirer.prompt(videoGameForm)
        if newVideoGame["continue"] is True:
            videoGame = VideoGame(
                newVideoGame["title"],
                newVideoGame["publisher"],
            )
            self.videoGames.append(videoGame)
            print(f"{bcolors.OKGREEN}[Success]Video Game successfully added.\n")
        else:
            print(f"{bcolors.FAIL}[Cancelled]Video game was not added.\n")    

    def importBook(self):
        print(f"\n{bcolors.UNDERLINE}Import a book with an ISBN {bcolors.ENDC} \n Example: 9780140817744 \n")
        print(f"Nineteen Eighty-Four, George Orwell \n")

        userInput = inquirer.prompt(importBook)
        while len(userInput['isbn']) != 13:
            print('length of isbn is', len(userInput['isbn']))
            print('[Input Error] Please enter a 13 digit ISBN number.')
            userInput = inquirer.prompt(importBook)
            
        data = self.callAPI(userInput['isbn'])
        
        # MICROSERVICE CALL
        microRes = self.callMicroservice(data)
        title, author = microRes['title'], microRes['authors'][0]
        # microRes = self.verifyResponse(microRes)
        title, author = self.verifyResponse(title, author)
        # book = Book(microRes['title'], microRes['authors'][0])
        book = Book(title, author)
        self.books.append(book)
        print(f"{bcolors.OKGREEN}[Success]Book successfully imported. \n")

    def callAPI(self, isbn):
        api_url = f"https://www.googleapis.com/books/v1/volumes?q=isbn{isbn}&key={API_KEY}"
        response = requests.get(api_url)
        if response.status_code != 200:
            print('[Error] API Call unsuccessful. Try again later.')
        else:
            data = response.json()
            data = data['items'][0]['volumeInfo']
            data = json.dumps(data)
            return data

    def callMicroservice(self, data):
        # connection to server
        HOST = 'localhost'
        PORT = 10103
        connection_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
        connection_socket.connect((HOST, PORT))

        msg_len = str(len(data))
        connection_socket.send(msg_len.encode())
        length_verification = connection_socket.recv(1024).decode()

        if length_verification == msg_len:
            connection_socket.send(data.encode())

            # receive from server
            full_msg = ""
            while True:
                msg = connection_socket.recv(1024).decode()
                full_msg += msg

               # when finished receiving
                if not msg:
                    msg_json = json.loads(full_msg)
                    connection_socket.close()
                    return msg_json
        else:
            connection_socket.close()
    
    def verifyResponse(self, title, author):
        """ Shows the user response from API and allows user to verify and make changes. """
        print(f'{bcolors.WARNING}Importing book: {title}, {author} {bcolors.ENDC}\n')
        userVerify = inquirer.prompt(confirmInfo)

        if userVerify['confirmation'] is False:
            print('Leave empty for no change.')
            updateInfo = inquirer.prompt(changeInfo)
            if updateInfo['title'] == '' and updateInfo['author'] != '':
                author = updateInfo['author']
                return title, author
            elif updateInfo['author'] == '' and updateInfo['title'] != '':
                title = updateInfo['title']
                return title, author
        return title, author


class Book:
    """Class representing a book item."""
    def __init__(self, title:str, author:str) -> None:
        self.title = title
        self.author = author


class Movie:
    """Class representing a movie item."""
    def __init__(self, title:str, director:str) -> None:
        self.title = title
        self.director = director

class VideoGame:
    """Class representing a video game item."""
    def __init__(self, title:str, publisher:str) -> None:
        self.title = title
        self.publisher = publisher

userChoices = [
        inquirer.List(
            "choice",
            message=f"{bcolors.UNDERLINE}What would you like to do? {bcolors.ENDC}",
            choices=[
                'Add an item',
                'Remove an item',
                'View Collection',
                'Quit'
            ],
        ), 
    ]

addChoices = inquirer.List(
            'choice', 
            message="What would you like to add? ", 
            choices=[
                '[Form]Book',
                '[Form]Movie', 
                '[Form]Video Game', 
                '[Advanced]Import Book', 
                'Go Back'
            ],
        ),

removeChoices = inquirer.List(
            'choice', 
            message="What would you like to remove? ", 
            choices=[
                'Book',
                'Movie', 
                'Video Game', 
                'Go Back'
            ],
        ),

removeTitle = [inquirer.Text('removeTitle', message='Title of item to be removed:')]

viewChoices = inquirer.List(
            'choice', 
            message="View options would you like to remove? ", 
            choices=[
                'Basic', 
                'Detailed', 
                'Go Back'
            ],
        ),

bookForm = [
        inquirer.Text("title", message="What is the title of the book?"),
        inquirer.Text("author", message="Who is the author of the book?"),
        inquirer.Confirm("continue", message="Finish submitting this book?"),
]

movieForm = [
        inquirer.Text("title", message="What is the title of the movie?"),
        inquirer.Text("director", message="Who is the director of the movie?"),
        inquirer.Confirm("continue", message="Finish submitting this movie?"),
]

importBook = [inquirer.Text("isbn", message="Enter the ISBN for your book")]

videoGameForm = [
        inquirer.Text("title", message="What is the title of the video game?"),
        inquirer.Text("publisher", message="Who is the publisher of the video game?"),
        inquirer.Confirm("continue", message="Finish submitting this video game?"),
]

confirmInfo = [inquirer.Confirm(
            "confirmation",
            message="Is the above information correct?",
        )]
changeInfo = [
        inquirer.Text('title', message="Change title to"),
        inquirer.Text('author', message="Change author to")
]

if __name__ == "__main__":
    userLibrary = Library()
    userLibrary.printWelcome()

    while True:
        userLibrary.getSummary()
        userChoice = inquirer.prompt(userChoices)
        if userChoice['choice'] == 'Add an item':
            userLibrary.handleAdd()                    
        elif userChoice["choice"] == "Remove an item":
            userLibrary.handleRemove()
        elif userChoice["choice"] == "View Collection":
            userLibrary.handleView()
        elif userChoice["choice"] == "Quit":
            break
