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
        print(f"{bcolors.OKCYAN}{bcolors.UNDERLINE}My Collection has: {bcolors.ENDC}")
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

    def addBook(self):
        """Takes in a book and adds it to the librarys dictionary."""
        newBook = inquirer.prompt(bookForm)
        if newBook["continue"] is True:
            book = Book(newBook["title"], newBook["author"], newBook["genre"])
            self.books.append(book)
            print(f"{bcolors.OKGREEN}[Success]Book successfully added. \n")
        else:
            print(f"{bcolors.FAIL}[Cancelled]Book was not added. \n")

    def addMovie(self):
        """Takes in a movie and adds it to the librarys dictionary."""
        newMovie = inquirer.prompt(movieForm)
        if newMovie["continue"] is True:
            movie = Movie(
                newMovie["title"], newMovie["director"], newMovie["genre"]
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
                newVideoGame["genre"],
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

        print(f'{bcolors.OKBLUE}Calling API with isbn {userInput["isbn"]}...{bcolors.ENDC}')
        data = self.callAPI(userInput['isbn'])
        
        # MICROSERVICE CALL
        print(f'{bcolors.OKBLUE}Calling microservice...{bcolors.ENDC}')
        microRes = self.callMicroservice(data)
        print(f'{bcolors.OKBLUE}Data received from microservice: {microRes} {bcolors.ENDC}\n')
        if 'categories' in microRes:
            book = Book(microRes['title'], microRes['authors'][0], microRes['categories'][0])
            print(book)
            self.books.append(book)
        else:
            book = Book(microRes['title'], microRes['author'])
            self.books.append(book)
        print(f"{bcolors.OKGREEN}[Success]Book successfully imported. \n")


    def callAPI(self, isbn):
        api_url = f"https://www.googleapis.com/books/v1/volumes?q=isbn{isbn}&key={API_KEY}"
        response = requests.get(api_url)
        if response.status_code != 200:
            print('[Error] API Call unsuccessful.')
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
        print(f"Connecting to {HOST}:{PORT}...")
        connection_socket.connect((HOST, PORT))

        # send message length
        # (required for when the server switches roles from recv'ing to send'ing)
        msg_len = str(len(data))
        # print(f"Sending length of message to server:\n\t{msg_len} characters")
        connection_socket.send(msg_len.encode())
        # receive length verification:
        length_verification = connection_socket.recv(1024).decode()

        if length_verification == msg_len:
            # send message
            # print(f"Sending the following message to the server:\n\t{data}")
            connection_socket.send(data.encode())
            # print("Send successful.")

            # recv message
            full_msg = ""
            while True:
                msg = connection_socket.recv(1024).decode()
                # print(f"Message received:\n\t{msg}")
                full_msg += msg

                # full message received
                if not msg:

                    # recv'd message formats
                    # print(f"Full data received as string: {full_msg}")
                    msg_json = json.loads(full_msg)
                    # print(f"Jason Object output: {msg_json}")
                    # print("Full message converted to dumped json\n",
                    # json.dumps(msg_json, indent=4))``

                    connection_socket.close()
                    print("Socket closed.")
                    return msg_json
                    # break
        else:
            connection_socket.close()
            print("Socket closed.")
    
    def displayCol(self):
        res = inquirer.prompt(printLibraryQ)
        books = userLibrary.getBooks()
        movies = userLibrary.getMovies()
        videoGames = userLibrary.getVideoGames()
        if res["choice"] == "Basic":
            for book in books:
                print(f"{book.name}, {book.author}")
            for movie in movies:
                print(f"{movie.name}, {movie.director}")
            for videoGame in videoGames:
                print(f"{videoGame.name}, {videoGame.publisher}")

        elif res["choice"] == "Detailed":
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

class Book:
    """Class representing a book item."""
    def __init__(self, title:str, author:str, genre:str = '') -> None:
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

bookForm = [
        inquirer.Text("title", message="What is the title of the book?"),
        inquirer.Text("author", message="Who is the author of the book?"),
        inquirer.Text("genre", message="What is the genre of the book?"),
        inquirer.Confirm("continue", message="Finish submitting this book?"),
]

movieForm = [
        inquirer.Text("title", message="What is the title of the movie?"),
        inquirer.Text("director", message="Who is the director of the movie?"),
        inquirer.Text("genre", message="What is the genre of the movie?"),
        inquirer.Confirm("continue", message="Finish submitting this movie?"),
]

importBook = [inquirer.Text("isbn", message="Enter the ISBN for your book")]

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

if __name__ == "__main__":
    userLibrary = Library()
    print(f"{bcolors.OKGREEN}Use < arrow > to scroll | use < enter > to select")

    while True:
        userLibrary.getSummary()
        userRes = inquirer.prompt(userChoices)
        if userRes["choice"] == "[Form]Add a book":
            userLibrary.addBook()
        elif userRes["choice"] == "[Advanced]Import a book":
            userLibrary.importBook()
        elif userRes["choice"] == "[Form]Add a movie":
            userLibrary.addMovie()
        elif userRes["choice"] == "[Form]Add a video game":
            userLibrary.addVideoGame()
        elif userRes["choice"] == "View Collection":
            if userLibrary.getLength() == 0:
                print(f"{bcolors.FAIL}[Error] Sorry, the library is empty.")
            else:
                userLibrary.displayCol()
        else:
            break
