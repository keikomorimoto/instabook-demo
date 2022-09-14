from db_management import get_db_connection


def add_book(title, author, isbn):
    """
    Adds a new book to the database.

    *(Tables involved: books b)*

    :param title: the title of the book to add
    :type title: str
    :param author: the author of the book to add
    :type author: str
    :param isbn: the isbn of the book to add
    :type isbn: str
    :return: the id of the newly added book
    :rtype: int
    """
    with get_db_connection() as connection:
        with connection.cursor(dictionary=True) as cursor:
            # Temporary code
            new_book_id = 1
            return new_book_id


def book_exists(isbn):
    """
    Finds whether a book with a particular isbn already exists in the database.

    *(Tables involved: books b)*

    :param isbn: the isbn to check the existence of
    :type isbn: str
    :return: <code>True</code> if a book with the isbn is taken, or <code>False</code> otherwise
    :rtype: bool
    """
    with get_db_connection() as connection:
        with connection.cursor(dictionary=True) as cursor:
            # Temporary code
            book = None
            return False if book is None else True


def search_books(title):
    """
    Finds all books whose titles are like a particular title.

    *(Tables involved: books b, book_ratings r)*

    :param title: the title to search for
    :type title: str
    :return: a list of dictionaries of the form
        <code>{'id': b.id, 'title': b.title, 'author': b.author, 'score': AVG(r.score) AS score}</code>
        representing books
    :rtype: list[dict]
    """
    with get_db_connection() as connection:
        with connection.cursor(dictionary=True) as cursor:
            cursor.execute("""SELECT b.id,
                                     b.title,
                                     b.author,
                                     ROUND(AVG(r.score), 1) AS score
                                FROM books AS b
                                JOIN book_ratings AS r
                                  ON b.id = r.book_id
                               WHERE b.title LIKE CONCAT('%', %s, '%')
                            GROUP BY r.book_id;""", [title])
            books = cursor.fetchall()
            return books


def get_book_details(book_id):
    """
    Gets details of a specific book.

    *(Tables involved: books b, book_ratings r)*

    :param book_id: the id of the book to get details for
    :type book_id: int
    :return: a dictionary of the form
        <code>{'id': b.id, 'title': b.title, 'author': b.author, 'score': AVG(r.score) AS score}</code>
        representing a book
    :rtype: dict
    """
    with get_db_connection() as connection:
        with connection.cursor(dictionary=True) as cursor:
            cursor.execute("""SELECT b.id,
                                     b.title,
                                     b.author,
                                     ROUND(AVG(r.score), 1) AS score
                                FROM books AS b
                                JOIN book_ratings AS r
                                  ON b.id = r.book_id
                               WHERE b.id = %s
                            GROUP BY r.book_id""", [book_id])
            book = cursor.fetchone()
            return book
