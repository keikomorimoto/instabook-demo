# To install flask, run `pip install flask`
from flask import Flask, request, flash, make_response, render_template, redirect, url_for
from werkzeug.exceptions import HTTPException

from book_management import add_book, search_books, get_book_details
from user_management import add_user, search_users, get_user_details, get_user_with_credentials
from follower_management import add_follower_pair, remove_follower_pair, follower_pair_exists
from rating_management import get_recent_book_ratings, get_recent_user_ratings, get_recent_followed_user_ratings, \
    get_book_rating_for_user, add_rating, remove_rating

from utils import should_be_signed_in, should_be_signed_in_as_admin, should_be_signed_out, \
    get_query_values, get_form_values, get_account_creation_error, get_book_creation_error, get_rating_creation_error
from config import FLASK_SECRET, FLASK_DEBUG

app = Flask(__name__)
app.secret_key = FLASK_SECRET


@app.get('/')
@should_be_signed_in
def view_feed():
    current_user_id = int(request.cookies.get('user_id'))
    recent_follower_ratings = get_recent_followed_user_ratings(current_user_id)
    return render_template('feed.html', ratings=recent_follower_ratings)


@app.get('/signup')
@should_be_signed_out
def view_signup():
    return render_template('signup.html')


@app.post('/signup')
@should_be_signed_out
def submit_signup():
    username, display_name, pin = get_form_values('username', 'display_name', 'pin')
    if error := get_account_creation_error(username, display_name, pin):
        flash(error)
        return redirect(url_for(view_signup.__name__))
    add_user(username, display_name, pin)
    return redirect(url_for(view_signin.__name__))


@app.get('/signin')
@should_be_signed_out
def view_signin():
    return render_template('signin.html')


@app.post('/signin')
@should_be_signed_out
def submit_signin():
    username, pin = get_form_values('username', 'pin')
    response = make_response(redirect(url_for(view_signin.__name__)))
    if (user_id := get_user_with_credentials(username, pin)) is None:
        flash('Invalid details, please try again')
    else:
        response.set_cookie('user_id', str(user_id), max_age=3600)
    return response


@app.post('/signout')
@should_be_signed_in
def submit_signout():
    response = make_response(redirect(url_for(view_signin.__name__)))
    response.delete_cookie('user_id')
    return response


@app.get('/books/search')
@should_be_signed_in
def find_book():
    title = get_query_values('title') or ''
    matching_books = search_books(title) if title else None
    return render_template('search_books.html', title=title, books=matching_books)


@app.get('/books/<int:book_id>')
@should_be_signed_in
def view_book(book_id):
    current_user_id = int(request.cookies.get('user_id'))
    book_details = get_book_details(book_id)
    book_ratings = get_recent_book_ratings(book_id)
    current_user_rating = get_book_rating_for_user(book_id, current_user_id)
    current_user_score = current_user_rating['score'] if current_user_rating is not None else None
    return render_template('view_book.html', current_user_id=current_user_id, current_user_score=current_user_score, book_details=book_details, book_ratings=book_ratings)


@app.get('/books/<int:book_id>/rate')
@should_be_signed_in
def view_rate_book(book_id):
    current_user_id = int(request.cookies.get('user_id'))
    book_details = get_book_details(book_id)
    current_rating = get_book_rating_for_user(book_id, current_user_id)
    current_score, current_review = (current_rating['score'], current_rating['review']) if current_rating else ('', '')
    return render_template('rate_book.html', book_details=book_details, current_score=current_score, current_review=current_review)


@app.post('/books/<int:book_id>/rate')
@should_be_signed_in
def submit_rate_book(book_id):
    current_user_id = int(request.cookies.get('user_id'))
    score, review = get_form_values('score', 'review')
    if error := get_rating_creation_error(score, review):
        flash(error)
        return redirect(url_for(view_rate_book.__name__))
    remove_rating(current_user_id, book_id)  # Remove any existing rating for the current user
    add_rating(current_user_id, book_id, score, review)  # Add the new rating
    return redirect(url_for(view_book.__name__, book_id=book_id))


@app.post('/books/<int:book_id>/unrate')
@should_be_signed_in
def submit_unrate_book(book_id):
    current_user_id = int(request.cookies.get('user_id'))
    remove_rating(current_user_id, book_id)
    return redirect(url_for(view_book.__name__, book_id=book_id))


@app.get('/books/add')
@should_be_signed_in_as_admin
def view_add_book():
    return render_template('add_book.html')


@app.post('/books/add')
@should_be_signed_in_as_admin
def submit_add_book():
    title, author, isbn = get_form_values('title', 'author', 'isbn')
    if error := get_book_creation_error(title, author, isbn):
        flash(error)
        return redirect(url_for(view_add_book.__name__))
    new_book_id = add_book(title, author, isbn)
    return redirect(url_for(view_book.__name__, book_id=new_book_id))


@app.get('/users/search')
@should_be_signed_in
def find_user():
    current_user_id = int(request.cookies.get('user_id'))
    name = get_query_values('name') or ''
    matching_users = search_users(name) if name else None
    return render_template('search_users.html', current_user_id=current_user_id, name=name, users=matching_users)


@app.get('/users/<int:user_id>')
@should_be_signed_in
def view_user(user_id):
    current_user_id = int(request.cookies.get('user_id'))
    is_current_user = (user_id == current_user_id)
    current_user_follows_user = follower_pair_exists(current_user_id, user_id)
    user_details = get_user_details(user_id)
    user_ratings = get_recent_user_ratings(user_id)
    return render_template('view_user.html', is_current_user=is_current_user, current_user_follows_user=current_user_follows_user, user_details=user_details, user_ratings=user_ratings)


@app.get('/users/me')
@should_be_signed_in
def view_self():
    current_user_id = int(request.cookies.get('user_id'))
    return redirect(url_for(view_user.__name__, user_id=current_user_id))


@app.post('/users/<int:user_id>/follow')
@should_be_signed_in
def follow_user(user_id):
    current_user_id = int(request.cookies.get('user_id'))
    add_follower_pair(current_user_id, user_id)
    return redirect(url_for(view_user.__name__, user_id=user_id))


@app.post('/users/<int:user_id>/unfollow')
@should_be_signed_in
def unfollow_user(user_id):
    current_user_id = int(request.cookies.get('user_id'))
    remove_follower_pair(current_user_id, user_id)
    return redirect(url_for(view_user.__name__, user_id=user_id))


@app.errorhandler(HTTPException)
def show_http_error(error):
    if error.code == 404:
        message = 'We couldn\'t find what you were looking for.'
    else:
        message = 'Something went wrong'
    return render_template('error.html', error_code=error.code, error_message=message)


app.run(debug=FLASK_DEBUG)
