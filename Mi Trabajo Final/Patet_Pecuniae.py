import csv
from datetime import datetime
from colorama import init, Fore
import pyfiglet
import time

# Inicializar colorama
init(autoreset=True)

# Definir una clase para representar una transacción (ingreso o gasto)
class Transaccion:
    def __init__(self, descripcion, cantidad, tipo, fecha, moneda='EUR'):
        self.descripcion = descripcion
        self.cantidad = cantidad
        self.tipo = tipo  # 'ingreso' o 'gasto'
        self.fecha = fecha  # fecha en formato 'DD-MM-YY'
        self.moneda = moneda  # Moneda, por defecto 'EUR'

# Definir una clase para representar el control de finanzas
class FinanzasPersonales:
    def __init__(self, archivo_csv):
        self.transacciones = []
        self.archivo_csv = archivo_csv
        self.cargar_desde_csv()

    def agregar_transaccion(self, transaccion):
        self.transacciones.append(transaccion)
        if transaccion.tipo == 'ingreso':
            print(Fore.GREEN + "Así me gusta Chaval... sigue así!!!")
        else:
            print(Fore.RED + "Chaval, controla el gasto!!!")
        print(Fore.RESET)
        self.guardar_en_csv()

    def mostrar_totales(self):
        total_ingresos = sum(t.cantidad for t in self.transacciones if t.tipo == 'ingreso')
        total_gastos = sum(t.cantidad for t in self.transacciones if t.tipo == 'gasto')
        balance = total_ingresos - total_gastos
        print(f"Total ingresos: {Fore.GREEN}{total_ingresos} EUR")
        print(f"Total gastos: {Fore.RED}{total_gastos} EUR")
        print(f"Balance: {balance} EUR")

    def mostrar_transacciones(self):
        if not self.transacciones:
            print("No hay transacciones registradas.")
            return
        print("Transacciones registradas:")
        for t in self.transacciones:
            color = Fore.GREEN if t.tipo == 'ingreso' else Fore.RED
            print(f"Fecha: {t.fecha}, Descripción: {t.descripcion}, Cantidad: {color}{t.cantidad} {t.moneda}, Tipo: {t.tipo}")
        print(Fore.RESET)

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

def imprimir_titulo(titulo):
    ascii_art = pyfiglet.figlet_format(titulo)
    lines = ascii_art.split("\n")
    for line in lines:
        print(Fore.YELLOW + line)
        time.sleep(1.0)  # Pequeño retraso para el efecto de animación
    print(Fore.RESET)

# Mostrar título animado y vistoso
imprimir_titulo("Patet Pecuniae")

def mostrar_menu_ingresos():
    print("\n*** Opciones de ingresos ***")
    print("1. Nómina")
    print("2. Extras")
    print("3. Otros")
    print("4. Volver al menú principal")

def mostrar_menu_gastos():
    print("\n*** Opciones de gastos ***")
    print("1. Alquiler")
    print("2. Mercado")
    print("3. Ocio")
    print("4. Combustible")
    print("5. Otros")
    print("6. Volver al menú principal")

# Función principal
def main():
    archivo_csv = 'transacciones.csv'
    finanzas = FinanzasPersonales(archivo_csv)

    while True:
        print("\n*** Mis Cuentas Claras ***")
        print("1. Agregar un ingreso")
        print("2. Agregar un gasto")
        print("3. Mostrar totales de ingresos y gastos")
        print("4. Mostrar todas las transacciones")
        print("5. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            mostrar_menu_ingresos()
            opcion_ingresos = input("Seleccione una opción de ingresos: ")
            if opcion_ingresos == "1":
                descripcion = "Nómina"
            elif opcion_ingresos == "2":
                descripcion = "Extras"
            elif opcion_ingresos == "3":
                descripcion = "Otros"
            elif opcion_ingresos == "4":
                continue
            else:
                print("Opción no válida. Por favor, seleccione una opción válida.")
                continue
            
            cantidad = float(input("Ingrese la cantidad de la transacción: "))
            fecha = input("Ingrese la fecha de la transacción (DD-MM-YY): ")
            
            try:
                # Validar el formato de la fecha
                datetime.strptime(fecha, '%d-%m-%y')
                tipo = 'ingreso'
                transaccion = Transaccion(descripcion, cantidad, tipo, fecha)
                finanzas.agregar_transaccion(transaccion)
            except ValueError:
                print("Fecha inválida. Por favor, ingrese la fecha en formato DD-MM-YY.")
        elif opcion == "2":
            mostrar_menu_gastos()
            opcion_gastos = input("Seleccione una opción de gastos: ")
            if opcion_gastos == "1":
                descripcion = "Alquiler"
            elif opcion_gastos == "2":
                descripcion = "Mercado"
            elif opcion_gastos == "3":
                descripcion = "Ocio"
            elif opcion_gastos == "4":
                descripcion = "Combustible"
            elif opcion_gastos == "5":
                descripcion = input("Ingrese una descripción para el gasto: ")
            elif opcion_gastos == "6":
                continue
            else:
                print("Opción no válida. Por favor, seleccione una opción válida.")
                continue
            
            cantidad = float(input("Ingrese la cantidad de la transacción: "))
            fecha = input("Ingrese la fecha de la transacción (DD-MM-YY): ")
            
            try:
                # Validar el formato de la fecha
                datetime.strptime(fecha, '%d-%m-%y')
                tipo = 'gasto'
                transaccion = Transaccion(descripcion, cantidad, tipo, fecha)
                finanzas.agregar_transaccion(transaccion)
            except ValueError:
                print("Fecha inválida. Por favor, ingrese la fecha en formato DD-MM-YY.")
        elif opcion == "3":
            finanzas.mostrar_totales()
        elif opcion == "4":
            finanzas.mostrar_transacciones()
        elif opcion == "5":
            print("Gracias por utilizar el programa.")
            break
        else:
            print("Opción no válida. Por favor, seleccione una opción válida.")

if __name__ == "__main__":
    main()