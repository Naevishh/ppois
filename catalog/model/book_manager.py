from typing import Optional

from model import Book


class BiblioManager:
    def __init__(self):
        self.books: list[Book] = []

    def load_from_xml(self, filepath: str):
        from .xml_handler import XMLBookReader
        self.books = XMLBookReader(filepath).parse()  # SAX внутри

    def save_to_xml(self, filepath: str):
        from .xml_handler import XMLWriter
        XMLWriter(self.records).save(filepath)

    @staticmethod
    def _check_boundaries(value, option, boundary):
        return value < boundary if option == 'less' else value > boundary

    def find_book(self, name: str = None, author: str = None, publisher: str = None,
                  circulation_limit: tuple[str, Optional[int]] = None,
                  volumes_range: tuple[Optional[int], Optional[int]] = None,
                  total_volumes_limit: tuple[str, Optional[int]] = None):
        result = []
        for book in self.books:
            # ФИО автора (регистронезависимо, точное совпадение)
            if author and book.author.strip().lower() != author.strip().lower():
                continue
            # Издательство
            if publisher and book.publisher.strip().lower() != publisher.strip().lower():
                continue
            # Название книги (поиск подстроки)
            if name and name.lower() != book.name.lower():
                continue
            # Диапазон томов
            if volumes_range:
                low, high = volumes_range
                if low is not None and book.volumes < low:
                    continue
                if high is not None and book.volumes > high:
                    continue
            # Тираж
            if circulation_limit:
                option, value = circulation_limit
                if not self._check_boundaries(book.circulation, option, value):
                    continue
            # Итого томов
            if total_volumes_limit:
                option, value = total_volumes_limit
                if not self._check_boundaries(book.total_volumes, option, value):
                    continue
            result.append(book)
        return result

    def add_book(self, name: str, author: str, publisher: str, circulation: int, number_of_volumes: int):
        self.books.append(Book(name, author, publisher, circulation, number_of_volumes, circulation*number_of_volumes))

    def delete_book(self, **kwargs):
        to_delete = self.find_book(**kwargs)
        if not to_delete:
            return None
        ids_to_remove = [b.book_id for b in to_delete]
        self.books = [b for b in self.books if b.book_id not in ids_to_remove]
        return len(ids_to_remove)



