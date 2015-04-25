import requests, csv, yaml, json, csv_lab

csv_path = '/bus_stop_None.csv'
new_path = 'bus_stop_None2.csv'
DIAMETER = 500    # The unit is Meter
total = 0
no_bus_stop = 0
MOCK_UP = [{'codeShort':'0', 'dist':'0'}]
total_rows = []
'''
!!!ATTENTION!!!
HSL system doesn't wgs84 coordinate system by default but can interpret it.
Their default is espg.
Add "epsg_in=wgs84&epsg_out=wgs84" to your query.
example request
http://api.reittiopas.fi/hsl/prod/?request=stops_area&center_coordinate=24.815548,60.187078&diameter=500&epsg_in=wgs84&epsg_out=wgs84&user=chendurkumar&pass=manimangai

Result:
[{"code":"2222225","name":"Innopoli, Laituri 2","city":"Espoo","coords":"24.813107985823,60.186165322784","dist":169,"codeShort":"E2220","address":"Tekniikantie"},
{"code":"2222226","name":"Innopoli, Laituri 1","city":"Espoo","coords":"24.81426713798,60.184937496573","dist":249,"codeShort":"E2221","address":"Tekniikantie"}]

There are two bus stops nearby.

Save both "code" and "codeShort", and distance.

60.2169587
http://api.reittiopas.fi/hsl/prod/?request=stop&user=claudio&pass=claudio&format=txt&code=1411101&format=json
'''


def get_buses(bus_stop_code):
	'''
	Search in the radius of 500 meters.
	'''
	global no_bus_stop
	#print "lng: %s, lat: %s" % (lng, lat)

	api_prefix = 'http://api.reittiopas.fi/hsl/prod/?request=stop&user=claudio&pass=claudio&format=txt&code='
	api_suffix = '&format=json'
	api = api_prefix + bus_stop_code + api_suffix
	r = requests.get(api)
	try:
		r.json()
	except ValueError as e:
		no_bus_stop += 1
		print "(%d) There is no bus stop with in %d meters of diameter at %s, %s" % (no_bus_stop, DIAMETER, lng, lat)
		return MOCK_UP
	else:
		buses = csv_lab.unicode_to_str(r)[0]['lines']
		buses = [csv_lab.strip_string(bus) for bus in buses]
		buses = [bus.split()[0] for bus in buses]
		return buses

def scrape(row, path):
	bus_stop_code = row[:-3]
	buses = get_bus_stop(bus_stop_code)
	
	## Duplicate the row as many as the number of bus stops
	new = [row[:] for __ in range(len(buses))]
	
	for index, bus in enumerate(buses):
		new[index][-1] = bus

	return new


def write_csv(data, path):
	with open(path, 'w') as f:
		writer = csv.writer(f)
		writer.writerows(data)
	print "!!!DONE!!!"


def take_csv(list):
	global total, rows
	
	for i in range(len(list)):
		row = list[i]
		if row[-1] == "None":    # dist
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


csv_list = csv_lab.csv_to_list(csv_path)
take_csv(csv_list)



















