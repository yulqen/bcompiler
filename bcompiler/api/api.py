from ..core import Master, Quarter


def project_data_from_master_api(master_file: str, quarter: int, year: int):
    m = Master(Quarter(quarter, year), master_file)
    return m
