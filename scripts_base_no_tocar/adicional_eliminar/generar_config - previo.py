#!/usr/bin/env python3
# ================================================================
# GENERADOR DE CONFIGURACIONES - METODOLOGIA PYMES
# ================================================================
# Script principal que combina archivos YAML y plantillas Jinja2
# para generar configuraciones de red completas
# 
# Uso: python generar_config.py --sede <nombre_sede> --tipo <tipo_sede>
# ================================================================

import yaml
import argparse
import os
import sys
from datetime import datetime
from jinja2 import Environment, FileSystemLoader, select_autoescape
import ipaddress

# ================================================================
# FUNCIONES AUXILIARES PARA JINJA2
# ================================================================

def cidr_to_netmask(cidr):
    """Convierte CIDR a netmask: /24 -> 255.255.255.0"""
    try:
        prefixlen = int(cidr)
        return str(ipaddress.IPv4Network(f'0.0.0.0/{prefixlen}', strict=False).netmask)
    except:
        return "255.255.255.0"  # Default

def cidr_to_acl(network_cidr):
    """Convierte red CIDR a formato ACL: 192.168.1.0/24 -> 192.168.1.0 0.0.0.255"""
    try:
        network = ipaddress.IPv4Network(network_cidr, strict=False)
        wildcard = ipaddress.IPv4Address(int(network.hostmask))
        return f"{network.network_address} {wildcard}"
    except:
        return "192.168.1.0 0.0.0.255"  # Default
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
# CLASE PRINCIPAL DEL GENERADOR
# ================================================================

class GeneradorConfiguraciones:
    def __init__(self):
        self.global_config = None
        self.sede_config = None
        self.dispositivo_config = None
        self.jinja_env = None
        
    def cargar_configuraciones(self, sede_nombre, tipo_sede, tipo_dispositivo):
        """Carga todos los archivos YAML necesarios"""
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
        """Configura el entorno Jinja2"""
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
    
    def validar_configuracion(self):
        """Validaciones basicas de la configuracion"""
        errores = []
        
        # Validar que bloques activos tengan configuracion
        if self.sede_config['sede']['bloques_activos']['cifrado']:
            if 'cifrado' not in self.sede_config or not self.sede_config['cifrado']:
                errores.append("Cifrado activo pero sin configuracion de cifrado")
        
        # Validar redes IP
        try:
            for vrf in ['main', 'invitados', 'gestion']:
                red = self.sede_config['direccionamiento'][vrf]['red_lan']
                ipaddress.IPv4Network(red, strict=False)
        except:
            errores.append(f"Red LAN invalida en VRF {vrf}")
        
        if errores:
            print("[ERROR] Errores de validacion:")
            for error in errores:
                print(f"  - {error}")
            return False
        
        print("[OK] Validaciones pasadas correctamente")
        return True
    
    def generar_configuracion(self, tipo_dispositivo, modulo_cifrado=False, modulo_gestion=False, modulo_sede_central=False):
        """Genera la configuracion final usando plantilla Jinja2"""
        try:
        # Determinar plantilla a usar
            if modulo_cifrado:
                plantilla_nombre = "cifrado_modulo.j2"
            elif modulo_gestion:
                if tipo_dispositivo.startswith('router'):
                    plantilla_nombre = "gestion_router_modulo.j2"
                elif tipo_dispositivo.startswith('switch'):
                    plantilla_nombre = "gestion_switch_modulo.j2"  # Para futuro
                else:
                    raise ValueError(f"Gestión no soportada para: {tipo_dispositivo}")    
            elif modulo_sede_central:
                plantilla_nombre = "cifrado_sede_central_modulo.j2"
            elif tipo_dispositivo.startswith('router'):
                plantilla_nombre = f"{tipo_dispositivo}.j2"
            elif tipo_dispositivo.startswith('switch'):
                plantilla_nombre = f"{tipo_dispositivo}.j2"
            else:
                raise ValueError(f"Tipo de dispositivo no soportado: {tipo_dispositivo}")
                
            print(f"[INFO] Usando plantilla: {plantilla_nombre}")
            plantilla = self.jinja_env.get_template(plantilla_nombre)
            
            # Preparar contexto para la plantilla
            contexto = {
                'global_config': self.global_config,
                'sede': self.sede_config['sede'],
                'direccionamiento': self.sede_config['direccionamiento'],
                'wan': self.sede_config['wan'],
                'configuracion': self.sede_config['configuracion'],
                'fecha_generacion': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Añadir configuracion de cifrado si esta activa
            if self.sede_config['sede']['bloques_activos']['cifrado']:
                contexto['cifrado'] = self.sede_config['cifrado']
            
            # Añadir configuracion especifica del dispositivo
            if tipo_dispositivo.startswith('router'):
                contexto['router'] = self.dispositivo_config['router']
                contexto['interfaces'] = self.dispositivo_config['interfaces']
            elif tipo_dispositivo.startswith('switch'):
                contexto['switch'] = self.dispositivo_config['switch']
                contexto['interfaces'] = self.dispositivo_config['interfaces']
            
            # Generar configuracion
            configuracion = plantilla.render(**contexto)
            
            print(f"[OK] Configuracion generada correctamente")
            return configuracion
            
        except Exception as e:
            print(f"[ERROR] Error generando configuracion: {e}")
            return None
    
    def guardar_configuracion(self, configuracion, sede_nombre, tipo_dispositivo):
        """Guarda la configuracion en archivo"""
        try:
            # Crear directorio de salida
            directorio = f"configuraciones/{sede_nombre}"
            os.makedirs(directorio, exist_ok=True)
            
            # Nombre del archivo
            timestamp = datetime.now().strftime("%Y%m%d_%H%M")
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
    
    def mostrar_resumen(self, sede_nombre, tipo_sede, tipo_dispositivo):
        """Muestra resumen de la configuracion generada"""
        print("\n" + "="*60)
        print("RESUMEN DE CONFIGURACION GENERADA")
        print("="*60)
        print(f"Sede: {sede_nombre}")
        print(f"Tipo de sede: {tipo_sede}")
        print(f"Dispositivo: {tipo_dispositivo}")
        
        # Bloques activos
        bloques_activos = [k for k, v in self.sede_config['sede']['bloques_activos'].items() if v]
        print(f"Bloques funcionales: {', '.join(bloques_activos)}")
        
        # Direccionamiento
        print(f"Red principal: {self.sede_config['direccionamiento']['main']['red_lan']}")
        print(f"Red invitados: {self.sede_config['direccionamiento']['invitados']['red_lan']}")
        print(f"Red gestion: {self.sede_config['direccionamiento']['gestion']['red_lan']}")
        
        print("="*60)

# ================================================================
# FUNCION PRINCIPAL
# ================================================================

def main():
    parser = argparse.ArgumentParser(description='Generador de configuraciones de red')
    parser.add_argument('--sede', required=True, help='Nombre de la sede (ej: Barcelona)')
    parser.add_argument('--tipo-sede', required=True, 
                       choices=['sede_simple', 'sede_central', 'sede_redundante'],
                       help='Tipo de sede')
    parser.add_argument('--dispositivo', required=True,
                       choices=['router_simple', 'router_central_principal', 'router_central_backup',
                               'router_redundante_principal', 'router_redundante_backup',
                               'switch_acceso_simple', 'switch_acceso_redundante', 
                               'switch_acceso_central', 'switch_distribucion_central'],
                       help='Tipo de dispositivo')
    parser.add_argument('--mostrar-pantalla', action='store_true',
                       help='Mostrar configuracion en pantalla ademas de guardarla')
    parser.add_argument('--modulo-cifrado', action='store_true',
                    help='Generar solo modulo de cifrado incremental')
    parser.add_argument('--modulo-sede-central-cifrado', action='store_true',
                    help='Generar modulo para añadir esta sede al cifrado de sede central')
    parser.add_argument('--modulo-gestion', action='store_true',
                    help='Generar solo modulo de gestion incremental')
    
    
    args = parser.parse_args()
    
    # Crear generador
    generador = GeneradorConfiguraciones()
    
    # Ejecutar proceso completo
    if not generador.cargar_configuraciones(args.sede, args.tipo_sede, args.dispositivo):
        sys.exit(1)
    
    if args.modulo_sede_central_cifrado:
        print("[INFO] Generando modulo de cifrado para sede central...")
        print("[NOTA] El parámetro --dispositivo se ignora para modulo sede central")

    if not generador.configurar_jinja():
        sys.exit(1)
    
    if not generador.validar_configuracion():
        sys.exit(1)
    
    configuracion = generador.generar_configuracion(args.dispositivo, args.modulo_cifrado, args.modulo_gestion, args.modulo_sede_central_cifrado)
    if not configuracion:
        sys.exit(1)
    
    archivo_guardado = generador.guardar_configuracion(configuracion, args.sede, args.dispositivo)
    if not archivo_guardado:
        sys.exit(1)
    
    # Mostrar resumen
    generador.mostrar_resumen(args.sede, args.tipo_sede, args.dispositivo)
    
    # Mostrar en pantalla si se solicita
    if args.mostrar_pantalla:
        print("\n" + "="*60)
        print("CONFIGURACION GENERADA:")
        print("="*60)
        print(configuracion)
    
    print(f"\n[COMPLETADO] Configuracion lista para implementar")

if __name__ == "__main__":
    main()