#!/usr/bin/env bash
#
# Copyright (C) 2016 Francesco Lumachi <francesco.lumachi@gmail.com>


# if [[ -z "$@" ]]; then files="*.bam"; else files="$@"; fi
if [[ -z "$@" ]]; then
  echo 'Usage: bam2sam [options] <files>'
  echo '- exe: bam2sam -F 4 *.bam'
fi

opt=()
files=()
for arg in "$@"; do
  if [[ $arg == *.* ]]; then files+="${arg} "; continue; fi
  opt+="${arg} "
  # if [[ $arg == -* ]]; then opt+="${arg} "; continue; fi
  # if [[ $arg == [:digit:] ]]; then opt+="${arg} "; continue; fi
done

echo "Converting $files:";
for file in $files; do
  echo " - cooking ${file%.*}..."
  samtools view $opt $file > ${file%.*}${opt// /_}.sam;
done
echo 'Done!'
