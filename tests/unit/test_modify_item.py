from model.Catalog import Catalog

catalog = Catalog()


# Tests whether a new book was successfully modified from the working memory
def test_modify_book_working_memory(new_book):
    catalog.add_item(new_book)

    new_title = "Till Human Voices Wake Us"
    new_book.title = new_title
    catalog.edit_items([new_book])

    book = catalog.get_item_by_id(new_book.prefix, new_book.id)

    assert book.title == new_title
    catalog.delete_items([book])


# Tests whether a new magazine was successfully modified from the working memory
def test_modify_magazine_working_memory(new_magazine):
    catalog.add_item(new_magazine)

    new_title = "Night Flight"
    new_magazine.title = new_title
    catalog.edit_items([new_magazine])

    magazine = catalog.get_item_by_id(new_magazine.prefix, new_magazine.id)

    assert magazine.title == new_title
    catalog.delete_items([magazine])


# Tests whether a new movie was successfully modified from the working memory
def test_modify_movie_working_memory(new_movie):
    catalog.add_item(new_movie)

    new_title = "Rosewood Lane"
    new_movie.title = new_title
    catalog.edit_items([new_movie])

    movie = catalog.get_item_by_id(new_movie.prefix, new_movie.id)

    assert movie.title == new_title
    catalog.delete_items([movie])


# Tests whether a new music was successfully modified from the working memory
def test_modify_music_working_memory(new_music):
    catalog.add_item(new_music)

    new_title = "Marathon Man"
    new_music.title = new_title
    catalog.edit_items([new_music])

    music = catalog.get_item_by_id(new_music.prefix, new_music.id)

    assert music.title == new_title
    catalog.delete_items([music])
