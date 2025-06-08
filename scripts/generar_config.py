# ================================================================
# GENERADOR DE CONFIGURACIONES - METODOLOGIA PYMES
# ================================================================
# Script principal que combina archivos YAML y plantillas Jinja2
# para generar configuraciones de red completas
# 
# Uso: python generar_config.py --sede <nombre_sede> --tipo <tipo_sede>
# Ejemplo: python scripts/generar_config.py --sede "alcorcon" --tipo-sede sede_simple --dispositivo router_simple
# Ejemplo: python scripts/generar_config.py --sede "alcorcon" --tipo-sede sede_simple --dispositivo router_simple --bloque-cifrado
# ================================================================

import yaml # Para leer archivos de configuracion
import argparse # Para manejar argumentos en la linea de comandos
import os  # Para crear directorios y manejar rutas de archivos
import sys # Para salir del programa en caso de errores
from datetime import datetime # Para poner fecha en archivos generados
from jinja2 import Environment, FileSystemLoader, select_autoescape # Motor de plantillas
import ipaddress # Para validar IPs , mascaras, etc

# ================================================================
# FUNCIONES AUXILIARES PARA JINJA2
# Estas funciones las usa Jinja2 dentro de las plantillas para convertir formatos de red automáticamente de CIDR a mascara de netmask, a wildcard para access-list, etc

# ================================================================


def cidr_to_netmask(cidr):
    """Convierte CIDR a netmask: /24 -> 255.255.255.0"""
    try:
        prefixlen = int(cidr)
        return str(ipaddress.IPv4Network(f'0.0.0.0/{prefixlen}', strict=False).netmask)
    except:
        return "255.255.255.0"  

def cidr_to_acl(network_cidr):
    """Convierte red CIDR a formato ACL: 192.168.1.0/24 -> 192.168.1.0 0.0.0.255"""
    try:
        network = ipaddress.IPv4Network(network_cidr, strict=False)
        wildcard = ipaddress.IPv4Address(int(network.hostmask))
        return f"{network.network_address} {wildcard}"
    except:
        return "192.168.1.0 0.0.0.255"  

def get_netmask_from_cidr_network(network_cidr):
    """Extrae netmask de red CIDR: 192.168.1.0/24 -> 255.255.255.0"""
    try:
        network = ipaddress.IPv4Network(network_cidr, strict=False)
        return str(network.netmask)
    except:
        return "255.255.255.0"

def next_ip(ip_address):
    """Calcula siguiente IP: 192.168.1.2 -> 192.168.1.3"""
    try:
        ip = ipaddress.IPv4Address(ip_address)
        return str(ip + 1)
    except:
        return ip_address

# ================================================================
# CLASE PRINCIPAL DEL GENERADOR CON LOS DISTINTOS METODOS
# ================================================================

class GeneradorConfiguraciones:
    """
    Clase principal
        Esta clase se encarga de juntar los datos de los YAMLs con las plantillas Jinja2
        para generar configuraciones de red listas para copiar y pegar en los equipos.
        1. Carga 3 archivos YAML (global + sede + dispositivo)  
        2. Elige la plantilla Jinja2 correcta
        3. Combina todo y genera la configuración final
    """
    def __init__(self):
        self.global_config = None
        self.sede_config = None
        self.dispositivo_config = None
        self.jinja_env = None
    
        
    def cargar_configuraciones(self, sede_nombre, tipo_sede, tipo_dispositivo):
        """
        Carga los 3 archivos YAML necesarios para generar una configuración
        Args:
            sede_nombre: Nombre de la sede (ej: "alcorcon")
            tipo_sede: Tipo de sede ("sede_simple", "sede_redundante")  
            tipo_dispositivo: Tipo de equipo ("router_simple", "switch_acceso_simple")
        Returns:
            bool: True si todo se cargó correctamente, False si hay errores
        Archivos que carga:
        - global_config.yaml: fichero global
        - sedes/{tipo_sede}.yaml: Datos específicos de la sede
        - dispositivos/{tipo_dispositivo}.yaml: Interfaces físicas del equipo
        """
        try:
            # Cargar configuracion global (siempre igual)
            print(f"[INFO] Cargando configuracion global...")
            with open('global_config.yaml', 'r', encoding='utf-8') as f:
                self.global_config = yaml.safe_load(f)
            
            # Cargar configuracion de sede
            archivo_sede = f'sedes/{tipo_sede}.yaml'
            print(f"[INFO] Cargando configuracion de sede: {archivo_sede}")
            with open(archivo_sede, 'r', encoding='utf-8') as f:
                self.sede_config = yaml.safe_load(f)
                
            # Personalizar con nombre especifico de sede
            if sede_nombre:
                self.sede_config['sede']['nombre'] = sede_nombre
                
            # Cargar configuracion de dispositivo
            archivo_dispositivo = f'dispositivos/{tipo_dispositivo}.yaml'
            print(f"[INFO] Cargando configuracion de dispositivo: {archivo_dispositivo}")
            with open(archivo_dispositivo, 'r', encoding='utf-8') as f:
                self.dispositivo_config = yaml.safe_load(f)
                
            print(f"[OK] Todas las configuraciones cargadas correctamente")
            return True
            
        except FileNotFoundError as e:
            print(f"[ERROR] Archivo no encontrado: {e}")
            return False
        except yaml.YAMLError as e:
            print(f"[ERROR] Error al procesar YAML: {e}")
            return False
        except Exception as e:
            print(f"[ERROR] Error inesperado: {e}")
            return False
    
    def configurar_jinja(self):
        """
        Configura el entorno Jinja2
        Jinja2 es lo que convierte las plantillas .j2 en configuraciones finales.
        Aquí se configura las funciones auxiliares para conversiones de IPs y redes
        """

        # Cargar plantillas del directorio y con ello probar si tengo listo el motor que convierte plantillas .j2 en configuraciones
        try:
            self.jinja_env = Environment(
                loader=FileSystemLoader('plantillas'),
                autoescape=select_autoescape(['html', 'xml']),
                trim_blocks=True,
                lstrip_blocks=True
            )
            
            # Registrar funciones auxiliares
            self.jinja_env.filters['cidr_to_netmask'] = cidr_to_netmask
            self.jinja_env.filters['cidr_to_acl'] = cidr_to_acl
            self.jinja_env.filters['next_ip'] = next_ip
            self.jinja_env.filters['get_netmask_from_cidr_network'] = get_netmask_from_cidr_network
            
            print(f"[OK] Entorno Jinja2 configurado")
            return True
            
        except Exception as e:
            print(f"[ERROR] Error configurando Jinja2: {e}")
            return False
    
    def validar_configuracion(self, bloque_cifrado=False, bloque_gestion=False, bloque_sede_central=False):
        """
        Validaciones basicas de la configuracion
        Revision de cosas como
        Si se pide cifrado, que existan los datos de cifrado
        Que las redes IP sean válidas
        Que no falten datos obligatorios
        """
        errores = []
        
        # Validaciones para bloques independientes
        if bloque_cifrado or bloque_sede_central:
            if 'cifrado' not in self.sede_config or not self.sede_config['cifrado']:
                errores.append("bloque cifrado solicitado pero sin configuracion de cifrado en archivo de sede")
                errores.append("SOLUCION: Completar seccion 'cifrado:' en el archivo YAML de sede")
        
        # Solo validar configuracion de sede si NO es un bloque independiente
        if not (bloque_cifrado or bloque_gestion or bloque_sede_central):
            # Validar bloques activos con configuracion
            if self.sede_config['sede']['bloques_activos']['cifrado']:
                if 'cifrado' not in self.sede_config or not self.sede_config['cifrado']:
                    errores.append("Cifrado activo en sede pero sin configuracion de cifrado")
        
        # Validar redes IP siempre
        try:
            for vrf in ['main', 'invitados', 'gestion']:
                red = self.sede_config['direccionamiento'][vrf]['red_lan']
                ipaddress.IPv4Network(red, strict=False)
        except Exception as e:
            errores.append(f"Red LAN invalida en VRF {vrf}: {e}")
        
        if errores:
            print("[ERROR] Errores de validacion:")
            for error in errores:
                print(f"  - {error}")
            return False
        
        print("[OK] Validaciones pasadas correctamente")
        return True
    
    def determinar_plantilla(self, tipo_dispositivo, bloque_cifrado, bloque_gestion, bloque_sede_central):
        """
        Determina que plantilla usar segun parametros
        Configuración completa: usa plantilla router_simple.j2
        Solo bloque cifrado: usa plantilla de cifrado_bloque.j2
        Solo bloque gestión: usa plantilla de gestion_router/switch_bloque.j2
        """
        if bloque_cifrado:
            return "cifrado_bloque.j2"
        elif bloque_sede_central:
            return "cifrado_sede_central_bloque.j2"
        elif bloque_gestion:
            if tipo_dispositivo.startswith('router'):
                return "gestion_router_bloque.j2"
            elif tipo_dispositivo.startswith('switch'):
                return "gestion_switch_bloque.j2"
            else:
                raise ValueError(f"Gestion no soportada para: {tipo_dispositivo}")
        else:
            # Plantilla completa normal
            return f"{tipo_dispositivo}.j2"
    
    def generar_configuracion(self, tipo_dispositivo, bloque_cifrado=False, bloque_gestion=False, bloque_sede_central=False):
        """
        Genera la configuracion final usando las plantillas Jinja2 y los YAML
        Coge todos los datos que se cargaron de los YAMLs y los pasa a la plantilla Jinja2 que corresponda
        Genera la configuración final lista para copiar y pegar en el equipo por el tecnico PYME
        """
        try:
            # Determinar plantilla
            plantilla_nombre = self.determinar_plantilla(tipo_dispositivo, bloque_cifrado, bloque_gestion, bloque_sede_central)
            
            if bloque_sede_central:
                print(f"[INFO] Generando configuracion para SEDE CENTRAL (ignorando parametro dispositivo)")
            
            print(f"[INFO] Usando plantilla: {plantilla_nombre}")
            plantilla = self.jinja_env.get_template(plantilla_nombre)
            
            # Preparar contexto/diccionario para la plantilla Jinja
            contexto = {
                'global_config': self.global_config, # Proviene de global_config.yaml
                'sede': self.sede_config['sede'], # Proviene de sede_simple.yaml
                'direccionamiento': self.sede_config['direccionamiento'], # Proviene de sede_simple.yaml
                'wan': self.sede_config['wan'], # Proviene de sede_simple.yaml
                'configuracion': self.sede_config['configuracion'], # Proviene de sede_simple.yaml
                'fecha_generacion': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Añadir configuracion de cifrado si existe (para bloques)
            # Solo se incluye si esta definido en el YAML y no esta vacio
            if 'cifrado' in self.sede_config and self.sede_config['cifrado']:
                contexto['cifrado'] = self.sede_config['cifrado']
            
            # Añadir configuracion especifica del dispositivo
            if tipo_dispositivo.startswith('router'):
                contexto['router'] = self.dispositivo_config['router'] # Proviene de router_simple.yaml
                contexto['interfaces'] = self.dispositivo_config['interfaces'] # Proviene de router_simple.yaml
            elif tipo_dispositivo.startswith('switch'):
                contexto['switch'] = self.dispositivo_config['switch'] # Proviene de switch_acceso_simple.yaml
                contexto['interfaces'] = self.dispositivo_config['interfaces'] # Proviene de switch_acceso_simple.yaml
            
            # Generar configuracion
            """
            Se utiliza .render como motor que rellena las {{ variables }} de las plantillas Jinja2 
            **contexto = pasa cada elemento dentro de contexto/diccionario por separado
            Si fuera plantilla.render(contexto), pasariamos el contexto/diccionario como un unico elemento
            """
            configuracion = plantilla.render(**contexto)
            
            print(f"[OK] Configuracion generada correctamente")
            return configuracion
            
        except Exception as e:
            print(f"[ERROR] Error generando configuracion: {e}")
            return None
    
    def guardar_configuracion(self, configuracion, sede_nombre, tipo_dispositivo, sufijo_bloque=""):
        """
        Guarda la configuracion en archivo txt
        Crea un archivo txt con la configuracion lista para copiar y pegar.
        El nombre incluye fecha/hora para evitar sobreescribir archivos y documentar mejor cuando se ha realizado
        """
        try:
            # Crear directorio de salida
            directorio = f"configuraciones/{sede_nombre}"
            os.makedirs(directorio, exist_ok=True)
            
            # Nombre del archivo
            timestamp = datetime.now().strftime("%Y%m%d_%H%M")
            if sufijo_bloque:
                nombre_archivo = f"{tipo_dispositivo}_{sufijo_bloque}_{timestamp}.txt"
            else:
                nombre_archivo = f"{tipo_dispositivo}_{timestamp}.txt"
            ruta_completa = os.path.join(directorio, nombre_archivo)
            
            # Guardar archivo
            with open(ruta_completa, 'w', encoding='utf-8') as f:
                f.write(configuracion)
            
            print(f"[OK] Configuracion guardada en: {ruta_completa}")
            return ruta_completa
            
        except Exception as e:
            print(f"[ERROR] Error guardando configuracion: {e}")
            return None
    
    def mostrar_resumen(self, sede_nombre, tipo_sede, tipo_dispositivo, es_bloque=False, tipo_bloque=""):
        """
        Muestra un resumen de lo que se generó para confirmar por el técnico
        Es util para que el técnico vea rápidamente qué se generó, con qué parámetros y con objetivo de documentar
        """
        print("\n" + "="*60)
        if es_bloque:
            print(f"RESUMEN bloque {tipo_bloque.upper()} GENERADO")
        else:
            print("RESUMEN DE CONFIGURACION GENERADA")
        print("="*60)
        print(f"Sede: {sede_nombre}")
        print(f"Tipo de sede: {tipo_sede}")
        
        if not es_bloque:
            print(f"Dispositivo: {tipo_dispositivo}")
            # Bloques activos
            bloques_activos = [k for k, v in self.sede_config['sede']['bloques_activos'].items() if v]
            print(f"Bloques funcionales: {', '.join(bloques_activos)}")
            
            # Direccionamiento
            print(f"Red principal: {self.sede_config['direccionamiento']['main']['red_lan']}")
            print(f"Red invitados: {self.sede_config['direccionamiento']['invitados']['red_lan']}")
            print(f"Red gestion: {self.sede_config['direccionamiento']['gestion']['red_lan']}")
        else:
            print(f"bloque: {tipo_bloque}")
            print(f"Dispositivo: {tipo_dispositivo}")
        
        print("="*60)

# ================================================================
# FUNCION PRINCIPAL
# ================================================================

def main():
    """
    Funcion principal que acepta y maneja los parametros que se introducen por la linea de comandos
    Define qué parámetros acepta el script y gestiona todo el proceso:
    Analizar parámetros introducidos por linea de comandos
    Valida que sean correctos  
    Llamar al generador de plantillas
    Muestra resultados
    """
    parser = argparse.ArgumentParser(description='Generador de configuraciones de red')
    parser.add_argument('--sede', required=True,
                        help='Nombre de la sede (ej: Alcorcon)')
    parser.add_argument('--tipo-sede', required=True, 
                       choices=['sede_simple', 'sede_redundante'],
                       help='Tipo de sede') #A futuro añadir 'sede_central'
    parser.add_argument('--dispositivo', required=True,
                       choices=['router_simple', 'router_redundante_principal', 'router_redundante_backup', 'switch_acceso_simple', 'switch_acceso_redundante'],
                       help='Tipo de dispositivo') #A futuro añadir 'router_central_principal', 'router_central_backup','switch_acceso_central', 'switch_distribucion_central'
    parser.add_argument('--mostrar-pantalla', action='store_true',
                       help='Mostrar configuracion por pantalla ademas de guardarla')
    parser.add_argument('--bloque-cifrado', action='store_true',
                       help='Generar solo bloque de cifrado')
    parser.add_argument('--bloque-sede-central-cifrado', action='store_true',
                       help='Generar bloque para añadir esta sede al cifrado de sede central')
    parser.add_argument('--bloque-gestion', action='store_true',
                       help='Generar solo bloque de gestion')
    
    args = parser.parse_args()
    
    # Verificar que solo se use un bloque a la vez
    bloques_activos = sum([args.bloque_cifrado, args.bloque_sede_central_cifrado, args.bloque_gestion])
    if bloques_activos > 1:
        print("[ERROR] Solo se puede usar un bloque a la vez")
        sys.exit(1)
    
    # Llamar al generador
    generador = GeneradorConfiguraciones()
    
    # Ejecutar proceso completo
    if not generador.cargar_configuraciones(args.sede, args.tipo_sede, args.dispositivo):
        sys.exit(1)
    
    if args.bloque_sede_central_cifrado:
        print("[INFO] Generando bloque de cifrado para sede central...")
        print("[NOTA] El parametro --dispositivo se ignora para bloque sede central")

    if not generador.configurar_jinja():
        sys.exit(1)
    
    if not generador.validar_configuracion(args.bloque_cifrado, args.bloque_gestion, args.bloque_sede_central_cifrado):
        sys.exit(1)
    
    configuracion = generador.generar_configuracion(
        args.dispositivo, 
        args.bloque_cifrado, 
        args.bloque_gestion, 
        args.bloque_sede_central_cifrado
    )
    if not configuracion:
        sys.exit(1)
    
    # Determinar sufijo para archivo
    sufijo_bloque = ""
    tipo_bloque = ""
    es_bloque = False
    
    if args.bloque_cifrado:
        sufijo_bloque = "bloque_cifrado"
        tipo_bloque = "cifrado"
        es_bloque = True
    elif args.bloque_sede_central_cifrado:
        sufijo_bloque = "bloque_sede_central"
        tipo_bloque = "cifrado sede central"
        es_bloque = True
    elif args.bloque_gestion:
        sufijo_bloque = "bloque_gestion"
        tipo_bloque = "gestion"
        es_bloque = True
    
    archivo_guardado = generador.guardar_configuracion(configuracion, args.sede, args.dispositivo, sufijo_bloque)
    if not archivo_guardado:
        sys.exit(1)
    
    # Mostrar resumen
    generador.mostrar_resumen(args.sede, args.tipo_sede, args.dispositivo, es_bloque, tipo_bloque)
    
    # Mostrar en pantalla si se solicita
    if args.mostrar_pantalla:
        print("\n" + "="*60)
        print("CONFIGURACION GENERADA:")
        print("="*60)
        print(configuracion)
    
    print(f"\n[Hecho] Configuracion lista para implementar, por favor introduce por partes para revisar errores.")

if __name__ == "__main__":
    main()