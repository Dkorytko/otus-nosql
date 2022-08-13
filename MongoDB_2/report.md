# MongoDB 2

# Настройка replica-set

## Каталоги для всех будущих реплика-сетов
```bash
$ mkdir /tmp/data
$ cd /tmp/data
$ mkdir config1 config2 config3 repset11 repset12 repset13 repset21 repset22 repset23 repset31 repset32 repset33
```

## keyfile, который будет использоваться всеми монгами
```bash
$ openssl rand -base64 756 > /tmp/data/keyfile.f
$ chmod 400 /tmp/data/keyfile.f
```

## Запускаем config-server и формируем replica-set config, создаём пользователя-администратора

```bash
$ mongod --configsvr --dbpath /tmp/data/config1 --port 26001 --replSet repsetConfig --fork --logpath /tmp/data/config1.log 
$ mongod --configsvr --dbpath /tmp/data/config2 --port 26002 --replSet repsetConfig --fork --logpath /tmp/data/config2.log 
$ mongod --configsvr --dbpath /tmp/data/config3 --port 26003 --replSet repsetConfig --fork --logpath /tmp/data/config3.log 
```

```
mongo --port 26001

rs.initiate(
    {
    "_id" : "repsetConfig", 
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
    user: "admin",
    pwd: "1", 
    roles: [ { role: "root", db: "admin" } ]
  }
)

```

## Создадим три реплика-сета, которые будут шардами и создадим пользователя-администратора

##  Replica Set 1

```
$ mongod --dbpath /tmp/data/repset11 --port 27101 --replSet repset1 --fork --logpath /tmp/data/repset11.log 
$ mongod --dbpath /tmp/data/repset12 --port 27102 --replSet repset1 --fork --logpath /tmp/data/repset12.log 
$ mongod --dbpath /tmp/data/repset13 --port 27103 --replSet repset1 --fork --logpath /tmp/data/repset13.log
```

```
$ mongo --port 27101
```

```
rs.initiate(
    {
    "_id" : "repset1", 
    members : 
        [
        {"_id" : 0, host : "127.0.0.1:27101"},
        {"_id" : 1, host : "127.0.0.1:27102"},
        {"_id" : 2, host : "127.0.0.1:27103"}
        ]
    }
);

use admin;

db.createUser(
    {
    user: "admin",
    pwd: "12345", 
    roles: [ { role: "root", db: "admin" } ]
    }
)
```

##  Replica Set 2

```
$ mongod --dbpath /tmp/data/repset21 --port 27201 --replSet repset2 --fork --logpath /tmp/data/repset21.log 
$ mongod --dbpath /tmp/data/repset22 --port 27202 --replSet repset2 --fork --logpath /tmp/data/repset22.log 
$ mongod --dbpath /tmp/data/repset23 --port 27203 --replSet repset2 --fork --logpath /tmp/data/repset23.log 

```

```
mongo --port 27201

```

```
rs.initiate(
    {
    "_id" : "repset2", 
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
    user: "admin",
    pwd: "12345", 
    roles: [ { role: "root", db: "admin" } ]
    }
)
```

##  Replica Set 3

```
$ mongod --dbpath /tmp/data/repset31 --port 27301 --replSet repset3 --fork --logpath /tmp/data/repset31.log 
$ mongod --dbpath /tmp/data/repset32 --port 27302 --replSet repset3 --fork --logpath /tmp/data/repset32.log 
$ mongod --dbpath /tmp/data/repset33 --port 27303 --replSet repset3 --fork --logpath /tmp/data/repset33.log 

```

```
mongo --port 27301

```

```
rs.initiate(
    {
    "_id" : "repset3", 
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
    user: "admin",
    pwd: "12345", 
    roles: [ { role: "root", db: "admin" } ]
    }
)
```

```
 14:10   0:09 mongod --configsvr --dbpath /tmp/data/config1 --port 26001 --replSet repsetConfig --fork --logpath /tmp/data/config1.log
 14:11   0:09 mongod --configsvr --dbpath /tmp/data/config2 --port 26002 --replSet repsetConfig --fork --logpath /tmp/data/config2.log
 14:11   0:09 mongod --configsvr --dbpath /tmp/data/config3 --port 26003 --replSet repsetConfig --fork --logpath /tmp/data/config3.log
 14:15   0:06 mongod --dbpath /tmp/data/repset11 --port 27101 --replSet repset1 --fork --logpath /tmp/data/repset11.log
 14:15   0:05 mongod --dbpath /tmp/data/repset12 --port 27102 --replSet repset1 --fork --logpath /tmp/data/repset12.log
 14:16   0:05 mongod --dbpath /tmp/data/repset13 --port 27103 --replSet repset1 --fork --logpath /tmp/data/repset13.log
 14:19   0:03 mongod --dbpath /tmp/data/repset21 --port 27201 --replSet repset2 --fork --logpath /tmp/data/repset21.log
 14:20   0:02 mongod --dbpath /tmp/data/repset22 --port 27202 --replSet repset2 --fork --logpath /tmp/data/repset22.log
 14:20   0:02 mongod --dbpath /tmp/data/repset23 --port 27203 --replSet repset2 --fork --logpath /tmp/data/repset23.log
 14:22   0:02 mongod --dbpath /tmp/data/repset31 --port 27301 --replSet repset3 --fork --logpath /tmp/data/repset31.log
 14:22   0:01 mongod --dbpath /tmp/data/repset32 --port 27302 --replSet repset3 --fork --logpath /tmp/data/repset32.log
 14:22   0:01 mongod --dbpath /tmp/data/repset33 --port 27303 --replSet repset3 --fork --logpath /tmp/data/repset33.log
```

Убьём все запущенные экземпляры с помощью kill и запустим заново с ключами --auth и --keyFile /tmp/data/keyFile.f, указыв, что они запущены в качестве шард-серверов ключом --shardsvr

```bash

$ mongod --configsvr --dbpath /tmp/data/config1 --port 26001 --replSet repsetConfig --fork --logpath /tmp/data/config1.log --auth --keyFile /tmp/data/keyfile.f
$ mongod --configsvr --dbpath /tmp/data/config2 --port 26002 --replSet repsetConfig --fork --logpath /tmp/data/config2.log --auth --keyFile /tmp/data/keyfile.f
$ mongod --configsvr --dbpath /tmp/data/config3 --port 26003 --replSet repsetConfig --fork --logpath /tmp/data/config3.log --auth --keyFile /tmp/data/keyfile.f

$ mongod --dbpath /tmp/data/repset11 --port 27101 --replSet repset1 --fork --logpath /tmp/data/repset11.log --auth --keyFile /tmp/data/keyfile.f --shardsvr
$ mongod --dbpath /tmp/data/repset12 --port 27102 --replSet repset1 --fork --logpath /tmp/data/repset12.log --auth --keyFile /tmp/data/keyfile.f --shardsvr
$ mongod --dbpath /tmp/data/repset13 --port 27103 --replSet repset1 --fork --logpath /tmp/data/repset13.log --auth --keyFile /tmp/data/keyfile.f --shardsvr

$ mongod --dbpath /tmp/data/repset21 --port 27201 --replSet repset2 --fork --logpath /tmp/data/repset21.log --auth --keyFile /tmp/data/keyfile.f --shardsvr
$ mongod --dbpath /tmp/data/repset22 --port 27202 --replSet repset2 --fork --logpath /tmp/data/repset22.log --auth --keyFile /tmp/data/keyfile.f --shardsvr
$ mongod --dbpath /tmp/data/repset23 --port 27203 --replSet repset2 --fork --logpath /tmp/data/repset23.log --auth --keyFile /tmp/data/keyfile.f --shardsvr

$ mongod --dbpath /tmp/data/repset31 --port 27301 --replSet repset3 --fork --logpath /tmp/data/repset31.log --auth --keyFile /tmp/data/keyfile.f --shardsvr
$ mongod --dbpath /tmp/data/repset32 --port 27302 --replSet repset3 --fork --logpath /tmp/data/repset32.log --auth --keyFile /tmp/data/keyfile.f --shardsvr
$ mongod --dbpath /tmp/data/repset33 --port 27303 --replSet repset3 --fork --logpath /tmp/data/repset33.log --auth --keyFile /tmp/data/keyfile.f --shardsvr

```

```
 14:46   0:03 mongod --configsvr --dbpath /tmp/data/config1 --port 26001 --replSet repsetConfig --fork --logpath /tmp/data/config1.log --auth --keyFile /tmp/data/keyfile.f
 14:46   0:02 mongod --configsvr --dbpath /tmp/data/config2 --port 26002 --replSet repsetConfig --fork --logpath /tmp/data/config2.log --auth --keyFile /tmp/data/keyfile.f
 14:46   0:02 mongod --configsvr --dbpath /tmp/data/config3 --port 26003 --replSet repsetConfig --fork --logpath /tmp/data/config3.log --auth --keyFile /tmp/data/keyfile.f
 14:46   0:02 mongod --dbpath /tmp/data/repset11 --port 27101 --replSet repset1 --fork --logpath /tmp/data/repset11.log --auth --keyFile /tmp/data/keyfile.f --shardsvr
 14:46   0:02 mongod --dbpath /tmp/data/repset12 --port 27102 --replSet repset1 --fork --logpath /tmp/data/repset12.log --auth --keyFile /tmp/data/keyfile.f --shardsvr
 14:47   0:02 mongod --dbpath /tmp/data/repset13 --port 27103 --replSet repset1 --fork --logpath /tmp/data/repset13.log --auth --keyFile /tmp/data/keyfile.f --shardsvr
 14:47   0:02 mongod --dbpath /tmp/data/repset21 --port 27201 --replSet repset2 --fork --logpath /tmp/data/repset21.log --auth --keyFile /tmp/data/keyfile.f --shardsvr
 14:47   0:01 mongod --dbpath /tmp/data/repset22 --port 27202 --replSet repset2 --fork --logpath /tmp/data/repset22.log --auth --keyFile /tmp/data/keyfile.f --shardsvr
 14:47   0:01 mongod --dbpath /tmp/data/repset23 --port 27203 --replSet repset2 --fork --logpath /tmp/data/repset23.log --auth --keyFile /tmp/data/keyfile.f --shardsvr
 14:47   0:01 mongod --dbpath /tmp/data/repset31 --port 27301 --replSet repset3 --fork --logpath /tmp/data/repset31.log --auth --keyFile /tmp/data/keyfile.f --shardsvr
 14:47   0:01 mongod --dbpath /tmp/data/repset32 --port 27302 --replSet repset3 --fork --logpath /tmp/data/repset32.log --auth --keyFile /tmp/data/keyfile.f --shardsvr
 14:48   0:01 mongod --dbpath /tmp/data/repset33 --port 27303 --replSet repset3 --fork --logpath /tmp/data/repset33.log --auth --keyFile /tmp/data/keyfile.f --shardsvr
```

## Проверим, что реплика-сеты теперь требуют авторизации

```bash 
$ mongo --host repsetConfig/127.0.0.1:26001,127.0.0.1:26002,127.0.0.1:26003
$ mongo --host repset1/127.0.0.1:27101,127.0.0.1:27102,127.0.0.1:27103
$ mongo --host repset2/127.0.0.1:27201,127.0.0.1:27202,127.0.0.1:27203
$ mongo --host repset3/127.0.0.1:27301,127.0.0.1:27302,127.0.0.1:27303
```

```
repset3:PRIMARY> rs.status();
{
	"ok" : 0,
	"errmsg" : "command replSetGetStatus requires authentication",
	"code" : 13,
	"codeName" : "Unauthorized"
}
repset3:PRIMARY> 
```

во всех получаю ошибку авторизации, указываю в строке подключения пользователя, пароль и БД авторизации:

```
$ mongo --host repsetConfig/127.0.0.1:26001,127.0.0.1:26002,127.0.0.1:26003 -u "admin" -p "12345" --authenticationDatabase "admin"
$ mongo --host repset1/127.0.0.1:27101,127.0.0.1:27102,127.0.0.1:27103 -u "admin" -p "12345" --authenticationDatabase "admin"
$ mongo --host repset2/127.0.0.1:27201,127.0.0.1:27202,127.0.0.1:27203 -u "admin" -p "12345" --authenticationDatabase "admin"
$ mongo --host repset3/127.0.0.1:27301,127.0.0.1:27302,127.0.0.1:27303 -u "admin" -p "12345" --authenticationDatabase "admin"
```

 rs.status() возвращает полную информацию о статусе реплика-сета
 ```json
 {
	"set" : "repset3",
	"date" : ISODate("2022-08-13T12:02:22.156Z"),
	"myState" : 1,
	"term" : NumberLong(2),
	"syncSourceHost" : "",
	"syncSourceId" : -1,
	"heartbeatIntervalMillis" : NumberLong(2000),
	"majorityVoteCount" : 2,
	"writeMajorityCount" : 2,
	"votingMembersCount" : 3,
	"writableVotingMembersCount" : 3,
	"optimes" : {
		"lastCommittedOpTime" : {
			"ts" : Timestamp(1660392138, 1),
			"t" : NumberLong(2)
		},
		"lastCommittedWallTime" : ISODate("2022-08-13T12:02:18.056Z"),
		"readConcernMajorityOpTime" : {
			"ts" : Timestamp(1660392138, 1),
			"t" : NumberLong(2)
		},
		"readConcernMajorityWallTime" : ISODate("2022-08-13T12:02:18.056Z"),
		"appliedOpTime" : {
			"ts" : Timestamp(1660392138, 1),
			"t" : NumberLong(2)
		},
		"durableOpTime" : {
			"ts" : Timestamp(1660392138, 1),
			"t" : NumberLong(2)
		},
		"lastAppliedWallTime" : ISODate("2022-08-13T12:02:18.056Z"),
		"lastDurableWallTime" : ISODate("2022-08-13T12:02:18.056Z")
	},
	"lastStableRecoveryTimestamp" : Timestamp(1660392098, 1),
	"electionCandidateMetrics" : {
		"lastElectionReason" : "electionTimeout",
		"lastElectionDate" : ISODate("2022-08-13T11:47:58.016Z"),
		"electionTerm" : NumberLong(2),
		"lastCommittedOpTimeAtElection" : {
			"ts" : Timestamp(0, 0),
			"t" : NumberLong(-1)
		},
		"lastSeenOpTimeAtElection" : {
			"ts" : Timestamp(1660391088, 1),
			"t" : NumberLong(1)
		},
		"numVotesNeeded" : 2,
		"priorityAtElection" : 1,
		"electionTimeoutMillis" : NumberLong(10000),
		"numCatchUpOps" : NumberLong(0),
		"newTermStartDate" : ISODate("2022-08-13T11:47:58.026Z"),
		"wMajorityWriteAvailabilityDate" : ISODate("2022-08-13T11:47:58.158Z")
	},
	"members" : [
		{
			"_id" : 0,
			"name" : "127.0.0.1:27301",
			"health" : 1,
			"state" : 1,
			"stateStr" : "PRIMARY",
			"uptime" : 877,
			"optime" : {
				"ts" : Timestamp(1660392138, 1),
				"t" : NumberLong(2)
			},
			"optimeDate" : ISODate("2022-08-13T12:02:18Z"),
			"lastAppliedWallTime" : ISODate("2022-08-13T12:02:18.056Z"),
			"lastDurableWallTime" : ISODate("2022-08-13T12:02:18.056Z"),
			"syncSourceHost" : "",
			"syncSourceId" : -1,
			"infoMessage" : "",
			"electionTime" : Timestamp(1660391278, 1),
			"electionDate" : ISODate("2022-08-13T11:47:58Z"),
			"configVersion" : 1,
			"configTerm" : 2,
			"self" : true,
			"lastHeartbeatMessage" : ""
		},
		{
			"_id" : 1,
			"name" : "127.0.0.1:27302",
			"health" : 1,
			"state" : 2,
			"stateStr" : "SECONDARY",
			"uptime" : 864,
			"optime" : {
				"ts" : Timestamp(1660392138, 1),
				"t" : NumberLong(2)
			},
			"optimeDurable" : {
				"ts" : Timestamp(1660392138, 1),
				"t" : NumberLong(2)
			},
			"optimeDate" : ISODate("2022-08-13T12:02:18Z"),
			"optimeDurableDate" : ISODate("2022-08-13T12:02:18Z"),
			"lastAppliedWallTime" : ISODate("2022-08-13T12:02:18.056Z"),
			"lastDurableWallTime" : ISODate("2022-08-13T12:02:18.056Z"),
			"lastHeartbeat" : ISODate("2022-08-13T12:02:22.053Z"),
			"lastHeartbeatRecv" : ISODate("2022-08-13T12:02:20.550Z"),
			"pingMs" : NumberLong(0),
			"lastHeartbeatMessage" : "",
			"syncSourceHost" : "127.0.0.1:27301",
			"syncSourceId" : 0,
			"infoMessage" : "",
			"configVersion" : 1,
			"configTerm" : 2
		},
		{
			"_id" : 2,
			"name" : "127.0.0.1:27303",
			"health" : 1,
			"state" : 2,
			"stateStr" : "SECONDARY",
			"uptime" : 852,
			"optime" : {
				"ts" : Timestamp(1660392138, 1),
				"t" : NumberLong(2)
			},
			"optimeDurable" : {
				"ts" : Timestamp(1660392138, 1),
				"t" : NumberLong(2)
			},
			"optimeDate" : ISODate("2022-08-13T12:02:18Z"),
			"optimeDurableDate" : ISODate("2022-08-13T12:02:18Z"),
			"lastAppliedWallTime" : ISODate("2022-08-13T12:02:18.056Z"),
			"lastDurableWallTime" : ISODate("2022-08-13T12:02:18.056Z"),
			"lastHeartbeat" : ISODate("2022-08-13T12:02:22.054Z"),
			"lastHeartbeatRecv" : ISODate("2022-08-13T12:02:21.425Z"),
			"pingMs" : NumberLong(0),
			"lastHeartbeatMessage" : "",
			"syncSourceHost" : "127.0.0.1:27302",
			"syncSourceId" : 1,
			"infoMessage" : "",
			"configVersion" : 1,
			"configTerm" : 2
		}
	],
	"ok" : 1
}

 ```


