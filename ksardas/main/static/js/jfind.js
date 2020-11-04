$(document).ready(function(){
    $('#id_name').on('input', searchspell);
    $('#id_ritual, #id_concentrate').on('change', searchspell);
    searchspell();
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
                countOfItems = 5;
                $('#pagination').empty();
                let pagination = document.querySelector('#pagination');

                let items = [];
                for (let i=1; i<= countOfItems; i++) {
                    let li = document.createElement('li');
                    li.classList.add("page-item");
                    pagination.appendChild(li);

                    let link = document.createElement('a');
                    link.classList.add("page-link");
                    link.innerHTML = i;
                    link.href = '#';
                    li.appendChild(link);

                    items.push(link);
                }
                liNavPrepare();
                let li_active;
                showPage(items[0]);

                [].forEach.call(items,function(item) {
                        item.addEventListener('click', function() {
                            showPage(this);
                        });
                });

                function liNavPrepare() {
                    linkAdd('prev', 'Назад');
                    linkAdd('first', '<<');
                    linkAdd('next', 'Вперёд');
                    linkAdd('last', '>>');
                }

                function linkAdd(action, caption) {
                    let li = document.createElement('li');
                    li.classList.add("page-item");

                    let link = document.createElement('a');
                    link.classList.add("page-link");
                    link.innerHTML = caption;
                    link.href = '#';
                    li.appendChild(link);

                    switch (action) {
                        case 'first':
                            pagination.insertBefore(li, pagination.firstElementChild);
                            li.addEventListener('click', function() {
                                showPage(items[0]);
                            });
                        break;

                        case 'prev':
                            pagination.insertBefore(li, pagination.firstElementChild);
                            li.addEventListener('click', function() {
                                let li_active = document.querySelector('#pagination li.active');
                                let page_number = +li_active.textContent;
                                // отсчёт в массиве с 0 + -1 страница == -2
                                page_number = page_number - 2;
                                if (page_number <= 0) {
                                    page_number = 0;
                                }
                                console.log(page_number);
                                showPage(items[page_number]);
                            });
                        break;

                        case 'next':
                            pagination.insertBefore(li, pagination.lastElementChild.nextSibling);
                            li.addEventListener('click', function() {
                                let li_active = document.querySelector('#pagination li.active');
                                let page_number = +li_active.textContent;
                                if (page_number >= items.length-1) {
                                    page_number = items.length-1;
                                }
                                console.log(page_number);
                                showPage(items[page_number]);
                            });
                        break;

                        case 'last':
                            pagination.insertBefore(li, pagination.lastElementChild.nextSibling);
                            li.addEventListener('click', function() {
                                showPage(items[items.length-1]);
                            });
                        break;
                    }
                }

                function showHide(elem) {
                    $(elem).hide();
                }

                function showPage(item) {
                            if (li_active) {
                                li_active.parentNode.classList.remove('active');
                            }
                            li_active = item;
                            item.parentNode.classList.add('active');

                            let pageNum = +item.innerHTML;
                            let start = (pageNum - 1) * recordsOnPage;
                            let end = start + recordsOnPage;
                            let records = data.slice(start, end)
                            console.log(records);

                            $('#id_spells').empty();
                            addRecords(records);
                }

                function addRecords(records) {
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