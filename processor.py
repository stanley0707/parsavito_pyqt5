#!/usr/bin/python3
# -*- coding: utf-8 -*-

import csv
import requests
#import xlsxwriter
import openpyxl
import pandas as pd
from bs4 import BeautifulSoup


class Process(object):
	
	def __inti__(self):
		self.file_name = ''
	
	def transliterate(self, name):
	
		slovar = {'а':'a','б':'b','в':'v','г':'g','д':'d','е':'e','ё':'e',
				'ж':'zh','з':'z','и':'i','й':'i','к':'k','л':'l','м':'m','н':'n',
				'о':'o','п':'p','р':'r','с':'s','т':'t','у':'u','ф':'f','х':'h',
				'ц':'c','ч':'cz','ш':'sh','щ':'scz','ъ':'','ы':'y','ь':'','э':'e',
				'ю':'u','я':'ya', 'А':'a','Б':'b','В':'v','Г':'g','Д':'d','Е':'e','Ё':'e',
				'Ж':'zh','З':'z','И':'i','Й':'i','К':'k','Л':'l','М':'m','Н':'n',
				'О':'o','П':'p','Р':'r','С':'s','Т':'t','У':'u','Ф':'F','х':'h',
				'Ц':'c','Ч':'cz','Ш':'sh','Щ':'scz','Ъ':'','Ы':'y','Ь':'','Э':'e',
				'Ю':'u','Я':'ya',',':'','?':'',' ':'_','~':'','!':'','@':'','#':'',
				'$':'','%':'','^':'','&':'','*':'','(':'',')':'','-':'','=':'','+':'',
				':':'',';':'','<':'','>':'','\'':'','"':'','\\':'','/':'','№':'',
				'[':'',']':'','{':'','}':'','ґ':'','ї':'', 'є':'','Ґ':'g','Ї':'i',
				'Є':'e'
			}
	
		for key in slovar:
			name = name.replace(key, slovar[key])
		return name
	
	def get_html(self, url):
		r = requests.get(url)
		return r.text

	def get_total_pages(self, html):
		"""
		разбираем юрл и берем кол-во страниц
		"""
		soup = BeautifulSoup(html, 'lxml')
		pages = soup.find('div', 
			class_='pagination-pages').find_all(
				'a', class_='pagination-page')[-1].get('href')
		total_pages = pages.spli('=')[1].split("&")[0]

		return int(total_pages)
	
	"""
	def file_writer_csv(self, data):
		
		file = self.file_name + '.csv'
		
		with open(file, 'a') as f:
			writer = csv.writer(f)

			writer.writerow({data['title'],
									data['price'],
									data['address'],
									data['url']})
			f.close()
	"""

	def file_save_xlsx(self, data, i):
		"""
		Write xlsx
		"""

		file = self.file_name + '.xlsx'

		workbook = openpyxl.load_workbook(file)
		sheet = workbook.active
		
		i+=1
		c1 = sheet.cell(row=i, column=1)
		c1.value = data['title']
		
		c2 = sheet.cell(row=i, column=2)
		c2.value = data['price']
		
		c3 = sheet.cell(row=i, column=3)
		c3.value = data['address']
		
		c4 = sheet.cell(row=i, column=4)
		c4.value = data['url']

		workbook.save(file)
		#worksheet = workbook.add_worksheet('worksheet')
		#worksheet.set_column('A:A', 50)
		#link_format = workbook.add_format({'color': 'blue', 
		#                                   'underline': True, 
		#                                   'text_wrap': True})
		#worksheet.write(0, i, data['title'])
		#worksheet.write(1, i, data['price'])
		#worksheet.write(2, i, data['address'])
		#worksheet.write(3, i, data['url'])
		#workbook.close()
		#print(i) 

	def get_page_data(self, html):
		soup = BeautifulSoup(html, 'lxml')

		ads = soup.find('div',
			class_='catalog-list').find_all('div',
			class_='item_table')
		
		i = 0 
		#print(len(ads))
		for ad in ads:
			
			try:
				title = ad.find('div', class_='description').find('h3').text.strip()
			except:
				title = ''

			try:
				url = 'https://www.avito.ru' + ad.find('div', class_='description').find('h3').find('a').get('href')
			except:
				url = ''

			try:
				price = ad.find('div', class_='about').text.strip()
			except:
				price = ''

			try:
				address = ad.find('p', class_='address').text.strip()
			except:
				address = ''

			data = {
				'title': title,
				'price': price,
				'address': address,
				'url': url
			}
			#self.file_writer_csv(data)
			self.file_save_xlsx(data, i)
			i+=1

	def result_hub(self, city, category):
		self.file_name = city + '_' + category
		
		base_url = 'https://www.avito.ru/'
		part = '?p='
		
		#total_pages = get_total_pages(get_html())
		
		for i in range(1, 4):
			url_gen = base_url + city + '/' + category + '/' + part + str(i)
			html = self.get_html(url_gen)
			self.get_page_data(html)

