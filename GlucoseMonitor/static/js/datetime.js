function datetimePickerBehaviour () {
    $('.datetimepicker').datetimepicker({
        locale: 'pt-br',
        maxDate: new Date(),
    });

    // Liked pickers
    $('.datetimepicker_linked:first').datetimepicker({
        locale: 'pt-br',
        maxDate: new Date(),
    });
    $('.datetimepicker_linked:last').datetimepicker({
        locale: 'pt-br',
        maxDate: new Date(),
        useCurrent: false,
    });
    $(".datetimepicker_linked:first").on("dp.change", function (e) {
        $(".datetimepicker_linked:last").data("DateTimePicker").minDate(e.date);
    });
    $(".datetimepicker_linked:last").on("dp.change", function (e) {
        $(".datetimepicker_linked:first").data("DateTimePicker").maxDate(e.date);
    });
}
