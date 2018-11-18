/*$('#book-modal').on('show.bs.modal', function (event) {
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
  })*/
function add_to_cart(id){
  if(id.substring(0,9) == "detailed_"){
    id = id.substring(9);
  }
  send_add_to_cart(id.substring(0,2), id.substring(2));
}

function send_add_to_cart(prefix, id){
  $.getJSON("/home/add_to_cart/" + prefix + "/" + id, {}, receive_add_to_cart);
}

function receive_add_to_cart(data){
  button = document.getElementById(data.item_prefix + data.item_id);
  detailed_button = document.getElementById("detailed_" + data.item_prefix + data.item_id);
  switch(data.result){
    case "added":
      button.innerHTML="Added To Cart";
      button.style.backgroundColor = "#4CAF50";
      button.setAttribute("onclick", "");
      detailed_button.innerHTML="Added To Cart";
      detailed_button.style.backgroundColor = "#4CAF50";
      detailed_button.setAttribute("onclick", "");
      break;
    case "unavailable":
      button.innerHTML="Unavailable";
      button.style.backgroundColor = "#888888";
      detailed_button.innerHTML="Unavailable";
      detailed_button.style.backgroundColor = "#888888";
      break;
    case "full":
      button.innerHTML="Cart Full";
      button.style.backgroundColor = "#EE7E3E";
      detailed_button.innerHTML="Cart Full";
      detailed_button.style.backgroundColor = "#EE7E3E";
      break;
  }
}

function receive_remove_from_cart(data){
  if(data.result == true){
    document.getElementById("table_row_" + data.physical_item_prefix + data.physical_item_id).setAttribute("class", "hidden");
  }else{
    document.getElementById("message").innerHTML="Item could not be removed";
  }
}

function send_remove_from_cart(prefix, id){
  $.getJSON("/cart/remove_from_cart/" + prefix + "/" + id, {}, receive_remove_from_cart);
}

function remove_from_cart(id){
  send_remove_from_cart(id.substring(0,2), id.substring(2));
}

function my_redirect_function(location){
  window.location.href=location
}
