#!/bin/bash
# Get a list of staged files
staged_files=$(git diff --cached --name-only | grep -v "lint.sh" | grep -vE "\.html$" | grep -v "\.json" | grep -vE "\.txt$" | grep -vE "\.yaml$" | grep "provenclub/")

# Get a list of files in the provenclub folder
provenclub_files=$(git ls-files "provenclub/")

# Take the intersection of staged_files and provenclub_files
intersection_files=$(comm -12 <(echo "$staged_files" | sort) <(echo "$provenclub_files" | sort))

# Check if there are intersection files
if [ -z $intersection_files ]; then
  echo "No intersection staged files to process."
  exit 0
fi

echo "Running autoflake"
autoflake --remove-all-unused-imports --recursive --in-place --ignore-init-module-imports --exclude 'migrations' $intersection_files
echo "Running black"
black -t py310 --fast --exclude='migrations\/' --force-exclude='system_policies\/' $intersection_files
echo "Running autopep8"
autopep8 --in-place --recursive $intersection_files
echo "Running flake"
flake8 $intersection_files --statistics --exclude-from-doctest='migrations/' --ignore=E501,E402,W503
