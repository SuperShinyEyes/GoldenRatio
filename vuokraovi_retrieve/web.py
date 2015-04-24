from lxml import html
import requests, unicodedata

#page2 = requests.get('http://asunnot.oikotie.fi/vuokrahaku#view=list&module=apartment-rent&offset=0&limit=48&sortby=published%20desc&arlocation[locationids][]=64|6|60.171185|24.93258|Helsinki&arpricerent[min]=&arpricerent[max]=&arsize[min]=&arsize[max]=&arsettings[changed]=1&arsettings[collapsed]=1&arbuildyear[min]=&arbuildyear[max]=&arpublished[published]=1')
page = requests.get('http://www.vuokraovi.com/searchlist?page=2')
tree = html.fromstring(page.text)

print tree

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
		string_stripped = string_stripped.strip(' /k\r\n')
	else:
		#string_stripped = ''.join(x for x in string_stripped if x not in remove_these)
		string_stripped = string_stripped.translate(None, '\r\n')
		string_stripped = ', '.join([x.strip() for x in string_stripped.split(',')])
		
	return string_stripped

#div class='size-price'
#prices = tree.xpath('//div[@class="district"]/text()')
prices = tree.xpath('//li[@class="rent"]/text()')
new_prices = []
for i in prices:
	i_stripped = i.strip()
	if i_stripped != '':
		i_stripped = strip_string(i_stripped, 'number')
		new_prices.append(i_stripped)

print [float(i) for i in new_prices]

properties = tree.xpath('//li[@class="semi-bold"]/text()')


addresses = tree.xpath('//span[@class="address"]/text()')
new_addresses = []
for i in addresses:
	i_stripped = i.strip()
	if i_stripped != '':
		i_stripped = strip_string(i_stripped)
		new_addresses.append(i_stripped)
print [strip_string(i) for i in new_addresses]

print "price: ", len(new_prices)
print "addresses: ", len(new_addresses)