function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

function showMessage(message, classAlert) {
    let div = document.createElement('div');
    div.classList.add("alert");
    div.classList.add(classAlert);
    div.setAttribute("role", "alert");
    div.innerHTML = message
    return div
}

function showData(status) {
    if (status > 0) {
        $('#id_status').empty();
        let div = showMessage('Найдено '+status+' заклинаний', 'alert-success');
        $('#id_status').append(div);
    } else {
        $('#id_status').empty();
        let div = showMessage('Найдено '+status+' заклинаний', 'alert-info');
        $('#id_status').append(div);
    }
}

// Функция для обновления заклинаний в карточках
function updateSpells(spells) {
    for (let i = 0; i <= 9; i++) {
        const levelDiv = document.querySelector(`.level${i}`);
        if (levelDiv) {
            levelDiv.innerHTML = '';
        }
    }
    spells.forEach(spell => {
        const levelDiv = document.querySelector(`.level${spell.level}`);
        if (levelDiv) {
            const spellDiv = document.createElement('div');
            spellDiv.className = 'form-check text-nowrap';
            spellDiv.innerHTML = `
                <input type="checkbox" name="char_spells" value="${spell.name}" id="${spell.name}">
                <label class="form-check-label" for="${spell.name}">${spell.name}</label>
            `;
            levelDiv.appendChild(spellDiv);
        }
    });
}


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
            let spell_content = data.spells;
            console.log('Успешный Ajax search_spell');
            console.log(spell_content);

            const $spells = $('#spells');
            $spells.empty();
            $.each(spell_content, function(index, item) {
                $spells.append($('<option></option>').attr('value', item.name).text(item.name + ' (Уровень: ' + item.level + ')'));
            });
            showData(status);
        /* ----- END of Success ---- */
        },
        error: function(data){
            console.log('Ошибка функции!!! Ajax search_spell');
            $('#id_spells').empty();
            console.log(data);
        }
    })
}

function spell_action(action ,spells, character) {
    let url = '/char/'+ character +'/spell/';
    $.ajax({
    type: 'POST',
    url: url,
    data: {
        'action': action,
        'character_name': character,
        'spells': spells,
        'csrfmiddlewaretoken': csrftoken,
    },
    success: function(response) {
        console.log('Success Ajax '+ action +' spell');
        console.log(response.character_spells);
        updateSpells(response.character_spells);
    },
    error: function(xhr, status, error) {
        console.log('Error Ajax '+ action +' spell');
    }
});
}

$(document).ready(function(){
    $('#id_name').on('input', search_spell);
    $('#id_ritual, #id_concentrate, #id_spell_levels, #id_spell_classes, #id_spell_schools').on('change', search_spell);
    search_spell();
    /**/

    let character_name = $('#character_name').val();
    console.log('Character name: ' + character_name);

    $('#add_spell').click(function() {
        let selectedOptions = $('#spells option:selected');
        let selectedValues = [];
        selectedOptions.each(function() {
            selectedValues.push($(this).val());
        });
        spell_action('Add', selectedValues, character_name);
    });
    /**/
    $('#del_spell').click(function() {
        const checkboxes = document.querySelectorAll('input[type="checkbox"][name="char_spells"]');
        const selectedValues = [];
        checkboxes.forEach(checkbox => {
            if (checkbox.checked) {
                selectedValues.push(checkbox.value);
            }
        });
        spell_action('Delete', selectedValues, character_name);
    });

})