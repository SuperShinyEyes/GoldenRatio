from lxml import html
import requests, unicodedata, json, time

"""
Must add an index(integer) in the end. It usually has up to 470 pages
Vuokraovi doesn't throw an error when page number exceeds
Instead, it will always show the last page.
http://maps.google.com/maps/api/geocode/json?address=
"""
url = 'http://www.vuokraovi.com/vuokra-asunnot/Uusimaa?page='
page_index = 1

prices = []
addresses = []
geocoor = []    # [(latitude, longitude)] -> [(60.14334, 24.72134)]
error_count = 0
total_item_num = 0

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
		string_stripped = float(string_stripped.strip(' /k\r\n'))
	else:
		string_stripped = string_stripped.translate(None, '\r\n')
		string_stripped = ', '.join([x.strip() for x in string_stripped.split(',')])
		
	return string_stripped


def process_string_list(raw, type=None):
	processed = []
	for i in raw:
		i_stripped = i.strip()
	
		if i_stripped != '':
			i_stripped = strip_string(i_stripped, type)
			processed.append(i_stripped)

	return processed


def get_geocoor(address):
	global geocoor, error_count
	success = False
	attempts = 0
	api = 'http://maps.google.com/maps/api/geocode/json?address='
	while success != True and attempts < 3:
		attempts += 1
		r = requests.get(api + address)
		parsed = json.loads(r.content)

		try:
			lat = parsed[u'results'][0][u'geometry'][u'location'][u'lat']
			lng = parsed[u'results'][0][u'geometry'][u'location'][u'lng']
		except IndexError as e:
			print "(%d) Error getting geocoordinates: %s" % (attempts, e)
			"""
			This error is due to too fast requests from Google maps api.
			Rest for two seconds and repeat twice more if failed.
			"""
			time.sleep(2)
			if attempts < 2:
				continue
			else:
				error_count += 1
				print "(%d) 3 Attempts all failed" % (error_count)
				print address
				## If failed three times, add a mock up coordinate
				geocoor.append((0, 0))
		else:
			geocoor.append((lat, lng))
			success = True


def append_list(new_prices, new_addresses):
	"""
	Add only the ones from Helsinki and Espoo
	"""
	global addresses, prices
	regions = ['helsinki,', 'espoo,']
	for index, address in enumerate(new_addresses):
		region = address.split()[0].lower()
		#print index, region
		if region in regions:
			#print 'true'
			addresses.append(address)
			prices.append(new_prices[index])
			get_geocoor(address)

def get_dict(index):
	"""
	Create a dict to insert either to json or csv.
	"""
	apt_dict = {}
	apt_dict['ads_id'] = total_item_num + index + 1
	apt_dict['price'] = prices[index]
	apt_dict['description'] = ''
	apt_dict['address'] = addresses[index]
	apt_dict['lat'] = geocoor[index][0]
	apt_dict['lat'] = geocoor[index][1]
	return apt_dict

def write_json(suffix):
	with open('data' + suffix + '.json', 'w') as f:
		for i in range(len(addresses)):
			dic = get_dict(i)
			json.dump(dic, f)


print "Scraping starts!"

while True:
	"""
	Scrape until the new search result is the same as the old one.
	"""
	r = requests.get(url + str(page_index))
	tree = html.fromstring(r.text)

	prices_scraped = tree.xpath('//li[@class="rent"]/text()')
	addresses_scraped = tree.xpath('//span[@class="address"]/text()')

	new_prices = process_string_list(prices_scraped, 'number')
	new_addresses = process_string_list(addresses_scraped)

	if(addresses[-len(new_addresses):] == new_addresses):
		print "Ended the end of the database!"
		break

	## Eliminate the offers outside the region of our interest
	append_list(new_prices, new_addresses)		

	print "Scraped page", page_index
	page_index += 1
	#print prices
	#print addresses
	#print geocoor
	if page_index % 20 == 0:
		write_json(str(page_index / 20))
		total_item_num += len(prices)
		prices = []
		addresses = []
		geocoor = []
























