# To install flask, run `pip install flask`
from flask import request, redirect

from user_management import username_available, is_admin_user
from book_management import book_exists


def should_be_signed_in(route_func):
    def decorated_route_func(*args, **kwargs):
        if request.cookies.get('user_id') is None:
            return redirect('/signin')
        return route_func(*args, **kwargs)
    decorated_route_func.__name__ = route_func.__name__
    return decorated_route_func


def should_be_signed_in_as_admin(route_func):
    def decorated_route_func(*args, **kwargs):
        if request.cookies.get('user_id') is None:
            return redirect('/signin')
        user_id = int(request.cookies.get('user_id'))
        if not is_admin_user(user_id):
            return redirect('/')
        return route_func(*args, **kwargs)
    decorated_route_func.__name__ = route_func.__name__
    return decorated_route_func


def should_be_signed_out(route_func):
    def decorated_route_func(*args, **kwargs):
        if request.cookies.get('user_id') is not None:
            return redirect('/')
        return route_func(*args, **kwargs)
    decorated_route_func.__name__ = route_func.__name__
    return decorated_route_func


def get_query_values(*keys):
    if len(keys) == 1:
        return request.args.get(keys[0])
    return map(request.args.get, keys)


def get_form_values(*keys):
    if len(keys) == 1:
        return request.form.get(keys[0])
    return map(request.form.get, keys)


def get_account_creation_error(username, display_name, pin):
    if not 1 <= len(username) <= 20:
        return 'Username must be between 1 and 20 characters long'
    if not username.isalnum():
        return 'Username must only include letters and numbers'
    if not 1 <= len(display_name) <= 20:
        return 'Display name must be between 1 and 50 characters long'
    if not pin.isdigit() or len(pin) != 4:
        return 'Pin must consist of 4 digits'
    if not username_available(username):
        return f'Username {username} is already taken'


def get_book_creation_error(title, author, isbn):
    if not 1 <= len(title) <= 255:
        return 'Title must be between 1 and 255 characters long'
    if author and len(author) > 255:
        return 'Author must be at most 255 characters long'
    if isbn and len(isbn) not in (10, 13):
        return 'ISBN must consist of exactly 10 or 13 digits'
    if isbn and book_exists(isbn):
        return f'A book with ISBN {isbn} already exists in the database'


def get_rating_creation_error(score, review):
    try:
        int(score)
    except ValueError:
        return 'Score must be a whole number'
    if not 1 <= int(score) <= 5:
        return 'Score must be between 1 and 5'
    if review and len(review) > 255:
        return 'Review must be at most 255 characters long'
