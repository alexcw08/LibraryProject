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
    Library class to represent users library collection. Can hold three
    types of items. Add methods available to add to dictionary.
    """

    def __init__(self) -> None:
        self.books: list[object] = []
        self.movies: list[object] = []
        self.videoGames: list[object] = []

    def getSummary(self):
        """Prints a summary of the librarys current holdings."""
        print(f"\n{bcolors.OKCYAN}{bcolors.UNDERLINE}My Collection has: {bcolors.ENDC}")
        print(
            f"{len(self.books)} Books \n{len(self.movies)} Movies \n{len(self.videoGames)} Video Games \n"
        )

    def getLength(self):
        return len(self.books) + len(self.movies) + len(self.videoGames)

    def getBooks(self):
        """Returns the dictionary of books."""
        return self.books

    def getMovies(self):
        """Returns the dictionary of movies."""
        return self.movies

    def getVideoGames(self):
        """Returns the dictionary of video games."""
        return self.videoGames

    def addBook(self, book):
        """Takes in a book and adds it to the librarys dictionary."""
        # self.books[book.name] = book
        self.books.append(book)
        print(f"{bcolors.OKGREEN}[Success]Book successfully added.")

    def addMovie(self, movie):
        """Takes in a movie and adds it to the librarys dictionary."""
        self.movies.append(movie)
        print(f"{bcolors.OKGREEN}[Success]Movie successfully added.")

    def addVideoGame(self, videoGame):
        """Takes in a video game and adds it to the librarys dictionary."""
        self.videoGames.append(videoGame)
        print(f"{bcolors.OKGREEN}[Success]Video Game successfully added.")

    def importBook(self):
        print(f"\n{bcolors.UNDERLINE}Import a book with an ISBN {bcolors.ENDC}")
        print("Example: 9780140817744")
        print(f"Nineteen Eighty-Four, George Orwell \n")
        isbn = inquirer.prompt(importBook)
        data = self.callAPI(isbn)
        self.callMicroservice(data)

    def callAPI(self, isbn):
        api_url = f"https://www.googleapis.com/books/v1/volumes?q=isbn{isbn}&key={API_KEY}"
        response = requests.get(api_url)
        data = response.json()
        data = data['items'][0]['volumeInfo']
        data = json.dumps(data)
        return data


    def callMicroservice(self, data):

        # connection to server
        HOST = 'localhost'
        PORT = 10103
        connection_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
        print(f"Connecting to {HOST}:{PORT}...")
        connection_socket.connect((HOST, PORT))

        # message

        # send message length
        # (required for when the server switches roles from recv'ing to send'ing)
        msg_len = str(len(data))
        print(f"Sending length of message to server:\n\t{msg_len} characters")
        connection_socket.send(msg_len.encode())
        # receive length verification:
        length_verification = connection_socket.recv(1024).decode()

        if length_verification == msg_len:
            # send message
            print(f"Sending the following message to the server:\n\t{data}")
            connection_socket.send(data.encode())
            print("Send successful.")

            # recv message
            full_msg = ""
            while True:
                msg = connection_socket.recv(1024).decode()
                # print(f"Message received:\n\t{msg}")
                full_msg += msg

                # full message received
                if not msg:

                    # recv'd message formats
                    print(f"Full data received as string: {full_msg}")
                    msg_json = json.loads(full_msg)
                    # print(f"Jason Object output: {msg_json}")
                    print("Full message converted to dumped json\n",
                        json.dumps(msg_json, indent=4))

                    connection_socket.close()
                    print("Socket closed.")
                    break
        else:
            connection_socket.close()
            print("Socket closed.")


class Book:
    """Class representing a book item."""

    def __init__(self, title:str, author:str, genre:str) -> None:
        self.name = title
        self.author = author
        self.genre = genre


class Movie:
    """Class representing a movie item."""

    def __init__(self, title:str, director:str, genre:str) -> None:
        self.name = title
        self.director = director
        self.genre = genre


class VideoGame:
    """Class representing a video game item."""

    def __init__(self, title:str, publisher:str, genre:str) -> None:
        self.name = title
        self.publisher = publisher
        self.genre = genre


if __name__ == "__main__":
    # Array holding user choice question / choices
    userChoices = [
        inquirer.List(
            "choice",
            message=f"{bcolors.UNDERLINE}What would you like to do? {bcolors.ENDC}",
            choices=[
                "[Form]Add a book",
                "[Form]Add a movie",
                "[Form]Add a video game",
                "[Advanced]Import a book",
                "View Collection",
                "Quit",
            ],
        )
    ]
    # Form arrays
    bookForm = [
        inquirer.Text("title", message="What is the title of the book?"),
        inquirer.Text("author", message="Who is the author of the book?"),
        inquirer.Text("genre", message="What is the genre of the book?"),
        inquirer.Confirm("continue", message="Finish submitting this book?"),
    ]

    importBook = [inquirer.Text("isbn", message="Enter the ISBN for your book")]

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
        inquirer.List(
            "choice",
            message=f"{bcolors.UNDERLINE}View options{bcolors.ENDC}",
            choices=["Basic", "Detailed", "Go Back"],
        )
    ]

    userLibrary = Library()

    print(f"{bcolors.OKGREEN}Use < arrow > to scroll | use < enter > to select")
    while True:
        userLibrary.getSummary()
        userRes = inquirer.prompt(userChoices)
        # User chooses to add BOOK
        if userRes["choice"] == "[Form]Add a book":
            newBook = inquirer.prompt(bookForm)
            if newBook["continue"] is True:
                addBook = Book(newBook["title"], newBook["author"], newBook["genre"])
                userLibrary.addBook(addBook)
            else:
                print(f"{bcolors.FAIL}[Cancelled]Book was not added.")
        # User chooses to add IMPORT A BOOK [USES API]
        elif userRes["choice"] == "[Advanced]Import a book":
            userLibrary.importBook()
        # User chooses to add MOVIE
        elif userRes["choice"] == "[Form]Add a movie":
            newMovie = inquirer.prompt(movieForm)
            if newMovie["continue"] is True:
                addMovie = Movie(
                    newMovie["title"], newMovie["director"], newMovie["genre"]
                )
                userLibrary.addMovie(addMovie)
            else:
                print(f"{bcolors.FAIL}[Cancelled]Movie was not added.")
        # User chooses to add VIDEO GAME
        elif userRes["choice"] == "[Form]Add a video game":
            newVideoGame = inquirer.prompt(videoGameForm)
            if newVideoGame["continue"] is True:
                addVideoGame = VideoGame(
                    newVideoGame["title"],
                    newVideoGame["publisher"],
                    newVideoGame["genre"],
                )
                userLibrary.addVideoGame(addVideoGame)
            else:
                print(f"{bcolors.FAIL}[Cancelled]Video game was not added.")
        # User chooses to VIEW COLLECTION
        elif userRes["choice"] == "View Collection":
            if userLibrary.getLength() == 0:
                print(f"{bcolors.FAIL}[Error] Sorry, the library is empty.")
            else:
                res = inquirer.prompt(printLibraryQ)
                books = userLibrary.getBooks()
                movies = userLibrary.getMovies()
                videoGames = userLibrary.getVideoGames()
                if res["choice"] == "Basic":
                    print("")
                    print("")
                    for book in books:
                        print(f"{book.name}, {book.author}")
                    for movie in movies:
                        print(f"{movie.name}, {movie.director}")
                    for videoGame in videoGames:
                        print(f"{videoGame.name}, {videoGame.publisher}")
                    print("")
                    print("")

                elif res["choice"] == "Detailed":
                    print("")
                    print("")
                    # print by category and above
                    print(f"{bcolors.OKCYAN}{bcolors.UNDERLINE}Books{bcolors.ENDC}")
                    for book in books:
                        print(f"{book.name}, {book.author}")
                    print(f"{bcolors.OKCYAN}{bcolors.UNDERLINE}Movies{bcolors.ENDC}")
                    for movie in movies:
                        print(f"{movie.name}, {movie.director}")
                    print(
                        f"{bcolors.OKCYAN}{bcolors.UNDERLINE}Video Games{bcolors.ENDC}"
                    )
                    for videoGame in videoGames:
                        print(f"{videoGame.name}, {videoGame.publisher}")
                    print("")
                    print("")
        # User chooses QUIT
        else:
            break
