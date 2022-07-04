

# Конфигурация сервера

![mermaid-diagram-1](./images/host.png)


# Запуск MongoDB

```yaml
version: "3"
services:
  mongo:
    image: mongo:4.2.21-bionic
    container_name: mongodb
    volumes:
      - ~/data/mongodb/db:/data/db
    ports:
      - "27017:27017"
```

```
docker-compose -f mongodbotus/docker-compose.yml 
```

# Подготовка набора данных *employees.json* для тестирования c помощью скрипта

Количество записей : 1 000 000 


```bash 
$ python3 generator_data.py
```
code: [Python скрипт для генерации данных](./geneartor_data.py)

Результат

```
root@vps-139128:~/mongodb# python3 generator_data.py 
Введите количество записей:1000000
Файл создан.

-rw-r--r-- 1 root root 125053139 Jul  4 16:15 employees.json

```


# Импорт данных

Заходим в контейнер и создаем БД в которую будем выполнять импорт данных.

```
docker exec -it mongodb bash
mongo
> use employees
> exit
exit
```


Копируем employees внутрь контейнера

```
docker cp employees.json mongodb:/
docker exec -it mongodb bash
mongoimport --db hw --collection employees --drop --jsonArray --file /employees.json
```

Результат
```
2022-07-04T13:31:31.283+0000	connected to: mongodb://localhost/
2022-07-04T13:31:31.284+0000	dropping: hw.employees
2022-07-04T13:31:34.283+0000	[#.......................] hw.employees	9.78MB/119MB (8.2%)
2022-07-04T13:31:37.283+0000	[#####...................] hw.employees	25.9MB/119MB (21.7%)
2022-07-04T13:31:40.283+0000	[########................] hw.employees	42.4MB/119MB (35.6%)
2022-07-04T13:31:43.283+0000	[###########.............] hw.employees	59.6MB/119MB (50.0%)
2022-07-04T13:31:46.283+0000	[###############.........] hw.employees	76.5MB/119MB (64.1%)
2022-07-04T13:31:49.283+0000	[##################......] hw.employees	93.5MB/119MB (78.4%)
2022-07-04T13:31:52.284+0000	[######################..] hw.employees	110MB/119MB (92.6%)
2022-07-04T13:31:54.056+0000	[########################] hw.employees	119MB/119MB (100.0%)
2022-07-04T13:31:54.057+0000	1000000 document(s) imported successfully. 0 document(s) failed to import.

```


Выполняем поиск 5 значений с "age" > 90  

```
mongo hw
> db.employees.find({ "age": {$gte: 90}}).limit(5)



```