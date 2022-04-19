sudo chmod 666 "/dev/ttyAMA0"

export PYTHONPATH=..:$PYTHONPATH

python main.py --port "/dev/ttyAMA0" --db_url "sqlite:///office.db"
