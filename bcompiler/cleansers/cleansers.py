import colorlog
import re

from dateutil.parser import parse

logger = colorlog.getLogger('bcompiler.cleanser')

DATE_REGEX = "^(\d{1,2})(/|-)(\d{1,2})(/|-)(\d{2,4})"
INTEGER_REGEX = "^[-+]?\d+$"
FLOAT_REGEX = "^[-+]?([0-9]*)\.[0-9]+$"
# FLOAT_REGEX = "[-+]?([0-9]*)[.]?[0-9]+" ## allows 223 23 233 23


def clean(string):
    """
    Takes a string, and cleans it.
    Clean action so far are:
        - remove commas
        - remove newlines
        - remove apostrophes
        - turn date text to date objects
        - convert integer-like string to integer
        - convert float-like string to float
    # TODO
        - convert \n\n to |
        - convert \n•
    """
    # bulls
    try:
        if '\n•' in string:
            return string.replace('\n•', ' | ')
    except TypeError:
        pass
    # commas
    try:
        if ',' in string:
            return string.replace(',', '')
    except TypeError:
        pass
    # newlines
    try:
        if '\n' in string:
            return string.replace('\n', ' | ')
    except TypeError:
        pass
    # apostrophes
    try:
        if string[0] == '\'':
            s = ''.join(
                [letter for letter in string if letter != '\''])
            return s
    except TypeError:
        pass
    # date strings
    try:
        if re.match(DATE_REGEX, string):
            m = re.match(DATE_REGEX, string)
            if int(m.groups()[-1]) in range(1965, 1967):
                logger.warning(
                    ("Dates inputted as dd/mm/65 will migrate as dd/mm/2065. "
                     "Dates inputted as dd/mm/66 will migrate as dd/mm/1966."))
            try:
                return parse(m.string)
            except ValueError:
                logger.error(
                    "This date is causing problems: {}".format(string))
                return string
    except TypeError:
        pass
    # integers
    try:
        if re.match(INTEGER_REGEX, string):
            m = re.match(INTEGER_REGEX, string)
            return int(string)
        if re.match(FLOAT_REGEX, string):
            m = re.match(FLOAT_REGEX, string)
            return float(string)
    except TypeError:
        pass
    return string


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
                # commas
                if ',' in c.value:
                    c.value = c.value.replace(',', '')
            except TypeError:
                pass
            try:
                # newlines
                if '\n' in c.value:
                    c.value = c.value.replace('\n', ' | ')
            except TypeError:
                pass
            try:
                # apostrophes
                if c.value[0] == '\'':
                    c.value = ''.join(
                        [letter for letter in c.value if letter != '\''])
            except TypeError:
                pass
            try:
                # dates
                if re.match(DATE_REGEX, c.value):
                    m = re.match(DATE_REGEX, c.value)
                    try:
                        c.value = parse(m.string)
                    except ValueError as e:
                        logger.error(("This date is causing problems: {} at "
                                      "file:{} sheet:{} cell:{}").format(
                            m.string, path, ws, c))
                        pass
            except TypeError:
                pass
            try:
                # integers
                if re.match(INTEGER_REGEX, c.value):
                    m = re.match(INTEGER_REGEX, c.value)
                    c.value = int(c.value)
            except TypeError:
                pass
            try:
                # floats
                if re.match(FLOAT_REGEX, c.value):
                    m = re.match(FLOAT_REGEX, c.value)
                    c.value = float(c.value)
            except TypeError:
                pass
    workbook.save(path)
