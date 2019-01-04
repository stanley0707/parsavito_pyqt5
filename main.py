#!./env/lib/python3
# -*- coding: utf-8 -*-
import os
import sys
import slug
import json
import asyncio
import requests
from PyQt5 import QtGui
from processor import Processor
from PyQt5.QtCore import pyqtSlot, QSize, Qt
from PyQt5.QtWidgets import (QMainWindow,  QLabel, QHBoxLayout, QApplication, QWidget,
	QPushButton, QAction, QLineEdit, QInputDialog, QMessageBox, QProgressBar)
from requests.exceptions import ConnectionError

class App(QMainWindow):
	def __init__(self):
		super().__init__()
		self.connect = False
		self.activate_status = self.check_activate()
		try:
			requests.post('http://google.com')
			self.message = 'После сканирования будет создан .xlsx документ \nс полученными данными'
			self.connect = True
		
		except ConnectionError:
			self.message = 'Содениние неустановлено, проверьте подключение'
		
		self.title = 'Поиск объектов avito'
		self.left = 200
		self.top = 200
		self.width = 880
		self.height = 370
		self.path_activate = 'activate_processor.json'
		self.proc = Processor()
		self.loop = asyncio.get_event_loop()
		# css love
		self.setStyleSheet("""
			App {
				background-image: url(humster.png);
				background-color:#D1CAC2;
				background-repeat: no-repeat;
				background-position: right
				}
			
			QLabel {
				font-size: 14px;
				font-weight 700;
				color:#fff;
				}
			
			QMessageBox{
				font-size: 14px;
				font-weight 700;
				background-color:#D1CAC2;
				color:#fff;
			}
			QLineEdit {
				border-radius: 5px;
			}
			
			QPushButton {
			  border-radius: 5px;
			  color:#f7f7f7;
			  font-size: 15px;
			  border: 2px solid #f7f7f7;
			  text-align: center;
			  padding: 1px 6px;
			}
			
			QPushButton:hover{ 
				color: #fff;
				font-size: 15px;
				border: 2px solid #fff
			}"
				""")
		self.initUi()
	
	def check_activate(self):
		return True if os.path.exists('key_.key') else False

	def initUi(self):
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)
		
		self.lbl1 = QLabel(self.message, self)
		self.lbl1.move(80, 0)
		self.lbl1.resize(420, 90)
		
		if self.activate_status == False:
			self.message = ''
			self.lbl1 = QLabel('Parser-Avito требует активации', self)
			self.lbl1.move(80, 0)
			self.lbl1.resize(420, 90)

		
		if self.connect and self.activate_status:
			self.citytext = QLineEdit(self)
			self.citytext.setPlaceholderText(" введите город")
			self.citytext.setToolTip('Введите город для поиска')
			self.citytext.move(80, 80)
			self.citytext.resize(280, 30)

			self.categorytext = QLineEdit(self)
			self.categorytext.setPlaceholderText(" введите категорию")
			self.categorytext.setToolTip('Категории: квартиры, телефоны, HTC или iphone')
			self.categorytext.move(80, 140)
			self.categorytext.resize(280, 30)

			self.progress = QProgressBar(self)
			self.progress.move(80, 180)
			self.progress.resize(280, 30)
			
			self.button = QPushButton('сканировать', self)
			self.button.setToolTip('Результат сканирования сгенерируется на рабочем столе')
			self.button.setCursor(Qt.PointingHandCursor)
			self.button.move(80, 220)
			self.button.resize(280, 30)
			self.button.clicked.connect(self.on_click)

		self.show()
	
	async def progress_checked(self):
		i = 2
		iterator = 2
		s = 0 
		while  0 < i <= iterator: # 1 / 1
			self.progress.setMaximum(self.proc.array_len)
			self.progress.setValue(s)
			mes = 'сканировано объектов: ' + str(s) +'\n'+ self.proc.text_to_user
			self.lbl1.setText(mes)
			QApplication.processEvents()
			if i == 1 and s < self.proc.array_len:
				iterator = self.proc.array_len
				i = self.proc.array_len
			i-=1
			iterator-=1
			s+=1
			await asyncio.sleep(0.002)
	
	@pyqtSlot()
	def on_click(self):

		CityValue = self.citytext.text()
		CategoryValue = self.categorytext.text()
		
		cuty = slug.slug(self.proc.transliterate(CityValue))
		category = slug.slug(self.proc.transliterate(CategoryValue))
		if cuty and category != '':
			tasks = [  
					asyncio.ensure_future(self.proc.result_hub(cuty, category, self.loop), loop=self.loop),
					asyncio.ensure_future(self.progress_checked()),
			]
			self.loop.run_until_complete(asyncio.wait(tasks))
		else:
			return False
		if self.proc.status:
			message = str('Сканирование завершено успешно! \n резултат:   ~/Desktop/avito_parser/' + cuty + '_' + category + '.xslx')
			
			QMessageBox.information(self, 'успешно', message, QMessageBox.Ok, QMessageBox.Ok)
			self.citytext.setText("")
			self.categorytext.setText("")
		else:
			message = str('Сканирование незавершено. Вероятно введены неверные данные.')
			QMessageBox.information(self, 'что-то пошло не так', message, QMessageBox.Ok, QMessageBox.Ok)
		

class Activate(QMainWindow):
	def __init__(self):
		super().__init__()
		self.title = 'активация'
		self.left = 200
		self.top = 200
		self.width = 880
		self.height = 370
		self.path_activate = 'activate_processor.json'
		self.app = False
		self.setStyleSheet("""
			Activate {
				background-image: url(activate.png);
				background-color:#D1CAC2;
				background-repeat: no-repeat;
				background-position: right
				}
			
			QLabel {
				font-size: 20px;
				font-weight 900;
				color:#fff;
				}
			
			QMessageBox{
				font-size: 14px;
				font-weight 700;
				background-color:#D1CAC2;
				color:#fff;
			}

			QLineEdit {
				border-radius: 5px;
			}
			QPushButton {
			  border-radius: 5px;
			  color:#f7f7f7;
			  font-size: 15px;
			  border: 2px solid #f7f7f7;
			  text-align: center;
			  padding: 1px 6px;
			}
			QPushButton:hover{ 
				color: #fff;
				font-size: 15px;
				border: 2px solid #fff
			}"
		""")
		
		self.initUi()

	def initUi(self):
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)
		self.lbl1 = QLabel('Добро пожаловать! Для продолжения работы, активируйте свой Parser-Avito:\n введите активационный ключ', self)
		self.lbl1.move(80, 0)
		self.lbl1.resize(720, 90)
		
		self.key_ = QLineEdit(self)
		self.key_.setPlaceholderText("введите ключ активации")
		self.key_.setToolTip('активационный ключ')
		self.key_.move(80, 150)
		self.key_.resize(280, 30)

		self.button = QPushButton('активировать', self)
		self.button.setToolTip('активация аккаунта')
		self.button.setCursor(Qt.PointingHandCursor)
		self.button.move(80, 220)
		self.button.resize(280, 30)
		self.button.clicked.connect(self.on_click)
		self.show()

	def continue_(self, key):
		with open('key_.key', 'w') as f:
			f.write(key)
		self.app = App()
		self.close()


	
	@pyqtSlot()
	def on_click(self):
		key_val = self.key_.text()

		with open(self.path_activate, 'r+') as f:
			data = json.load(f)
		try:	
			for key, value in data.items():
				if key_val == key:
					del data[key]
					with open(self.path_activate, 'w') as f2:
						json.dump(data, f2, indent=4)
					self.continue_(key_val)
					break
			f.close()
			f2.close()
		
		except UnboundLocalError:
			return False
		
		message = str('Parser-Avito успешно активирован')
		QMessageBox.information(self, 'success', message, QMessageBox.Ok, QMessageBox.Ok)



if __name__ == '__main__':
	app = QApplication(sys.argv)
	if os.path.exists('key_.key'):
		ex = App()
	else:
		ex = Activate()
	
	sys.exit(app.exec_())
