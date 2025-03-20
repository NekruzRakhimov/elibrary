import db


def print_menu():
    print("Выберите нужную команду:")
    print("0. Выход")
    print("1. Показать список книг")
    print("2. Показать список авторов")
    print("3. Показать список жанров")
    print("4. Показать детальную информацию по id книги (автор и жанры)")
    print("5. Добавить автора")


def app():
    db.init_db()
    print("Таблицы успешно созданы!")

    print("Вас приветствует, Онлайн Библиотека!")
    while True:
        print_menu()
        cmd = int(input("Введите номер команды: "))

        if cmd == 0:
            print("До скорой встречи!)")
            break
        elif cmd == 1:
            print("=" * 20)
            print("Список книг:")
            books = db.get_all_books()
            for book in books:
                print(f"ID: {book[0]} - Название: {book[1]}.")
            print("=" * 20)
        elif cmd == 2:
            print("=" * 20)
            print("Список авторов:")
            authors = db.get_all_authors()
            for author in authors:
                print(f"ID: {author[0]} - ФИО: {author[1]}.")
            print("=" * 20)
        elif cmd == 3:
            print("=" * 20)
            print("Список жанров:")
            genres = db.get_all_genres()
            for genre in genres:
                print(f"ID: {genre[0]} - Название: {genre[1]}.")
            print("=" * 20)
        elif cmd == 4:
            print("=" * 20)
            book_id = int(input("Введите ID книгу информацию о которой хотите получить: "))
            book_details = db.get_book_full_info_by_id(book_id)
            if book_details is None:
                print("Нет такой книги!")
            else:
                book_info = book_details["book_info"]
                print(f'ID: {book_info[0]} - Название: {book_info[1]}')

                genres = book_details["genres"]
                print("Жанры:")
                for genre in genres:
                    print(genre[0], end=" | ")

                authors = book_details["authors"]
                print("\nАвторы:")
                for author in authors:
                    print(author[0], end=" | ")
                print()

            print("=" * 20)
        elif cmd == 5:
            print("=" * 20)
            print("Добавление нового автора:")
            full_name = input("Введи ФИО автора: ")
            try:
                db.create_author(full_name)
                print("Автор успешно создан!")
            except Exception as e:
                print(f"Что-то пошло не так! {e}")
            print("=" * 20)
        else:
            print("Вы ввели несуществующею команду. Попробуйте еще раз!")


app()
