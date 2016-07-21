#!/usr/bin/env bash
#
# Copyright (C) 2016 Francesco Lumachi <francesco.lumachi@gmail.com>

# Given a list of *.bam, convert all in *.sam
# (by default, search all *.bam in current dir)
# if [[ -z "$@" ]]; then files="*.bam"; else files="$@"; fi
if [[ -z "$@" ]]; then
  echo 'Usage: bam2sam view [options] <files>'
fi

opt=()
files=()
for arg in "$@"; do
  if [[ $arg == -? ]]; then opt+="${arg} "; fi
  if [[ $arg == *.* ]]; then files+="${arg} "; fi
done

echo $opt

# echo "Converting $files:";
# for file in $files; do
#   echo " - cooking ${file%.*}..."
#   samtools view $opt $file > ${file%.*}.sam;
# done
echo 'Done!'
