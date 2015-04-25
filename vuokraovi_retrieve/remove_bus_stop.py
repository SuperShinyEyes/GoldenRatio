import csv_lab

csv_path = 'img_url.csv'

csv_list = csv_lab.csv_to_list(csv_path)
column = ['None']

for index, row in enumerate(csv_list):
	if index == 0:
		continue
	row[-2] = 'None'
	row[-1] = 'None'

csv_lab.write_list_to_csv(csv_list, 'img_url2.csv')