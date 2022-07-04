

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

# Импорт данных

Заходим в контейнер и создаем БД в которую будем выполнять импорт данных.

```
docker exec -it mongodb bash
mongo
> use orders
> exit
exit
```