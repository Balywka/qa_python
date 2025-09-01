import pytest
from main import BooksCollector

@pytest.fixture()  # создаю фикстуру на добавление объекта, чтоб не писать в каждом тесте.
def collector():
    return BooksCollector()