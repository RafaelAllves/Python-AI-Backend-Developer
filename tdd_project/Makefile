run:
	@uvicorn store.main:app --reload

precommit-install:
	@pre-commit install

test:
	@pytest

test-matching:
	@pytest -s -rx -k $(T) --pdb store ./tests/
