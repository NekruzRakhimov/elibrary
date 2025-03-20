import psycopg2

DB_CONFIG = {
    "dbname": "elibrary_db",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": "5432"
}


def connect_db():
    return psycopg2.connect(**DB_CONFIG)


def init_db():
    with connect_db() as conn, conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS books
            (
                id    SERIAL PRIMARY KEY, -- serial = int + autoincrement
                title VARCHAR(100) UNIQUE
            );
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS authors
            (
                id        SERIAL PRIMARY KEY,
                full_name VARCHAR(150) UNIQUE
            );
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS genres
            (
                id   SERIAL PRIMARY KEY,
                name VARCHAR(100) UNIQUE
            );
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS books_authors
            (
                id        SERIAL PRIMARY KEY,
                book_id   INT REFERENCES books (id) ON DELETE CASCADE,
                author_id INT REFERENCES authors (id) ON DELETE CASCADE
            );
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS books_genres
            (
                id       SERIAL PRIMARY KEY,
                book_id  INT REFERENCES books (id) ON DELETE CASCADE,
                genre_id INT REFERENCES genres (id) ON DELETE CASCADE
            )
        """)


def get_all_books():
    with connect_db() as conn, conn.cursor() as cur:
        cur.execute("SELECT * FROM books")

        books = cur.fetchall()
        return books


def get_all_authors():
    with connect_db() as conn, conn.cursor() as cur:
        cur.execute("SELECT * FROM authors")

        authors = cur.fetchall()
        return authors


def get_all_genres():
    with connect_db() as conn, conn.cursor() as cur:
        cur.execute("SELECT * FROM genres")

        genres = cur.fetchall()
        return genres


def get_book_full_info_by_id(book_id):
    with connect_db() as conn, conn.cursor() as cur:
        # Получение информации о книге
        cur.execute("SELECT * FROM books WHERE id = %s", (book_id,))
        book_info = cur.fetchone()

        # Получение списка авторов книги
        cur.execute("""
                    SELECT a.full_name
            FROM books_authors ba
                     JOIN authors a ON ba.author_id = a.id
            WHERE ba.book_id = %s""", (book_id,))

        authors = cur.fetchall()

        # Получение жанров книги
        cur.execute("""
                SELECT g.name
                FROM books_genres bg
                         JOIN genres g ON bg.genre_id = g.id
                WHERE bg.book_id = %s""", (book_id,))

        genres = cur.fetchall()
        return {
            "book_info": book_info,
            "authors": authors,
            "genres": genres
        }


def create_author(full_name):
    with connect_db() as conn, conn.cursor() as cur:
        cur.execute("INSERT INTO authors (full_name) VALUES (%s)", (full_name,))
