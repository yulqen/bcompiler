import bcompiler.compile as compile_module
from ..compile import parse_source_cells as parse
from ..compile import run
#from ..compile import transpose_master_xlsx

from datetime import date

from openpyxl import load_workbook


def test_compile(populated_template, datamap):
    data = parse(populated_template, datamap)
    assert data[0]['gmpp_key'] == 'Project/Programme Name'
    assert data[0]['gmpp_key_value'] == 'PROJECT/PROGRAMME NAME 9'


def test_run(datamap):
    # print([item for item in dir(compile_module) if not item.startswith("__")])
    # patching module attributes to get it working
    setattr(compile_module, 'RETURNS_DIR', '/tmp/bcompiler-test/')
    setattr(compile_module, 'OUTPUT_DIR', '/tmp/bcompiler-test-output/')
    setattr(compile_module, 'TODAY', date.today().isoformat())
    setattr(compile_module, 'DATAMAP_RETURN_TO_MASTER', datamap)
    run()


#def test_master_xlsx_transpose(master):
#    tm = transpose_master_xlsx(master)
#    wb = load_workbook(tm)
#    ws = wb.active
#    assert ws['A1'].value == "Project/Programme Name"
#    assert ws['A2'].value == "PROJECT/PROGRAME NAME 1"
