mkdir pylint_test
cd pylint_test
mkdir dataset
touch dataset/__init__.py
mkdir dataset_123
echo "# pylint: disable=missing-docstring\nfrom collections import Counter" > dataset_123/a.py
PYTHONPATH=. pylint --recursive=y .

mv dataset train
mv dataset_123 train_123
PYTHONPATH=. pylint --recursive=y . 
