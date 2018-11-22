$(function() {
    var button = $('#submit');
    button.attr('class', 'form-control btn btn-primary float-right disabled')
    button.attr('disabled', 'disabled')
    $('.checkboxes').change(function(e) {
        if ($('.checkboxes:checked').length) {
            button.attr('class', 'form-control btn btn-primary float-right active')
            button.removeAttr('disabled')
        } else {
            button.attr('class', 'form-control btn btn-primary float-right disabled')
            button.attr('disabled', 'disabled')
        }
    });
});