#!/usr/bin/env python3
import sys
import re

line = sys.stdin.readline()

if not re.match(r"(0|[1-9][0-9]*) (0|[1-9][0-9]*)\r?\n", line):
    sys.exit(43)

n, m = map(int, line.split())
if not ((0 <= n <= 1000) and (0 <= m <= 1000)):
    sys.exit(43)
if sys.stdin.readline() != "":
    sys.exit(43)
sys.exit(42)
