from bcmaster import BCMasterCSV

m = BCMasterCSV('source_files/master.csv')

m = m.transpose_csv()
m.seek(0)
print(m.read())
