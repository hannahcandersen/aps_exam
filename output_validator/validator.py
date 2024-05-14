#!/usr/bin/env python3
# Kan blive kaldt fra kommando linjen med følgende argumenter:
# usage: python3 validator.py input_file correct_output output_dir < contestants_output
# echo "Dracarys 4" | python3 output_validator/validator.py data/sample/1.in data/sample/1.ans

import sys

def die(msg):
    print(msg)
    exit(43)

def accept():
    print('correct')
    exit(42)

answer_file = sys.argv[2]

# Read the correct answer from the file
with open(answer_file) as f:
    correct_answer = f.read().strip()
    print(correct_answer)

# Read the given answer from stdin
try:
    given_answer = sys.stdin.read().strip()
    print(given_answer)
except:
    die('unable to read stdin')

#Check if the given answer, is in fact the correct answer
if given_answer == correct_answer:
    accept()
else:
    die('wrong!')
    
