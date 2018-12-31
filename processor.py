#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import csv
import requests
import shutil
import openpyxl
import asyncio
from number import getPhone
from bs4 import BeautifulSoup
from selenium import webdriver
from PyQt5.QtWidgets import (QMainWindow)


class Processor(object):
	
	def __init__(self):
		self.file_name = ''
		self.file = ''
		self.array_len = 0
		self.completed = 0
		self.loop_ = asyncio.new_event_loop()

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
		workbook = openpyxl.load_workbook(self.file)
		sheet = workbook.active
		
		i+=1
		c1 = sheet.cell(row=i, column=1)
		c1.value = data['title']
		
		c2 = sheet.cell(row=i, column=2)
		c2.value = data['price']
		
		c3 = sheet.cell(row=i, column=3)
		c3.value = data['address']
		
		c4 = sheet.cell(row=i, column=4)
		c4.value = data['phone']

		c5 = sheet.cell(row=i, column=5)
		c5.value = data['url']

		workbook.save(self.file)
		

	async def get_page_data(self, html):
		soup = BeautifulSoup(html, 'lxml')
		
		ads = soup.find('div',
			class_='catalog-list').find_all('div',
			class_='item_table')
		
		self.array_len = len(ads)
		
		self.file = self.file_name + '.xlsx'
		book = openpyxl.Workbook(self.file)
		book.save(self.file)

		i = 0 
		for ad in ads:
			
			try:
				title = ad.find('div', class_='description').find('h3').text.strip()
			except:
				title = ''

			try:
				url = 'https://www.avito.ru' + ad.find('div', class_='description').find('h3').find('a').get('href')
				m_url = 'https://m.avito.ru/' + ad.find('div', class_='description').find('h3').find('a').get('href')
			except:
				url = ''

			try:
				price = ad.find('div', class_='about').text.strip()
			except:
				price = ''

			try:
				phone = getPhone(m_url)
			
			except:
				phone = ''

			try:
				address = ad.find('p', class_='address').text.strip()
			except:
				address = ''

			data = {
				'title': title,
				'price': price,
				'address': address,
				'phone': phone,
				'url': url
			}
			print('request', i)
			#self.file_writer_csv(data)
			self.file_save_xlsx(data, i)
			self.complited = i
			i+=1
			await asyncio.sleep(1)
		
		directory = "~/Desktop/avito_parser/"
		directory = os.path.expanduser(directory)
			
		if not os.path.exists(directory):
			os.makedirs(directory)
		
		direct = directory + self.file
		
		shutil.copy2(self.file, direct) 
		os.remove(self.file)
		self.loop_.stop()
	
	async def result_hub(self, city, category):
		self.file_name = city + '_' + category
		
		base_url = 'https://www.avito.ru/'
		part = '?p='
		tasks = []
		
		for i in range(1, 2):
			url_gen = base_url + city + '/' + category + '/' + part + str(i)
			html = self.get_html(url_gen)
			tasks += [  
				asyncio.ensure_future(self.get_page_data(html)),
			]
		await asyncio.sleep(1)
		self.loop_.run_until_complete(asyncio.wait(tasks))
		self.loop_.stop()

		

			

	


