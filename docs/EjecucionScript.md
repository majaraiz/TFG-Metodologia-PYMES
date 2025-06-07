# Guia basica de ejecucion del Script #
  Para poder lanzar el script primero es necesario tener instalad Python y las librerias que permiten  manejar Jinja2 y YAML
  Por favor sigue los pasos de la ### Guia Basica instalación python y librerias.md ###

  Para lanzar el script con los argumentos correspondientes acceder la carpeta del equipo donde se encuentren los ficheros
  Ejemplo en Windows c:\TFG-Metodologia-PYMES\

---

## Ayuda
```bash
python scripts/generar_config.py --help
```

## Ejecución básica

### Router completo (con bloques activos según YAML)
```bash
python scripts/generar_config.py --sede "alcorcon" --tipo-sede sede_simple --dispositivo router_simple
```

### Switch completo (con bloques activos según YAML)
```bash
python scripts/generar_config.py --sede "alcorcon" --tipo-sede sede_simple --dispositivo switch_acceso_simple
```

### Ver en pantalla (añadir --mostrar-pantalla a cualquier comando)
```bash
python scripts/generar_config.py --sede "alcorcon" --tipo-sede sede_simple --dispositivo router_simple --mostrar-pantalla
```

## Bloque de Cifrado

### Añadir cifrado al router de sede remota
```bash
python scripts/generar_config.py --sede "alcorcon" --tipo-sede sede_simple --dispositivo router_simple --bloque-cifrado
```

## Configurar sede central para cifrar con esta sede
```bash
python scripts/generar_config.py --sede "alcorcon" --tipo-sede sede_simple --dispositivo router_simple --bloque-sede-central-cifrado
```

## Bloque de Gestion

### Añadir gestión completa al router
```bash
python scripts/generar_config.py --sede "alcorcon" --tipo-sede sede_simple --dispositivo router_simple --bloque-gestion
```

### Añadir gestión completa al switch
```bash
python scripts/generar_config.py --sede "alcorcon" --tipo-sede sede_simple --dispositivo switch_acceso_simple --bloque-gestion
```

## Generar Documentacion del Script
```bash
python -m pydoc -w scripts.generar_config
```
