from dateutil.parser import parse
import re

DATE_REGEX = "^\d{1,2}(/|-)(\d{1,2})(/|-)\d{2,4}"


def clean_master(workbook, sheet, path):
    """
    Pass it an openpyxl workbook, a sheet name, look for commas in each cell,
    replace them with spaces, then return the workbook.
    """
    path = path.replace('.xlsx', '_cleaned.xlsx')
    workbook.guess_types = True
    ws = workbook[sheet]
    rows = ws.rows
    for r in rows:
        for c in r:
            try:
                if ',' in c.value:
                    c.value = c.value.replace(',', '')
            except TypeError:
                pass
            try:
                if '\n' in c.value:
                    c.value = c.value.replace('\n', ' | ')
            except TypeError:
                pass
            try:
                if c.value[0] == '\'':
                    c.value = ''.join(
                        [letter for letter in c.value if letter != '\''])
            except TypeError:
                pass
            try:
                if re.match(DATE_REGEX, c.value):
                    m = re.match(DATE_REGEX, c.value)
                    c.value = parse(m.string)
            except TypeError:
                pass
    workbook.save(path)
