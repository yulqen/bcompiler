import colorlog
from operator import itemgetter
import re

from dateutil.parser import parse

logger = colorlog.getLogger('bcompiler.cleanser')

COMMA_REGEX = r",\s?"
COMMA_FIX = r" "
APOS_REGEX = r"^'"
APOS_FIX = r""
DATE_REGEX = r"^(\d{1,2})(/|-)(\d{1,2})(/|-)(\d{2,4})"
INT_REGEX = r"^[-+]?\d+$"
FLOAT_REGEX = r"^[-+]?([0-9]*)\.[0-9]+$"
NL_REGEX = r"\ \n"
NL_FIX = r" |"
CHAR_NL_CHAR_REGEX = r"\S\n\S"
CHAR_NL_CHAR_FIX = r" | "
SPACE_PIPE_CHAR_REGEX = r"\ \|\S"
SPACE_PIPE_CHAR_FIX = r" | "


class Cleanser:
    """
    Takes a string, and cleans it.
    Clean action so far are:
        - remove commas
        - remove newlines
        - remove apostrophes
        - turn date text to date objects
        - convert integer-like string to integer
        - convert float-like string to float
        - convert \n\n to |
        - convert \n•
    """

    def __init__(self, string):
        self.string = string

        # a list of dicts that describe everything needed to fix errors in
        # string passed to class constructor. Method self.clean() runs through
        # them,  fixing each in turn.
        self._checks = [
            dict(
                c_type='commas',
                rule=COMMA_REGEX,
                fix=COMMA_FIX,
                func=self._commas,
                count=0),
            dict(
                c_type='leading_apostrophe',
                rule=APOS_REGEX,
                fix=APOS_FIX,
                func=self._apostrophe,
                count=0),
            dict(
                c_type='newline',
                rule=NL_REGEX,
                fix=NL_FIX,
                func=self._newline,
                count=0),
            dict(
                c_type='char_newline_char',
                rule=CHAR_NL_CHAR_REGEX,
                fix=CHAR_NL_CHAR_FIX,
                func=self._char_newline_char,
                count=0),
            dict(
                c_type='double_space',
                rule="  ",
                fix=" ",
                func=self._doublespace,
                count=0),
            dict(
                c_type='pipe_char',
                rule=SPACE_PIPE_CHAR_REGEX,
                fix=SPACE_PIPE_CHAR_FIX,
                func=self._space_pipe_char,
                count=0),
        ]
        self.checks_l = len(self._checks)
        self._analyse()

    def _sort_checks(self):
        """
        Sorts the list of dicts in self._checks by their count, highest
        first, so that when the fix methods run down them, they always have
        a count with a value higher than 0 to run with, otherwise later
        fixes might not get hit.
        """
        self._checks = sorted(
            self._checks, key=itemgetter('count'), reverse=True)

    def _commas(self, regex, fix):
        """
        Handles commas in self.string according to rule in self._checks
        """
        # we want to sort the list first so self._checks has any item
        # with a count > 0 up front, otherwise if a count of 0 appears
        # before it in the list, the > 0 count never gets fixed
        return re.sub(regex, fix, self.string)

    def _apostrophe(self, regex, fix):
        """Handles apostrophes as first char of the string."""
        return self.string.lstrip('\'')

    def _newline(self, regex, fix):
        """Handles newlines anywhere in string."""
        return re.sub(regex, fix, self.string)

    def _char_newline_char(self, regex, fix):
        """Handles newlines preceded and succeeded by chars."""
        return re.sub(regex, fix, self.string)

    def _doublespace(self, regex, fix):
        """Handles double-spaces anywhere in string."""
        return re.sub(regex, fix, self.string)

    def _space_pipe_char(self, regex, fix):
        """Handles space pipe char anywhere in string."""
        return re.sub(regex, fix, self.string)

    def _access_checks(self, c_type):
        """Helper method returns the index of rule in self._checks
        when given a c_type"""
        return self._checks.index(next(
            item for item in self._checks if item['c_type'] == c_type))

    def _analyse(self):
        """
        Uses the self._checks table as a basis for counting the number of
        each cleaning target required, and calling the appropriate method
        to clean.
        """
        i = 0
        while i < self.checks_l:
            matches = re.finditer(self._checks[i]['rule'], self.string)
            if matches:
                self._checks[i]['count'] += len(list(matches))
            i += 1

    def clean(self):
        """Runs each applicable cleaning action and returns the cleaned
        string."""
        self._sort_checks()
        for check in self._checks:
            if check['count'] > 0:
                self.string = check['func'](
                    check['rule'], check['fix'])
                check['count'] = 0
            else:
                # shouldn't ever get here but hey...
                return self.string
            self._sort_checks()
        return self.string


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
        - convert \n\n to |
        - convert \n•
    """
    # newlines
    try:
        if '\n' in string:
            # do these first (order is important)
            # bulls
            if '\n•' in string:
                string = string.replace('\n•', ' | ')
            # doubles
            elif '\n\n' in string:
                string = string.replace('\n\n', ' | ')
            else:
                string = string.replace('\n', ' | ')
            return string.replace('\n', ' | ')
    except TypeError:
        pass
    # commas
    try:
        if ',' in string:
            return string.replace(',', '')
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
        if re.match(INT_REGEX, string):
            m = re.match(INT_REGEX, string)
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
                if re.match(INT_REGEX, c.value):
                    m = re.match(INT_REGEX, c.value)
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
