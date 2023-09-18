"""Proyecto Final
Luis Gustavo Montoya Villalobos
Programacion I"""

from os import system
import sqlite3
from datetime import datetime
system("cls")


connCl = sqlite3.connect('DataBaseCliente.db')
connCu = sqlite3.connect('DataBaseCuentas.db')
connMo = sqlite3.connect('DataBaseMovimientos.db')

cl = connCl.cursor()
cu = connCu.cursor()
mo = connMo.cursor()

#Creacion de las bases de datos
cl.execute(""" CREATE TABLE IF NOT EXISTS cliente(
          cedula INT PRIMARY KEY,
          nombre TEXT NOT NULL,
          apellido1 TEXT NOT NULL,
          apellido2 TEXT NOT NULL)""")

cu.execute(""" CREATE TABLE IF NOT EXISTS cuentas(
          cedula INT PRIMARY KEY,
          numCuenta INT NOT NULL,
          montoDisponible INT NOT NULL,
          estado TEXT NOT NULL)""")

mo.execute(""" CREATE TABLE IF NOT EXISTS movimientos(
          cedula INT NOT NULL,
          numCuenta INT NOT NULL,
          abono INT,
          retiro INT,
          balance INT NOT NULL)""")


#Metodo Ingresar Cliente con validaciones para elementos numericos
def ingresoCliente():

    while True:
        try:
            ced = int(input("Digite el numero de cedula: "))
        except ValueError:
            print("Debes escribir un número.")
            continue

        if ced < 0:
            print("Debes escribir un número positivo.")
            continue
        else:
            break

    while True:
        nom = input("Digite el nombre del cliente: ")
        numero= ''
        for caracter in nom:
            
            if caracter.isdigit():
                numero+=caracter
        if numero != '':
            print('El nombre posee caracteres numericos. Favor ingresar de nuevo')
        else:
            break
    
    while True:
        ape1 = input("Digite el primer apellido: ")
        numero= ''
        for caracter in ape1:
            if caracter.isdigit():
                numero+=caracter
        if numero != '':
            print('El nombre posee caracteres numericos. Favor ingresar de nuevo')
        else:
            break    

    while True:
        ape2 = input("Digite el segundo apellido: ")
        numero= ''
        for caracter in ape2:  
            if caracter.isdigit():
                numero+=caracter
        if numero != '':
            print('El nombre posee caracteres numericos. Favor ingresar de nuevo')
        else:
            break       
    
    while True:
        try:
            numCuenta = int(input("Digite el numero de cuenta: "))
        except ValueError:
            print("Debes escribir un número.")
            continue

        if numCuenta < 0:
            print("Debes escribir un número positivo.")
            continue
        else:
            break

    while True:
        try:
            monto= int(input("Digite el monto a ingresar: "))
        except ValueError:
            print("Debes escribir un número.")
            continue

        if monto < 0:
            print("Debes escribir un número positivo.")
            continue
        else:
            break

    cl.execute("INSERT INTO cliente VALUES (?, ?, ?, ?)", (ced,nom,ape1,ape2))
    cu.execute("INSERT INTO cuentas VALUES (?, ?, ?, ?)", (ced,numCuenta,monto,"ACTIVA"))
    mo.execute("INSERT INTO movimientos VALUES (?, ?, ?, ?, ?)", (ced,numCuenta,0,0,monto))
    connCl.commit()
    connCu.commit()
    connMo.commit()




#Metodo estado de cuenta. Activar o Desactivar Cuenta
def EstadoCuenta():

    ced = int(input("Digite el numero de cedula del cliente que desea modificar: "))
    i=int(input("Seleccione una opcion: 1)ACTIVAR   2)DESACTIVAR    3)Cancelar operacion:  "))
    if i == 1:
        cambioEstado = "Update cuentas SET estado = ? where cedula = ?"
        connCu.execute(cambioEstado,('ACTIVA',ced))
        connCu.commit()
    elif i==2:
        cambioEstado = "Update cuentas SET estado = ? where cedula = ?"
        connCu.execute(cambioEstado,('INACTIVA',ced))
        connCu.commit()
    elif i==3:
        menu_principal()
        system('cls')
    else: 
        input("Valor no encontrado. Digite ENTER para continuar. ")
    print('Estado modificado con Exito')
    input('Presione Enter para continuar')


#Metodo para abonar a una cuenta
def abonoCuenta():
    c = int(input("Digite el numero de cedula del cliente: "))
    EstadoCuenta = "SELECT estado FROM cuentas WHERE cedula =?"
    cu.execute(EstadoCuenta,(c,))
    estados = cu.fetchone()
    for estado in estados:    
        print('-'*50)
    if estado == 'ACTIVA':
        numeroCuenta = "SELECT numCuenta FROM cuentas WHERE cedula =?"
        cu.execute(numeroCuenta,(c,))
        cuentas = cu.fetchone()
        for cuenta in cuentas:    
            print("El numero de cuenta es ",cuenta,' ',estado)

        disponible = "SELECT montoDisponible FROM cuentas WHERE cedula =?"
        cu.execute(disponible,(c,))
        filas = cu.fetchone()
        for fila in filas:    
            print("Monto Disponible: ",fila)

        while True:
            try:
                abono = int(input("Digite el monto que desea depositar: "))
            except ValueError:
                print("Debes escribir un número.")
                continue

            if abono < 0:
                print("Debes escribir un número positivo.")
                continue
            else:
                break
        
        ac = fila+abono
        print("El monto actual es de ",ac)
        nuevoMonto = "Update cuentas SET montoDisponible = ? where cedula = ?"
        connCu.execute(nuevoMonto,(ac,c))
        connCu.commit()

        mo.execute("INSERT INTO movimientos VALUES (?, ?, ?, ?, ?)", (c,cuenta,abono,0,ac))
        connMo.commit()
        input("Digite Enter ") 
    
    else:
        print('Cliente posee cuenta INACTIVA. Favor ACTIVAR la Cuenta para realizar movimientos')
        input("Digite Enter ") 

#Metodo para retirar de una cuenta
def retiroCuenta():
    c = int(input("Digite el numero de cedula del cliente: "))

    EstadoCuenta = "SELECT estado FROM cuentas WHERE cedula =?"
    cu.execute(EstadoCuenta,(c,))
    estados = cu.fetchone()
    for estado in estados:    
        print('-'*50)
    if estado == 'ACTIVA':
        numeroCuenta = "SELECT numCuenta FROM cuentas WHERE cedula =?"
        cu.execute(numeroCuenta,(c,))
        cuentas = cu.fetchone()
        for cuenta in cuentas:    
            print("El numero de cuenta es ",cuenta)

        disponible = "SELECT montoDisponible FROM cuentas WHERE cedula =?"
        cu.execute(disponible,(c,))
        filas = cu.fetchone()
        for fila in filas:    
            print("Monto Disponible: ",fila)

        if fila > 0:
           
            v = True
            while v == True:
                while True:
                    try:
                        retiro = int(input("Digite el monto que desea retirar: "))
                    except ValueError:
                        print("Debes escribir un número.")
                        continue

                    if retiro < 0:
                        print("Debes escribir un número positivo.")
                        continue
                    else:
                        break                
                
                if fila >= retiro:
                    ac = fila-retiro
                    print("El monto actual es de ",ac)
                    nuevoMonto = "Update cuentas SET montoDisponible = ? where cedula = ?"
                    connCu.execute(nuevoMonto,(fila-retiro,c))
                    connCu.commit()

                    mo.execute("INSERT INTO movimientos VALUES (?, ?, ?, ?, ?)", (c,cuenta,0,retiro,ac))
                    connMo.commit()
                    v = False
            
                else:
                    print("Monto digitado es mayor que el disponible")
                    input("Digite Enter ")
            input("Digite Enter ")
        else:
            print('Cuenta con fondos insuficientes')
            input("Digite Enter ")
    
    else:
        print('Cliente posee cuenta INACTIVA. Favor ACTIVAR la Cuenta para realizar movimientos')
        input("Digite Enter ") 

def reporte():
    c = int(input("Digite el numero de cedula del cliente: "))
    mo.execute("SELECT * FROM movimientos")
    reporte = mo.fetchall()
    print('Cuenta\t Abono\tRetiro\tBalance')
    for datos in reporte:    
        if datos[0] == c:
            print(datos[1],'\t',datos[2],'\t',datos[3],'\t',datos[4])

    input("Digite Enter ")





#Menu Principal
def menu_principal():
   
    continuar = True
    while continuar:
        system("cls")       
        print("--------- MENU DE INICIO ----------")
        print("1- Ingresar cliente nuevo a base de datos")
        print("2- Activar/Desactivar Cuenta")
        print("3- Deposito a Cuenta")
        print("4- Retiro a Cuenta")
        print("5- Reporte de Movientos")
        print("0- Salir")
        seleccion = input("Digite su seleccion: ")
        if(seleccion == '1'):
            system("cls")
            ingresoCliente()
        elif(seleccion == '2'):
            system("cls")
            EstadoCuenta()
        elif(seleccion == '3'):
            system("cls")
            abonoCuenta()
        elif(seleccion == '4'):
            system("cls")
            retiroCuenta()
        elif(seleccion == '5'):
            system("cls")
            reporte()
        elif(seleccion == '0'):
            system("cls")                     
            input("Saliendo del Sistema... \nEjecucion Finalizada")
            continuar = False
        else:
            input("Seleccion no se encuentra disponible. Presione ENTER: ")

menu_principal()
connCl.close()
connCu.close()
connMo.close()