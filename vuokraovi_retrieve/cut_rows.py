import csv

original_path = '/Users/young/datahackathon/vuokraovi_retrieve/data_bus_stop.csv'
new_path = '/Users/young/datahackathon/vuokraovi_retrieve/mini.csv'

def cut(row_len):

	with open(original_path) as origianl_file:
		original = [i for i in csv.reader(origianl_file)]

		with open(new_path, 'w') as new_file:
			writer = csv.writer(new_file)
			writer.writerows(original[:row_len+1])

cut(10)

