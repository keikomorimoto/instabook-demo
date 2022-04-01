from db_management import get_db_connection


def add_user(username, display_name, pin):
    """
    Adds a new user to the database.

    *(Tables involved: users u)*

    :param username: the username of the user to add
    :type username: str
    :param display_name: the display name of the user to add
    :type display_name: str
    :param pin: the pin of the user to add
    :type pin: str
    :rtype: None
    """
    with get_db_connection() as connection:
        with connection.cursor(dictionary=True) as cursor:
            # Temporary code
            pass


def username_available(username):
    """
    Finds whether a particular username already exists in the database.

    *(Tables involved: users u)*

    :param username: the username to check the availability of
    :type username: str
    :return: <code>True</code> if the username is available, or <code>False</code> otherwise
    :rtype: bool
    """
    with get_db_connection() as connection:
        with connection.cursor(dictionary=True) as cursor:
            # Temporary code
            user = None
            return True if user is None else False


def get_user_with_credentials(username, pin):
    """
    Finds the id of the user with a specific username and pin combination.

    *(Tables involved: users u)*

    :param username: the username of the user
    :type username: str
    :param pin: the pin of the user
    :type pin: str
    :return: the id of the user, if found
    :rtype: int or None
    """
    with get_db_connection() as connection:
        with connection.cursor(dictionary=True) as cursor:
            cursor.execute("""SELECT u.id
                              FROM users AS u
                              WHERE u.username = %s
                              AND u.pin = %s""", [username, pin])
            user = cursor.fetchone()
            if user is not None:
                return user['id']


def search_users(name):
    """
    Finds all users whose username or display name is like a particular name.

    *(Tables involved: users u)*

    :param name: the name to search for
    :type name: str
    :return: a list of dictionaries of the form
        <code>{'id': u.id, 'username': u.username, 'display_name': u.display_name, 'is_admin': u.is_admin}</code>
        representing users
    :rtype: list[dict]
    """
    with get_db_connection() as connection:
        with connection.cursor(dictionary=True) as cursor:
            # Temporary code
            users = [
                {'id': 1, 'username': 'somebody',     'display_name': 'Some Body',     'is_admin': True},
                {'id': 2, 'username': 'somebodyelse', 'display_name': 'Somebody Else', 'is_admin': False},
            ]
            return users


def get_user_details(user_id):
    """
    Gets details of a specific user.

    *(Tables involved: users u)*

    :param user_id: the id of the user to get details for
    :type user_id: int
    :return: a dictionary of the form
        <code>{'id': u.id, 'username': u.username, 'display_name': u.display_name, 'is_admin': u.is_admin}</code>
        representing a user
    :rtype: dict
    """
    with get_db_connection() as connection:
        with connection.cursor(dictionary=True) as cursor:
            # Temporary code
            user = {'id': user_id, 'username': 'somebody', 'display_name': 'Some Body', 'is_admin': True}
            return user


def is_admin_user(user_id):
    """
    Finds whether a particular user is an admin user.

    *(Tables involved: users u)*

    :param user_id: the id of the user to check
    :type user_id: int
    :return: <code>True</code> if the user is an admin user, or <code>False</code> otherwise
    :rtype: bool
    """
    user = get_user_details(user_id)
    return user['is_admin']
