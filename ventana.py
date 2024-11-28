# Archivo que sirve para para todos los demás proyectos

from DemandaYCables_ui import *
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox, QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton, QWidget, QRadioButton
import math

demandaMaximaCasa = 0
espacios = 0
nivelConsumo = ""
# Factores de corrección por temperatura ambiente diferentes de 30°C a ser aplicadasa las capacidades de conducción de corriente
tabla_temperatura = {
    10: {"PVC": 1.22, "EPR o XLPE": 1.15},
    15: {"PVC": 1.17, "EPR o XLPE": 1.12},
    20: {"PVC": 1.12, "EPR o XLPE": 1.08},
    25: {"PVC": 1.07, "EPR o XLPE": 1.04},
    35: {"PVC": 0.93, "EPR o XLPE": 0.98},
    40: {"PVC": 0.87, "EPR o XLPE": 0.96},
    45: {"PVC": 0.79, "EPR o XLPE": 0.94},
    50: {"PVC": 0.71, "EPR o XLPE": 0.92},
    55: {"PVC": 0.61, "EPR o XLPE": 0.87},
    60: {"PVC": 0.50, "EPR o XLPE": 0.84},
    65: {"PVC": None, "EPR o XLPE": 0.82},
    70: {"PVC": None, "EPR o XLPE": 0.80},
    75: {"PVC": None, "EPR o XLPE": 0.72},
    80: {"PVC": None, "EPR o XLPE": 0.61},
}

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args,  **kwargs)
        self.setupUi(self)

        """ Primera Interfaz """
        self.ocultarLabels()
        self.pushButton_generarTabla.clicked.connect(self.generarTabla)

        # Layout principal
        self.layout = QtWidgets.QVBoxLayout(self.centralwidget)

        blocked_cells = [(0, col) for col in range(self.tableWidget.columnCount())]  # Bloquear la fila 0
        blocked_cells += [(row, col) for row in range(self.tableWidget.rowCount()) for col in [3, 4]]  # Bloquear columnas 3 y 4

        # Bloquear celdas especificadas
        for row, col in blocked_cells:
            item = self.tableWidget.item(row, col)
            
            if item is None:  # Si la celda no tiene item, crear uno vacío
                item = QTableWidgetItem("")
                self.tableWidget.setItem(row, col, item)

            # Bloquear la edición de la celda
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)

        # Centrar texto de las columnas
        for row in range(self.tableWidget.rowCount()):
            for col in range(self.tableWidget.columnCount()):
                item = self.tableWidget.item(row, col)
                if item:  # Verificar que la celda no esté vacía
                    item.setTextAlignment(Qt.AlignCenter)
  
        # Ajustar el tamaño de la primera columna
        self.tableWidget.setColumnWidth(0, 222)

        self.tableWidget.hide()

        # Verificar que las celdas de los datos tengan números
        self.tableWidget.cellChanged.connect(self.verificarNumeroEnCelda)

        # Verificar que las celdas estén llenes y posteriormente realizar el cálculo de demanda
        self.pushButton_calcularDemandaCasa.clicked.connect(self.verificarCeldasLlenas)

        self.lineEdit_anchoCasa.textChanged.connect(lambda: self.verificarNumeroInterfaz1(1))
        self.lineEdit_largoCasa.textChanged.connect(lambda: self.verificarNumeroInterfaz1(2))
        self.lineEdit_numeroAires.textChanged.connect(lambda: self.verificarNumeroInterfaz1(3))
        self.lineEdit_potenciaAire.textChanged.connect(lambda: self.verificarNumeroInterfaz1(4))

        # Demanda máxima del conjunto
        self.pushButton_calcularDemandaConjunto.clicked.connect(self.demandaMaxConjunto)

        # Cálculo del cable
        self.pushButton_calcularCable.clicked.connect(self.calcularCable)

        """ Segunda Interfaz """
        self.lineEdit_numeroCasas.textChanged.connect(lambda: self.verificarNumeroInterfaz2(1))
        self.lineEdit_numeroLocales.textChanged.connect(lambda: self.verificarNumeroInterfaz2(2))
        self.lineEdit_demandaMaxLocal.textChanged.connect(lambda: self.verificarNumeroInterfaz2(3))
        self.lineEdit_demandaMaxServicios.textChanged.connect(lambda: self.verificarNumeroInterfaz2(4))

        self.pushButton_calcularDemandaMaxConjunto.clicked.connect(self.calcularDemandaConjunto)
        self.pushButton_volver.clicked.connect(self.ocultarLabels)

        """ Tercera Interfaz """
        self.lineEdit_longitudCable.textChanged.connect(lambda: self.verificarNumeroInterfaz3(1))
        self.lineEdit_temperatura.textChanged.connect(lambda: self.verificarNumeroInterfaz3(2))
        self.lineEdit_tubosVerticales.textChanged.connect(lambda: self.verificarNumeroInterfaz3(3))
        self.lineEdit_tubosHorizontales.textChanged.connect(lambda: self.verificarNumeroInterfaz3(4))

        self.pushButton_calcularSeccionCable.clicked.connect(self.calcularSeccionCable)
        self.pushButton_volver_2.clicked.connect(self.ocultarLabels)

    """ PRIMERA INTERFAZ """

    def generarTabla(self):
        global espacios

        self.ocultarLabels()
        self.label_enunciado_2.setVisible(True)

        # Obtener el texto del input
        str_numeroEspacios = self.spinBox_numeroEspacios.text()

        # Convertir texto a lista de números
        espacios = int(str_numeroEspacios) + 1
        # Configurar tabla
        self.tableWidget.setRowCount(espacios)
        self.tableWidget.setColumnCount(5)
        
        # Mostrar tabla excepto las columnas 3 (tomacorrientes) y 4 (puntos de iluminación)
        self.tableWidget.show()
        for col in range (3):
            self.tableWidget.setColumnHidden(col, False)

        # Mostrar botón de calcular Demanda
        self.pushButton_calcularDemandaCasa.setVisible(True)

    def ocultarLabels(self):
        self.stackedWidget.setCurrentIndex(0)
        # Ocultar columnas 3 (tomacorrientes) y 4 (puntos de iluminación)

        self.tableWidget.hide()
        self.tableWidget.setColumnHidden(3, True)
        self.tableWidget.setColumnHidden(4, True)

        # Ocultar los labels y botones
        self.label_enunciado_2.setVisible(False)
        self.label_titulo2.setVisible(False)
        self.label_titulo3.setVisible(False)
        self.label_titulo4.setVisible(False)
        self.label_titulo5.setVisible(False)
        self.label_potenciaInsIluminacion.setVisible(False)
        self.label_potenciaInsTomas.setVisible(False)
        self.label_potenciaFuerza.setVisible(False)
        self.label_demandaMaxima.setVisible(False)
        self.pushButton_calcularDemandaCasa.setVisible(False)
        self.pushButton_calcularDemandaConjunto.setVisible(False)
        self.pushButton_calcularCable.setVisible(False)

    # Función para validar que los valores sean números
    def verificarNumeroEnCelda(self, row, col):
        item = self.tableWidget.item(row, col)
        if item != "":
            # Centra el texto en la celda cambiada
            item.setTextAlignment(Qt.AlignCenter)

        # Ignorar la validación si la celda está en la primera columna (nombre de los espacios)
        if col == 0 or col == 3 or col == 4:
            return
    
        # Obtenemos el texto de la celda
        valor_celda = self.tableWidget.item(row, col).text()

        try:
            # Si hay un valor en la celda, intentamos convertir el valor a un número flotante
            if valor_celda != "":
                valor = float(valor_celda)

                if valor <= 0:
                    QMessageBox.warning(self, "Error", "Por favor, ingrese un número válido.")
                    # Restablecemos el valor de la celda
                    self.tableWidget.item(row, col).setText("")

        except ValueError:
            # Si hay un error en la conversión (no es un número válido), mostramos un mensaje de error
            QMessageBox.warning(self, "Error", "Por favor, ingrese un número válido.")
            # Restablecemos el valor de la celda
            self.tableWidget.item(row, col).setText("")

    def verificarCeldasLlenas(self):
        # Verificar si todas las celdas (excepto de las últimas dos columnas) tienen valores
        for row in range(self.tableWidget.rowCount()):
            for col in range(self.tableWidget.columnCount()):
                if col != 3 and col != 4: 
                    item = self.tableWidget.item(row, col)
                    if item is None or item.text() == "":
                        # Si alguna celda (excepto de las últimas dos columnas) está vacía, mostrar un mensaje de error y salir de la función
                        QMessageBox.warning(self, "Error", "Por favor, complete todas las celdas antes de calcular.")
                        return 
        
        if self.lineEdit_anchoCasa.text() == "" or self.lineEdit_largoCasa.text() == "":
            QMessageBox.warning(self, "Error", "Por favor, complete todas las celdas antes de calcular.")
            return 
        
        # Si todos los campos tienen valores, calcular la demanda
        self.calcularDemandaCasa()

    def calcularDemandaCasa(self):
        global nivelConsumo, demandaMaximaCasa

        self.mostrarItemsOcultosInterfaz1()

        potenciaInstaladaIluminacion = 0
        potenciaInstaladaTomas = 0

        # Nivel de consumo de la casa
        anchoCasa = float(self.lineEdit_anchoCasa.text())
        largoCasa = float(self.lineEdit_largoCasa.text())
        str_numeroAires = self.lineEdit_numeroAires.text()
        numeroAires = int(str_numeroAires) if str_numeroAires != "" else 0
        str_potenciaAire = self.lineEdit_potenciaAire.text()
        potenciaAire = int(str_potenciaAire) if str_potenciaAire != "" else 0
        
        superficieCasa = anchoCasa * largoCasa

        if superficieCasa <= 80:
            nivelConsumo = "Mínimo"
        elif superficieCasa <= 140:
            nivelConsumo = "Medio"
        else:
            nivelConsumo = "Elevado"
        
        # Recorremos todas las filas de la tabla
        for row in range(1, self.tableWidget.rowCount()):
            str_nombre = self.tableWidget.item(row, 0) # Columna 0 (Nombre)
            str_anchoEspacio = self.tableWidget.item(row, 1)  # Columna 1 (Ancho)
            str_largoEspacio = self.tableWidget.item(row, 2)  # Columna 2 (Largo)

            anchoEspacio = float(str_anchoEspacio.text())
            largoEspacio = float(str_largoEspacio.text())

            areaEspacio = largoEspacio * anchoEspacio
            perimetroEspacio = largoEspacio * 2 + anchoEspacio * 2

            tomasPorArea = math.ceil(areaEspacio / 10)
            tomasPorPerimetro = math.ceil(perimetroEspacio / 5)

            if nivelConsumo == "Mínimo":
                densidadCarga = 10
            elif nivelConsumo == "Medio":
                densidadCarga = 15
            else:
                densidadCarga = 20

            if str_nombre.text().lower() == "baño":
                tomasEspacio = 1
                puntosIluminados = 1
                demandaPotenciaIluminacion = 60
            else:
                tomasEspacio = tomasPorArea if tomasPorArea >= tomasPorPerimetro else tomasPorPerimetro
                puntosIluminados = areaEspacio * densidadCarga / 100
                if puntosIluminados % 1 != 0:
                    puntosIluminados += 1
                demandaPotenciaIluminacion = int(puntosIluminados) * 100

            demandaPotenciaTomas = tomasEspacio * 200

            potenciaInstaladaIluminacion += demandaPotenciaIluminacion
            potenciaInstaladaTomas += demandaPotenciaTomas

            # Demanda de potencia de las tomacorrientes
            str_demandaPotenciaIluminacion = str(int(tomasEspacio)) + " tomas de " + str(200) + "W" if tomasEspacio > 1 else "1 toma de " + str(200) + "W"
            self.tableWidget.setItem(row, 3, QTableWidgetItem(str_demandaPotenciaIluminacion))
            # Demanda de potencia de los puntos de iluminación
            str_demandaPotenciaTomas = str(int(puntosIluminados)) + " puntos de " + (str(60) if str_nombre.text().lower() == "baño" else str(100)) + "W" if puntosIluminados > 1 else "1 punto de " + (str(60) if str_nombre.text().lower() == "baño" else str(100)) + "W"
            self.tableWidget.setItem(row, 4, QTableWidgetItem(str_demandaPotenciaTomas))

            # Bloquear la edición de la celda
            item = self.tableWidget.item(row, 3)
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)

            item = self.tableWidget.item(row, 4)
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)

        # Potencia instalada en iluminación
        self.label_potenciaInsIluminacion.setText(str(int(potenciaInstaladaIluminacion)) + "W")

        # Potencia instalada en las tomacorrientes
        self.label_potenciaInsTomas.setText(str(potenciaInstaladaTomas) + "W")

        # Potencia en fuerza
        potenciaFuerza = numeroAires * potenciaAire

        # Demanda máxima de la casa
        potenciaTotalInstalada = potenciaInstaladaIluminacion + potenciaInstaladaTomas

        # Factor de Demanda de las tomacorrientes y los puntos de iluminación
        # Definimos la demanda máxima de tomas e iluminación
        if potenciaTotalInstalada > 3000:
            # Inicializamos la demanda máxima con el valor base
            demandaMaximaTomasEIluminacion = 3000
            
            # Calculamos la potencia restante después de 3000
            potenciaInstaladaRestante1 = potenciaTotalInstalada - 3000
            
            if potenciaInstaladaRestante1 > 5000:
                potenciaInstaladaRestante2 = potenciaInstaladaRestante1 - 5000
                demandaMaximaTomasEIluminacion += 5000 * 0.35  # Demanda para los primeros 5000
                demandaMaximaTomasEIluminacion += potenciaInstaladaRestante2 * 0.25  # Resto de la potencia
            else:
                demandaMaximaTomasEIluminacion += potenciaInstaladaRestante1 * 0.35  # Si la potencia restante es menor o igual a 5000
        else:
            # Si la potencia total es 3000 o menor, la demanda máxima es igual a la potencia instalada
            demandaMaximaTomasEIluminacion = potenciaTotalInstalada

        # Factor de demanda de fuerza

        if numeroAires <= 2:
            demandaMaximaFuerza = potenciaFuerza
        elif numeroAires <= 5:
            demandaMaximaFuerza = potenciaFuerza * 0.75
        else:
            demandaMaximaFuerza = potenciaFuerza * 0.5

        self.label_potenciaFuerza.setText(str(round(demandaMaximaFuerza)) + "W")

        demandaMaximaCasa = round(demandaMaximaTomasEIluminacion + demandaMaximaFuerza)
        self.label_demandaMaxima.setText(str(demandaMaximaCasa) + "W")

    def verificarNumeroInterfaz1(self, numeroEntrada):
        if numeroEntrada == 1:
            entrada = self.lineEdit_anchoCasa.text()
        elif numeroEntrada == 2:
            entrada = self.lineEdit_largoCasa.text()
        elif numeroEntrada == 3:
            entrada = self.lineEdit_numeroAires.text()
        else:
            entrada = self.lineEdit_potenciaAire.text()

        try:
            # Si hay un valor en la celda, intentamos convertir el valor a un número flotante
            if entrada != "":
                valor = float(entrada)
                if (numeroEntrada != 3 and valor <= 0) or (numeroEntrada == 3 and valor < 0) or (numeroEntrada == 4 and valor < 0):
                    self.setearEntradaInterfaz1(numeroEntrada)
        except ValueError:
            self.setearEntradaInterfaz1(numeroEntrada)

    def setearEntradaInterfaz1(self, entrada):
        QMessageBox.warning(self, "Error", "Por favor, ingrese un número válido.")
        if entrada == 1:
            self.lineEdit_anchoCasa.setText("")
        elif entrada == 2:
            self.lineEdit_largoCasa.setText("")
        elif entrada == 3:
            self.lineEdit_numeroAires.setText("")
        else:
            self.lineEdit_potenciaAire.setText("")

    def mostrarItemsOcultosInterfaz1(self):
        # Mostrar nuevamente la columna 3 (tomacorrientes) y 4 (puntos de iluminación)
        self.tableWidget.setColumnHidden(3, False)
        self.tableWidget.setColumnHidden(4, False)

        # Mostrar los labels y botones
        self.label_titulo2.setVisible(True)
        self.label_titulo3.setVisible(True)
        self.label_titulo4.setVisible(True)
        self.label_titulo5.setVisible(True)
        self.label_potenciaInsIluminacion.setVisible(True)
        self.label_potenciaInsTomas.setVisible(True)
        self.label_potenciaFuerza.setVisible(True)
        self.label_demandaMaxima.setVisible(True)
        self.pushButton_calcularDemandaConjunto.setVisible(True)
        self.pushButton_calcularCable.setVisible(True)

    """ SEGUNDA INTERFAZ """

    def demandaMaxConjunto(self):
        self.stackedWidget.setCurrentIndex(1)
        self.label_titulo_demandaMaxConjunto.setVisible(False)
        self.label_demandaMaxConjunto.setVisible(False)

    def verificarNumeroInterfaz2(self, numeroEntrada):
        if numeroEntrada == 1:
            entrada = self.lineEdit_numeroCasas.text()
        elif numeroEntrada == 2:
            entrada = self.lineEdit_numeroLocales.text()
        elif numeroEntrada == 3:
            entrada = self.lineEdit_demandaMaxLocal.text()
        else:
            entrada = self.lineEdit_demandaMaxServicios.text()

        try:
            # Si hay un valor en la celda, intentamos convertir el valor a un número flotante
            if entrada != "":
                valor = float(entrada)

                if (numeroEntrada == 1 and valor <= 0) or (numeroEntrada != 1 and valor < 0):
                    self.setearEntradaInterfaz1(numeroEntrada)
        except ValueError:
            self.setearEntradaInterfaz2(numeroEntrada)
    
    def setearEntradaInterfaz2(self, entrada):
        QMessageBox.warning(self, "Error", "Por favor, ingrese un número válido.")
        if entrada == 1:
            self.lineEdit_numeroCasas.setText("")
        elif entrada == 2:
            self.lineEdit_numeroLocales.setText("")
        elif entrada == 3:
            self.lineEdit_demandaMaxLocal.setText("")
        else:
            self.lineEdit_demandaMaxServicios.setText("")

    def calcularDemandaConjunto(self):
        global nivelConsumo

        try:
            numeroCasas = int(self.lineEdit_numeroCasas.text())
        except:
            QMessageBox.warning(self, "Error", "Por favor, ingrese el número de casas.")
            return
        
        str_numeroLocales = self.lineEdit_numeroLocales.text()
        numeroLocales = int(str_numeroLocales) if str_numeroLocales != "" else 0
        str_demandaMaxLocal = self.lineEdit_demandaMaxLocal.text()
        demandaMaxLocal = float(str_demandaMaxLocal) if str_demandaMaxLocal != "" else 0
        str_demandaMaxServicios = self.lineEdit_demandaMaxServicios.text()
        demandaMaxServicios = float(str_demandaMaxServicios) if str_demandaMaxServicios != "" else 0

        if numeroCasas <= 4:
            factor = 0.8 if nivelConsumo == "Elevado" else 1.0
        elif numeroCasas <= 10:
            factor = 0.7 if nivelConsumo == "Elevado" else 0.8
        elif numeroCasas <= 20:
            factor = 0.5 if nivelConsumo == "Elevado" else 0.6
        else:
            factor = 0.3 if nivelConsumo == "Elevado" else 0.4

        demandaMaximaConjunto = demandaMaximaCasa * numeroCasas * factor

        potenciaInstaladaLocales = numeroLocales * demandaMaxLocal

        if potenciaInstaladaLocales > 20000:
            demandaMaximaConjunto += 20000
            potenciaInstaladaLocalesRestante = potenciaInstaladaLocales - 20000
            demandaMaximaConjunto += potenciaInstaladaLocalesRestante * 0.7
        else:
            demandaMaximaConjunto += potenciaInstaladaLocales

        demandaMaximaConjunto += demandaMaxServicios

        self.label_demandaMaxConjunto.setText(str(round(demandaMaximaConjunto)) + "W")
        self.mostrarItemsOcultosInterfaz2()
    
    def mostrarItemsOcultosInterfaz2(self):
        # Mostrar los labels
        self.label_titulo_demandaMaxConjunto.setVisible(True)
        self.label_demandaMaxConjunto.setVisible(True)

    """ TERCERA INTERFAZ """
    def calcularCable(self):
        self.stackedWidget.setCurrentIndex(2)
        self.label_titulo_criterioCaidaTension.setVisible(False)
        self.label_criterioCaidaTension.setVisible(False)
        self.label_titulo_criterioCaidaConduccion.setVisible(False)
        self.label_criterioCaidaConduccion.setVisible(False)
        self.label_titulo_seccionCable.setVisible(False)
        self.label_seccionCable.setVisible(False)

    def verificarNumeroInterfaz3(self, numeroEntrada):
        if numeroEntrada == 1:
            entrada = self.lineEdit_longitudCable.text()
        elif numeroEntrada == 2:
            entrada = self.lineEdit_temperatura.text()
        elif numeroEntrada == 3:
            entrada = self.lineEdit_tubosVerticales.text()
        else:
            entrada = self.lineEdit_tubosHorizontales.text()

        try:
            # Si hay un valor en la celda, intentamos convertir el valor a un número flotante
            if entrada != "":
                valor = float(entrada)

                if numeroEntrada != 2 and valor <= 0:
                    self.setearEntradaInterfaz3(numeroEntrada)
        except ValueError:
            self.setearEntradaInterfaz3(numeroEntrada)

    def setearEntradaInterfaz3(self, entrada):
        QMessageBox.warning(self, "Error", "Por favor, ingrese un número válido.")
        if entrada == 1:
            self.lineEdit_longitudCable.setText("")
        elif entrada == 2:
            self.lineEdit_temperatura.setText("")
        elif entrada == 3:
            self.lineEdit_tubosVerticales.setText("")
        else:
            self.lineEdit_tubosHorizontales.setText("")

    def calcularSeccionCable(self):
        global demandaMaximaCasa, tabla_temperatura
        tipoSistema = ""
        aislamientoConductor = ""
        tipoCaidaTension = ""

        demandaMaximaCasa = 35000

        try:
            longitudCable = float(self.lineEdit_longitudCable.text())
            temperatura = int(self.lineEdit_temperatura.text())
            tubosVerticales = int(self.lineEdit_tubosVerticales.text())
            tubosHorizontales = int(self.lineEdit_tubosHorizontales.text())
        except:
            QMessageBox.warning(self, "Error", "Por favor, ingrese todos los valores.")
            return

        if temperatura not in tabla_temperatura:
            # Si no está, mostrar el mensaje de error con las temperaturas permitidas
            temperaturas_permitidas = ", ".join(map(str, tabla_temperatura.keys()))
            mensaje = f"La temperatura debe ser alguno de estos valores: {temperaturas_permitidas}"
            QMessageBox.warning(self, "Error", mensaje)
            return
        
        # Obtener el tipo de sistema seleccionado seleccionado
        for opcion in self.groupBox_tipoSistema.findChildren(QRadioButton):
            if opcion.isChecked():
                tipoSistema = opcion.text()  # Guardar el texto de la opción seleccionada

        # Obtener el aislamiento del conductor seleccionado seleccionado
        for opcion in self.groupBox_aislamientoConductor.findChildren(QRadioButton):
            if opcion.isChecked():
                aislamientoConductor = opcion.text()  # Guardar el texto de la opción seleccionada

        # Obtener la caída de tensión seleccionada seleccionado
        for opcion in self.groupBox_caidaTension.findChildren(QRadioButton):
            if opcion.isChecked():
                tipoCaidaTension = opcion.text()  # Guardar el texto de la opción seleccionada

        if tipoSistema == "" or aislamientoConductor == "" or tipoCaidaTension == "":
            QMessageBox.warning(self, "Error", "Por favor, ingrese todos los valores.")
            return
        
        voltaje = 110 if tipoSistema == "Monofásico" else 220
        print(f"Voltaje: {voltaje}")

        # Tablas

        # Factores de corrección por agrupamiento para tubos protectores al aire libre en función de su disposición
        tabla_tubos = [
            [1.00, 0.94, 0.91, 0.88, 0.87, 0.86],  # B = 1
            [0.92, 0.87, 0.84, 0.81, 0.80, 0.79],  # B = 2
            [0.85, 0.81, 0.78, 0.76, 0.75, 0.74],  # B = 3
            [0.82, 0.78, 0.74, 0.73, 0.72, 0.72],  # B = 4
            [0.80, 0.76, 0.72, 0.71, 0.70, 0.70],  # B = 5
            [0.79, 0.75, 0.71, 0.70, 0.69, 0.68],  # B = 6
        ]

        # Capacidad de conducción de corriente para conductores aislados con PVC 70°C a temperatura ambiente de 30°C
        tabla_capacidad_conduccion_PVC = {
            1.0: {"Monofásico": 13.5, "Trifásico": 12},
            1.5: {"Monofásico": 17.5, "Trifásico": 15.5},
            2.5: {"Monofásico": 24, "Trifásico": 21},
            4: {"Monofásico": 32, "Trifásico": 28},
            6: {"Monofásico": 41, "Trifásico": 36},
            10: {"Monofásico": 57, "Trifásico": 50},
            16: {"Monofásico": 76, "Trifásico": 68},
            25: {"Monofásico": 101, "Trifásico": 89},
            35: {"Monofásico": 125, "Trifásico": 111},
            50: {"Monofásico": 151, "Trifásico": 134},
            70: {"Monofásico": 192, "Trifásico": 171},
            95: {"Monofásico": 232, "Trifásico": 207},
            120: {"Monofásico": 269, "Trifásico": 239},
            150: {"Monofásico": 309, "Trifásico": 272},
            185: {"Monofásico": 353, "Trifásico": 310},
            240: {"Monofásico": 415, "Trifásico": 364},
            300: {"Monofásico": 473, "Trifásico": 419},
            400: {"Monofásico": 566, "Trifásico": 502},
            500: {"Monofásico": 651, "Trifásico": 578},
        }

        # Capacidad de conducción de corriente para conductores aislados con goma etileno propileno (EPR) o polietileno reticulado (XLPE) a temperatura ambiente de 30°C
        tabla_capacidad_conduccion_EPR_XLPE = {
            1.0: {"Monofásico": 18, "Trifásico": 16},
            1.5: {"Monofásico": 23, "Trifásico": 20},
            2.5: {"Monofásico": 31, "Trifásico": 27},
            4: {"Monofásico": 42, "Trifásico": 36},
            6: {"Monofásico": 54, "Trifásico": 48},
            10: {"Monofásico": 74, "Trifásico": 66},
            16: {"Monofásico": 100, "Trifásico": 88},
            25: {"Monofásico": 132, "Trifásico": 116},
            35: {"Monofásico": 163, "Trifásico": 144},
            50: {"Monofásico": 198, "Trifásico": 175},
            70: {"Monofásico": 252, "Trifásico": 222},
            95: {"Monofásico": 305, "Trifásico": 268},
            120: {"Monofásico": 353, "Trifásico": 311},
            150: {"Monofásico": 400, "Trifásico": 353},
            185: {"Monofásico": 456, "Trifásico": 402},
            240: {"Monofásico": 536, "Trifásico": 474},
            300: {"Monofásico": 617, "Trifásico": 545},
            400: {"Monofásico": 738, "Trifásico": 652},
            500: {"Monofásico": 848, "Trifásico": 750},
        }

        # Caída de tensión en V/A*km para conductores de cobre aislados
        tabla_k = {
            1: {"Monofásico": 34.00, "Trifásico": 29.00},
            1.5: {"Monofásico": 23.00, "Trifásico": 20.00},
            2.5: {"Monofásico": 14.00, "Trifásico": 12.00},
            4: {"Monofásico": 8.70, "Trifásico": 7.50},
            6: {"Monofásico": 5.80, "Trifásico": 5.10},
            10: {"Monofásico": 3.50, "Trifásico": 3.00},
            16: {"Monofásico": 3.31, "Trifásico": 1.96},
            25: {"Monofásico": 1.52, "Trifásico": 1.28},
            35: {"Monofásico": 1.12, "Trifásico": 0.96},
            50: {"Monofásico": 0.82, "Trifásico": 0.73},
            70: {"Monofásico": 0.63, "Trifásico": 0.54},
            95: {"Monofásico": 0.49, "Trifásico": 0.42},
            120: {"Monofásico": 0.41, "Trifásico": 0.35},
            150: {"Monofásico": 0.36, "Trifásico": 0.31},
            185: {"Monofásico": 0.32, "Trifásico": 0.27},
            240: {"Monofásico": 0.26, "Trifásico": 0.23},
            300: {"Monofásico": 0.23, "Trifásico": 0.20},
            400: {"Monofásico": 0.20, "Trifásico": 0.18},
            500: {"Monofásico": 0.19, "Trifásico": 0.16},
        }

        # --------------------- CABLE CORTO ---------------------

        if tipoCaidaTension == "Alimentador":
            caidaTension = 0.02 # 2%
        elif tipoCaidaTension == "Circuito derivado":
            caidaTension = 0.03 # 3%
        else:
            caidaTension = 0.05 # 5%

        print(f"Caída de tensión: {caidaTension}")

        corriente = demandaMaximaCasa / (math.sqrt(3) * voltaje * 0.9)
        print(f"Corriente {corriente}")

        factorCorreccionPorAgrupamiento = tabla_tubos[tubosVerticales - 1][tubosHorizontales - 1]
        if aislamientoConductor != "PVC":
            aislante = "EPR o XLPE"
        else:
            aislante = aislamientoConductor
        factorCorreccionPorTemperatura = tabla_temperatura[temperatura][aislante]
        print(f"Factor de corrección por agrupamiento: {factorCorreccionPorAgrupamiento}")
        print(f"Factor de corrección por temperatura: {factorCorreccionPorTemperatura}")

        corrienteEquivalente = corriente / (factorCorreccionPorAgrupamiento * factorCorreccionPorTemperatura)
        print(f"Corriente equivalente: {corrienteEquivalente}")
        
        if longitudCable <= 40:
            if aislamientoConductor == "PVC":
                # Itera la tabla de PVC para buscar la seccion adecuada
                for seccion, corrientes in tabla_capacidad_conduccion_PVC.items():
                    if corrienteEquivalente <= corrientes[tipoSistema]:
                        seccionCable1 = seccion
                        break
            else:
                # Itera la tabla de EPR para buscar la seccion adecuada
                for seccion, corrientes in tabla_capacidad_conduccion_EPR_XLPE.items():
                    if corrienteEquivalente <= corrientes[tipoSistema]:
                        seccionCable1 = seccion
                        break

            k = tabla_k[seccionCable1][tipoSistema]
            print(f"K: {k}")
            deltaV = k * corriente * longitudCable / 1000
            print(f"DeltaV: {deltaV}")
            voltajeConCaidaTension = voltaje * caidaTension
            print(f"Voltaje con Caida de Tension: {voltajeConCaidaTension}")

            seccionCable2 = seccionCable1
            if deltaV > voltajeConCaidaTension:
                # Seleccionamos la tabla adecuada según el aislamiento
                tabla_capacidad_conduccion = tabla_capacidad_conduccion_PVC if aislamientoConductor == "PVC" else tabla_capacidad_conduccion_EPR_XLPE
                
                # Obtenemos la lista de secciones
                lista_secciones = list(tabla_capacidad_conduccion.keys())

                seccionCable2 = seccionCable1
                # Buscamos la sección actual y pasamos a la siguiente si existe
                for i, seccion in enumerate(lista_secciones):
                    if seccionCable1 == tabla_capacidad_conduccion[seccion][tipoSistema]:
                        if i + 1 < len(lista_secciones):  # Verificamos si hay una sección siguiente
                            seccionCable2 = lista_secciones[i + 1]  # Guardamos la siguiente clave
                        break
        else:
            # --------------------- CABLE LARGO ---------------------
            deltaV = voltaje * caidaTension
            print(f"DeltaV: {deltaV}")

            k = deltaV / (corriente * longitudCable / 1000)
            print(f"K: {k}")

            seccionAnterior = None
            for seccion, valoresK in reversed(list(tabla_k.items())):
                # Guardamos la sección anterior si la condición se cumple
                if valoresK[tipoSistema] >= k:
                # Si el valor actual es mayor o igual a k, tomamos la sección anterior
                    if seccionAnterior is not None:
                        seccionCable1 = seccionAnterior
                    break
    
                # Actualizamos previous_seccion con la sección actual
                seccionAnterior = seccion

            if aislamientoConductor == "PVC":
                # Itera la tabla de PVC para buscar la corriente que soporta
                for seccion, corrientes in tabla_capacidad_conduccion_PVC.items():
                    if seccionCable1 == seccion:
                        corrienteQueSoporta = corrientes[tipoSistema]
                        break
            else:
                # Itera la tabla de EPR para buscar la corriente que soporta
                for seccion, corrientes in tabla_capacidad_conduccion_EPR_XLPE.items():
                    if seccionCable1 == seccion:
                        corrienteQueSoporta = corrientes[tipoSistema]
                        break

            print(f"Corriente que soporta: {corrienteQueSoporta}")
            
            seccionCable2 = seccionCable1
            if corrienteEquivalente > corrienteQueSoporta:
                # Seleccionamos la tabla adecuada según el aislamiento
                tabla_capacidad_conduccion = tabla_capacidad_conduccion_PVC if aislamientoConductor == "PVC" else tabla_capacidad_conduccion_EPR_XLPE
                
                # Obtenemos la lista de secciones
                lista_secciones = list(tabla_capacidad_conduccion.keys())

                # Buscamos la sección actual y pasamos a la siguiente si existe
                for i, seccion in enumerate(lista_secciones):
                    if seccionCable1 == tabla_capacidad_conduccion[seccion][tipoSistema]:
                        if i + 1 < len(lista_secciones):  # Verificamos si hay una sección siguiente
                            seccionCable2 = lista_secciones[i + 1]  # Guardamos la siguiente clave
                        break

        if seccionCable1 >= seccionCable2:
            seccionCable = seccionCable1
        else:
            seccionCable = seccionCable2

        # Labels
        
        self.label_criterioCaidaTension.setText(str(seccionCable2))
        self.label_criterioCaidaConduccion.setText(str(seccionCable1))
        self.label_seccionCable.setText(str(seccionCable))
        self.mostrarItemsOcultosInterfaz3()

    
    def mostrarItemsOcultosInterfaz3(self):
        # Mostrar los labels
        self.label_titulo_criterioCaidaTension.setVisible(True)
        self.label_criterioCaidaTension.setVisible(True)
        self.label_titulo_criterioCaidaConduccion.setVisible(True)
        self.label_criterioCaidaConduccion.setVisible(True)
        self.label_titulo_seccionCable.setVisible(True)
        self.label_seccionCable.setVisible(True)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()