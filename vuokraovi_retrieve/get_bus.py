import requests, csv, yaml, json, csv_lab

csv_path = 'bus7.csv'
new_path = 'bus8.csv'
another_path = '/Users/young/Documents/datahackathon_file/bus_stop/' + new_path
capacity_empty = False
no_bus = 0
total = 0


total_rows = []
'''
http://api.reittiopas.fi/hsl/prod/?request=stop&user=chendurkumar&pass=manimangai&format=txt&code=E2217&format=json
'''

#api = 'http://api.reittiopas.fi/hsl/prod/?request=stop&user=claudio&pass=claudio&format=txt&code=E1101&format=json'

def get_buses(bus_stop_code):
	global no_bus, capacity_empty
	api_prefix = 'http://api.reittiopas.fi/hsl/prod/?request=stop&user=claudio&pass=claudio&format=txt&code='
	api_suffix = '&format=json'
	api = api_prefix + bus_stop_code + api_suffix
	r = requests.get(api)
	try:
		r.json()
	except ValueError as e:
		no_bus += 1
		
		print "(%d) Capacity all used" % no_bus
		return ['0']
	else:
		buses = csv_lab.unicode_to_str(r)[0]['lines']
		buses = [csv_lab.strip_string(bus) for bus in buses]
		buses = [bus.split()[0] for bus in buses]
		buses = [bus.split(':')[0] for bus in buses]
		buses = list(set(buses))   # remove duplicates
		return buses


def scrape(row, path):
	bus_stop_code = row[-3]
	buses = get_buses(bus_stop_code)
	
	## Duplicate the row as many as the number of bus stops
	new_row = [row[:] for __ in range(len(buses))]
	
	for index, bus in enumerate(buses):
		new_row[index][-1] = bus

	return new_row


def write_csv(data, path):
	with open(path, 'w') as f:
		writer = csv.writer(f)
		writer.writerows(data)
	print "!!!DONE!!!"


def take_csv(list):
	global total, rows
	
	for i in range(len(list)):
		row = list[i]
		if row[-1] == "None":    # bus
			print "go scraping"
			row = scrape(row, new_path)
		else:
			row = [row]
		for i in row:
			total_rows.append(i)
		
		total += 1
		if total % 10 == 0:
			print "(%d) Done." % total
	
	csv_lab.write_list_to_csv(total_rows, new_path)
	csv_lab.write_list_to_csv(total_rows, another_path)


csv_list = csv_lab.csv_to_list(csv_path)
take_csv(csv_list)
















