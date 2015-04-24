from lxml import html
import requests, csv, os, shutil

csv_path = '/Users/young/CODE projects/datahackathon/csv/0424-1430/data1.csv'
mockup_img_num = 0
agency_missing = 0
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
	file_path = '/Users/young/CODE projects/datahackathon/img/' + id + '.jpg'
	response = requests.get(url, stream=True)

	with open(file_path, 'wb') as out_file:
		for chunk in response.iter_content(chunk_size):
			out_file.write(chunk)        
		#out_file.write(response.content)
	del response
	print "img downloaded! id#: %s" % id


def save_mockup_img(id):
	global mockup_img_num
	mockup_img = '/Users/young/CODE projects/datahackathon/house.png'
	img_dir = '/Users/young/CODE projects/datahackathon/img/'

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
	for i in len(agencies):
		data[i+1].append(agencies[i])

	with open(new) as f:
		writer = csv.writer(f)
		writer.writerows(data)

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
		print "(%d) Agency name missing: %s" % (agency_missing, e)
	finally:
		agencies.append(agency)
		print "(%d) Agency name: %s" % (len(agencies), agency)

def take_csv_column(file):
	reader = csv.DictReader(file)
	for row in reader:
		url = row['URL']
		id = row['id']
		print url
		img_link = get_agency(url)

	add_column('agency', 'example.csv')


def take_csv_img(file, type=None):
	reader = csv.DictReader(file)
	for row in reader:
		url = row['URL']
		id = row['id']
		img_link = get_img_link(url)
		if img_link == None:
			save_mockup_img(id)
		else:
			download(url, id)



if __name__ == '__main__':
	with open(csv_path) as f:
		#take_csv(f)
		take_csv_column(f)

	print "Total mockup_img: %d" % mockup_img_num




'''
r3 = requests.get('http://www.vuokraovi.com//vuokra-asunto/helsinki/kalasatama/kerrostalo/kaksio/187925')
tree = html.fromstring(r3.text)
tree.xpath('//div[@class="rentalContactInfo"]/p/b/a/text()')
'''








