import csv_lab

csv_path = 'img_url2.csv'
new_path = 'data1.csv'

csv_list = csv_lab.csv_to_list(csv_path)
new = []
def is_end(index):
	return index + 1 == len(csv_list)

for row in csv_list:
	is_empty = len(new) == 0
	if not is_empty:
		is_diff = new[-1][0] != row[0]
	if is_empty or is_diff:
		new.append(row)
	
csv_lab.write_list_to_csv(new, new_path)
	