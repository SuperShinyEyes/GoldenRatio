import requests, csv, yaml, json


def unicode_to_str(response):
	dump = json.dumps(response.json())
	return yaml.safe_load(dump)


def write_list_to_csv(list, path):
	with open(path, 'w') as f:
		writer = csv.writer(f)
		writer.writerows(list)
	print("CSV file was written to\n %s" % path)


def csv_to_list(csv_path):
	with open(csv_path) as f:
		return [row for row in csv.reader(f)]

## append_column(['bus_stop_code', 'dist'], 'data_bus_stop.csv')
def append_column(old_csv_list, columns, new_path):
	csv_list = old_csv_list[:]

	## Add to header
	for c in columns:
		csv_list[0].append(c)

	## Fill the new column with None
	empty_data = ['None' for __ in range(len(columns))]

	for i in range(len(csv_list) - 1):
		csv_list[i+1] += empty_data

	write_list_to_csv(csv_list, new_path)


def insert_column(old_csv_list, columns, pos, new_path):
	csv_list = old_csv_list[:]
	## Add to header
	csv_list[0] = csv_list[0][:pos] + columns + csv_list[0][pos:]

	## Fill the new column with None
	empty_data = ['None' for __ in range(len(columns))]

	for i in range(len(csv_list) - 1):
		csv_list[i+1] = csv_list[i+1][:pos] + empty_data[i] + csv_list[i+1][pos:]

	write_list_to_csv(csv_list, new_path)		

def column_transpose(columns):
	length = len(columns[0])
	transposed = []
	for i in range(length):
		transposed.append([column[i] for column in columns])
	return transposed


def modify_row_item(old_csv_list, columns, pos, new_path):
	error_count = 0
	csv_list = old_csv_list[:]
	mockup_img_url = ['http://icons.iconarchive.com/icons/double-j-design/origami-colored-pencil/256/blue-home-icon.png']
	transposed = column_transpose(columns)
	print transposed

	for i in range(len(csv_list) - 1):
		try:
			csv_list[i+1] = csv_list[i+1][:pos] + transposed[i] + csv_list[i+1][pos+1:]
		except IndexError as e:
			error_count += 1
			print "(%d) Save mockup image url: %s" % (error_count, e)
			csv_list[i+1] = csv_list[i+1][:pos] + mockup_img_url + csv_list[i+1][pos+1:]

	write_list_to_csv(csv_list, new_path)


def strip_string(string, type=None):
	remove_these = '\r\n'
	## Convert from unicode to ASCII string
	if isinstance(string, unicode):
		string_stripped = unicodedata.normalize('NFKD', string).encode('ascii', 'ignore') 
	else:
		string_stripped = string
	
	## '1 200,50 / kk'(rent per month) -> '1200.50' 
	if type == 'number':
		string_stripped = string_stripped.replace(' ', '')
		string_stripped = string_stripped.replace(',', '.')
		string_stripped = (string_stripped.strip(' \r\n'))
		string_stripped = float(string_stripped.split('/')[0])
	else:
		#string_stripped = ''.join(x for x in string_stripped if x not in remove_these)
		string_stripped = string_stripped.translate(None, '\r\n')
		string_stripped = ', '.join([x.strip() for x in string_stripped.split(',')])
		
	return string_stripped

def remove_decimal(item):
	return item.split('.')[0]

def cut(original_path, new_path, row_beg, row_end):
	original = csv_to_list(original_path)

	with open(new_path, 'w') as file:
		writer = csv.writer(file)
		writer.writerows(original[row_beg:row_end])
	print("%s was cut ")



