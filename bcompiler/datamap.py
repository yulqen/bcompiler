# datamap classes
import csv


class DatamapLine(object):
    """
    The object containing the data with the Datamap.
    """

    def __init__(self):
        self.cellname = None
        self.sheet = None
        self.cellref = None
        self.dropdown_txt = None

    def pretty_print(self):
        return ("Name: {} | Sheet: {} | Cellref: {} | Dropdown: {}".format(self.cellname, self.sheet, self.cellref,
                                                                           self.dropdown_txt))

    def __repr__(self):
        return "DatamapLine object keyed on {}".format(self.cellname)


class Datamap(object):
    """
    The link between the source of the data and the output, which maps field values to MS Excel sheets
    and cell references.

    There are three implementations of Datamap:

    1. Returns to Master    (how to build a compiled Master spreadsheet (xlsx) from multiple Return Excel files; includes
                            'totals')
    2. Master to Returns    (how to populate a blank Return Excel sheet based on the data a project provided in the
                            previous Quarter, which is in a Master spreadsheet).
    3. Master to GMPP       (how to populate a blank GMPP Return Excel sheet based on data from a Master spreadsheet)

    """

    def __init__(self, type=None, source_file=None):
        # TODO 'type' param is redundant at the moment
        self.type = type
        self.source_file = source_file
        self.is_cleaned = False
        self.dml_with_verification = []
        self.dml_with_no_verification = []
        self.dml_no_regex = []
        self.dml_single_item_lines = []
        self.data = []
        self._clean()

    def _clean(self):
        """First thing that happens on initialisation is that the datamap gets a clean. This means
        that missing trailing commas as included."""
        try:
            with open(self.source_file, 'r', encoding='utf-8') as sf:
                for line in sf.readlines():
                    newline = line.rstrip()
                    if ',' in newline[-1]:
                        newline = newline[:-1]
                    dml_data = newline.split(',')
                    # we're expecting three values for non-dropdown cells, four otherwise
                    # if we get less than that, we have dead data
                    if len(dml_data) == 4:
                        # we've got a verified/dropdown cell
                        dml = DatamapLine()
                        dml.cellname = dml_data[0]
                        dml.sheet = dml_data[1]
                        dml.cellref = dml_data[2]
                        dml.dropdown_txt = dml_data[3]
                        self.dml_with_verification.append(dml)
                        self.data.append(dml)

                    if len(dml_data) == 3:
                        # MOST LIKELY we've got a normal cell reference - but we test for a regex at end
                        dml = DatamapLine()
                        dml.cellname = dml_data[0]
                        dml.sheet = dml_data[1]
                        dml.cellref = dml_data[2]
                        self.dml_with_no_verification.append(dml)
                        self.data.append(dml)

                    if len(dml_data) == 2:
                        # only two items in the line
                        dml = DatamapLine()
                        dml.cellname = dml_data[0]
                        dml.sheet = dml_data[1]
                        self.dml_no_regex.append(dml)
                        self.data.append(dml)

                    if len(dml_data) == 1:
                        # only one item in the line
                        dml = DatamapLine()
                        dml.cellname = dml_data[0]
                        self.dml_single_item_lines.append(dml)
                        self.data.append(dml)
                self.is_cleaned = True
        except FileNotFoundError:
            print("There is no applicable datemap file - in this case {}".format(self.source_file))

    @property
    def verified_lines(self):
        """
        Count of the number of datamap verified_lines in the datamap. Four items.
        :return:
        """
        return len(self.dml_with_verification)

    @property
    def non_verified_lines(self):
        """
        Count of the number of datamap non-verified_lines in the datamap. Three items.
        :return:
        """
        return len(self.dml_with_no_verification)

    @property
    def non_tranferring_value_lines(self):
        """
        Count of the number of datamap non-transferring lines in the datamap. Two items.
        :return:
        """
        return len(self.dml_no_regex)

    @property
    def single_item_lines(self):
        """
        Count of the number of datamap non-transferring lines in the datamap. One item.
        :return:
        """
        return len(self.dml_single_item_lines)


class DatamapGMPP(Datamap):
    def __init__(self, type='master-to-gmpp', source_file=None):
        super(DatamapGMPP, self).__init__(type, source_file)

    def _clean(self):
        """The implementation here is based on testing the datamap as a CSV file, therefore the treatment of commas
        is different. The CSV file from a spreadsheet program does not include a trailing comma, so we have to use a
        DictReader."""
        with open(self.source_file, 'r', encoding='utf-8') as sf:
            sd_data_reader = csv.reader(sf)
            for row in sd_data_reader:
                if len(row) == 3:
                    dml = DatamapLine()
                    dml.cellname = row[0]
                    dml.sheet = row[1]
                    dml.cellref = row[2]
                    self.data.append(dml)
                    self.dml_with_no_verification.append(dml)
                else:
                    print("You can only have three cells in the GMPP datamap")

    def __repr__(self):
        return "DatamapGMPP {}".format(__name__)
