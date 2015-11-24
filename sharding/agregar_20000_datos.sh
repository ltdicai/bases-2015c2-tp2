#!/bin/bash
if [[ $1 == "" ]]; then
	echo "Falta ubicación de la base (<host>:<port>/<dbase>)"
	exit 1
fi
mongo $1 --shell "./test.js"