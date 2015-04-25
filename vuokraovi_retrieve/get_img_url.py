from lxml import html
import requests, csv, os, shutil, unicodedata, json, time, csv_lab

csv_path = '/Users/young/datahackathon/vuokraovi_retrieve/no_decimal_imgage.csv'
mockup_img_url = 'http://icons.iconarchive.com/icons/double-j-design/origami-colored-pencil/256/blue-home-icon.png'
mockup_img_num = 0
agency_missing = 0
total = 0
error_count = 0
urls = []

def get_img_url(url):
	r = requests.get(url)
	tree = html.fromstring(r.text)
	path = '//div[@id="mainImageSlider"]/img[@itemprop="contentURL"]/attribute::src'
	img_url_list = tree.xpath(path)
	if len(img_url_list) == 0:
		return None
		print "No image"
	else:
		return img_url_list[0]

print "start!"
csv_list = csv_lab.csv_to_list(csv_path)
for index, row in enumerate(csv_list):
	if index == 0:
		continue
	ad_url = row[4]
	id = row[0]
	img_url = get_img_url(ad_url)
	if img_url == None:
		urls.append(mockup_img_url)
	else:
		urls.append(img_url)
	
	total += 1
	if total % 10 == 0:
		print "(%d) link Saved!" % total


csv_lab.modify_row_item(csv_list, [urls], 5, 'img_url.csv')
		










