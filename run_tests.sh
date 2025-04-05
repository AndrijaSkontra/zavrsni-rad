#!/bin/bash

# Set the working directory to the project folder
cd "$(dirname "$0")/project"

# Set environment variables for testing if needed
export DJANGO_SETTINGS_MODULE=main.settings

# Run the tests with coverage report
echo "Running tests with coverage..."
python -m coverage run --source='.' manage.py test
TEST_EXIT_CODE=$?

# Generate coverage report (even if tests fail, we want to see the coverage)
echo -e "\nGenerating coverage report..."
python -m coverage report

# Generate HTML coverage report (optional)
echo -e "\nGenerating HTML coverage report..."
python -m coverage html
echo "HTML coverage report generated in htmlcov/ directory"

# Run specific app tests if requested
if [ "$1" != "" ]; then
    echo -e "\nRunning tests for app: $1"
    python manage.py test $1
    # If specific app tests were requested, use that exit code
    TEST_EXIT_CODE=$?
fi

if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo -e "\nTests completed successfully!"
else
    echo -e "\nTests failed with exit code $TEST_EXIT_CODE"
fi

# Return the test exit code
exit $TEST_EXIT_CODE
