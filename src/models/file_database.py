import json, os

class FileDataBase:

	def __init__(self, ruta):
		self._rutaBase = ruta
		self._dbDirname, self._dbBasename = os.path.split(self._rutaBase)

	@property
	def rutabase(self):
		return self._rutaBase

	@property
	def dbDirname(self):
		return self._dbDirname

	@property
	def dbBasename(self):
		return self._dbBasename

	def leer_txt(self):
		with open(self._rutaBase, 'r') as entrada:
			return entrada.read()

	def escribir_txt(self, new_content):
		with open(self._rutaBase, 'w') as salida:
			print(new_content, file=salida)

	def leer_json(self):
		try:
			with open(self._rutaBase, 'r', encoding = 'utf-8') as entrada:
				return json.load(entrada)
		except FileNotFoundError:
			return []

	def escribir_json(self, new_object):
		with open(self._rutaBase, 'w', encoding = 'utf-8') as salida:
			json.dump(new_object, salida, indent = 4, ensure_ascii = False)


	@staticmethod
	def leer_archivo_txt(ruta):
		db_tmp = FileDataBase(ruta)
		return db_tmp.leer_txt()

	@staticmethod
	def escribir_archivo_txt(content, ruta):
		db_tmp = FileDataBase(ruta)
		db_tmp.escribir_txt(content)

	@staticmethod
	def leer_archivo_json(ruta):
		db_tmp = FileDataBase(ruta)
		return db_tmp.leer_json()

	@staticmethod
	def escribir_archivo_json(content, ruta):
		db_tmp = FileDataBase(ruta)
		db_tmp.escribir_json(content)