#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2016 Francesco Lumachi <francesco.lumachi@gmail.com>

import vcf as pyvcf
import pandas as pd
import os, sys, argparse

# Extract from vcf interesting field
def vcf_iterable(vcf):
    for var in vcf:
        record = [
            '{0}:{1}'.format(var.CHROM,var.POS), \
            ', '.join([str(x) for x in var.INFO['OPOS']]), \
            ', '.join([str(x) for x in var.INFO['OREF']]), \
            ', '.join([str(x) for x in var.INFO['OALT']]), var.QUAL, \
            ] + [sample['GT'] for sample in var.samples]
        yield record

# Merge information
def mergeOne(ion_file, vcf_file):
    ion = pd.read_table(ion_file)
    in_vcf = pyvcf.Reader(open(vcf_file))
    vcf = pd.DataFrame.from_records(list(vcf_iterable(in_vcf)), \
            columns=['# locus','_OPOS','_OREF','_OALT','_QUAL'] + \
                    ['_'+sample+'_GT' for sample in in_vcf.samples])
    return pd.merge(ion, vcf, on='# locus')

# Read input
parser = argparse.ArgumentParser()
parser.add_argument("files", nargs='+', help="List of tables and vcfs to merge")
parser.add_argument("-o", "--output_suffix", help="Specify a suffix to merged \
                    output files. If provided, files will be saved in same \
                    input tables directory.")
args = parser.parse_args()
files = args.files
out_suffix = args.output_suffix

# Split files by extension and (hopefully) paired by lexicographic sorting
tables = sorted([t for t in files if os.path.splitext(t)[1] != '.vcf'])
vcfs = sorted([v for v in files if os.path.splitext(v)[1] == '.vcf'])

# Process by pair
for table, vcf in zip(tables, vcfs):
    # Print on stdout (if multiple file, header will be repeated) or append to
    # table name the provided suffix and write to multiple file
    out = sys.stdout if out_suffix is None else os.path.splitext(table)[0] + \
                                                out_suffix + \
                                                os.path.splitext(table)[1]
    mergeOne(table, vcf).to_csv(out, sep='\t', index=False)
