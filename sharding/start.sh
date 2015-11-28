#!/bin/bash

START_PORT=10000
BASE_DIR="/tmp/mongo_sharding"
SHARD_COUNT=$1

if [[ $SHARD_COUNT == "" ]]; then
	SHARD_COUNT=2
fi

stop(){
	kill `jobs -p` &> "/dev/null"
	exit 0
}

trap stop 2

wait_for_it(){	
	RETRY=0
	if grep -q "Address already in use for socket" "$LOG" &> "/dev/null"; then
		echo "Address already in use... maybe it's already running"
		return
	fi
	until [[ $LOG != "" ]] && 
		! grep -q "now exiting\|dbexit" "$LOG" &> "/dev/null" && 
		grep -q "waiting for connections" "$LOG" &> "/dev/null"
	do
		if (( "$RETRY" > "30" ))
		then
			echo "Timeout reached"
			stop
		fi
		RETRY=$(($RETRY + 1))
		sleep 1
	done
	cat "$LOG"
}


for (( i = 0; i < $SHARD_COUNT; i++ )); do
	CURR_DIR="${BASE_DIR}/shard${i}"
	LOG="${CURR_DIR}/log"
	echo "Launching shard $i"
	mkdir -p "$CURR_DIR" &&
	mongod --shardsvr --smallfiles --port $(($START_PORT + $i)) --dbpath "$CURR_DIR" --logpath "$LOG" &> "${CURR_DIR}/output.log" &
	wait_for_it
done

echo "Launching config server"

LOG="${BASE_DIR}/cfgserver/log"
mkdir -p "${BASE_DIR}/cfgserver" &&
mongod --port $(($START_PORT + $SHARD_COUNT)) --smallfiles --dbpath "${BASE_DIR}/cfgserver" --logpath "$LOG" &> "${BASE_DIR}/cfgserver/output.log" &
wait_for_it

echo "Launched config server successfully!"

echo "Launching main server"

LOG="${BASE_DIR}/mainserver/log"
mkdir -p "${BASE_DIR}/mainserver" &&
mongos --port $(($START_PORT + $SHARD_COUNT + 1)) --configdb localhost:$(($START_PORT + $SHARD_COUNT)) --logpath "$LOG" &> "${BASE_DIR}/mainserver/output.log" &
wait_for_it

echo "Launched main server successfully!"

echo "Adding shards to server"
for (( i = 0; i < $SHARD_COUNT; i++ )); do
	CURR_PORT=$(($START_PORT + $i))
	echo mongo localhost:$(($START_PORT + $SHARD_COUNT + 1))/admin  --eval "printjson(sh._adminCommand({addshard:'localhost:$(echo $CURR_PORT)', name:'shard${i}'}))"
	mongo localhost:$(($START_PORT + $SHARD_COUNT + 1))/admin --eval "printjson(sh._adminCommand({addshard: 'localhost:${CURR_PORT}', name: 'shard${i}'}))"
done

# echo "Enabling sharding"
# mongo localhost:$(($START_PORT + $SHARD_COUNT + 1))/admin --eval "printjson(db.runCommand({enableSharding: 'sharding_test'}))"

echo "Press CTRL+C to stop everything"

while : 
do
	sleep 60 &
	wait $!
done