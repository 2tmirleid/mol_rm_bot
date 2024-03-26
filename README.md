<h2>Для развертывания сборки произвести следующие шаги:</h2>
<ul>
<li>
    
    $ git clone https://github.com/2tmirleid/aiogram_2tmirleid.git

</li>
<li>
    Изменить название файла .env-example на .env
</li>
<li>
    Заменить заглушки в переменных окружениях на значения токена и доступов для СУБД
</li>
</ul>
<p>
    Далее необходимо собрать и запустить саму сборку:
</p>

```
$ docker-compose build
```

```
$ docker-compose up -d
```
