
$(document).ready(function(){
    $('#id_name').on('input', searchspell);
    function searchspell() {
        var fspells = $('#id_name').val();
        $.ajax({
            method : "GET",
            url: '/main/accounts/profile/find-spells/',
            data: {
                'fspells': fspells
            },
            dataType: 'json',
            success: function (data) {
                console.log(data);
                $('#id_spells').empty();
                for (var n in data)
                    $('#id_spells').append('<div class="row">'+
                        '<div class="card border-primary mt-5">'+
                        '<div class="card-header bg-light">'+
                        '<h4 class="card-title"><a href="/main/accounts/profile/edit-spell/'+data[n].pk+'">'+
                        data[n].fields.name+'_JS</a></h4>'+
                        '</div>'+
                        '<div class="card-body">'+
                        '<b>Уровень:</b> '+data[n].fields.level+'<br>'+
                        '<b>Компоненты:</b> '+data[n].fields.components+'<br>'+
                        '<b>Дистанция:</b> '+data[n].fields.distance+'<br>'+
                        '<b>Длительность:</b> '+data[n].fields.duration+'<br>'+
                        '<b>Время чтения:</b> '+data[n].fields.cast_time+'<br>'+
                        '<b>Описание:</b> '+data[n].fields.description+'<br>'+
                        '<a class="badge badge-light" href="/main/accounts/profile/edit-spell/'+data[n].pk+'">'+
                        'Редактировать заклинание</a><br>'+
                        '</div></div></div>');
            },
            error: function(data){
                 $('#id_spells').empty();
                console.log(data);
            }
        })
    }
})