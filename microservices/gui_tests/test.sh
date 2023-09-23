#!/bin/sh

# Get the current date and time
timestamp=$(date +"%Y-%m-%d %H:%M:%S")

# Append the timestamp to the test_result.txt file
echo "Test started at: $timestamp" >> test_results.txt

if python test_functions.py >> /tests/test_results.txt 2>&1 && python test_app.py >> /tests/test_results.txt 2>&1
then
  echo "Both tests passed!" >> /tests/test_results.txt
  TESTRESULT="SUCCESS"
else
  echo "Test: test_functions.py FAILED, test: test_app.py was NOT processed!" >> /tests/test_results.txt
  TESTRESULT="FAILED"
fi

# Get the current date and time again
timestamp=$(date +"%Y-%m-%d %H:%M:%S")

# Append the ending timestamp to the test_result.txt file
echo "Test ended at: $timestamp" >> test_results.txt

echo $TESTRESULT