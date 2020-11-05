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

<link rel="stylesheet" type="text/css" href="{% static 'main/pagination.css' %}">



    <div class="container">
        <div class="row">
            <div class="form-group col-md-4">
                <label for="charclasses">Выберите класс персонажа:</label>
                <select multiple class="form-control" id="charclasses" size="12">
                {% for charclass1, charclass2 in charclasses %}
                    <option>{{ charclass1 }}</option>
                {% endfor %}
                </select>
            </div>
            <div class="form-group col-md-4">
                <label for="spell_levels">Выберите уровень заклинания:</label>
                <select multiple class="form-control" id="spell_levels" size="10">
                {% for level in spell_levels %}
                    <option>{{ level }}</option>
                {% endfor %}
                </select>
            </div>
        </div>
    </div>