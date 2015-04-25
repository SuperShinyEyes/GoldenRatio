import csv

original_path = '/Users/young/datahackathon/vuokraovi_retrieve/data_bus_stop_full.csv'
new_path = '/Users/young/datahackathon/vuokraovi_retrieve/data_bus_stop_full2.csv'

def check_swap(original):
	new = original[:]
	for row_index, row in enumerate(original):
		for item_index, item in enumerate(row):
			if item == '0':
				new[row_index][item_index] = 'None'
	return new


def swap():

	with open(original_path) as origianl_file:
		original = [i for i in csv.reader(origianl_file)]

		original = check_swap(original)

		with open(new_path, 'w') as new_file:
			writer = csv.writer(new_file)
			writer.writerows(original)

swap()

