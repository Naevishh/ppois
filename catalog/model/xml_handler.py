import xml.sax
from pathlib import Path
import uuid

def get_filepath(file_name: str) -> Path:
    current_module_dir = Path(__file__).resolve().parent
    project_root = current_module_dir.parent
    data_dir = project_root / "data"
    if not data_dir.exists():
        data_dir = current_module_dir / "data"

    return data_dir / file_name

class XMLBookReader:
    def __init__(self, file_name):
        self.filepath = get_filepath(file_name)

    class _XMLBookHandler(xml.sax.ContentHandler):
        def __init__(self):
            self.books = []  # Final result goes here
            self.current_book = None  # Temporary storage for one <book>
            self.current_field = None  # Tracks which subtag we're inside
            self.char_buffer = []  # Handles SAX text chunking

        def startElement(self, tag, attrs):
            if tag == "book":
                # Start a new book dictionary
                self.current_book = {"id": attrs.get("id", "")}
            else:
                # We're inside a subtag like <title>, <author>, etc.
                self.current_field = tag
                self.char_buffer = []

        def characters(self, content):
            if self.current_field:
                self.char_buffer.append(content)

        def endElement(self, tag):
            if tag == "book" and self.current_book:
                # Finished an <book>, save it
                self.books.append(self.current_book)
                self.current_book = None
            elif self.current_field == tag and self.current_book is not None:
                # Finished a subtag, store the text
                self.current_book[tag] = "".join(self.char_buffer).strip()

            self.current_field = None
            self.char_buffer = []

    def parse(self):
        parser = xml.sax.make_parser()
        handler = self._XMLBookHandler()
        parser.setContentHandler(handler)

        current_module_dir = Path(__file__).resolve().parent
        project_root = current_module_dir.parent
        data_dir = project_root / "data"
        if not data_dir.exists():
            data_dir = current_module_dir / "data"

        self.filepath = data_dir / "catalog.xml"

        # Parse the file (replace with your actual file)
        parser.parse(self.filepath)

        # 🟢 THIS is your parsed data:
        return handler.books



from xml.dom import minidom

# Пример XML-данных
xml_data = """
<catalog>
    <book id="1" category="books">
        <title>Python Basics</title>
        <author>John Doe</author>
    </book>
    <book id="2" category="electronics">
        <title>Laptop</title>
        <author>Jane Smith</author>
    </book>
</catalog>
"""

class XMLBookWriter:
    def __init__(self, file_name, doc, root):
        self.filepath = get_filepath(file_name)

    def create_book(self, name, author, publisher, circulation, number_of_volumes, total_volumes):
        book = doc.createElement('book')
        book.setAttribute('id', str(uuid.uuid4())[:8])
        for loc, val in locals().items():
            el = doc.createElement(loc)
            el.appendChild(doc.createTextNode(val))
            book.appendChild(el)

# 1. Загрузка/Парсинг XML
doc = minidom.parseString(xml_data)

# 2. Получение элементов по имени тега
books = doc.getElementsByTagName('book')

# 3. Обход элементов и получение данных
for book in books:
    # Получение атрибута
    book_id = book.getAttribute('id')
    category = book.getAttribute('category')

    # Получение вложенных тегов
    title = book.getElementsByTagName('title')[0].firstChild.nodeValue
    author = book.getElementsByTagName('author')[0].firstChild.nodeValue

    print(f"ID: {book_id}, Категория: {category}")
    print(f"  Название: {title}")
    print(f"  Автор: {author}")
    print("-" * 20)

# Освобождение памяти
doc.unlink()

from xml.dom.minidom import Document

# 1. Создаем документ

if __name__ == "__main__":

    current_module_dir_ = Path(__file__).resolve().parent
    project_root_ = current_module_dir_.parent
    data_dir_ = project_root_ / "data"
    if not data_dir_.exists():
        data_dir_ = current_module_dir_ / "data"

    filepath_ = data_dir_ / "test.xml"

    doc = Document()

    # 2. Создаем корневой элемент
    root = doc.createElement('catalog')
    doc.appendChild(root)


    for book in self.books:

    # 3. Создаем дочерний элемент
        book_item = doc.createElement('book')
        root.appendChild(book_item)

    # 4. Добавляем атрибут
        book_item.setAttribute('id', '1')

    # 5. Добавляем текстовый узел (имя)
    name = doc.createElement('name')
    name.appendChild(doc.createTextNode('Иван Иванов'))
    employee.appendChild(name)

    # 6. Записываем в файл
    xml_str = doc.toprettyxml(indent="  ")  # Форматирование
    with open(filepath_, "w", encoding="UTF-8") as f:
        f.write(xml_str)

    print("Файл успешно создан: company.xml")

    real_books = [
        # Русская классика
        ('Война и мир', 'Лев Толстой', 'Эксмо', 4, 50000),
        ('Преступление и наказание', 'Фёдор Достоевский', 'АСТ', 1, 30000),
        ('Анна Каренина', 'Лев Толстой', 'Азбука', 2, 25000),
        ('Мастер и Маргарита', 'Михаил Булгаков', 'Эксмо', 1, 100000),
        ('Тихий Дон', 'Михаил Шолохов', 'АСТ', 4, 20000),
        ('Доктор Живаго', 'Борис Пастернак', 'Азбука', 1, 15000),
        ('Отцы и дети', 'Иван Тургенев', 'Просвещение', 1, 50000),
        ('Герой нашего времени', 'Михаил Лермонтов', 'Дрофа', 1, 40000),
        ('Мёртвые души', 'Николай Гоголь', 'Эксмо', 1, 35000),
        ('Евгений Онегин', 'Александр Пушкин', 'Просвещение', 1, 100000)]