# Install mysql-connector-python using pip
import mysql.connector


def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        database='instabook',
        user='admin',
        password='admin'
    )


with get_db_connection() as connection:
    with connection.cursor(dictionary=True) as cursor:
        try:
            cursor.execute("""INSERT
                                INTO users (username, display_name, pin)
                              VALUES ('ruth', 'Mary Ruth', '1234')""")
        except mysql.connector.errors.IntegrityError:
            print("Mary Ruth is already in the database.")
        else:
            connection.commit()

with get_db_connection() as connection:
    with connection.cursor(dictionary=True) as cursor:
        cursor.execute("""SELECT *
                            FROM users AS u""")
        results = cursor.fetchall()

print("All users:")
for result in results:
    print(result)

with get_db_connection() as connection:
    with connection.cursor(dictionary=True) as cursor:
        cursor.execute("""SELECT *
                            FROM users AS u
                           WHERE u.id = 1""")
        result = cursor.fetchone()

print("User number 1:")
print(result)

with get_db_connection() as connection:
    with connection.cursor(dictionary=True) as cursor:
        title = "The Thirst Games"
        author = "Suzanne Collins"
        isbn = "1234567654321"
        try:
            cursor.execute("""INSERT
                                INTO books
                                     (title, author, isbn)
                              VALUES (%s, %s, %s)""", [title, author, isbn])
        except mysql.connector.errors.IntegrityError:
            print("The Thirst Games is already in the database.")
        else:
            connection.commit()

with get_db_connection() as connection:
    with connection.cursor(dictionary=True) as cursor:
        cursor.execute("""SELECT *
                            FROM books AS b""")
        results = cursor.fetchall()

print("All books:")
for result in results:
    print(result)