#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import slug
import time
import asyncio
from urllib.request import urlopen
from processor import Processor
from PyQt5.QtCore import pyqtSlot, QSize
from PyQt5 import QtGui
from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget,
	QPushButton, QAction, QLineEdit, QMessageBox, QProgressBar)

"""def benchmark(func, *args, **kwargs):
		started = time.time()
		result = func(*args, **kwargs)
		worked = time.time() - started
		print('Функция"{}" выполнилась за {:f} микросекунд'.format(
			func.__name__,worked * 1e6
		))
		return result"""

class App(QMainWindow):
	def __init__(self):
		super().__init__()
		self.title = 'Поиск объектов'
		self.left = 200
		self.top = 200
		self.width = 540
		self.height = 340
		self.initUi()
		self.proc = Processor()
		self.loop = asyncio.get_event_loop()
		self.setStyleSheet("background-image: url(icon.png)")
	
	def initUi(self):
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)

		mainMenu = self.menuBar()
		fileMenu = mainMenu.addMenu('info')
		info = QAction( 'info', self )
		
		self.citytext = QLineEdit(self)
		self.citytext.setPlaceholderText(" введите город")
		self.citytext.move(120, 20)
		self.citytext.resize(280, 30)

		self.categorytext = QLineEdit(self)
		self.categorytext.setPlaceholderText(" введите категорию")
		self.categorytext.move(120, 80)
		self.categorytext.resize(280, 30)
		
		self.progress = QProgressBar(self)
		self.progress.move(120, 220)
		self.progress.resize(280, 30)
		
		self.button = QPushButton('сканировать', self)
		self.button.move(120, 180)
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
			if i == 1 and s < self.proc.array_len:
				iterator = self.proc.array_len # 50
				i = self.proc.array_len
			i-=1
			iterator-=1
			s +=1
			await asyncio.sleep(0.001)
	
	@pyqtSlot()
	def on_click(self):

		CityValue = self.citytext.text()
		CategoryValue = self.categorytext.text()
		
		cuty = slug.slug(self.proc.transliterate(CityValue))
		category = slug.slug(self.proc.transliterate(CategoryValue))
		
		#loop = asyncio.get_event_loop()

		tasks = [  
			asyncio.ensure_future(self.proc.result_hub(cuty, category, self.loop), loop=self.loop),
			asyncio.ensure_future(self.progress_checked()),
		]
		self.loop.run_until_complete(asyncio.wait(tasks))
		
		message = str('Сканирование завершено успешно! \n резултат:   ~/Desktop/avito_parser/' + cuty + '_' + category + '.xslx')
		
		QMessageBox.information(self, 'успешно', message, QMessageBox.Ok, QMessageBox.Ok)
		self.citytext.setText("")
		self.categorytext.setText("")


if __name__ == '__main__':

	if sys.version_info[:3] == (3, 6, 0):
		import asyncio.events as _ae
		import os as _os

		_ae._RunningLoop._pid = None

		def _get_running_loop():
			if _ae._running_loop._pid == _os.getpid():
				return _ae._running_loop._loop

		def _set_running_loop(loop):
			_ae._running_loop._pid = _os.getpid()
			_ae._running_loop._loop = loop

		_ae._get_running_loop = _get_running_loop
		_ae._set_running_loop = _set_running_loop
	
	app = QApplication(sys.argv)
	ex = App()
	sys.exit(app.exec_())
