from model.Catalog import Catalog

catalog = Catalog()

# Tests whether a new book was successfully removed from the working memory
def test_remove_book_working_memory(new_book):
    catalog.insert_item(new_book)
    result = catalog.delete_item(new_book.id)
    assert result == True


# Tests whether a new magazine was successfully removed from the working memory
def test_remove_magazine_working_memory(new_magazine):
    catalog.insert_item(new_magazine)
    result = catalog.delete_item(new_magazine.id)
    assert result == True

# Tests whether a new movie was successfully removed from the working memory
def test_remove_movie_working_memory(new_movie):
    catalog.insert_item(new_movie)
    result = catalog.delete_item(new_movie.id)
    assert result == True

# Tests whether a new music was successfully removed from the working memory
def test_remove_music_working_memory(new_music):
    catalog.insert_item(new_music)
    result = catalog.delete_item(new_music.id)
    assert result == True