def test_existance(datamap):
    with open(datamap, 'r') as f:
        assert next(f).startswith('Project/Programme Name')
