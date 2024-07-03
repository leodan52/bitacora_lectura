from controllers.madre_controller import VentanaMadre
from PyQt5.QtWidgets import QApplication


def main():
	app = QApplication([])
	Ventana = VentanaMadre()
	Ventana.show()
	app.exec_()


main()