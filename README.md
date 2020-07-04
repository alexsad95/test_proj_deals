
# test_proj_deals

Тестовое задание по Django. [ТЗ](https://github.com/alexsad95/test_proj_deals/blob/master/files/ТЗ.png)
Как запустить приложение.
 - Склонировать репозиторий, перейти в папку с приложением
 - Сделать сборку через docker-compose build
 - Запустить docker-compose up
 - Запустить init_db.sh в контейнере docker

```sh
$ git clone https://github.com/alexsad95/test_proj_deals
$ cd test_proj_deals/test_deals
$ docker-compose build
$ docker-compose up -d 
$ docker-compose run web sh init_db.sh
```

Отправка POST запроса с файлом csv для загрузки данных в бд, можно это сделать с помощью Postman: 

![](https://github.com/alexsad95/test_proj_deals/blob/master/files/POST.png)

После можно проверить и зайти на `localhost:8000/api/deals`:

![](https://github.com/alexsad95/test_proj_deals/blob/master/files/GET.png)

