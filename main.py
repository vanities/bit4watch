from urllib.request import urlopen, urlretrieve
from json import loads
from random import randint
from time import sleep
from os.path import join, expanduser, isfile, exists
from os import makedirs
from subprocess import call
from sys import stdout
import csv

ops=[]

names = ['bitcoin', 'Bitcoin', 'Btc', 'BTC', 
		  'litecoin', 'Litecoin', 'ltc', 'LTC', 'Ltc,'
		  'etherium', 'Etherium', 'Eth', 'ETH',
		  'tron', 'Tron', 'TRON',
		  'neo', 'NEO', 'Neo',
		  'REQ', 'Request',
		  'XLM'
		  'XRP', 'xrp', 'Xrp', 'Ripple', 'ripple',
		  'ark', 'ARK',
		  'Bat', 'BAT',
		  'XMR', 'Xmr', 'xmr', 'Monero', 'monero',
		  'Link', 'LNK', 'LINK',
		  'Wabi', 'WABI', 'wabi',
		  'OMG', 'omg', 'Omg',
		  'NEM', 'Nem', 'nem',
		  'Dash', 'DASH', 'dash'
		  ]

def main():
	check_posts()
	output_csv()

def check_posts():
	# uses the 4chan api to get an image from /wg/			

	sticky=False
	
	for page in range(1,9):
		for thread in range(0,14):

			print('page: ', page, 'thread: ', thread)

			# make sure we recieve the object from the api
			try:
				post=0

				op={}

				with urlopen('https://a.4cdn.org/biz/' + str(page) + '.json') as url:
					json = loads(url.read().decode())

					# set the thread and post
					thread = json['threads'][thread]

					OP = thread['posts'][0]

					print(OP)

					if 'name' in OP:
						op['name'] = OP['name']
					else:
						op['name'] = 'None'


					op['time'] = OP['now']


					if 'sub' in OP:
						op['title'] = OP['sub']

						for x in names:
							if x in op['title']:
								op['shill'] = x

					else:
						op['title'] = 'None'


					if 'com' in OP:
						op['post'] = OP['com']

						for x in names:
							if x in op['post']:
								op['shill2'] = x
					else:
						op['post'] = 'None'



					if 'replies' in OP:
						op['replies'] = OP['replies']
					else:
						op['replies'] = 'None'

					ops.insert(post,op)
					post+=1



			except (HTTPError):
				print('Could not connect to /biz/..')
				sleep(1)	 # api rule
				main()


			# take a breather for a second
			sleep(1)

def output_csv():
	keys = ops[0].keys()
	with open('data.csv', 'a') as output_file:
		dict_writer = csv.DictWriter(output_file, keys)
		dict_writer.writeheader()
		dict_writer.writerows(ops)


if __name__ == "__main__":
	main()