$(document).ready(function(){
    $('#id_name').on('input', search_spell);
    $('#id_ritual, #id_concentrate, #id_spell_levels, #id_spell_classes, #id_spell_schools').on('change', search_spell);
    search_spell();
    function search_spell() {
        var ritual = $('#id_ritual').prop('checked');
        var concentrate = $('#id_concentrate').val();
        var name = $('#id_name').val();
        var level = $('#id_spell_levels').val();
        var spc = $('#id_spell_classes').val();
        var school = $('#id_spell_schools').val();
        $.ajax({
            method : "GET",
            url: '/main/accounts/profile/get-spells/',
            data: {
                'name': name,
                'ritual': ritual,
                'concentrate': concentrate,
                'level': level,
                'spc' : spc,
                'school': school,
            },
            dataType: 'json',
            success: function (data) {
                /* ----- Success ---- */
                let status = data.status;
                let spell_cont = data.spells;
                console.log(spell_cont);
                $('#spells').empty();
                showData(status);

                function showData(status) {
                    if (status > 0) {
                        $('#id_status').empty();
                        let div = showMessage('Найдено '+status+' заклинаний', 'alert-success');
                        $('#id_status').append(div);
                    } else {
                        $('#id_status').empty();
                        let div = showMessage('Найдено '+status+' заклинаний', 'alert-info');
                    }
                }

                function showMessage(message, classAlert) {
                    let div = document.createElement('div');
                    div.classList.add("alert");
                    div.classList.add(classAlert);
                    div.setAttribute("role", "alert");
                    div.innerHTML = message
                    return div
                }
            /* ----- END of Success ---- */
            },
            error: function(data){
                $('#id_spells').empty();
                console.log(data);
            }
        })
    }
})