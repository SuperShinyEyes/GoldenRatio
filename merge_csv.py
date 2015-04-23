import csv, os, errno

path = 'csv/04141811/data'
file_index = 1
suffix = '.csv'

new_index = 1
new_path = 'csv/04231600/'


def merge_process(new, old):
	fieldnames = ['ads_id', 'price', 'description', 'address', 'lat', 'lng']
	reader = csv.DictReader(old)
	writer = csv.DictWriter(new, fieldnames=fieldnames)

	writer.writeheader()
	for row in reader:
		writer.writerow(row)


def merge_factory(new):
	global file_index
	for i in range(30):
		try:
			old = open(path + str(file_index) + suffix)
		except IOError:
			return False    # meaning it's done
		else:
			with old:
				merge_process(new, old)
			file_index += 1

	return True

def make_sure_path_exists(path):
	try:
		os.makedirs(path)
	except OSError as e:
		if e.errno != errno.EEXIST:
			raise


make_sure_path_exists(new_path)

while True:

	with open(new_path + 'data' + str(new_index) + suffix, 'w') as new_csv:
		if not merge_factory(new_csv):
			break
		else:
			new_index += 1

	#with open(path + file_index + suffix) as f:
