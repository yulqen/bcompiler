"""
Docstring here
"""
# datamap classes
import csv
import logging

logger = logging.getLogger('bcompiler.datamap')


class DatamapLine(object):
    """
    The object containing the data with the Datamap.
    """

    def __init__(self):
        """
        :type cellname: str
        :type sheet: str
        :type cellref: str
        :type dropdown_txt: str
        """
        self.cellname = None
        self.sheet = None
        self.cellref = None
        self.dropdown_txt = None

    def pretty_print(self):
        """
        :return str: a nicely formated but barely useful string of the
        components of the object
        """
        return ("Name: {} | Sheet: {} | Cellref: {} | Dropdown: {}".format(
            self.cellname, self.sheet, self.cellref, self.dropdown_txt))

    def __repr__(self):
        return "DatamapLine(cellname={}, sheet={}, cellref={},\
            dropdowntext={})".format(
                self.cellname, self.sheet, self.cellref, self.dropdown_txt)


class Datamap(object):
    """
    The link between the source of the data and the output, which maps field
    values to MS Excel sheet and cell references.

    There are three implementations of Datamap:

    1. Returns to Master    (how to build a compiled Master spreadsheet (xlsx)
                            from multiple Return Excel files; includes
                            'totals')
    2. Master to Returns    (how to populate a blank Return Excel sheet based
                            on the data a project provided in the previous
                            Quarter, which is in a Master spreadsheet).
    3. Master to GMPP       (how to populate a blank GMPP Return Excel sheet
                            based on data from a Master spreadsheet)

    Try a doctest:

    >>> dm = Datamap(
    ...     'returns-to-master',
    ...     '/home/lemon/Documents/bcompiler/source/datamap-returns-to-master')
    >>> dm.data[0] # doctest: +ELLIPSIS
    DatamapLine(...)

    dm.data is just a list:
    >>> type(dm.data)
    <class 'list'>

    check the source file:
    >>> dm.source_file
    '/home/lemon/Documents/bcompiler/source/datamap-returns-to-master'

    """

    def __init__(self, datamap_type, source_file):
        # TODO 'type' param is redundant at the moment
        self.datamap_type = datamap_type
        self.source_file = source_file
        self.is_cleaned = False
        self._dml_cname_sheet_cref_ddown = []
        self._dml_cname_sheet_cref = []
        self._dml_cname_sheet = []
        self._dml_cname = []
        self.data = []
        self._clean()

    def _clean(self):
        """First thing that happens on initialisation is that the datamap gets
        a clean. This means that missing trailing commas as included."""
        try:
            with open(self.source_file, 'r', encoding='utf-8') as sf:
                for line in sf.readlines():
                    newline = line.rstrip()
                    if ',' in newline[-1]:
                        newline = newline[:-1]
                    else:
                        logger.debug(
                            'No COMMA at end of line starting'
                            '"{}..." ending ->"{}"'.format(
                                newline[:15],
                                newline[-7:]))
                    dml_data = newline.split(',')

                    # we're expecting three values for non-dropdown cells,
                    # four otherwise if we get less than that, we have dead
                    # data
                    if len(dml_data) == 4:
                        # we've got a verified/dropdown cell
                        logger.debug(
                            'Line starting "{}" has verification '
                            'text: "{}"'.format(
                                dml_data[0], dml_data[-1]))
                        dml = DatamapLine()
                        dml.cellname = dml_data[0]
                        dml.sheet = dml_data[1]
                        dml.cellref = dml_data[2]
                        dml.dropdown_txt = dml_data[3]
                        self._dml_cname_sheet_cref_ddown.append(dml)
                        self.data.append(dml)

                    if len(dml_data) == 3:
                        # MOST LIKELY we've got a normal cell reference -
                        # but we test for a regex at end
                        logger.debug(
                            'Line starting "{}" ends in cellref: {}'.format(
                                dml_data[0],
                                dml_data[-1]))
                        dml = DatamapLine()
                        dml.cellname = dml_data[0]
                        dml.sheet = dml_data[1]
                        dml.cellref = dml_data[2]
                        self._dml_cname_sheet_cref.append(dml)
                        self.data.append(dml)

                    if len(dml_data) == 2:
                        # only two items in the line
                        dml = DatamapLine()
                        dml.cellname = dml_data[0]
                        dml.sheet = dml_data[1]
                        logger.debug(
                            "Datamap line: {} -- only TWO items. "
                            "It will not migrate.".format(dml_data[0]))
                        self._dml_cname_sheet.append(dml)
                        self.data.append(dml)

                    if len(dml_data) == 1:
                        # only one item in the line
                        dml = DatamapLine()
                        dml.cellname = dml_data[0]
                        logger.debug(
                            "Datamap line: {} -- only ONE item. "
                            "It will not migrate.".format(dml_data[0]))
                        self._dml_cname.append(dml)
                        self.data.append(dml)
                self.is_cleaned = True
        except FileNotFoundError:
            print(
                "There is no applicable datemap file in "
                "this case {}".format(self.source_file))

    @property
    def count_dml_with_dropdown_text(self):
        """
        Count of the number of datamap count_dml_with_dropdown_text in",
        "the datamap. Four items.
        :return:
        """
        return len(self._dml_cname_sheet_cref_ddown)

    @property
    def count_dml_with_cell_reference_no_dropdown(self):
        """
        Count of the number of datamap non-count_dml_with_dropdown_text",
        "in the datamap. Three items.
        :return:
        """
        return len(self._dml_cname_sheet_cref)

    @property
    def count_dml_sheet_no_cellref(self):
        """
        Count of the number of datamap non-transferring lines in",
        "the datamap. Two items.
        :return:
        """
        return len(self._dml_cname_sheet)

    @property
    def count_dml_cellname_only(self):
        """
        Count of the number of datamap non-transferring lines in",
        "the datamap. One item.
        :return:
        """
        return len(self._dml_cname)

    def __repr__(self):
        return "Datamap(datamap_type={}, source_file={}".format(
            self.datamap_type, self.source_file)


class DatamapGMPP(Datamap):

    def __init__(self, source_file):
        self._dml_no_cellref = []
        self._dict_reader_lines = []
        Datamap.__init__(self, 'master-to-gmpp', source_file)

    @property
    def no_cellrefs(self):
        return len(self._dml_no_cellref)

#    def print_no_cellref_lines(self):
#        # TODO we can't do this on a close csv file
#        # remove for now
#        return [line for line in self._dict_reader_lines
#                if None in line['gmpp_template_cell_reference']]

    def _clean(self):
        """The implementation here is based on testing the datamap as a
        "CSV file, therefore the treatment of commas
        is different. The CSV file from a spreadsheet program does not
        "include a trailing comma, so we have to use a
        DictReader."""
        with open(self.source_file, 'r', encoding='utf-8') as sf:
            sd_data_reader = csv.DictReader(sf, restkey='extra_data')
            self._dict_reader_lines = sd_data_reader
            for row in sd_data_reader:
                if 'extra_data' in row.keys():
                    extra_st = ' '.join(row['extra_data'])
                    logger.info(
                        "Only three fields will migrate. {}"
                        "rejected".format(extra_st))
                if (row['gmpp_template_sheet_reference'] is ''
                        or row['gmpp_template_cell_reference']) is '':
                    logger.debug("Not enough items in {}".format(row))
                    dml = DatamapLine()
                    if row['master_cellname'] == '':
                        dml.cellname = None
                    else:
                        dml.cellname = row['master_cellname']
                    if row['gmpp_template_sheet_reference'] == '':
                        dml.sheet = None
                    else:
                        dml.sheet = row['gmpp_template_sheet_reference']
                    if row['gmpp_template_cell_reference'] == '':
                        dml.cellref = None
                        self._dml_no_cellref.append(
                            row['gmpp_template_cell_reference'])
                    else:
                        dml.cellref = row['gmpp_template_cell_reference']
                    self.data.append(dml)
                    self._dml_cname_sheet_cref.append(dml)
                else:
                    dml = DatamapLine()
                    dml.cellname = row['master_cellname']
                    dml.sheet = row['gmpp_template_sheet_reference']
                    dml.cellref = row['gmpp_template_cell_reference']
                    self.data.append(dml)
                    self._dml_cname_sheet_cref.append(dml)

    def __repr__(self):
        return "DatamapGMPP(source_file={}".format(self.source_file)
