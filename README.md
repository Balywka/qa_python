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
    def test_add_new_book_duplicate_name(self, collector):
        collector.add_new_book('1984')
        collector.add_new_book('1984')  # Повторное добавление
        assert len(collector.get_books_genre()) == 1 # одна книга добавилась

# 3 Тест: установка жанра для существующей книги
    def test_set_book_genre_valid(self, collector):
        collector.add_new_book('Марсианин') # добавляю книгу
        collector.set_book_genre('Марсианин', 'Фантастика') # добавляю жанр
        assert collector.get_book_genre('Марсианин') == 'Фантастика' # Проверяем жанр книги фантастика

# 4 Тест: нельзя установить жанр, которого нет в списке
    def test_set_book_genre_invalid_genre(self, collector):
        collector.add_new_book('Темные тайны') # добавляю книгу
        collector.set_book_genre('Темные тайны', 'Триллер') # жанр которого нет в списке
        assert collector.get_book_genre('Темные тайны') == '' # Проверяем жанр книги пустой

# 5 Тест: нельзя установить жанр несуществующей книге
    def test_set_book_genre_book_not_exist(self, collector):
        collector.set_book_genre('Не добавленная книга', 'Комедии') # книга которой нет
        assert collector.get_book_genre('Не добавленная книга') is None # возвращаем ноне если книги нет

# 6 Тест: получение книг по жанру параметризация для теста разных жанров
    @pytest.mark.parametrize('genre, expected_books', [
        ('Фантастика', ['Дюна', 'Марсианин']),
        ('Комедии', ['Безумные годы']),
        ('Ужасы', []),
        ])

    def test_get_books_with_specific_genre(self, collector, genre, expected_books): # несколько книг
        collector.add_new_book('Дюна')
        collector.add_new_book('Марсианин')
        collector.add_new_book('Безумные годы')
        collector.set_book_genre('Дюна', 'Фантастика')
        collector.set_book_genre('Марсианин', 'Фантастика')
        collector.set_book_genre('Безумные годы', 'Комедии')

        result = collector.get_books_with_specific_genre(genre) # получаю список книг
        assert result == expected_books  # книги добавлены

# 7 Тест: книги с возрастным рейтингом отсутствуют в списке для детей
    def test_get_books_for_children_excludes_age_restricted(self, collector):
        collector.add_new_book('Призрак в темноте') # добавление 3 книг
        collector.add_new_book('Шерлок Холмс')
        collector.add_new_book('Мультик про кота')

        collector.set_book_genre('Призрак в темноте', 'Ужасы') # назначение жанров
        collector.set_book_genre('Шерлок Холмс', 'Детективы')
        collector.set_book_genre('Мультик про кота', 'Мультфильмы')

        children_books = collector.get_books_for_children() # список книг для детей
        assert children_books == ['Мультик про кота'] # одна книга попадает

# 8 Тест: добавление книги в избранное
    def test_add_book_in_favorites(self, collector):
        collector.add_new_book('Гарри Поттер') # добавление книги
        collector.add_book_in_favorites('Гарри Поттер') # в избранное
        assert 'Гарри Поттер' in collector.get_list_of_favorites_books() # книга есть в списке

# 9 Тест: нельзя добавить в избранное несуществующую книгу
    def test_add_book_in_favorites_book_not_exist(self, collector):
        collector.add_book_in_favorites('Несуществующая книга') # книга которой нет
        assert len(collector.get_list_of_favorites_books()) == 0 # список пуст

# 10 Тест: удаление книги из избранного
    def test_delete_book_from_favorites(self, collector):
        collector.add_new_book('Властелин колец') # Добавление книги
        collector.add_book_in_favorites('Властелин колец') # Добавление в избранное
        collector.delete_book_from_favorites('Властелин колец') # Удаление из избранного
        assert 'Властелин колец' not in collector.get_list_of_favorites_books() # книги нет
