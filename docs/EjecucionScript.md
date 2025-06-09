# Guia basica de ejecucion del Script #
  Para poder lanzar el script primero es necesario tener instalado Python y las librerias que permiten  manejar Jinja2 y YAML
  Por favor sigue los pasos de la ### Guia Basica instalación python y librerias.md ###

  Para lanzar el script con los argumentos correspondientes acceder la carpeta del equipo donde se encuentren los ficheros
  Ejemplo en Windows c:\TFG-Metodologia-PYMES\

### Estructura de comandos:
### python scripts/generar_config.py --sede <nombre> --tipo-sede <tipo> --dispositivo <dispositivo> [opciones]  
  
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

---


### TODOS LOS COMANDOS DISPONIBLES


###  SEDE SIMPLE 
python scripts/generar_config.py --sede "Alcorcon" --tipo-sede sede_simple --dispositivo router_simple

python scripts/generar_config.py --sede "Alcorcon" --tipo-sede sede_simple --dispositivo switch_acceso_simple

###  SEDE REDUNDANTE 
python scripts/generar_config.py --sede "Soria" --tipo-sede sede_redundante --dispositivo router_redundante_principal

python scripts/generar_config.py --sede "Soria" --tipo-sede sede_redundante --dispositivo router_redundante_backup

python scripts/generar_config.py --sede "Soria" --tipo-sede sede_redundante --dispositivo switch_acceso_redundante

###  BLOQUES INCREMENTALES 

### Cifrado
python scripts/generar_config.py --sede "Alcorcon" --tipo-sede sede_simple --dispositivo router_simple --bloque-cifrado

python scripts/generar_config.py --sede "Soria" --tipo-sede sede_redundante --dispositivo router_redundante_principal --bloque-cifrado

python scripts/generar_config.py --sede "Soria" --tipo-sede sede_redundante --dispositivo router_redundante_backup --bloque-cifrado

### Gestión
python scripts/generar_config.py --sede "Alcorcon" --tipo-sede sede_simple --dispositivo router_simple --bloque-gestion

python scripts/generar_config.py --sede "Alcorcon" --tipo-sede sede_simple --dispositivo switch_acceso_simple --bloque-gestion

python scripts/generar_config.py --sede "Soria" --tipo-sede sede_redundante --dispositivo router_redundante_principal --bloque-gestion

python scripts/generar_config.py --sede "Soria" --tipo-sede sede_redundante --dispositivo router_redundante_backup --bloque-gestion

python scripts/generar_config.py --sede "Soria" --tipo-sede sede_redundante --dispositivo switch_acceso_redundante --bloque-gestion

### Cifrado sede central
python scripts/generar_config.py --sede "Alcorcon" --tipo-sede sede_simple --dispositivo router_simple --bloque-sede-central-cifrado

python scripts/generar_config.py --sede "Soria" --tipo-sede sede_redundante --dispositivo router_redundante_principal --bloque-sede-central-cifrado


### Ver resultado en pantalla (añadir --mostrar-pantalla)
python scripts/generar_config.py --sede "Alcorcon" --tipo-sede sede_simple --dispositivo router_simple --mostrar-pantalla

python scripts/generar_config.py --sede "Soria" --tipo-sede sede_redundante --dispositivo router_redundante_principal --bloque-cifrado --mostrar-pantalla

---


## NOTAS IMPORTANTES ##


1. Archivos generados:
   - Se guardan en: configuraciones/<nombre_sede>/
   - Formato: <dispositivo>_<timestamp>.txt
   - Ejemplo: router_simple_20250609_1430.txt

2. Tipos de sede disponibles:
   - sede_simple: 1 router + 1 switch
   - sede_redundante: 2 routers + 1 switch

3. Dispositivos disponibles:
   - router_simple
   - router_redundante_principal
   - router_redundante_backup
   - switch_acceso_simple
   - switch_acceso_redundante

4. Bloques incrementaleS:
   - --bloque-cifrado: Solo configuracion IPSec
   - --bloque-gestion: Solo configuracion SSH/SNMP/Syslog/NTP/AAA local
   - --bloque-sede-central-cifrado: Configuracion de cifrado adicional para sede central

5. Validaciones:
   - Solo se puede usar un bloque a la vez
   - Los dispositivos deben coincidir con el tipo de sede
