install:
	pip install -r requirements.txt

# test:
# 	python -m pytest -s test_*.py

format:
	black financialaiagent/*.py

lint:
	pylint --disable=R,C,no-value-for-parameter,W0718,W0611 financialaiagent/*.py

all: install format lint
	@echo "All tasks completed successfully."
