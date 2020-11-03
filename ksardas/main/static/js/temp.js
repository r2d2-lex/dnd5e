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


{% for spell in spells %}
    <div class="row">
        {% include 'main/spell_content.html' %}
    </div>
{% endfor %}
