# Author: Leonardo D. Santiago
# Clase que representa un registro en la bitácora de lectura

from datetime import datetime
import re, copy
from unidecode import unidecode

from models.file_database import FileDataBase
from models.historial_versiones import HistorialVersiones

class Registro:

	_fecha_formato = r'%Y-%m-%d %H:%M:%S'

	def __init__(self, titulo_obra, ultimo_leido, fecha_hora):
		self._titulo = titulo_obra
		self._ultimo_leido = ultimo_leido
		self._fecha = fecha_hora

	def __eq__(self, other):
		titulo_comparar = (self._titulo) == (other._titulo)
		ultimo_comparar = (self._ultimo_leido) == (other._ultimo_leido)
		fecha_comparar = (self._fecha) == (other._fecha)

		return titulo_comparar and ultimo_comparar and fecha_comparar

	@property
	def titulo(self):
		return self._titulo

	@titulo.setter
	def titulo(self, nuevo_titulo):
		self._titulo = nuevo_titulo

	@property
	def ultimo_leido(self):
		return self._ultimo_leido

	@property
	def fecha(self):
		return self._fecha

	def __repr__(self):
		fecha_cadena = self._fecha.strftime(self._fecha_formato)

		return f'{fecha_cadena} :\n\t{self._titulo}\n\t\tÚltimo leído: {self._ultimo_leido}'

	@classmethod
	def strfregistro(cls, cadena):
		pattern_fecha = r'\d{4}(-\d{2}){2} \d{2}(:\d{2}){2}'
		pattern_ultimo = r'Último leído: (\d+)'

		lineas = cadena.strip().split('\n')
		lineas = list(map(lambda x: x.strip(), lineas))
		fecha_cadena = re.match(pattern_fecha, lineas[0])[0]

		fecha = datetime.strptime(fecha_cadena, cls._fecha_formato)
		titulo = lineas[1]
		ultimo = re.match(pattern_ultimo, lineas[2])[1]

		return cls(titulo, ultimo, fecha)


class Bitacora:

	def __init__(self):
		self._lista = []
		self._num_cambios = 0
		self._db = None
		self._historial = None

	def cargar_ruta_db(self, rutaDB):
		self._db = FileDataBase(rutaDB)
		self._historial = HistorialVersiones(self._db)

	def cargar_data(self):
		if not self._db:
			print("Error: no se ha cargado una ruta para la DB")

		data_json = self._db.leer_json()

		for data in data_json:
			registro = Registro(data['titulo'], data['ultimo'], datetime.fromisoformat(data['datetime']))

			if registro not in self._lista:
				self._lista.append(registro)

	def guardar_data(self):
		if not self._db:
			print("Error: no se ha cargado una ruta para la DB")

		if not self._lista:
			return

		self._historial.leer_db_actual()

		data_json = map(lambda x: {
			'titulo': x.titulo,
			'ultimo' : x.ultimo_leido,
			'datetime' : x.fecha.isoformat()
		}, self._lista)

		self._db.escribir_json(list(data_json))
		self._num_cambios = 0
		self._historial.guardar_nueva_version()

	@property
	def lista(self):
		return self._lista

	@property
	def num_cambios(self):
		return self._num_cambios

	def __str__(self):
		lista_cadenas = list(map(str, self._lista))

		return '\n\n'.join(lista_cadenas)

	def __iter__(self):
		yield from self._lista

	def __getitem__(self, key):
		return self._lista[key]

	def __eq__(self, other):
		return self._lista == other._lista

	def copy(self):
		return copy.deepcopy(self)

	def leer_archivoTXT(self, ruta):
		contenido = FileDataBase.leer_archivo_txt(ruta)

		pattern = re.compile('.+\n\t.+\n\t{2}.+')
		matches = pattern.finditer(contenido)

		for match_ in matches:
			registro = Registro.strfregistro(match_[0])

			if registro not in self._lista:
				self._lista.append(registro)
				self._num_cambios += 1

	def escribir_archivoTXT(self, ruta):
		self.ordenar()

		if not self._lista:
			return

		FileDataBase.escribir_archivo_txt(str(self), ruta)

	def agregar_registro(self, registro):
		if registro not in self._lista:
			self._lista.append(registro)
			self._num_cambios += 1
		else:
			print('El registro ya se encuentra en la bitácora')

	def agregar(self, titulo_obra, ultimo_leido, fecha_hora):
		registro = Registro(titulo_obra, ultimo_leido, fecha_hora)

		self.agregar_registro(registro)

	def ordenar(self):
		lista_antigua = self._lista.copy()
		self._lista = sorted(self._lista, key = lambda x: x.fecha)

		if lista_antigua != self._lista:
			self._num_cambios += 1

	def unique_titulos(self):
		titulos = set(map(lambda x: x.titulo, self._lista))
		titulos = list(titulos)
		titulos.sort()

		salida = []

		for t in titulos:
			registros = list(filter(lambda x: t == x.titulo, self._lista))

			titulo = t
			numero_registros = len(registros)
			ultimo = max(registros, key=lambda x: x.fecha).fecha

			salida.append({
				'titulo' : titulo,
				'conteo' : numero_registros,
				'ultimo' : ultimo
			})

		return salida

	def buscar_titulo(self, patron):

		if patron in self.unique_titulos():
			registros_encontrados = list(filter(lambda x: patron == x.titulo, self._lista))
		else:
			patron = unidecode(patron).lower()
			registros_encontrados = list(filter(lambda x: patron in unidecode(x.titulo).lower(), self._lista))

		return registros_encontrados

	def editar_titulo(self, titulo_anterior, nuevo_titulo):
		for r in self._lista:
			if titulo_anterior == r.titulo:
				r.titulo = nuevo_titulo
			self._num_cambios += 1

	def eliminar_registro(self, registro):
		if registro in self._lista:
			self._lista.remove(registro)
			self._num_cambios += 1
