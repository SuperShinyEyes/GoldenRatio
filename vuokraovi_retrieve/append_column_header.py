import csv_lab

original_path = 'data_no_dup.csv'
new_path = 'bus1.csv'

csv_list = csv_lab.csv_to_list(original_path)
new = []

for index, row in enumerate(csv_list):
	new_row = row[:]
	if index == 0:
		item = 'bus'
	else:
		item = 'None'
	new_row.append(item)
	new.append(new_row)

csv_lab.write_list_to_csv(new, new_path)