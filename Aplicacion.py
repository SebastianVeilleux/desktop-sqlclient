# from this import d
import sys
import pandas as pd
import pymysql
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUi

# Clase principal
class Conexion(QMainWindow):
    # Metodo constructor
    def __init__(self):
        super(Conexion, self).__init__()
        loadUi(r"C:\Users\soporte\Desktop\Python\Proyecto\ventanaConexion.ui",self)
        self.setWindowIcon(QIcon(r"C:\Users\soporte\Desktop\Python\Proyecto\logoQT.png"))
        self.txtContrasena.setEchoMode(QLineEdit.Password)
        # Asociar los metodos a los botones
        self.btnConectarse.clicked.connect(self.conexion)
        self.btnCancelar.clicked.connect(self.salirConexion)

    def abrirConsultas(self):
        self.hide()
        consultas = Consultas(self)
        consultas.show()

    def salirConexion(self):
        pregunta = QMessageBox.question(self,"Atención","¿Realmente desea salir de la aplicación?", QMessageBox.Yes | QMessageBox.No)

        if pregunta == QMessageBox.Yes:
            self.close()

    def conexion(self):
        global h,u,p,d

        h = self.txtHost.text()
        u = self.txtUsuario.text()
        p = self.txtContrasena.text()
        d = self.txtBD.text()

        try:
            self.con = pymysql.connect(host=h,user=u,password=p,db=d)
            self.cursor = self.con.cursor()
            QMessageBox.information(self,"Conexión","Conexión establecida exitosamente")
            # Mostrar la ventana consultas
            self.abrirConsultas()
        except Exception as error:
            QMessageBox.warning(self,"Error",str(error))            

# Clase para la interfaz de consultas
class Consultas(QMainWindow):
    # parent = padre/madre | none = ninguno
    def __init__(self, parent=None):
        super(Consultas, self).__init__(parent)
        loadUi(r"C:\Users\soporte\Desktop\Python\Proyecto\ventanaConsultas.ui",self)
        self.mostrarTablas()
        self.btnSalir.clicked.connect(self.regresarConexion)
        self.btnConsultar.clicked.connect(self.datos)
        self.btnExportar.clicked.connect(self.exportarDatos)

    def regresarConexion(self):
        pregunta = QMessageBox.question(self,"Atención","¿Realmente desea cerrar y abrir otra conexión?", QMessageBox.Yes | QMessageBox.No)

        if pregunta == QMessageBox.Yes:
            self.parent().show()
            self.close()

    def conexionConsultas(self,h,u,p,d):
        try:
            self.con = pymysql.connect(host=h,user=u,password=p,db=d)
            self.cursor = self.con.cursor()
        except Exception as error:
            QMessageBox.warning(self,"Error",str(error))

    def mostrarTablas(self):

        self.conexionConsultas(h,u,p,d)

        try:
            # Consulta para recuperar el nombre de las tablas
            nombre_tablas = "SHOW TABLES"
            # Ejecutar la consulta
            self.cursor.execute(nombre_tablas)
            # Recuperar los valores de la consulta
            nombre_tablas = self.cursor.fetchall()
            # Recorrer el nombre de las tablas
            for n in nombre_tablas:
                self.cbTablas.addItem(str(n[0]))
        except Exception as error:
            QMessageBox.warning(self,"Error",str(error))        

    def datos(self):
        # Conexión a la base de datos
        self.conexionConsultas(h,u,p,d)

        # 1) Proceso para recuperar la cantidad de columnas de la tabla
        tabla = self.cbTablas.currentText()
        try:
            # Consulta
            campos = "SELECT COUNT(*) AS CANTIDAD_CAMPOS FROM Information_Schema.Columns WHERE Table_Name = '{}' GROUP BY Table_Name".format(tabla)
            # Ejecutar la consulta
            self.cursor.execute(campos)
            # Recuperar los valores
            campos = self.cursor.fetchone()
            # Recorrer el resultado y guardar el valor en la variable
            for c in campos:
                cantidad = int(c)
            # Enviar la cantidad de columnas a la tabla
            self.tabla.setColumnCount(cantidad)
        except Exception as error:
            QMessageBox.warning(self,"Error",str(error))

        # 2) Proceso para recuperar el nombre de las columnas
        try:
            # Consulta
            nombre_columnas = "SELECT COLUMN_NAME FROM Information_Schema.Columns WHERE Table_Name = '{}'".format(tabla)
            # Ejecutar la consulta
            self.cursor.execute(nombre_columnas)
            # Recuperar los valores
            nombre_columnas = self.cursor.fetchall()
            # Declarar una lista
            lista = []
            # Recorrer el nombre de las columnas
            for n in nombre_columnas:
                valor = n[0]
                print(valor)
                lista.append(valor)
            # Declarar una tupla
            tupla = tuple(lista)  
            # Establecer las etiquetas de la QTable usando la tupla
            self.tabla.setHorizontalHeaderLabels(tupla)
        except Exception as error:
            QMessageBox.warning(self,"Error",str(error))

        # 3) Proceso para recuperar los datos de la tabla seleccionada
        consulta = "SELECT * FROM {}".format(tabla)
        try:
            # Ejecutar la consulta
            self.cursor.execute(consulta)
            consulta = self.cursor.fetchall()
            print(consulta)
            # Guardamos los datos recuperados en un objeto
            tuplas = consulta
            # Limpiar la QTable
            self.tabla.clearContents()

            # Recorrer las tuplas
            fila = 0
            for tupla in tuplas:
                # Agregamos la fila donde se posicionaran los datos
                self.tabla.setRowCount(fila + 1)

                columna = 0

                while columna <= cantidad - 1:
                    self.tabla.setItem(fila,columna, QTableWidgetItem(str(tupla[columna])))

                    columna +=1

                    if columna == cantidad:
                        fila += 1
        except Exception as error:
            QMessageBox.warning(self,"Error",str(error))

    def exportarDatos(self):
        pass

# Constructor general
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = Conexion()
    main.show()
    sys.exit(app.exec())


