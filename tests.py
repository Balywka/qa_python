import pytest
from main import BooksCollector


# класс TestBooksCollector объединяет набор тестов, которыми мы покрываем наше приложение BooksCollector
# обязательно указывать префикс Test
class TestBooksCollector:

    # пример теста:
    # обязательно указывать префикс test_
    # дальше идет название метода, который тестируем add_new_book_
    # затем, что тестируем add_two_books - добавление двух книг
    def test_add_new_book_add_two_books(self):
        # создаем экземпляр (объект) класса BooksCollector
        collector = BooksCollector()

        # добавляем две книги
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')

        # проверяем, что добавилось именно две
        # словарь books_rating, который нам возвращает метод get_books_rating, имеет длину 2
        assert len(collector.get_books_genre()) == 2

    # напиши свои тесты ниже
    # чтобы тесты были независимыми в каждом из них создавай отдельный экземпляр класса BooksCollector()
# 1 Тест: нельзя добавить книгу с пустым названием или длинным названием
# параметризация для 4 данных
    @pytest.mark.parametrize('name, expected_count', [
        ('', 0), #пустое имя — книга не должна добавиться
        ('A' * 41, 0),# 41 символ — слишком длинное имя, не должно добавиться
        ('A' * 40, 1),# 40 символов — должно добавиться
        ('A', 1) # 1 символ — минимальная длина, должно добавиться
    ])
    def test_add_new_book_invalid_name_length(self, collector, name, expected_count):
        collector.add_new_book(name) # книга с именем
        assert len(collector.get_books_genre()) == expected_count # сколько книг 0 или 1


# 2 Тест: нельзя добавить одну и ту же книгу дважды
    def test_add_new_book_duplicate_does_nothing(self, collector):
        collector.add_new_book('1984')
        collector.add_new_book('1984')  # Повторное добавление
        assert len(collector.get_books_genre()) == 1 # одна книга добавилась


# 3 Тест: установка жанра для существующей книги
    def test_set_book_genre_valid_book_and_genre_sets_genre(self, collector):
        collector.add_new_book('Марсианин') # добавляю книгу
        collector.set_book_genre('Марсианин', 'Фантастика') # добавляю жанр
        assert collector.get_book_genre('Марсианин') == 'Фантастика' # Проверяем жанр книги фантастика

# 4 Тест: нельзя установить жанр, которого нет в списке
    def test_set_book_genre_invalid_genre_does_not_set(self, collector):
        collector.add_new_book('Темные тайны') # добавляю книгу
        collector.set_book_genre('Темные тайны', 'Триллер') # жанр которого нет в списке
        assert collector.get_book_genre('Темные тайны') == '' # Проверяем жанр книги пустой

# 5 Тест: нельзя установить жанр несуществующей книге
    def test_set_book_genre_book_not_exist(self, collector):
        collector.set_book_genre('Не добавленная книга', 'Комедии') # книга которой нет
        assert collector.get_book_genre('Не добавленная книга') is None # возвращаем ноне если книги нет

# 6 Тест: получение жанра сущестующей книги
    def test_fet_book_genre_existing_book_returns_genre(self, collector):
        collector.add_new_book('Дюна') # добавляю книгу
        collector.set_book_genre('Дюна', 'Фантастика') # устанавливаю жанр
        assert collector.get_book_genre('Дюна') == 'Фантастика' # возвращение правильного жанра у книги

# 7 Тест: получение жанра несущестующей книги
    def test_get_book_genre_nonexistent_book_returns_none(self, collector):
        assert collector.get_book_genre('Несуществующая книга') is None # если книги нет, возвращаем ноне

# 8 Тест: у новой книги по умолчанию жанр - пустая строка
    def test_get_book_genre_new_book_returns_empty_string(self, collector):
        collector.add_new_book('Новая книга') # книга без жанра
        assert collector.get_book_genre('Новая книга') == '' # жанр пуст

# 9 Тест: получение книги по жанру
    @pytest.mark.parametrize('genre, expected_books', [
        ('Фантастика', ['Дюна', 'Марсианин']),
        ('Комедии', ['Безумные годы']),
        ('Ужасы', []),
    ])
    def test_get_books_with_specific_genre(self, collector, genre, expected_books): # несколько книг
        collector.add_new_book('Дюна')
        collector.add_new_book('Марсианин')
        collector.set_book_genre('Дюна', 'Фантастика')
        collector.add_new_book('Безумные годы')
        collector.set_book_genre('Марсианин', 'Фантастика')
        collector.set_book_genre('Безумные годы', 'Комедии')
        result = collector.get_books_with_specific_genre(genre) # получаю список книг
        assert result == expected_books  # книги добавлены

# 10 Тест: получение словаря книг с жанрами
    def test_get_books_genre_after_adding_book_returns_filled_dict(self, collector):
        collector.add_new_book('Книга') # Добавляю книгу
        collector.set_book_genre('Книга', 'Фантастика') # Устанавливаю жанр
        assert collector.get_books_genre() == {'Книга': 'Фантастика'} # словарь содержит книгу с жанром

# 11 Тест: книги с возрастным рейтингом отсутствуют в списке для детей
    def test_get_books_for_children_excludes_age_restricted(self, collector):
        collector.add_new_book('Призрак в темноте') # добавление 3 книг
        collector.add_new_book('Шерлок Холмс')
        collector.add_new_book('Мультик про кота')

        collector.set_book_genre('Призрак в темноте', 'Ужасы') # назначение жанров
        collector.set_book_genre('Шерлок Холмс', 'Детективы')
        collector.set_book_genre('Мультик про кота', 'Мультфильмы')
        assert collector.get_books_for_children() == ['Мультик про кота']

# 12 Тест: добавление книги в избранное
    def test_add_book_in_favorites(self, collector):
        collector.add_new_book('Гарри Поттер') # добавление книги
        collector.add_book_in_favorites('Гарри Поттер') # в избранное
        assert 'Гарри Поттер' in collector.get_list_of_favorites_books() # книга есть в списке

# 13 Тест: нельзя добавить в избранное несуществующую книгу
    def test_add_book_in_favorites_book_not_exist(self, collector):
        collector.add_book_in_favorites('Несуществующая книга') # книга которой нет
        assert len(collector.get_list_of_favorites_books()) == 0 # список пуст

# 14 Тест: удаление книги из избранного
    def test_delete_book_from_favorites(self, collector):
        collector.add_new_book('Властелин колец') # Добавление книги
        collector.add_book_in_favorites('Властелин колец') # Добавление в избранное
        collector.delete_book_from_favorites('Властелин колец') # Удаление из избранного
        assert 'Властелин колец' not in collector.get_list_of_favorites_books() # книги нет

# 15. Тест: получение списка избранных книг (после добавления)
    def test_get_list_of_favorites_books_after_adding_returns_filled_list(self, collector):
        collector.add_new_book('Люди как боги') # добавляем книгу
        collector.add_book_in_favorites('Люди как боги') # добавляем в избранное
        assert collector.get_list_of_favorites_books() == ['Люди как боги'] # избранное с книгой