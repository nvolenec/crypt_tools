#!/usr/bin/sh
awk '!seen[$0]++' $1
