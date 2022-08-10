import os
from datetime import datetime
from decimal import Decimal, ROUND_UP
import json
import FreeCAD, FreeCADGui
from PySide import QtGui
from . import LANGUAGEPATH, ICONPATH

def report(msg):
	now = datetime.now().strftime("%H:%M:%S")
	FreeCAD.Console.PrintMessage(f"\n{now} {msg}")

class language:
	def __init__(self):
		try:
			'''load settings'''
			with open(f'{os.path.join(LANGUAGEPATH, FreeCAD.ParamGet("User parameter:BaseApp/Preferences/General").GetString("Language"))}.json', 'r') as jsonfile:
				self.language = json.loads(jsonfile.read().replace('\n', ''))
		except:
			with open(f'{os.path.join(LANGUAGEPATH, "English")}.json', 'r') as jsonfile:
				self.language = json.loads(jsonfile.read().replace('\n', ''))
	def chunk(self, chunk):
		return self.language[chunk]
LANG=language()

def ExternalDirected(*void):
	report ("external directed")

def InternalDirected(*void):
	report ("internal directed")

def ExternalDouble(*void):
	report ("external double")

def InternalDouble(*void):
	report ("internal double")