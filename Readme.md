# Procesamiento de Calificaciones

## Descripción
Este proyecto permite unificar información de calificaciones de estudiantes a partir de múltiples archivos CSV de calificaciones y una lista de estudiantes. Los datos se consolidan en un único archivo de salida que muestra la información organizada por estudiante.

## Autor
**Ramiro Hualpa**

## Requisitos
- Python 3.x
- Librerías estándar de Python: `os`, `csv`, `re`, `json`, `sys`, `io`, `collections`

## Estructura de Archivos
```
/Proyecto
  ├── procesar_calificaciones.py  # Script principal
  ├── config.json                  # Configuración del proyecto
  ├── /Calificaciones               # Carpeta con archivos CSV de calificaciones
  ├── /Lista de estudiantes         # Carpeta con el CSV de la lista de estudiantes
  ├── reporte_final.csv             # Archivo de salida generado
```

## Configuración
El archivo `config.json` define los parámetros clave del proyecto:

```json
{
    "ruta_calificaciones": "./Calificaciones",
    "ruta_estudiantes": "./Lista de estudiantes",
    "archivo_salida": "reporte_final.csv",
    "columnas_calificaciones": {
        "correo": "Dirección de correo",
        "calificacion": "Calificación/10,00"
    },
    "columnas_estudiantes": {
        "correo": "Dirección de correo",
        "nombre": "Nombre",
        "apellido": "Apellido(s)"
    }
}
```

### Explicación de los parámetros:
- **`ruta_calificaciones`**: Directorio donde se almacenan los archivos CSV con calificaciones. Puede ser una ruta relativa (`./Calificaciones`) o absoluta (`C:/Usuarios/Ramiro/Calificaciones`).
- **`ruta_estudiantes`**: Carpeta que contiene el archivo CSV con la lista de estudiantes inscritos.
- **`archivo_salida`**: Nombre del archivo CSV generado con la consolidación de datos.
- **`columnas_calificaciones`**: Definición de los nombres de columnas esperadas en los archivos de calificaciones.
- **`columnas_estudiantes`**: Nombres de las columnas esperadas en la lista de estudiantes.

## Uso
### 1. Preparar los archivos
- Ubicar los archivos CSV de calificaciones en la carpeta `Calificaciones`.
- Asegurar que el archivo de la lista de estudiantes esté en `Lista de estudiantes`.
- Revisar que los nombres de las columnas en los archivos coincidan con los definidos en `config.json`.

### 2. Ejecutar el script
Ejecutar el siguiente comando en la terminal dentro del directorio del proyecto:
```sh
python procesar_calificaciones.py
```

### 3. Revisar la salida
El archivo `reporte_final.csv` se generará en la misma carpeta del script con la información consolidada.

## Manejo de Errores y Depuración
- El script imprime en la terminal las columnas detectadas en cada archivo CSV para verificar la coincidencia con la configuración.
- Si un archivo no contiene las columnas esperadas, se omitirá con una advertencia.
- Se ha forzado la codificación `utf-8` y `utf-8-sig` para evitar problemas con caracteres especiales.

## Licencia
Este proyecto es de uso libre y puede ser modificado según las necesidades del usuario.

