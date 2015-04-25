from lxml import html
import requests, csv, os, shutil, unicodedata, json, time

csv_path = '/Users/young/datahackathon/csv/0424-1430/data1.csv'
mockup_img_num = 0
agency_missing = 0
total = 0
error_count = 0
agencies = []
"""
Open csv file and get URL one by one
Open Request and get src.
tree.xpath('//div[@id="mainImageSlider"]/img[@itemprop="contentURL"]/attribute::src')
This will give lists of URLs.
The image url should start with 'http://' and ends with '.jpg'
Save the image and the name should be 'id#.jpg'
"""
def download(url, id):
	chunk_size = 10
	file_path = '/Users/young/datahackathon/img/' + id + '.jpg'
	response = requests.get(url, stream=True)

	with open(file_path, 'wb') as out_file:
		for chunk in response.iter_content(chunk_size):
			out_file.write(chunk)        
		#out_file.write(response.content)
	del response
	print url
	print "img downloaded! id#: %s" % id


def save_mockup_img(id):
	global mockup_img_num
	mockup_img = '/Users/young/datahackathon/house.png'
	img_dir = '/Users/young/datahackathon/img/'

	shutil.copy(mockup_img, img_dir + id + '.jpg')
	mockup_img_num += 1
	print "Saved mockup image for %s" % id

def get_img_link(url):
	r = requests.get(url)
	tree = html.fromstring(r.text)
	path = '//div[@id="mainImageSlider"]/img[@itemprop="contentURL"]/attribute::src'
	img_url_list = tree.xpath(path)
	if len(img_url_list) == 0:
		return None
	else:
		return img_url_list[0]

def get_csv(name):
	with open(name) as f:
		d = [i for i in csv.reader(f)]
	return d

def add_column(column, new):
	data = get_csv(csv_path)
	data[0].append(column)
	for i in range(len(agencies)):
		data[i+1].append(agencies[i])

	with open(new, 'w') as f:
		writer = csv.writer(f)
		writer.writerows(data)

def write_to_text(url, e):
	with open('output2.txt', 'a') as f:
		f.write(url)
		f.write("\n(%d) Agency name missing: %s\n" % (agency_missing, e))


def strip_string(string, type=None):
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
		string_stripped = string_stripped.translate(None, '\r\n')
		
	return string_stripped

def get_agency(url):
	global agencies, agency_missing
	r = requests.get(url)
	tree = html.fromstring(r.text)
	path = '//div[@id="rentalContactInfo"]/p/b/a/text()'
	agency_list = tree.xpath(path)
	try:
		agency = agency_list[0]
	except IndexError as e:
		agency_missing += 1
		agency = "Agency info missing"
		write_to_text(url, e)
		print url
		print "(%d) Agency name missing: %s" % (agency_missing, e)
	else:
		agency = strip_string(agency)
		print "(%d) Successful!" % total
	finally:
		agencies.append(agency)
		#print "(%d) Agency name: %s" % (len(agencies), agency)

def take_csv_column(file):
	global total
	reader = csv.DictReader(file)

	for row in reader:
		url = row['URL']
		id = row['id']
		#print url
		img_link = get_agency(url)
		total += 1

	add_column('agency', 'example.csv')


def take_csv_img(file, type=None):
	global total
	reader = csv.DictReader(file)
	for row in reader:
		url = row['URL']
		id = row['id']
		img_link = get_img_link(url)
		if img_link == None:
			save_mockup_img(id)
		else:
			download(img_link, id)
		total += 1
		print "(%d) Saved!" % total


def get_coor(address):
	global error_count
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
				return (0, 0)
		else:
			success = True
			print (lat, lng)
			return (lat, lng)


def edit_coor(row, coor):
	new = row[:]
	new[-3:-1] = coor
	return new


def take_csv_coor(file):
	global total
	data = get_csv('data_agency.csv')
	new = []
	
	for row in data:	
		if row[-3] == '0':
			address = row[3]
			coor = get_coor(address)
			row = edit_coor(row, coor)

		new.append(row)
		total += 1
		print "(%d) Row!" % total

	with open('data_all.csv', 'w') as f:
		writer = csv.writer(f)
		writer.writerows(new)


if __name__ == '__main__':
	with open(csv_path) as f:
		#take_csv_img(f)
		#take_csv_column(f)
		take_csv_coor(f)

	print "Total mockup_img: %d" % mockup_img_num




'''
r3 = requests.get('http://www.vuokraovi.com//vuokra-asunto/helsinki/kalasatama/kerrostalo/kaksio/187925')
tree = html.fromstring(r3.text)
tree.xpath('//div[@class="rentalContactInfo"]/p/b/a/text()')
'''








