import os
import csv
import re
import json
import sys
import io
from collections import defaultdict

# Configurar la codificación de salida para evitar errores de Unicode
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

def cargar_configuracion(config_file="config.json"):
    with open(config_file, "r", encoding="utf-8") as f:
        return json.load(f)

def limpiar_nombre_archivo(nombre):
    match = re.search(r'Cuestionario(?: de)? (.*?) -', nombre)
    return match.group(1) if match else nombre

def leer_calificaciones(ruta, columnas):
    calificaciones = defaultdict(dict)
    archivos = [f for f in os.listdir(ruta) if f.endswith(".csv")]
    nombres_archivos = []
    
    for archivo in archivos:
        ruta_completa = os.path.join(ruta, archivo)
        nombre_limpio = limpiar_nombre_archivo(archivo)
        nombres_archivos.append(nombre_limpio)
        
        try:
            with open(ruta_completa, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                columnas_detectadas = reader.fieldnames
                print(f"Columnas detectadas en {archivo}: {columnas_detectadas}")
                
                if columnas["correo"] not in columnas_detectadas or columnas["calificacion"] not in columnas_detectadas:
                    print(f"Advertencia: Archivo {archivo} no contiene las columnas esperadas. Se omitirá.")
                    continue
                
                for row in reader:
                    try:
                        correo = row[columnas["correo"]].strip().lower()
                        calificacion = row.get(columnas["calificacion"], "-")
                        calificaciones[correo][nombre_limpio] = calificacion
                    except KeyError as e:
                        print(f"Error procesando fila en {archivo}: {e}")
        except Exception as e:
            print(f"Error al leer el archivo {archivo}: {e}")
    
    return calificaciones, nombres_archivos

def leer_estudiantes(ruta, columnas):
    estudiantes = {}
    
    try:
        archivo_lista = [f for f in os.listdir(ruta) if f.endswith(".csv")][0]
        ruta_completa = os.path.join(ruta, archivo_lista)
        
        # Cambiar encoding a 'utf-8-sig' para remover el BOM
        with open(ruta_completa, newline='', encoding='utf-8-sig') as csvfile:  # <- Corrección aquí
            reader = csv.DictReader(csvfile)
            columnas_detectadas = reader.fieldnames
            print(f"Columnas detectadas en {archivo_lista}: {columnas_detectadas}")
            
            # Verificar columnas sin BOM
            if (columnas["correo"] not in columnas_detectadas or 
                columnas["nombre"] not in columnas_detectadas or 
                columnas["apellido"] not in columnas_detectadas):
                print(f"Advertencia: Archivo {archivo_lista} no contiene las columnas esperadas. Se omitirá.")
                return estudiantes
            
            for row in reader:
                try:
                    correo = row[columnas["correo"]].strip().lower()
                    nombre = row[columnas["nombre"]].strip().title()
                    apellido = row[columnas["apellido"]].strip().title()
                    estudiantes[correo] = {"Nombre": nombre, "Apellido": apellido}
                except KeyError as e:
                    print(f"Error procesando fila en {archivo_lista}: {e}")
    except IndexError:
        print("Error: No se encontró ningún archivo de estudiantes en la ruta especificada.")
    except Exception as e:
        print(f"Error al leer el archivo de estudiantes: {e}")
    
    return estudiantes

def generar_reporte(estudiantes, calificaciones, nombres_archivos, salida):
    encabezado = ["Nombre", "Apellido", "Correo"] + nombres_archivos
    
    try:
        with open(salida, mode='w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(encabezado)
            
            for correo, datos in estudiantes.items():
                fila = [datos["Nombre"], datos["Apellido"], correo]
                fila += [calificaciones[correo].get(nombre, "-") for nombre in nombres_archivos]
                writer.writerow(fila)
        
        print(f"Archivo generado: {salida}")
    except Exception as e:
        print(f"Error al escribir el archivo de salida: {e}")

def main():
    config = cargar_configuracion()
    ruta_calificaciones = config.get("ruta_calificaciones", "./Calificaciones")
    ruta_estudiantes = config.get("ruta_estudiantes", "./Lista de estudiantes")
    salida = config.get("archivo_salida", "reporte_final.csv")
    
    columnas_calificaciones = config.get("columnas_calificaciones", {"correo": "Dirección de correo", "calificacion": "Calificación/10,00"})
    columnas_estudiantes = config.get("columnas_estudiantes", {"correo": "Dirección de correo", "nombre": "Nombre", "apellido": "Apellido(s)"})
    
    calificaciones, nombres_archivos = leer_calificaciones(ruta_calificaciones, columnas_calificaciones)
    estudiantes = leer_estudiantes(ruta_estudiantes, columnas_estudiantes)
    generar_reporte(estudiantes, calificaciones, nombres_archivos, salida)

if __name__ == "__main__":
    main()