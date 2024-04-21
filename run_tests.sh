#!/bin/bash
RunUnitTests() {
    echo "Running Django Unit Tests"
    cd provenclub/ || exit
    python3 manage.py test -v 2 --force-color --traceback --parallel # --keepdb
    # coverage run --parallel-mode manage.py test --verbosity=2 --parallel # --keepdb
    cd - || exit
}

source venv/bin/activate

RunUnitTests
