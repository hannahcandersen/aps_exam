#!/usr/bin/env python3
# Kann blive kaldt fra kommando linjen med følgende argumenter:
# usage: python3 validator.py input_file correct_output output_dir < contestants_output


import sys

def die(msg):
    print(msg)
    exit(43)

def accept():
    exit(42)

answer_file = sys.argv[2]
output_dir = sys.argv[3]

# Read the correct answer from the file
with open(answer_file) as f:
    correct_answer = f.read()

# Read the given answer from stdin
try:
    given_answer = sys.stdin.read().strip()
except:
    die('unable to read stdin')

#Check if the given answer, is in fact the correct answer
if given_answer == correct_answer:
    accept()
else:
    die('wrong!')
