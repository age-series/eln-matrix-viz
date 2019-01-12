#!/bin/bash
mkdir png
for filename in dots/*.dot; do
	echo $filename
	dot -Tpng "$filename" -o "png/$(basename "$filename").png"
done
