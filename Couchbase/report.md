# Couchbase

## Разворачиваем кластер Couchbase 


Запустите сервер:
```bash
docker run -d --name db -p 8091-8093:8091-8093 -p 11210:11210 couchbase
```

Просмотр логов:

```
docker logs db

Starting Couchbase Server -- Web UI available at http://<ip>:8091
and logs available in /opt/couchbase/var/lib/couchbase/logs
```

Логи показывают, что консоль Couchbase доступна по адресу http://83.166.241.71:8091. Имя пользователя по умолчанию — Administrator, а пароль — password.

## Настроить контейнер Couchbase Docker

Настройка памяти для службы данных и индексов

```bash
curl -v -X POST http://83.166.241.71:8091/pools/default -d memoryQuota=300 -d indexMemoryQuota=300
```

```
*   Trying 83.166.241.71:8091...
* Connected to 83.166.241.71 (83.166.241.71) port 8091 (#0)
> POST /pools/default HTTP/1.1
> Host: 83.166.241.71:8091
> User-Agent: curl/7.79.1
> Accept: */*
> Content-Length: 36
> Content-Type: application/x-www-form-urlencoded
> 
* Mark bundle as not supporting multiuse
< HTTP/1.1 200 OK
< Cache-Control: no-cache,no-store,must-revalidate
< Content-Length: 0
< Date: Sun, 14 Aug 2022 19:12:54 GMT
< Expires: Thu, 01 Jan 1970 00:00:00 GMT
< Pragma: no-cache
< Server: Couchbase Server
< X-Content-Type-Options: nosniff
< X-Frame-Options: DENY
< X-Permitted-Cross-Domain-Policies: none
< X-XSS-Protection: 1; mode=block
< 
* Connection #0 to host 83.166.241.71 left intact
```

Настройка служб данных, запросов и индексов

```
curl -v http://83.166.241.71:8091/node/controller/setupServices -d 'services=kv%2Cn1ql%2Cindex'
```

```
*   Trying 83.166.241.71:8091...
* Connected to 83.166.241.71 (83.166.241.71) port 8091 (#0)
> POST /node/controller/setupServices HTTP/1.1
> Host: 83.166.241.71:8091
> User-Agent: curl/7.79.1
> Accept: */*
> Content-Length: 26
> Content-Type: application/x-www-form-urlencoded
> 
* Mark bundle as not supporting multiuse
< HTTP/1.1 200 OK
< Cache-Control: no-cache,no-store,must-revalidate
< Content-Length: 0
< Date: Sun, 14 Aug 2022 19:16:35 GMT
< Expires: Thu, 01 Jan 1970 00:00:00 GMT
< Pragma: no-cache
< Server: Couchbase Server
< X-Content-Type-Options: nosniff
< X-Frame-Options: DENY
< X-Permitted-Cross-Domain-Policies: none
< X-XSS-Protection: 1; mode=block
< 
* Connection #0 to host 83.166.241.71 left intact
```

## Настройка учетных данных для сервера Couchbase

```
curl -v -X POST  http://83.166.241.71:8091/settings/web -d port=8091 -d username=Admin -d password=Admin123
```

```
*   Trying 83.166.241.71:8091...
* Connected to 83.166.241.71 (83.166.241.71) port 8091 (#0)
> POST /settings/web HTTP/1.1
> Host: 83.166.241.71:8091
> User-Agent: curl/7.79.1
> Accept: */*
> Content-Length: 42
> Content-Type: application/x-www-form-urlencoded
> 
* Mark bundle as not supporting multiuse
< HTTP/1.1 200 OK
< Cache-Control: no-cache,no-store,must-revalidate
< Content-Length: 43
< Content-Type: application/json
< Date: Sun, 14 Aug 2022 19:18:39 GMT
< Expires: Thu, 01 Jan 1970 00:00:00 GMT
< Pragma: no-cache
< Server: Couchbase Server
< X-Content-Type-Options: nosniff
< X-Frame-Options: DENY
< X-Permitted-Cross-Domain-Policies: none
< X-XSS-Protection: 1; mode=block
< 
* Connection #0 to host 83.166.241.71 left intact
{"newBaseUri":"http://83.166.241.71:8091/"}%  
``` 

## Наполним небольшими тестовыми данными

```
curl -v -u Admin:Admin123 -X POST http://83.166.241.71:8091/sampleBuckets/install -d '["travel-sample"]'
```

```
*   Trying 83.166.241.71:8091...
* Connected to 83.166.241.71 (83.166.241.71) port 8091 (#0)
* Server auth using Basic with user 'Admin'
> POST /sampleBuckets/install HTTP/1.1
> Host: 83.166.241.71:8091
> Authorization: Basic QWRtaW46QWRtaW4xMjM=
> User-Agent: curl/7.79.1
> Accept: */*
> Content-Length: 17
> Content-Type: application/x-www-form-urlencoded
> 
* Mark bundle as not supporting multiuse
< HTTP/1.1 202 Accepted
< Cache-Control: no-cache,no-store,must-revalidate
< Content-Length: 2
< Content-Type: application/json
< Date: Sun, 14 Aug 2022 19:33:10 GMT
< Expires: Thu, 01 Jan 1970 00:00:00 GMT
< Pragma: no-cache
< Server: Couchbase Server
< X-Content-Type-Options: nosniff
< X-Frame-Options: DENY
< X-Permitted-Cross-Domain-Policies: none
< X-XSS-Protection: 1; mode=block
< 
* Connection #0 to host 83.166.241.71 left intact
[]%  
```

## Запрос Couchbase с помощью CBQ

Запустим инструмент CBQ:

```
docker run -it --link db:db couchbase cbq --engine http://db:8093
```
```
cbq> select * from `travel-sample` limit 1;
{
    "requestID": "5c4a97cb-2fe3-48b5-8136-3a8de67601ec",
    "errors": [
        {
            "code": 4000,
            "msg": "No index available on keyspace `default`:`travel-sample` that matches your query. Use CREATE PRIMARY INDEX ON `default`:`travel-sample` to create a primary index, or check that your expected index is online."
        }
    ],
    "status": "fatal",
    "metrics": {
        "elapsedTime": "3.267553ms",
        "executionTime": "3.048505ms",
        "resultCount": 0,
        "resultSize": 0,
        "serviceLoad": 25,
        "errorCount": 1
    }
}
```

## Проверим отказоустойчивость

