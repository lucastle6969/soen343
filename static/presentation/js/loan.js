$(function() {
    var button = $('#submit');
    button.attr('class', 'form-control btn btn-primary float-right disabled')
    button.attr('disabled', 'disabled')
    $('.return').change(function(e) {
        if ($('.return:checked').length) {
            button.attr('class', 'form-control btn btn-primary float-right active')
            button.removeAttr('disabled')
        } else {
            //$('#sub').attr('disabled', 'disabled');
            button.attr('class', 'form-control btn btn-primary float-right disabled')
            button.attr('disabled', 'disabled')
        }
    });
});