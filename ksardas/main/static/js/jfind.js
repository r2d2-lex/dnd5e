$(document).ready(function(){
    $('#id_name').on('input', searchspell);
    $('#id_ritual, #id_concentrate, #id_spell_levels, #id_spell_classes, #id_spell_schools').on('change', searchspell);
    searchspell();
    function searchspell() {
        var rit = $('#id_ritual').prop('checked');
        var con = $('#id_concentrate').val();
        var name = $('#id_name').val();
        var level = $('#id_spell_levels').val();
        var spc = $('#id_spell_classes').val();
        var school = $('#id_spell_schools').val();
        $.ajax({
            method : "GET",
            url: '/main/accounts/profile/get-spells/',
            data: {
                'name': name,
                'ritual': rit,
                'concentrate': con,
                'level': level,
                'spc' : spc,
                'school': school,
            },
            dataType: 'json',
            success: function (data) {
                /* ----- Success ---- */
                let status = data.status;
                let recordsOnPage = 5;
                let tabsOnPage = 5;
                let countOfItems = Math.ceil(data.spells.length / recordsOnPage);
                // countOfItems = 5;
                let tab_active;
                $('#id_spells').empty();
                $('#pagination').empty();
                let pagination = document.querySelector('#pagination');

                let items = [];
                for (let i=1; i<= countOfItems; i++) {
                    let li = createTab(i);
                    $(li).hide();
                    li.addEventListener('click', function() { showPage(this); });
                    items.push(li);
                }
                showData(status);

                function showData(status) {
                    if (status > 0) {
                        $('#id_status').empty();
                        let div = showMessage('Найдено '+status+' записей', 'alert-success');
                        $('#id_status').append(div);
                        tabsNavPrepare();
                        showPage(items[0]);
                    } else {
                        $('#id_status').empty();
                        let div = showMessage('Найдено '+status+' записей', 'alert-info');
                        $('#id_status').append(div);
                        tabsNavPrepare();
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

                function createTab (index) {
                    let elem = document.createElement('li');
                    elem.classList.add("page-item");
                    pagination.appendChild(elem);

                    let link = document.createElement('a');
                    link.classList.add("page-link");
                    link.innerHTML = index;
                    link.href = '#';
                    elem.appendChild(link);
                    return elem;
                }

                function hideAllTabs () {
                    for (let i=0; i<= countOfItems; i++) {
                        $(items[i]).hide();
                    }
                }

                function calculateTabs (tabIndex) {
                    hideAllTabs();
                    if (items.length <= tabsOnPage) {
                        [].forEach.call(items,function(item) {
                                $(item).show();
                        });
                    } else {
                        tabsLR = 2;
                        tabMax = items.length-1;
                        tabToMax = tabMax - tabIndex;
                        tabToMin = 0 + tabIndex;
                        let tabStart = NaN;
                        let tabEnd = NaN;

                        if (tabToMax < 2) { // Индекс в конце списка
                            tabEnd = tabIndex + tabToMax;
                            tabStart = tabIndex - 2 - tabsLR;
                        } else {
                            tabStart = tabIndex - 2;
                            tabEnd = tabIndex + 2;
                        }

                        if (tabToMin < 2) { // Индекс в начале списка
                            tabStart = tabIndex - tabToMin;
                            tabEnd = tabIndex + 2 + tabsLR;
                        } else {
                            tabStart = tabIndex - 2;
                            tabEnd = tabIndex + 2;
                        }

                        console.log('___');
                        console.log('TabStart:', tabStart);
                        console.log('tabIndex:', tabIndex);
                        console.log('TabEnd:', tabEnd);
                        for (let j=tabStart; j<= tabEnd; j++) {
                            $(items[j]).show();
                        }
                    }
                }

                function tabsNavPrepare() {
                    linkAdd('prev', 'Назад');
                    linkAdd('first', '<<');
                    linkAdd('next', 'Вперёд');
                    linkAdd('last', '>>');
                }

                function linkAdd(action, caption) {
                    /*
                     action:
                     prev - страница назад, first - первая страница,
                     next - страница вперёд, last - последняя страница
                     caption - заголовок таба пагинации
                    */
                    let li = createTab(caption);
                    switch (action) {
                        case 'first':
                            pagination.insertBefore(li, pagination.firstElementChild);
                            li.addEventListener('click', function() { showPage(items[0]); });
                        break;

                        case 'prev':
                            pagination.insertBefore(li, pagination.firstElementChild);
                            li.addEventListener('click', function() {
                                let page_number = +tab_active.textContent;
                                // отсчёт в массиве с 0 + -1 страница == -2
                                page_number = page_number - 2;
                                if (page_number <= 0) {
                                    page_number = 0;
                                }
                                showPage(items[page_number]);
                            });
                        break;

                        case 'next':
                            pagination.insertBefore(li, pagination.lastElementChild.nextSibling);
                            li.addEventListener('click', function() {
                                let page_number = +tab_active.textContent;
                                if (page_number >= items.length-1) {
                                    page_number = items.length-1;
                                }
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

                function showPage(item) {
                    let pageNum = +item.childNodes[0].innerHTML;

                    if (tab_active) {
                        tab_active.classList.remove('active');
                        calculateTabs(pageNum-1);
                    } else {
                        calculateTabs(0);
                    }
                    tab_active = item;
                    item.classList.add('active');

                    let start = (pageNum - 1) * recordsOnPage;
                    let end = start + recordsOnPage;
                    let records = data.spells.slice(start, end);

                    $('#id_spells').empty();
                    addRecords(records);

                    // Копируем панель навигации для footer
                    // $('#id_footer').empty();
                    // $('#pagination').clone(true, true).appendTo("#id_footer");
                }

                function addRecords(records) {
                    let reqUrl = '/main/accounts/profile/spell/';
                    for (let record in records) {
                        $('#id_spells').append('<div class="row">'+
                            '<div class="card border-primary mt-5">'+
                            '<div class="card-header bg-light">'+
                            '<h4 class="card-title"><a href="'+reqUrl+records[record].pk+'">'+
                            records[record].name+'</a></h4>'+
                            '</div>'+
                            '<div class="card-body">'+
                            '<b>Уровень:</b> '+records[record].level+'<br>'+
                            '<b>Компоненты:</b> '+records[record].components+'<br>'+
                            '<b>Дистанция:</b> '+records[record].distance+'<br>'+
                            '<b>Длительность:</b> '+records[record].duration+'<br>'+
                            '<b>Время чтения:</b> '+records[record].cast_time+'<br>'+
                            '<b>Описание:</b> '+records[record].description+'<br>'+
                            '<a class="badge badge-light" href="'+reqUrl+records[record].pk+'">'+
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