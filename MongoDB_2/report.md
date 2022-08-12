# MongoDB 2

# Настройка replica-set

Создаём каталоги для всех будущих реплика-сетов
```bash
$ mkdir /tmp/data
$ cd /tmp/data
$ mkdir cfg1 cfg2 cfg3 rs11 rs12 rs13 rs21 rs22 rs23 rs31 rs32 rs33
```

Создаём keyfile, который будет использоваться всеми монгами
```bash
$ openssl rand -base64 756 > /tmp/data/keyfile.f
$ chmod 400 /tmp/data/keyfile.f
```

Запускаем config-server'а, формируем replica-set cfg, создаём пользователя-администратора с максимальными привилегиями (роль root)
```bash
$ mongod --configsvr --dbpath /tmp/data/cfg1 --port 26001 --replSet rsCfg --fork --logpath /tmp/data/cfg1.log 
$ mongod --configsvr --dbpath /tmp/data/cfg2 --port 26002 --replSet rsCfg --fork --logpath /tmp/data/cfg2.log 
$ mongod --configsvr --dbpath /tmp/data/cfg3 --port 26003 --replSet rsCfg --fork --logpath /tmp/data/cfg3.log 
```

```
mongosh --port 26001

rs.initiate(
    {
    "_id" : "rsCfg", 
    configsvr: true, 
    members : 
        [
        {"_id" : 0, host : "127.0.0.1:26001"},
        {"_id" : 1, host : "127.0.0.1:26002"},
        {"_id" : 2, host : "127.0.0.1:26003"}
        ]
    }
);

use admin;

db.createUser(
  {
    user: "adm",
    pwd: "1", 
    roles: [ { role: "root", db: "admin" } ]
  }
)

```

Запускаю три реплика-сета, которые будут шардами, создаю такого же пользователя-администратора

```
$ mongod --dbpath /tmp/data/rs11 --port 27101 --replSet rs1 --fork --logpath /tmp/data/rs11.log 
$ mongod --dbpath /tmp/data/rs12 --port 27102 --replSet rs1 --fork --logpath /tmp/data/rs12.log 
$ mongod --dbpath /tmp/data/rs13 --port 27103 --replSet rs1 --fork --logpath /tmp/data/rs13.log
```

```
$ mongosh --port 26001
```

```
rs.initiate(
    {
    "_id" : "rs2", 
    members : 
        [
        {"_id" : 0, host : "127.0.0.1:27201"},
        {"_id" : 1, host : "127.0.0.1:27202"},
        {"_id" : 2, host : "127.0.0.1:27203"}
        ]
    }
);

use admin;

db.createUser(
    {
    user: "adm",
    pwd: "1", 
    roles: [ { role: "root", db: "admin" } ]
    }
)
```

```
$ mongod --dbpath /tmp/data/rs31 --port 27301 --replSet rs3 --fork --logpath /tmp/data/rs31.log 
$ mongod --dbpath /tmp/data/rs32 --port 27302 --replSet rs3 --fork --logpath /tmp/data/rs32.log 
$ mongod --dbpath /tmp/data/rs33 --port 27303 --replSet rs3 --fork --logpath /tmp/data/rs33.log 


```

```
mongosh --port 27301

```

```
rs.initiate(
    {
    "_id" : "rs3", 
    members : 
        [
        {"_id" : 0, host : "127.0.0.1:27301"},
        {"_id" : 1, host : "127.0.0.1:27302"},
        {"_id" : 2, host : "127.0.0.1:27303"}
        ]
    }
);

use admin;

db.createUser(
    {
    user: "adm",
    pwd: "1", 
    roles: [ { role: "root", db: "admin" } ]
    }
)
```

Убиваю все запущенные экземпляры с помощью kill и запускаю заново с ключами --auth и --keyFile /tmp/data/keyFile.f, указываю, что они запущены в качестве шард-серверов ключом --shardsvr

