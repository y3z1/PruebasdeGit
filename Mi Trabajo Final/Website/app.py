from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import csv
from colorama import init, Fore

# Inicializar colorama (aunque no se usará en la web)
init(autoreset=True)

# Definir la clase Transaccion
class Transaccion:
    def __init__(self, descripcion, cantidad, tipo, fecha, moneda='EUR'):
        self.descripcion = descripcion
        self.cantidad = cantidad
        self.tipo = tipo  # 'ingreso' o 'gasto'
        self.fecha = fecha  # fecha en formato 'DD-MM-YY'
        self.moneda = moneda  # Moneda, por defecto 'EUR'

# Definir la clase FinanzasPersonales
class FinanzasPersonales:
    def __init__(self, archivo_csv):
        self.transacciones = []
        self.archivo_csv = archivo_csv
        self.cargar_desde_csv()

    def agregar_transaccion(self, transaccion):
        self.transacciones.append(transaccion)
        self.guardar_en_csv()

    def mostrar_totales(self):
        total_ingresos = sum(t.cantidad for t in self.transacciones if t.tipo == 'ingreso')
        total_gastos = sum(t.cantidad for t in self.transacciones if t.tipo == 'gasto')
        balance = total_ingresos - total_gastos
        return total_ingresos, total_gastos, balance

    def mostrar_transacciones(self):
        return self.transacciones

    def guardar_en_csv(self):
        with open(self.archivo_csv, mode='w', newline='') as archivo:
            escritor_csv = csv.writer(archivo)
            escritor_csv.writerow(['Fecha', 'Descripción', 'Cantidad', 'Tipo', 'Moneda'])
            for t in self.transacciones:
                escritor_csv.writerow([t.fecha, t.descripcion, int(t.cantidad), t.tipo, t.moneda])

    def cargar_desde_csv(self):
        try:
            with open(self.archivo_csv, mode='r') as archivo:
                lector_csv = csv.reader(archivo)
                next(lector_csv)  # Saltar la cabecera
                for fila in lector_csv:
                    if fila:
                        fecha, descripcion, cantidad, tipo, moneda = fila
                        transaccion = Transaccion(descripcion, float(cantidad), tipo, fecha, moneda)
                        self.transacciones.append(transaccion)
        except FileNotFoundError:
            print("El archivo CSV no existe, se creará uno nuevo al guardar las transacciones.")

# Inicializar la aplicación Flask
app = Flask(__name__)
finanzas = FinanzasPersonales('transacciones.csv')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    if request.method == 'POST':
        descripcion = request.form['descripcion']
        cantidad = float(request.form['cantidad'])
        tipo = request.form['tipo']
        fecha = request.form['fecha']
        try:
            datetime.strptime(fecha, '%d-%m-%y')
            transaccion = Transaccion(descripcion, cantidad, tipo, fecha)
            finanzas.agregar_transaccion(transaccion)
            return redirect(url_for('index'))
        except ValueError:
            return "Fecha inválida. Por favor, ingrese la fecha en formato DD-MM-YY."
    return render_template('agregar.html')

@app.route('/mostrar_totales')
def mostrar_totales():
    total_ingresos, total_gastos, balance = finanzas.mostrar_totales()
    return render_template('mostrar_totales.html', total_ingresos=total_ingresos, total_gastos=total_gastos, balance=balance)

@app.route('/transacciones')
def transacciones():
    transacciones = finanzas.mostrar_transacciones()
    return render_template('transacciones.html', transacciones=transacciones)

if __name__ == "__main__":
    app.run(debug=True)
