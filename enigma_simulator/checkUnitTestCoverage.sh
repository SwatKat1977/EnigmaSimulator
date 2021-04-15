rm -rf .coverage
python -m coverage run simulation_tests.py -v
python -m coverage report -m