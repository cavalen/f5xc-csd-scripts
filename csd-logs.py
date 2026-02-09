import argparse
import requests
from datetime import datetime, timedelta
import sys
import os
import json
import csv

def main():
    # --- 1. Configuración de Argumentos ---
    parser = argparse.ArgumentParser(
                        description='Script API F5XC (CSD) con paginacion y Salida CSV/JSON',
                        epilog="Valida que exista variable de entorno APITOKEN con el Token de F5XC")
    
    parser.add_argument('-t', '--tenant', required=True, help='Nombre del Tenant')
    parser.add_argument('-n', '--namespace', required=True, help='Nombre del Namespace')
    parser.add_argument('-h_time', '--hours', required=True, type=int, help='Horas de log a extraer')
    parser.add_argument('-v', '--verbose', action='store_true', help='Ver debug info al final de la ejecucion')
    
    parser.add_argument('-f', '--format', 
                        choices=['json', 'csv'], 
                        default='json', 
                        help='Formato de salida json/csv (default: json)')

    args = parser.parse_args()

    # Variable para acumular los logs
    verbose_logs = []

    def log(message):
        """Helper para acumular mensajes si verbose está activo"""
        if args.verbose:
            verbose_logs.append(message)

    def print_logs():
        """Helper para imprimir todos los logs acumulados en stderr"""
        if args.verbose and verbose_logs:
            print("\n--- Verbose Log Output ---", file=sys.stderr)
            for line in verbose_logs:
                print(line, file=sys.stderr)
            print("--------------------------", file=sys.stderr)

    # --- 2. Verificar Token ---
    api_token = os.getenv('APITOKEN')
    if not api_token:
        # Aquí imprimimos directo porque es un error crítico de configuración inicial
        print("Error: Variable de entorno 'APITOKEN' no definida.", file=sys.stderr)
        sys.exit(1)

    # --- 3. Calcular Tiempos ---
    now = datetime.now()
    start_dt = now - timedelta(hours=args.hours)
    end_time_epoch = int(now.timestamp())
    start_time_epoch = int(start_dt.timestamp())

    log(f"Configuración: Tenant={args.tenant}, Namespace={args.namespace}")
    log(f"Ventana de tiempo: {datetime.fromtimestamp(start_time_epoch)} ({start_time_epoch}) a {datetime.fromtimestamp(end_time_epoch)} ({end_time_epoch})")

    # --- 4. Configuración Request ---
    base_url = f"https://{args.tenant}.console.ves.volterra.io/api/shape/csd/namespaces/{args.namespace}/scripts"
    
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"APIToken {api_token}"
    }

    # Variable acumuladora de resultados
    json_api_response = [] 
    
    current_page_token = ""
    page_counter = 0

    log("--- Iniciando Recolección de Datos ---")

    # --- 5. Bucle de Paginación ---
    while True:
        page_counter += 1
        
        params = {
            "end_time": end_time_epoch,
            "start_time": start_time_epoch,
            "namespace": "",
            "page_size": 0,
            "page_token": current_page_token
        }

        try:
            log(f"Consultando página {page_counter}...")

            response = requests.get(base_url, params=params, headers=headers)
            response.raise_for_status()
            
            data = response.json()

            # Extraer scripts
            batch_scripts = data.get("scripts", [])
            count_batch = len(batch_scripts)
            json_api_response.extend(batch_scripts)
            
            log(f"  > Scripts encontrados en página {page_counter}: {count_batch}")

            # Verificar siguiente página
            next_token = data.get("next_page_token")
            
            if not next_token:
                log("  > No hay más páginas (token vacío). Finalizando bucle.")
                break
            
            log(f"  > Siguiente página detectada. Token: {next_token[:20]}...")
            current_page_token = next_token

        except requests.exceptions.HTTPError as err:
            log(f"Error HTTP Fatal en página {page_counter}: {err}")
            print_logs() # Imprimimos los logs antes de salir por error
            sys.exit(1)
        except Exception as err:
            log(f"Error Inesperado Fatal: {err}")
            print_logs() # Imprimimos los logs antes de salir por error
            sys.exit(1)

    # --- 6. Generación de Salida (JSON o CSV) ---
    
    if args.format == 'json':
        final_output = {
            #"total_count_retrieved": len(json_api_response),
            "scripts": json_api_response
        }
        print(json.dumps(final_output, indent=4))
        log (f"Total de entradas obtenidas: {len(json_api_response)}")

    elif args.format == 'csv':
        if not json_api_response:
            log("Alerta: La respuesta de la API no contiene scripts. No se generará CSV.")
        else:
            # Obtener encabezados del primer elemento
            headers_csv = json_api_response[0].keys()
            
            # CAMBIO: Delimiter ahora es coma ','
            writer = csv.DictWriter(sys.stdout, fieldnames=headers_csv, delimiter=',')
            
            writer.writeheader()
            writer.writerows(json_api_response)

    # --- 7. Imprimir Logs al Final ---
    print_logs()

if __name__ == "__main__":
    main()
