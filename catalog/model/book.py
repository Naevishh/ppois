import sqlalchemy as db
import sqlite3

class Book:
    def __init__(self, book_id: str, name: str, author: str, publisher: str, circulation: int, number_of_volumes: int, total_volumes: int):
        self.book_id=book_id
        self.name=name
        self.author=author
        self.publisher=publisher
        self.circulation=circulation
        self.volumes=number_of_volumes
        self.total_volumes=total_volumes

engine = db.create_engine('sqlite:///books_database.db')
conn = engine.connect()
metadata = db.MetaData()

books = db.Table('books', metadata,
    db.Column('book_name', db.Text),
    db.Column('book_author', db.Text),
    db.Column('book_publisher', db.Text),
    db.Column('book_circulation', db.Integer, default=False),
    db.Column('book_volumes_number', db.Integer),
    db.Column('book_total_volumes', db.Integer),
)

metadata.create_all(engine)

insertion_query = books.insert().values([[
    {
        "book_name": "Война и мир",
        "book_author": "Лев Толстой",
        "book_publisher": "Эксмо",
        "book_circulation": 150_000,
        "book_volumes_number": 4,
        "book_total_volumes": 150_000 * 4
    },
    {
        "book_name": "Преступление и наказание",
        "book_author": "Фёдор Достоевский",
        "book_publisher": "АСТ",
        "book_circulation": 200_000,
        "book_volumes_number": 1,
        "book_total_volumes": 200_000 * 1
    },
    {
        "book_name": "Мастер и Маргарита",
        "book_author": "Михаил Булгаков",
        "book_publisher": "Рипол Классик",
        "book_circulation": 120_000,
        "book_volumes_number": 1,
        "book_total_volumes": 120_000 * 1
    },
    {
        "book_name": "Анна Каренина",
        "book_author": "Лев Толстой",
        "book_publisher": "Художественная литература",
        "book_circulation": 80_000,
        "book_volumes_number": 2,
        "book_total_volumes": 80_000 * 2
    },
    {
        "book_name": "Евгений Онегин",
        "book_author": "Александр Пушкин",
        "book_publisher": "Просвещение",
        "book_circulation": 300_000,
        "book_volumes_number": 1,
        "book_total_volumes": 300_000 * 1
    }
]])

conn.execute(insertion_query)
conn.commit()