# datamap class

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
        self.type = type
        self.source_file = source_file
        self.is_cleaned = False
        self.datamap_lines = []
        self._clean()


    def _clean(self):
        """First thing that happens on initialisation is that the datamap gets a clean. This means
        that missing trailing commas as included."""
        self.datamap_lines = []
        with open(self.source_file, 'r', encoding='utf-8') as sf:
            for line in sf.readlines():
                newline = line.rstrip()
                if ',' in newline[-1]:
                    newline += '\n'
                    self.datamap_lines.append(newline)
                else:
                    newline = newline + ',' + '\n'
                    self.datamap_lines.append(newline)
            self.is_cleaned = True

    @property
    def lines(self):
        """
        Count of the number of datamap lines in the datamap.
        :return:
        """
        return len(self.datamap_lines)
