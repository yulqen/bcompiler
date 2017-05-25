def get_lines(source: str) -> list:
    with open(source, 'r') as f:
        return [x.rstrip() for x in f]


def get_first_field_from_fields(source: list) -> list:
    return [x.split(',')[0] for x in source]


def intersect(a: list, b: list) -> list:
    return list(set(a) - set(b))


if __name__ == '__main__':
    dm_lines = get_lines('/home/lemon/Documents/bcompiler/source/datamap-returns-to-master')
    dm_lines_field1 = get_first_field_from_fields(dm_lines)

    q3_lines = get_lines('/tmp/work/q3_col_a')

    print("Lines in datamap: {}".format(len(dm_lines_field1)))
    print("Lines in q3_lines: {}".format(len(q3_lines)))

    u = intersect(dm_lines_field1, q3_lines)
    for x in u:
        print(x)
    print(len(u))
