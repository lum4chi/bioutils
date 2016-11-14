#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (C) 2016 Francesco Lumachi <francesco.lumachi@gmail.com>
''' Goal of this script is automatically analise VCFs in order to filter them
    and achieve maximum compatibility to various application. '''

from osutils.common import appendSuffix
import vcf as pyvcf
import os, sys, argparse
from itertools import chain

def noFAIL(record):
    # record.FILTER is an array: do a boolean mask on condition 'FAIL'
    isPassed = [True if e!='FAIL' else False for e in record.FILTER]
    # return True only if all element are passed
    return all(isPassed)

def noAD(record):
    # AD is an optional field, if not exist skip
    try:
        # first run through samples and test if AD exist
        ads = [all(s['AD']) for s in record.samples]
        # then, if any sample doesn't have AD, skip
        return all(ads)
    except:
        return False

# Filter example
def dummyFilter(record):
    return True

def isOK(record):
    return all([f(record) for f in FILTERS])

def filterVCF(iname, oname):
    vcf_reader = pyvcf.Reader(filename=iname)
    vcf_writer = pyvcf.Writer(oname, vcf_reader)
    for record in vcf_reader:
        if isOK(record): vcf_writer.write_record(record)

if __name__ == '__main__':

    FILTERS = [noFAIL, noAD]

    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs='+', help="List of vcfs to filter")
    parser.add_argument("-o", "--output_suffix", help="Specify a suffix to \
                        merged output files. If provided, files will be saved \
                        in same input directory.")
    args = parser.parse_args()
    files = args.files
    suffix = args.output_suffix
    for vcf in files:
        out = sys.stdout if suffix is None else \
                                        open(appendSuffix(vcf, suffix), 'w')
        filterVCF(vcf, out)
