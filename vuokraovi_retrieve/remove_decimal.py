import csv_lab

csv_path = '/Users/young/datahackathon/vuokraovi_retrieve/bus_stop_Zero.csv'
csv_list = csv_lab.csv_to_list(csv_path)

for index, row in enumerate(csv_list):
	if index == 1:
		print row
	
	row[2] = csv_lab.remove_decimal(row[2])

csv_lab.write_list_to_csv(csv_list, 'no_decimal.csv')
