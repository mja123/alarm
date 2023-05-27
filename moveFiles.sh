#! /bin/bash

folder=/setUp/sdk
target=/setUp/sdk/tools

for file in $folder/*
do
    if [[ $file == $target ]]; then
	continue
    fi
    if [ -d $file ]; then
	echo "here"
	mv $file/ $target 
	continue
    fi
    echo "File: "$file
    mv $file $target 
done
