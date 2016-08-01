function validateForm() {
    $("form").parsley({
        excluded: 'input:hidden',
        errorClass: 'has-error',
        classHandler: function (el) {
            return el.$element.closest('.form-group');
        },
        errorsContainer: function(el) {
            return el.$element.closest('.form-group');
        },
        errorsWrapper: "<span class='help-block'></span>",
        errorTemplate: "<span></span>",
    });
}
