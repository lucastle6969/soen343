$('#book-modal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget) // Button that triggered the modal
    var title = button.data('title') // Extract info from data-* attributes
    var author = button.data('author')
    var format = button.data('format')
    var pages = button.data('pages')
    var publisher = button.data('publisher')
    var language = button.data('language')
    var isbn10 = button.data('isbn10')
    var isbn13 = button.data('isbn13')
    // Update the modal's content. 
    var modal = $(this)
    modal.find('.modal-title').text(title)
    modal.find('.modal-body #book-title').text(title)
    modal.find('.modal-body #book-author').text(author)
    modal.find('.modal-body #book-format').text(format)
    modal.find('.modal-body #book-pages').text(pages)
    modal.find('.modal-body #book-publisher').text(publisher)
    modal.find('.modal-body #book-language').text(language)
    modal.find('.modal-body #book-isbn10').text(isbn10)
    modal.find('.modal-body #book-isbn13').text(isbn13)
  })