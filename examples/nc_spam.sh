#!/usr/bin/env bash

while true; do
    nc -q 0 localhost 41000 < nc_data.txt
    sleep .1
done