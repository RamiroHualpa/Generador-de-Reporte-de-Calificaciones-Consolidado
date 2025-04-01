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

def extraer_regional(grupos):
    grupos_lista = [g.strip() for g in grupos.split(",")]
    return next((g for g in grupos_lista if not re.match(r'M\d{4}-\d{2}', g)), grupos_lista[-1])

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
                
                if columnas["correo"] not in reader.fieldnames or columnas["calificacion"] not in reader.fieldnames:
                    continue
                
                for row in reader:
                    correo = row[columnas["correo"]].strip().lower()
                    calificacion = row.get(columnas["calificacion"], "-")
                    
                    if calificacion not in ["-"]:
                        try:
                            calificacion = round(float(calificacion.replace(",", ".")))
                        except ValueError:
                            calificacion = "-"
                    
                    calificaciones[correo][nombre_limpio] = calificacion
        except Exception as e:
            print(f"Error al leer el archivo {archivo}: {e}")
    
    return calificaciones, nombres_archivos

def leer_estudiantes(ruta, columnas):
    estudiantes = {}
    try:
        archivo_lista = [f for f in os.listdir(ruta) if f.endswith(".csv")][0]
        ruta_completa = os.path.join(ruta, archivo_lista)
        
        with open(ruta_completa, newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            
            if (columnas["correo"] not in reader.fieldnames or 
                columnas["nombre"] not in reader.fieldnames or 
                columnas["apellido"] not in reader.fieldnames or
                "Grupos" not in reader.fieldnames):
                return estudiantes
            
            for row in reader:
                correo = row[columnas["correo"].strip()].lower()
                nombre = row[columnas["nombre"].strip()].title()
                apellido = row[columnas["apellido"].strip()].title()
                regional = extraer_regional(row["Grupos"].strip())
                
                estudiantes[correo] = {"Regional": regional, "Nombre": nombre, "Apellido": apellido}
    except Exception as e:
        print(f"Error al leer el archivo de estudiantes: {e}")
    
    return estudiantes

def generar_reporte(estudiantes, calificaciones, nombres_archivos, salida):
    encabezado = ["Regional", "Nombre", "Apellido", "Correo"] + nombres_archivos
    
    try:
        with open(salida, mode='w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(encabezado)
            
            for correo, datos in estudiantes.items():
                fila = [datos["Regional"], datos["Nombre"], datos["Apellido"], correo]
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
