def clean_master(workbook, sheet, path):
    """
    Pass it an openpyxl workbook, a sheet name, look for commas in each cell,
    replace them with spaces, then return the workbook.
    """
    path = path.replace('.xlsx', '_cleaned.xlsx')
    ws = workbook[sheet]
    rows = ws.rows
    for r in rows:
        for c in r:
            if ',' in c.value:
                c.value = c.value.replace(',', '')
            if '\n' in c.value:
                c.value = c.value.replace('\n', ' | ')
    workbook.save(path)
