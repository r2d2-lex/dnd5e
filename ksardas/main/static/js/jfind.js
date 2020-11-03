$(document).ready(function(){
    $('#id_name').on('input', searchspell);
    $('#id_ritual, #id_concentrate').on('change', searchspell);
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
                /* ----- Success ---- */
                console.log(data);
                console.log(data.length);

                let recordsOnPage = 3;
                let countOfItems = Math.ceil(data.length / recordsOnPage);
                $('#pagination').empty();
                let pagination = document.querySelector('#pagination');

                let items = [];
                for (let i=1; i<= countOfItems; i++) {
                    let li = document.createElement('li');
                    li.innerHTML = i;
                    pagination.appendChild(li)
                    items.push(li);
                }
                let li_active;
                showPage(items[0]);

                [].forEach.call(items,function(item) {
                        item.addEventListener('click', function() {
                            showPage(this);
                        });
                });

                function showPage(item) {
                            /* let active = document.querySelector('#pagination li.active');
                            if (active) {
                                active.classList.remove('active');
                            }*/
                            if (li_active) {
                                li_active.classList.remove('active');
                            }
                            //active = this;
                            li_active = item;
                            item.classList.add('active');

                            let pageNum = +item.innerHTML;
                            let start = (pageNum - 1) * recordsOnPage;
                            let end = start + recordsOnPage;
                            let records = data.slice(start, end)
                            console.log(records);

                            $('#id_spells').empty();
                            for (let record in records) {
                                $('#id_spells').append('<div class="row">'+
                                    '<div class="card border-primary mt-5">'+
                                    '<div class="card-header bg-light">'+
                                    '<h4 class="card-title"><a href="/main/accounts/profile/spell/'+records[record].pk+'">'+
                                    records[record].fields.name+'_JS</a></h4>'+
                                    '</div>'+
                                    '<div class="card-body">'+
                                    '<b>Уровень:</b> '+records[record].fields.level+'<br>'+
                                    '<b>Компоненты:</b> '+records[record].fields.components+'<br>'+
                                    '<b>Дистанция:</b> '+records[record].fields.distance+'<br>'+
                                    '<b>Длительность:</b> '+records[record].fields.duration+'<br>'+
                                    '<b>Время чтения:</b> '+records[record].fields.cast_time+'<br>'+
                                    '<b>Описание:</b> '+records[record].fields.description+'<br>'+
                                    '<a class="badge badge-light" href="/main/accounts/profile/spell/'+records[record].pk+'">'+
                                    'Просмотреть заклинание</a><br>'+
                                    '</div></div></div>');
                            }
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