from lxml import html
import requests, unicodedata, json, time, csv, os, errno
from datetime import datetime

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
total_count = 0
getcoord_retrieve_failed = 0
now = datetime.now().strftime("%m%d%H%M")

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


def process_string_list(raw, type=None):
	processed = []
	for i in raw:
		i_stripped = i.strip()
	
		if i_stripped != '':
			i_stripped = strip_string(i_stripped, type)
			processed.append(i_stripped)

	return processed

def get_geocoor(address):
	global geocoor, error_count, getcoord_retrieve_failed
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
			"""
			This error is due to too fast requests from Google maps api.
			Rest for two seconds and repeat twice more if failed.
			"""
			print "(%d) Error getting geocoordinates: %s" % (attempts, e)
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
	global addresses, prices
	addresses += new_addresses
	prices += new_prices
	for address in new_addresses:
		get_geocoor(address)


def filter_region(new_prices, new_addresses):
	"""
	Add only the ones from Helsinki and Espoo
	"""
	filtered_prices = []
	filtered_addresses = []
	regions = ['helsinki,', 'espoo,']
	for index, address in enumerate(new_addresses):
		region = address.split()[0].lower()
		
		if region in regions:
			filtered_prices.append(new_prices[index])
			filtered_addresses.append(address)

	return filtered_prices, filtered_addresses


def get_dict(index):
	"""
	Create a dict to insert either to json or csv.
	"""
	apt_dict = {}
	apt_dict['ads_id'] = total_count + index + 1
	apt_dict['price'] = prices[index]
	apt_dict['description'] = ''
	apt_dict['address'] = addresses[index]
	apt_dict['lat'] = geocoor[index][0]
	apt_dict['lng'] = geocoor[index][1]
	return apt_dict


def write_json(suffix):
	with open('data' + suffix + '.json', 'w') as f:
		for i in range(len(addresses)):
			dic = get_dict(i)
			json.dump(dic, f)


def make_sure_path_exists(path):
	try:
		os.makedirs(path)
	except OSError as e:
		if e.errno != errno.EEXIST:
			raise


def write_csv(suffix):
	path = 'csv/' + now + "/"
	make_sure_path_exists(path)

	path += 'data' + suffix + '.csv'
	with open(path, 'w') as f:
		fieldnames = ['ads_id', 'price', 'description', 'address', 'lat', 'lng']
		writer = csv.DictWriter(f, fieldnames=fieldnames)
		writer.writeheader()
		for i in range(len(addresses)):
			dic = get_dict(i)
			writer.writerow(dic)



if __name__ == '__main__':
	print "Scraping starts!"

	while True:
		"""
		Scrape until the new search result is the same as the old one.
		In other words, scrape until it reaches the last page.
		vuokraovi.com doesn't throw an error even if the page number exceeds.
		"""
		r = requests.get(url + str(page_index))
		tree = html.fromstring(r.text)

		prices_scraped = tree.xpath('//li[@class="rent"]/text()')
		addresses_scraped = tree.xpath('//span[@class="address"]/text()')

		new_prices = process_string_list(prices_scraped, 'number')
		new_addresses = process_string_list(addresses_scraped)
		#print "number of item per page:", len(new_addresses)

		## Eliminate the offers outside the region of our interest
		new_prices, new_addresses = filter_region(new_prices, new_addresses)

		#print "total"
		#print addresses[-len(new_addresses):]
		#print "new"
		#print new_addresses 
		if(addresses[-len(new_addresses):] == new_addresses):
			write_csv(str(page_index / 20 + 1))
			print "Ended the end of the database!"
			break

		append_list(new_prices, new_addresses)

		print "Scraped page", page_index
		page_index += 1
		
		"""
		Write to a csv file every 20 pages.
		20 ads * 20 pages = 400 ads
		In reality it will be less than 400, because 
		regions outside Helsinki and Espoo will be eliminated
		"""
		interval = 40
		if page_index % interval == 0:
			write_csv(str(page_index / interval))
			total_count += len(prices)
			del prices[:]
			del addresses[:]
			del geocoor[:]
























