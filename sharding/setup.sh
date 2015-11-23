#!/bin/bash

START_PORT=10000
BASE_DIR="/tmp/mongo_sharding"
SHARD_COUNT=$1

if [[ $SHARD_COUNT == "" ]]; then
	SHARD_COUNT=2
fi

for (( i = 0; i < $SHARD_COUNT; i++ )); do
	CURR_DIR="${BASE_DIR}/shard${i}"
	echo "Launching shard $i"
	mkdir -p $CURR_DIR &&
	mongod -v --rest --shardsvr --port $(($START_PORT + $i)) --dbpath "$CURR_DIR" --logpath "${CURR_DIR}/log" &> "${CURR_DIR}/output.log" &
done