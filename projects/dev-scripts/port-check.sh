#!/bin/bash
PORT=${1:-3000}
echo "Checking port $PORT ..."
lsof -i :$PORT | grep LISTEN || echo "Port $PORT is free"
