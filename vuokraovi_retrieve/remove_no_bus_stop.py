import csv_lab

original_path = 'bus5.csv'
new_path = 'bus6.csv'

csv_list = csv_lab.csv_to_list(original_path)
new = []

for row in csv_list:
	if row[-1] != '0' and row[-1] != 'None':
		new.append(row)

csv_lab.write_list_to_csv(new, new_path)
