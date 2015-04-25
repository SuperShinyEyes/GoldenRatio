import csv_lab

csv_path = '/Users/young/datahackathon/vuokraovi_retrieve/no_decimal.csv'
csv_list = csv_lab.csv_to_list(csv_path)

pos = 5
columns = ['image']
new_path = 'no_decimal_imgage.csv'
csv_lab.insert_column(csv_list, columns, 5, new_path)
