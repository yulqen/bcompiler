import csv
def test_existence(datamap):
    with open(datamap, 'r', newline='') as f:
        assert next(f).startswith('Project/Programme Name')
        reader = csv.reader(f)
        assert next(reader)[2] == 'B49'


