from xml.dom import minidom
import uuid



def create_book(name, author, publisher, circulation, number_of_volumes, total_volumes):
    book = doc.createElement('book')
    book.setAttribute('id', str(uuid.uuid4())[:8])
    for loc, val in locals().items():
        el=doc.createElement(loc)
        el.appendChild(doc.createTextNode(val))
        book.appendChild(el)


if __name__ == "__main__":
    # 1. Создание нового документа
    doc = minidom.Document()

    # 2. Создание корневого элемента
    root = doc.createElement('catalog')
    doc.appendChild(root)



    # 3. Создание дочернего элемента
    child = doc.createElement('book')
    child.setAttribute('id', '1')
    name=doc.createElement('name')
    name.appendChild(doc.createTextNode('Текстовое содержимое'))
    child.appendChild(name)

    child.appendChild(doc.createTextNode('Текстовое содержимое'))
    root.appendChild(child)
    xml_str = doc.toprettyxml(indent="  ")
    with open("output.xml", "w", encoding="utf-8") as f:
        f.write(xml_str)

