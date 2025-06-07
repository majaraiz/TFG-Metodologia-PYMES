# Guía Básica

## Instalación Python Windows y librerías Jinja2 y PyYAML

### Paso 1: Descargar Python

1. Ir a la página oficial: **https://python.org**

2. Hacer clic en "Downloads"

3. Hacer clic en "Download Python 3.13.4" (o la versión deseada)

4. Ir a la carpeta donde se encuentre el fichero descargado y hacer doble clic en el archivo para comenzar el proceso de instalación

**¡IMPORTANTE!** Marcar la casilla **"Add Python to PATH"** antes de continuar.

5. Una vez finalizado abrir el CMD de Windows (Símbolo de sistema) para comprobar la correcta instalación

6. Escribir: `python --version` y pulsar Enter

Debe aparecer algo similar a:

```
pip 25.0.1 from C:\Users\admin\AppData\Local\Programs\Python\Python313\Lib\site-packages\pip (python 3.13) Python 3.13.4
```

## Instalar bibliotecas necesarias

### Instalar Jinja2

1. En la ventana de CMD escribir `pip install jinja2` + Enter

2. Esperar que finalice el proceso

3. Una vez finalizado para comprobar la correcta instalación escribir `pip show Jinja2`

Deberá de aparecer algo similar a:

```
Name: Jinja2
Version: 3.1.6
```

### Instalar PyYAML

1. En la ventana de CMD escribir `pip install pyyaml` + Enter

2. Esperar que finalice el proceso

3. Una vez finalizado para comprobar la correcta instalación escribir `pip show PyYAML`

Deberá de aparecer algo similar a:

```
Name: PyYAML
Version: 6.0.2
```
