#!/bin/bash

START_PORT=10000
BASE_DIR="/tmp/mongo_sharding"
SHARD_COUNT=$1

if [[ $SHARD_COUNT == "" ]]; then
	SHARD_COUNT=2
fi

rm -f "./proclist" && touch "./proclist"

for (( i = 0; i < $SHARD_COUNT; i++ )); do
	CURR_DIR="${BASE_DIR}/shard${i}"
	echo "Launching shard $i"
	mkdir -p $CURR_DIR &&
	mongod -v --rest --shardsvr --port $(($START_PORT + $i)) --dbpath "$CURR_DIR" --logpath "${CURR_DIR}/log" &> "${CURR_DIR}/output.log" &
	echo $! >> "./proclist"
done

echo "Launching config server"

mkdir -p "${BASE_DIR}/cfgserver" &&
mongod --rest --port $(($START_PORT + $SHARD_COUNT)) --dbpath "${BASE_DIR}/cfgserver" --logpath "${BASE_DIR}/cfgserver/log" &> "${BASE_DIR}/cfgserver/output.log" &
echo $! >> "./proclist"
sleep 10

echo "Launching main server"

mongos --port $(($START_PORT + $SHARD_COUNT + 1)) --configdb localhost:$(($START_PORT + $SHARD_COUNT)) > run_routing_service_log &
echo $! >> "./proclist"

sleep 5

echo "Adding shards to server"
for (( i = 0; i < $SHARD_COUNT; i++ )); do
	CURR_PORT=$(($START_PORT + $i))
	echo mongo localhost:$(($START_PORT + $SHARD_COUNT + 1))/admin  --eval "printjson(sh._adminCommand({addshard:'localhost:$(echo $CURR_PORT)', name:'shard${i}'}))"
	mongo localhost:$(($START_PORT + $SHARD_COUNT + 1))/admin --eval "printjson(sh._adminCommand({addshard: 'localhost:${CURR_PORT}', name: 'shard${i}'}))"
done

echo "Enabling sharding"
mongo localhost:$(($START_PORT + $SHARD_COUNT + 1))/admin --eval "printjson(db.runCommand({enableSharding: 'sharding_test'}))"

echo "Press CTRL+C to stop everything"

stop(){
	FILENAME="./proclist"
	exec 3< "$FILENAME"
	echo ""
	echo "Stopping!"
	while read -u 3 proc
	do
		kill $proc 
	done
	exec 3<&-
	rm -f "./proclist"
	exit 0
}

trap stop 2

while : 
do
	sleep 60 &
	wait $!
done