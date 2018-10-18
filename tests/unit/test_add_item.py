from model.Catalog import Catalog

catalog = Catalog()

# Tests whether a new book was successfully added to the working memory
def test_add_book_working_memory(new_book_form):
    result = catalog.add_item("Book", new_book_form)
    assert result == True

# Tests whether a new magazine was successfully added to the working memory
def test_add_magazine_working_memory(new_magazine_form):
    result = catalog.add_item("Magazine", new_magazine_form)
    assert result == True

# Tests whether a new movie was successfully added to the working memory
def test_add_movie_working_memory(new_movie_form):
    result = catalog.add_item("Movie", new_movie_form)
    assert result == True

# Tests whether a new movie was successfully added to the working memory
def test_add_music_working_memory(new_music_form):
    result = catalog.add_item("Music", new_music_form)
    assert result == True