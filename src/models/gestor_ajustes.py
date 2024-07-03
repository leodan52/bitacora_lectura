import json

class Ajustes:
	def __init__(self, ruta_archivo):
		self._ruta = ruta_archivo
		self._ajustes = None

	def cargar_ajustes(self):
		try:
			with open(self._ruta, 'r', encoding = 'utf-8') as entrada:
				self._ajustes = json.load(entrada)
		except FileNotFoundError:
			self._ajustes = dict()

	def _actualizar_archivo_ajustes(self):
		with open(self._ruta, 'w', encoding = 'utf-8') as salida:
			json.dump(self._ajustes, salida, indent = 4, ensure_ascii = False)

	def __getitem__(self, key):
		return self._ajustes[key]

	def __setitem__(self, key, value):
		self._ajustes[key] = value
		self._actualizar_archivo_ajustes()