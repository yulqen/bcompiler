from bcmaster import BCMasterCSV
import csv

m = BCMasterCSV('source_files/master.csv', as_dataframe=True)

m = m.flip()

with open('source_files/transposed.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print(row['SRO Full Name'])
