from models.file_database import FileDataBase
import os, re, json
from datetime import datetime

class HistorialVersiones:
	def __init__(self, filedatabase, carpeta_versiones = 'versiones_anteriores/', limite_versiones = 50):
		self._db = filedatabase
		self._carpeta_versiones = carpeta_versiones
		self._contenido_anterior = []
		self._dirname_versiones = os.path.join(self._db.dbDirname, self._carpeta_versiones)
		self._limite_versiones = limite_versiones
		self._lista_versiones_anteriores = []

		if not os.path.exists(self._dirname_versiones):
			os.mkdir(self._dirname_versiones)

		self.obtener_lista_versiones()
		self.guardar_nueva_version()

	def obtener_lista_versiones(self):
		listar_archivos = os.listdir(self._dirname_versiones)

		if not listar_archivos:
			self._lista_versiones_anteriores = []

		pattern = re.compile(r'\d{4}(-\d{2}){2} \d{2}(:\d{2}){2}')

		matches = map(lambda x: pattern.search(x), listar_archivos)
		self._lista_versiones_anteriores = list(filter(lambda x: x, matches))

	def obtener_version_mas_reciente(self):
		try:
			return max(self._lista_versiones_anteriores, key = lambda x: datetime.fromisoformat(x.group(0)))
		except ValueError:
			return None

	def obtener_version_mas_antigua(self):
		try:
			return min(self._lista_versiones_anteriores, key = lambda x: datetime.fromisoformat(x.group(0)))
		except ValueError:
			return None

	def leer_db_actual(self):
		self._contenido_anterior = self._db.leer_json()

	def leer_archivo_version(self, matcher):
		if not matcher:
			return []
		ruta = os.path.join(self._dirname_versiones, matcher.string)
		return FileDataBase.leer_archivo_json(ruta)

	def _crear_ruta_archivo(self):
		dt = datetime.now().strftime(r'%Y-%m-%d %H:%M:%S')
		nombre_version = self._db.dbBasename.replace('.json', f'_{dt}.json')
		nuevaruta = os.path.join(self._dirname_versiones, nombre_version)

		return nuevaruta

	def guardar_nueva_version(self):
		new_content = self._db.leer_json()
		mas_reciente = self.leer_archivo_version(self.obtener_version_mas_reciente())

		if (new_content == mas_reciente) and (mas_reciente):
			return

		nuevaruta = self._crear_ruta_archivo()

		FileDataBase.escribir_archivo_json(new_content, nuevaruta)
		self.limitar_versiones()

	def limitar_versiones(self):
		self.obtener_lista_versiones()
		while len(self._lista_versiones_anteriores) > self._limite_versiones:
			antigua = self.obtener_version_mas_antigua()

			a_borrar = os.path.join(self._dirname_versiones, antigua.string)
			os.remove(a_borrar)
			self.obtener_lista_versiones()