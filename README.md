# DnD5E
=======
'DnD5E - проект' предназначен для помощи по игре в системе Dungeon and Dragons (Версии: 5e) 
Доступны возможности: создания, кастомизации персонажей, 
получения информации по заклинаниям, регистрация пользователей. 
Проект написан на фреймворке Django.
 
### Установка:
______
1. Создайте виртуальное окружение и активируйте его
2. Установите необходимые зависимости:


    pip install -r requirements.txt
    
3. Установите Redis (Необходим для Celery)



    #apt install redis

### Список файлов:
______
* **requirements.txt** - список требуемых библиотек для работы со скриптом pdf_to_html
* **xardas/classes_for_spells.py** - Программа парсит файл '**data/char_spells.html**' полученный скриптом pdf_to_html.py
и заносит соответствие классов к заклинаниям в БД SQLite
* **xardas/settings.py** - Программа с настройками проекта

* **data/spells.html** - Страницы заклинаний из книги игрока
* **data/char_spells.html** - Список доступных заклинаний для каждого класса персонажа


### Настройка
______


### Занесение заклинаний в БД:
______

    shell:./xardas/$ ./mange.py import_html_spells data/spells.html
    
### Добавление соответствий классов персонажа к заклинаниям:
______
Укажите путь до директории с приложением:
```python
    KSA_PATH = '/%Full_Path_To_Project_Dir%/xardas/'
```

Выполните:

    shell:./xardas/xardas$ ./classes_for_spells.py ../data/char_spells.html
    
### Запуск приложения в контейнере Docker

    1. Установите Docker и Docker-compose
    2. Установите переменные окружения в файле docker-compose.yml:
      - DJ_DEFAULT_FROM_EMAIL=webmaster@hostname
      - DJ_EMAIL_HOST_USER=User
      - DJ_EMAIL_HOST_PASSWORD=Password
      - DJANGO_SECRET_KEY=ENTER_YOUR_KEY
      - REDIS_HOST=REDIS_HOST
    3. Войдите в директорию проекта и выполните:
        $ sudo docker-compose build
        $ sudo docker-compose up
    4. Подключитесть через браузер на:
        http://localhost:8080 или http://localhost:8080/admin
