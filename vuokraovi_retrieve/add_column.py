import csv

csv_path = '/Users/young/datahackathon/csv/apartments.csv'


def get_csv(name):
	with open(name) as f:
		d = [i for i in csv.reader(f)]
	return d

def add_column(columns, new):
	data = get_csv(csv_path)
	for c in columns:
		data[0].append(c)

	empty_data = ['None' for __ in range(len(columns))]

	for i in range(len(data) - 1):
		data[i+1] += empty_data

	with open(new, 'w') as f:
		writer = csv.writer(f)
		writer.writerows(data)


add_column(['bus_stop_code', 'dist'], 'data_bus_stop.csv')
print "Done!"