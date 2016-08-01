function toggleNotesFormGroup() {
    $('#notes').toggle(200);

    var currentTxt = $('#notesBtn').html();
    var btnTxt = (currentTxt == 'Adicionar notas') ? 'Ocultar' : 'Adicionar notas';
    $('#notesBtn').html(btnTxt);
}

function displayPeriodInterval () {
    var selectedOption = $("select[name='period']").val();
    if(selectedOption === 'custom') {
        $('#periodInterval').show(200);
    } else {
        $('#periodInterval').hide(200);
    }
}

function displayDeleteAlert (id) {
    $('#alertModal a:last-child').attr('href', '/measures/delete/' + id + '?return_path=' + window.location.pathname + window.location.search);
    $('#alertModal').modal();
}
