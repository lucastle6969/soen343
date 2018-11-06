// The following replaces the dropdown menu text with the text of the selected item
// It is used in the home page for the dropdown to select search filter
$("a.dropdown-item").click(function(){
  var selText = $(this).text();
  $(this).parents('.btn-group').find('.dropdown-toggle').html(selText+' <span class="caret"></span>');
});