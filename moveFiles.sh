#! /bin/bash

tools_sorting() {
  folder=/setUp/sdk
  target=/setUp/sdk/tools

  for file in $folder/*
  do
      if [[ $file == $target ]]; then
        continue
      fi
      if [ -d $file ]; then
        mv $file/ $target
        continue
      fi
      mv $file $target
  done
}

sdk_sorting() {
  target=/setUp/sdk
  folder=$target/cmdline-tools/latest

  for file in $folder/*
  do
      if [ -d $file ]; then
        mv $file/ $target
      else
        mv $file $target
      fi
      echo $file
      ls /setUp/sdk
  done
}