from ..utils import project_data_from_master
from pathlib import Path


class ProjectData:
    """
    ProjectData class
    """
    def __init__(self, d: dict):
        """
        ordered_dict is easiest to get from project_data_from_master[x]
        """
        self.data = d

    def __len__(self):
        return len(self.data)

    def __getitem__(self, item):
        return self.data[item]


class Master:
    """
    Master class.
    """
    def __init__(self, quarter, path: Path):
        self._quarter = quarter
        self.path = Path(path)
        self._data = project_data_from_master(self.path)
        self._project_titles = [item for item in self.data.keys()]
        self.year = self._quarter.year

    def __getitem__(self, project_name):
        return ProjectData(self._data[project_name])

    @property
    def data(self):
        return self._data

    @property
    def quarter(self):
        return self._quarter.quarter

    @property
    def filename(self):
        return self.path.name

    @property
    def projects(self):
        return self._project_titles
