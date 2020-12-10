#!/usr/bin/env sh


####
# Script to initialize a new day for the advent of code challenge.
# This script expects the day number as the only argument.
####

if [ -z "$1" ]; then
    echo "Give the day number as a argument"
    exit 1
fi

PYTAB="    " # use 4 spaces as tab char
DIR="day$1"
FILE="main.py"

if [ -d "$DIR" ]; then
    echo "$DIR already exists. Exiting without doing anything."
    exit 2
fi

FILE_CONTENTS=(
"import sys"
"sys.path.insert(0, '..')\n"
"from helpers import filemap\n"
"def main():\n${PYTAB}pass\n"
"if __name__ == '__main__':\n${PYTAB}main()"
)

mkdir "$DIR"
for line in "${FILE_CONTENTS[@]}"; do
    echo "$line" >> "$DIR/$FILE"
done
