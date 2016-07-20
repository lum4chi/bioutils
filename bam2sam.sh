#!/usr/bin/env bash
#
# Copyright (C) 2016 Francesco Lumachi <francesco.lumachi@gmail.com>

# Given a list of *.bam, convert all in *.sam
# (by default, search all *.bam in current dir)
if [[ -z "$@" ]]; then files="*.bam"; else files="$@"; fi

echo "Converting $files:";
for file in $files; do
        echo " - cooking ${file%.*}..."
        samtools view $file > ${file%.*}.sam;
done;
echo 'Done!';
