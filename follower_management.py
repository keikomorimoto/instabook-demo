from db_management import get_db_connection


def add_follower_pair(follower_user_id, followed_user_id):
    """
    Adds a new follower for a specific user.

    *(Tables involved: followers f)*

    :param follower_user_id: the user id of the new follower
    :type follower_user_id: int
    :param followed_user_id: the user id of the newly followed user
    :type followed_user_id: int
    :rtype: None
    """
    with get_db_connection() as connection:
        with connection.cursor(dictionary=True) as cursor:
            # Temporary code
            pass


def remove_follower_pair(follower_user_id, followed_user_id):
    """
    Removes a follower for a specific user.

    *(Tables involved: followers f)*

    :param follower_user_id: the user id of the former follower
    :type follower_user_id: int
    :param followed_user_id: the user id of the formerly followed user
    :type followed_user_id: int
    :rtype: None
    """
    with get_db_connection() as connection:
        with connection.cursor(dictionary=True) as cursor:
            # Temporary code
            pass


def follower_pair_exists(follower_user_id, followed_user_id):
    """
    Finds whether a particular user follows another specified user.

    *(Tables involved: followers f)*

    :param follower_user_id: the user id of the follower to check
    :type follower_user_id: int
    :param followed_user_id: the user id of the followed user to check
    :type followed_user_id: int
    :return: <code>True</code> if a follower pair exists, or <code>False</code> otherwise
    :rtype: bool
    """
    with get_db_connection() as connection:
        with connection.cursor(dictionary=True) as cursor:
            # Temporary code
            follower_pair = None
            return True if follower_pair is not None else False
