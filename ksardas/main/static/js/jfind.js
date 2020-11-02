
$(document).ready(function(){
    $('#id_name').on('input', searchspell);
    $('#id_ritual').on('change', searchspell);
    $('#id_concentrate').on('change', searchspell);
    function searchspell() {
        var rit = $('#id_ritual').prop('checked');
        var con = $('#id_concentrate').prop('checked');
        var name = $('#id_name').val();
        $.ajax({
            method : "GET",
            url: '/main/accounts/profile/get-spells/',
            data: {
                'name': name,
                'ritual': rit,
                'concentrate': con,
            },
            dataType: 'json',
            success: function (data) {
                console.log(data);
                $('#id_spells').empty();
                for (var n in data)
                    $('#id_spells').append('<div class="row">'+
                        '<div class="card border-primary mt-5">'+
                        '<div class="card-header bg-light">'+
                        '<h4 class="card-title"><a href="/main/accounts/profile/spell/'+data[n].pk+'">'+
                        data[n].fields.name+'_JS</a></h4>'+
                        '</div>'+
                        '<div class="card-body">'+
                        '<b>Уровень:</b> '+data[n].fields.level+'<br>'+
                        '<b>Компоненты:</b> '+data[n].fields.components+'<br>'+
                        '<b>Дистанция:</b> '+data[n].fields.distance+'<br>'+
                        '<b>Длительность:</b> '+data[n].fields.duration+'<br>'+
                        '<b>Время чтения:</b> '+data[n].fields.cast_time+'<br>'+
                        '<b>Описание:</b> '+data[n].fields.description+'<br>'+
                        '<a class="badge badge-light" href="/main/accounts/profile/spell/'+data[n].pk+'">'+
                        'Просмотреть заклинание</a><br>'+
                        '</div></div></div>');
            },
            error: function(data){
                 $('#id_spells').empty();
                console.log(data);
            }
        })
    }
})