import csv
import os

class CSVWriter():

	filename = None
	fp = None
	writer = None

	def __init__(self, filename):
		self.filename = filename
		self.fp = open(self.filename, 'w', encoding='utf8')
		self.writer = csv.writer(self.fp, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL, lineterminator='\n')

	def close(self):
		print("Done Writing New CSV!\n")
		self.fp.close()

	def write(self, elems):
		self.writer.writerow(elems)

	def writeHeader(self, headerelems):
		self.writer.writerow(headerelems)

	def size(self):
		return os.path.getsize(self.filename)

	def fname(self):
		return self.filename