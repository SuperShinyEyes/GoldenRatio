import csv, csv_lab

original_path = 'data1.csv'
new_path = 'mini.csv'

def cut(row_len):

	with open(original_path) as origianl_file:
		original = [i for i in csv.reader(origianl_file)]

		with open(new_path, 'w') as new_file:
			writer = csv.writer(new_file)
			writer.writerows(original[:row_len+1])

#cut(10)


csv_lab.cut(original_path, new_path, 0, 10)