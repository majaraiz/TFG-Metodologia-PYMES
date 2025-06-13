# TFG-Metodologia Building Blocks-PYMES
# Metodología de Automatización de Redes para PYMEs

## Descripción del proyecto

Este proyecto nace del estudio de la metodología **Cisco SAFE** y las necesidades detectadas en las **pequeñas y medianas empresas (PYMEs)** para implementar redes empresariales seguras y escalables.
A pesar de que Cisco SAFE proporciona un marco arquitectónico robusto  y consolidado, su aplicación práctica en organizaciones con recursos técnicos y económicos limitados resulta compleja debido a la ausencia de metodologías estructuradas y herramientas que faciliten su implementación.

En base a ello, se ha diseñado una **metodología de building blocks modulares** que pretende **facilitar el acceso a buenas prácticas de diseño de redes empresariales seguras mediante la implementación de herramientas sencillas y accesibles a entornos con recursos tecnicos y economicos limitados**.

## Objetivos

La metodología desarrollada busca:

- **Simplificar la implementación** de arquitecturas Cisco SAFE en PYMEs.
- **Automatizar la generación** de configuraciones de red mediante plantillas parametrizables.
- **Reducir la dependencia** de conocimiento especializado y consultoría externa.
- **Proporcionar herramientas modulares** que permitan implementación por fases según presupuesto.
- **Facilitar la transferencia de conocimiento** dentro de las organizaciones.

## Componentes principales

### Estructura Modular-Bloques
```
├── global_config.yaml          # Estándares globales de la metodología
├── sedes/                      # Configuraciones específicas por tipo de sede
├── dispositivos/               # Parámetros físicos de equipos
├── plantillas/                 # Templates Jinja2 para configuraciones
├── scripts/                    # Automatización en Python
└── configuraciones/            # Salida: archivos listos para implementar
```

### Building blocks implementados

- **Segmentación**: VRFs y VLANs para aislamiento de tráfico
- **Enrutamiento**: BGP y HSRP para conectividad y redundancia
- **Cifrado**: Túneles IPSec para protección de comunicaciones
- **Gestión**: SSH, SNMP, Syslog, NetFlow para administración centralizada

### Tecnologías utilizadas

- **Python**: Motor de procesamiento y automatización
- **Jinja2**: Sistema de plantillas para configuraciones
- **YAML**: Formato de datos legible para parametrización
- **Cisco IOS**: Plataforma de red 
- **EVE-NG**: Entorno de validación y pruebas

## Uso rápido

### Generar configuración completa
```bash
# Router de sede simple
python scripts/generar_config.py --sede "alcorcon" --tipo-sede sede_simple --dispositivo router_simple

# Switch de acceso
python scripts/generar_config.py --sede "alcorcon" --tipo-sede sede_simple --dispositivo switch_acceso_simple

# Sede redundante
python scripts/generar_config.py --sede "Soria" --tipo-sede sede_redundante --dispositivo router_redundante_principal
python scripts/generar_config.py --sede "Soria" --tipo-sede sede_redundante --dispositivo router_redundante_backup
python scripts/generar_config.py --sede "Soria" --tipo-sede sede_redundante --dispositivo switch_acceso_redundante
```

### Implementación de bloques 
```bash
# Solo cifrado
python scripts/generar_config.py --sede "alcorcon" --tipo-sede sede_simple --dispositivo router_simple --bloque-cifrado

python scripts/generar_config.py --sede "Soria" --tipo-sede sede_redundante --dispositivo router_redundante_principal --bloque-cifrado
python scripts/generar_config.py --sede "Soria" --tipo-sede sede_redundante --dispositivo router_redundante_backup --bloque-cifrado

# Solo gestión
python scripts/generar_config.py --sede "alcorcon" --tipo-sede sede_simple --dispositivo router_simple --bloque-gestion
python scripts/generar_config.py --sede "Soria" --tipo-sede sede_redundante --dispositivo router_redundante_principal --bloque-gestion
python scripts/generar_config.py --sede "Soria" --tipo-sede sede_redundante --dispositivo router_redundante_backup --bloque-gestion
python scripts/generar_config.py --sede "Soria" --tipo-sede sede_redundante --dispositivo switch_acceso_redundante --bloque-gestion

# Cifrado sede central
python scripts/generar_config.py --sede "Alcorcon" --tipo-sede sede_simple --dispositivo router_simple --bloque-sede-central-cifrado
python scripts/generar_config.py --sede "Soria" --tipo-sede sede_redundante --dispositivo router_redundante_principal --bloque-sede-central-cifrado
```


## Resultados validados en entorno de laboratorio

**Conectividad**: Comunicación entre sedes verificada  
**Segmentación**: Aislamiento de VRFs funcionando  
**Cifrado**: Túneles IPSec operativos  
**Gestión**: Servicios de administración configurados  
**Automatización**: Generación de configuraciones sin errores  

## Contexto académico

Este proyecto GitHub forma parte de un **Trabajo Fin de Grado** que:

- Aborda un **problema real** identificado en el sector empresarial de las PYME
- Proporciona una **solución práctica y reutilizable** 
- Ha sido **validado experimentalmente** en laboratorio

## Fases [Estados]

### Fase 1 - Sede simple [COMPLETADO]
- Configuración completa funcional
- Bloques modulares implementados
- Validado en laboratorio EVE-NG

### Fase 2 - Sedes redundantes [COMPLETADO]
- Expansión para sedes con 2 routers
- Configuraciones HSRP diferenciadas

### Fase 3 - Sede central [FUTURO]
- Routers principales + backup
- Switches de distribución y acceso

### Fase 4 - Nuevos bloques [FUTURO]
- Firewalls
- QoS (Quality of Service)
- 802.1X y NAC

## Documentación

- **Memoria técnica completa**: Tras publicación del TFG
- **Guías de implementación y uso , pruebas, esquemas, laboratorio de pruebas, etc.**: En directorio `/docs`
- **Plantillas base para implementación**: En directorios `/*_base_no_tocar`
- **Ejemplos prácticos**: En directorios `/sedes /dispositivos /plantillas /configuraciones`

## Contribución

Tras la finalización de este TFG el proyecto estará abierto a:
- **Mejoras en los building blocks existentes**
- **Nuevos bloques funcionales**
- **Soporte para otros fabricantes**
- **Optimizaciones en la automatización**


## Autor y contacto

**Miguel Ángel Jaraíz Orden**  
majaraiz@alu.ucam.edu  

- Trabajo Fin de Grado - Miguel Ángel Jaraíz Orden - Universidad Católica de Murcia (UCAM)
