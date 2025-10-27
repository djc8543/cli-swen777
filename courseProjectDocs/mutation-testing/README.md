# Setup to run mutation tests

1. pip install mutmut==2.5.1

2. pip install pony==0.7.14

3. coverage erase

4. coverage run -m pytest -q tests/test_utils.py

5. coverage report -m httpie/utils.py

6. mutmut run

7. mutmut results

8. mutmut html
