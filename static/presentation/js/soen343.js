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
      button.innerHTML="Added To Cart <img src='/static/presentation/img/in_cart.png'>";
      button.style.backgroundColor = "#4CAF50";
      button.setAttribute("onclick", "");
      button.setAttribute("onmouseover", "display_add_to_cart(this.id)");
      detailed_button.innerHTML="Added To Cart <img src='/static/presentation/img/in_cart.png'>";
      detailed_button.style.backgroundColor = "#4CAF50";
      detailed_button.setAttribute("onclick", "");
      detailed_button.setAttribute("onmouseover", "display_add_to_cart(this.id)");
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
  if(data.result == "True"){
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

function display_add_to_cart(id){
  button = document.getElementById(id);
  button.innerHTML="Add To Cart <img src='/static/presentation/img/in_cart.png'>";
  button.style.backgroundColor = "#0062cc";
  button.setAttribute("onclick", "add_to_cart(this.id)");
}