class User():
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.books = {}
    def get_email(self):
        return self.email
    def change_email(self, new_email):
        self.email = new_email
        print('{} email has been updated'.format(self.name))
    def __repr__(self):
        return 'User {}, email: {}, books read: {}'.format(self.name, self.email, len(self.books))
    def __eq__(self, other_user):
        if self.name == other_user.name and self.email == other_user.email:
            return True
        else:
            return False
    def __hash__(self):
        return hash((self.name, self.email))
    def read_book(self, book, rating = None):
        self.books[book] = rating
    def get_average_rating(self):
        ratings_sum = 0
        for rating in self.books.values():
            if rating != None:
                ratings_sum += rating
        try:
            return ratings_sum/len(self.books)
        except ZeroDivisionError:
            return 0
            print('{} hasn\'t read any books yet'.format(self.name))

class Book():
    def __init__(self, title, isbn, price):
        self.title = title
        self.isbn = isbn
        self.price = price
        self.ratings = []
    def get_title(self):
        return self.title
    def get_isbn(self):
        return self.isbn
    def get_price(self):
        return self.price
    def set_isbn(self, new_isbn):
        self.isbn = new_isbn
        print('\"{}\" ISBN has been changed'.format(self.title))
    def add_rating(self, rating):
        if rating == None:
            print('User hasn\'t rated \"{}\" yet'.format(self.title))
        elif rating >= 0 and rating <= 4:
            self.ratings.append(rating)
        else:
            print('Invalid Rating')
    def __eq__(self, other_book):
        if self.title == other_book.title and self.isbn == other_book.isbn and self.price == other_book.price:
            return True
        else:
            return False
    def get_average_rating(self):
        rating_sum = 0
        for rating in self.ratings:
            rating_sum += rating
        try:
            return rating_sum/len(self.ratings)
        except ZeroDivisionError:
            return 0
            print('\"{}\" hasn\'t been rated yet'.format(self.title))
    def __hash__(self):
        return hash((self.title, self.isbn, self.price))
    def __repr__(self):
        return '{title}, ISBN - {isbn}'.format(title = self.title, isbn = self.isbn)

class Fiction(Book):
    def __init__(self, title, author, isbn, price):
        super().__init__(title, isbn, price)
        self.author = author
    def get_author(self):
        return self.author
    def __repr__(self):
        return '{title} by {author}'.format(title = self.title, author = self.author)

class Non_Fiction(Book):
    def __init__(self, title, subject, level, isbn, price):
        super().__init__(title, isbn, price)
        self.subject = subject
        self.level = level
    def get_subject(self):
        return self.subject
    def get_level(self):
        return self.level
    def __repr__(self):
        return '{title}, a {level} manual on {subject}'.format(title = self.title, level = self.level, subject = self.subject)

class TomeRater():
    def __init__(self):
        self.users = {}
        self.books = {}
        self.isbns = []
    def create_book(self, title, isbn, price):
        if isbn not in self.isbns:
            self.isbns.append(isbn)
            return Book(title,isbn, price)
        else:
            print('Book with this ISBN already exists in catalog')
    def create_novel(self, title, author, isbn, price):
        if isbn not in self.isbns:
            self.isbns.append(isbn)
            return Fiction(title, author, isbn, price)
        else:
            print('Book with this ISBN already exists in catalog')
    def create_non_fiction(self, title, subject, level, isbn, price):
        if isbn not in self.isbns:
            self.isbns.append(isbn)
            return Non_Fiction(title, subject, level, isbn, price)
        else:
            print('Book with this ISBN already exists in catalog')  
    def add_book_to_user(self, book, email, rating = None):
        if email in self.users:
            self.users[email].read_book(book, rating)
            book.add_rating(rating)
            if book in self.books:
                self.books[book] += 1
            else:
                self.books[book] = 1
        else:
            print('No user with email {email}!'.format(email = email))
    def add_user(self, name, email, user_books = None):
        email_characters = ['.com','.edu','.org']
        if email in self.users:
            print('User already exists!')
        elif '@' in email:
            for char in email_characters:
                if char in email:
                    self.users[email] = User(name, email)
                    if user_books != None:
                        for book in user_books:
                            self.add_book_to_user(book, email)
                    break
        else:
            print('{} - this email address is invalid'.format(email))
    def print_catalog(self):
        for book in self.books:
            print(book)
    def print_users(self):
        for user in self.users:
            print(user)
    def most_read_book(self):
        read_count = 0
        for book in self.books:
            if self.books[book] > read_count:
                read_count = self.books[book]
        for book, count in self.books.items():
            if count == read_count:
                return book
    def highest_rated_book(self):
        highest_rating = 0
        books_ratings = {}
        for book in self.books:
            books_ratings[book] = book.get_average_rating()
            if book.get_average_rating() > highest_rating:
                highest_rating = book.get_average_rating()
        for book, rating in books_ratings.items():
            if rating == highest_rating:
                return book
    def most_positive_user(self):
        highest_rating = 0
        users_ratings = {}
        for user in self.users:
            users_ratings[user] = self.users[user].get_average_rating()
            if users_ratings[user] > highest_rating:
                highest_rating = users_ratings[user]
        for user, rating in users_ratings.items():
            if rating == highest_rating:
                return user
    def get_n_most_read_books(self, n):
        n_most_read_books = sorted(self.books.keys(), key = self.books.__getitem__, reverse = True)
        if n > len(self.books):
            n = len(self.books)
        for i in range(n):
            print(n_most_read_books[i])
    def get_n_most_prolific_readers(self, n):
        users_read_count = {}
        for user in self.users.values():
            users_read_count[user] = len(user.books)
        n_most_prolific_readers = sorted(users_read_count.keys(), key = users_read_count.__getitem__, reverse = True)
        if n > len(self.users):
            n = len(self.users)
        for i in range(n):
            print(n_most_prolific_readers[i])
    def get_n_most_expensive_books(self, n):
        books_prices = {}
        for book in self.books:
            books_prices[book] = book.price
        n_most_expensive_books = sorted(books_prices.keys(), key = books_prices.__getitem__)
        if n > len(books_prices):
            n = len(books.prices)
        for i in range(n):
            print('{}  {}$'.format(n_most_expensive_books[i],n_most_expensive_books[i].price))
    def get_worth_of_user(self, user_email):
        total = 0
        for book in self.users[user_email].books:
            total += book.price
        return '{}$'.format(total)
    def __repr__(self):
        return 'Catalog includes {total_books} books \nThere are {total_users} users registered'.format(total_books=len(self.books),total_users=len(self.users))
    def __eq__(self, other_tomerater):
        if self.users == other_tomerater.users and self.books == other_tomerater.books:
            return True
