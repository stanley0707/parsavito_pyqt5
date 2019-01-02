#!./env/lib/python3
# -*- coding: utf-8 -*-
import sys
import slug
import asyncio
from processor import Processor
from PyQt5.QtCore import pyqtSlot, QSize
from PyQt5 import QtGui
from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget,
	QPushButton, QAction, QLineEdit, QMessageBox, QProgressBar)


class App(QMainWindow):
	def __init__(self):
		super().__init__()
		self.title = 'Поиск объектов avito'
		self.left = 200
		self.top = 200
		self.width = 540
		self.height = 340
		self.proc = Processor()
		self.loop = asyncio.get_event_loop()
		#self.array = 0
		#self.setStyleSheet("background-image: url(parser-avito.ico)")
		self.initUi()
	
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
			QApplication.processEvents()
			if i == 1 and s < self.proc.array_len:
				iterator = self.proc.array_len
				i = self.proc.array_len
			i-=1
			iterator-=1
			s += 1
			await asyncio.sleep(0.002)
	
	@pyqtSlot()
	def on_click(self):

		CityValue = self.citytext.text()
		CategoryValue = self.categorytext.text()
		
		cuty = slug.slug(self.proc.transliterate(CityValue))
		category = slug.slug(self.proc.transliterate(CategoryValue))
		
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

	app = QApplication(sys.argv)
	ex = App()
	sys.exit(app.exec_())
