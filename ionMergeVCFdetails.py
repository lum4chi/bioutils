#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2016 Francesco Lumachi <francesco.lumachi@gmail.com>

import vcf as pyvcf
import pandas as pd
import sys, argparse

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

# Read input
parser = argparse.ArgumentParser()
parser.add_argument("input_table")
parser.add_argument("input_vcf")
args = parser.parse_args()
ion_file, vcf_file = args.input_table, args.input_vcf


# Merge information
ion = pd.read_table(ion_file)
in_vcf = pyvcf.Reader(open(vcf_file))
vcf = pd.DataFrame.from_records(list(vcf_iterable(in_vcf)), columns=['# locus','_OPOS','_OREF','_OALT','_QUAL']+['_'+sample+'_GT' for sample in in_vcf.samples])
merged = pd.merge(ion, vcf, on='# locus')
merged.to_csv(sys.stdout, sep='\t', index=False)
