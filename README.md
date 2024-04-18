<h2>Для развертывания фреймворка произвести следующие шаги:</h2>
<ul>
<li>
    
    $ git clone https://github.com/2tmirleid/IBotEngine.git

</li>
<li>
    Изменить название файла .env-example на .env
</li>
<li>
    Заменить заглушки в переменных окружениях на значения токена и доступов для СУБД
</li>
</ul>
<p>
    Далее необходимо собрать и запустить сам фреймворк:
</p>

```
$ docker-compose build
```

```
$ docker-compose up -d
```
