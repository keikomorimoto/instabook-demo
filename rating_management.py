from db_management import get_db_connection


def get_book_rating_for_user(book_id, user_id):
    """
    Gets a specific user's rating for a book.

    *(Tables involved: book_ratings r)*

    :param user_id: the id of the user to retrieve the rating for
    :type user_id: int
    :param book_id: the id of the book to retrieve the rating for
    :type book_id: int
    :return: a dictionary of the form
        <code>{'score': r.score, 'review': r.review}</code>
        representing a rating
    :rtype: dict
    """
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("""SELECT r.score, r.review
                                FROM book_ratings AS r
                               WHERE r.user_id = %s
                                 AND r.book_id = %s""", [user_id, book_id])
            rating = cursor.fetchone()
            return rating


def get_recent_book_ratings(book_id):
    """
    Gets any 10 ratings for a book, along with details of the users who created them.

    *(Tables involved: users u, book_ratings r)*

    :param book_id: the id of the book to retrieve the ratings for
    :type book_id: int
    :return: a list of dictionaries of the form
        <code>{'user_id': r.user_id, 'username': u.username, 'display_name': u.display_name, 'score': r.score, 'review': r.review}</code>
        representing ratings
    :rtype: dict
    """
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            # Temporary code
            ratings = [
                {'user_id': 1, 'username': 'somebody',     'display_name': 'Some Body',     'score': 5, 'review': 'Banging'},
                {'user_id': 2, 'username': 'somebodyelse', 'display_name': 'Somebody Else', 'score': 4, 'review': 'It was good I guess'},
            ]
            return ratings


def get_recent_user_ratings(user_id):
    """
    Gets any 10 ratings from a user, along with details of the books they were for.

    *(Tables involved: books b, book_ratings r)*

    :param user_id: the id of the user to retrieve the ratings for
    :type user_id: int
    :return: a list of dictionaries of the form
        <code>{'book_id': r.book_id, 'title': b.title, 'author': b.author, 'score': r.score, 'review': r.review}</code>
        representing ratings
    :rtype: dict
    """
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            # Temporary code
            ratings = [
                {'book_id': 1, 'title': 'Some Book',       'author': 'Some Author',       'score': 5, 'review': 'Banging'},
                {'book_id': 2, 'title': 'Some Other Book', 'author': 'Some Other Author', 'score': 4, 'review': 'It was good I guess'},
            ]
            return ratings


def get_recent_followed_user_ratings(user_id):
    """
    Gets any 10 ratings from users followed by a particular user, along with details of who created them and the books they were for.

    *(Tables involved: users u, followers f, books b, book_ratings r)*

    :param user_id: the id of the user to retrieve the followed user ratings for
    :type user_id: int
    :return: a list of dictionaries of the form
        <code>{'user_id': r.user_id, 'username': u.username, 'display_name': u.display_name, 'book_id': r.book_id, 'title': b.title, 'author': b.author, 'score': r.score, 'review': r.review}</code>
        representing ratings
    :rtype: dict
    """
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            # Temporary code
            ratings = [
                {'user_id': 1, 'username': 'somebody',     'display_name': 'Some Body',     'book_id': 1, 'title': 'Some Book',       'author': 'Some Author',       'score': 5, 'review': 'Banging'},
                {'user_id': 2, 'username': 'somebodyelse', 'display_name': 'Somebody Else', 'book_id': 2, 'title': 'Some Other Book', 'author': 'Some Other Author', 'score': 4, 'review': 'It was good I guess'},
            ]
            return ratings


def add_rating(user_id, book_id, score, review):
    """
    Adds a user rating for a specific book.

    *(Tables involved: book_ratings r)*

    :param user_id: the id of the user to add the rating for
    :type user_id: int
    :param book_id: the id of the book to add the rating for
    :type book_id: int
    :param score: the rating score
    :type score: int
    :param review: the rating review
    :type review: str
    :rtype: None
    """
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            # Temporary code
            pass


def remove_rating(user_id, book_id):
    """
    Removes a user rating for a specific book.

    *(Tables involved: book_ratings r)*

    :param user_id: the id of the user to remove the rating for
    :type user_id: int
    :param book_id: the id of the book to remove the rating for
    :type book_id: int
    :rtype: None
    """
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            # Temporary code
            pass
