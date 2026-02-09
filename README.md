# F5 Distributed Cloud - Client Side Defense Script exporter

This Python script queries the F5 Distributed Cloud API to retrieve information about scripts executed within a specific **Tenant** and **Namespace** over a defined time window.

The script automatically handles API pagination and allows you to export the results in **JSON** or **CSV** format.

## Prerequisites

* Python 3.6 or higher.
* Access to the F5 Distributed Cloud Console.
* A valid **API Token** generated from the console.

## Environment Setup (Installation)

Follow these steps to isolate dependencies and run the script safely.

### 1. Create a Virtual Environment (venv)

Open your terminal in the folder where you saved the script (`api_request.py`) and run:

**On Windows:**
```bash
python -m venv path_to_venv
path_to_venv\bin\activate
```

**On Linux / macOS:**

```
python3 -m venv path_to_venv
source path_to_venv\bin\activate
```

### 2. Install Dependencies

The script requires the requests library. Install it by running:

```
pip install requests
```

### Authentication

The script uses an environment variable to read the security token. This prevents hardcoding credentials directly into the command line.
Before running the script, you must export your token:

**Windows (PowerShell):**
``` PowerShell
$env:APITOKEN="your_xc_token_here"
```

**Linux / macOS (Bash/Zsh):**
``` bash/ash
export APITOKEN="your_xc_token_here"
```

## Usage
The basic syntax is:
python api_request.py -t <TENANT> -n <NAMESPACE> -h_time <HOURS> [options]

|Parameter|Long Name  |Required|Description                               |
----------|-----------|--------|------------------------------------------|
|-t       |--tenant   |Yes     |"Your Tenant Name" (e.g., my-company)     |
|-n       |--namespace|Yes     |"Namespace Name" (e.g., default, prod)    |
|-h_time  |--hours    |Yes     |Number of hours to look back (time window)|
|-o       |--output   |No      |Output format: json (default) / csv       |
|-v       |--verbose  |No      |Shows debug logs at the end of execution  |
|-h       |--help     |No      |Quick help/Usage                          |


### Execution Examples
**1. Standard JSON Output (Default)**
Retrieves data from the last 24 hours and prints formatted JSON to the screen.

```bash
python csd-logs.py -t my-company -n default -h_time 24
```

**2. Save JSON Output to a File**
You can use your operating system's redirection operator `>` to save the result.
```sh
python csd-logs.py -t my-company -n default -h_time 24 > report.json
```

**3. CSV Output**
```sh
python csd-logs.py -t my-company -n default -h_time 48 -o csv
```

**4. Verbose Mode (Debugging)**
```
python csd-logs.py -t my-company -n default -h_time 12 -v
```
Output example:
```
...
        {
            "id": "s-asvoxxCEJU",
            "script_name": "https://app.client.com/path/script.js",
            "risk_level": "Low Risk",
            "locations": [
                "https://app.client.com/"
            ],
            "network_interactions": 0,
            "form_fields_read": 1,
            "new_behaviors": 0,
            "first_seen": "1770224442",
            "last_seen": "1770224473",
            "status": "",
            "justifications": [],
            "affected_users_count": 0
        }
    ]
}

--- Verbose Log Output ---
Configuración: Tenant=client, Namespace=default
Ventana de tiempo: 2026-02-04 12:01:09 (1770224469) a 2026-02-09 12:01:09 (1770656469)
--- Iniciando Recolección de Datos ---
Consultando página 1...
  > Scripts encontrados en página 1: 500
  > Siguiente página detectada. Token: rieDz_ws-7XmcVmR4__S...
Consultando página 2...
  > Scripts encontrados en página 2: 273
  > No hay más páginas (token vacío). Finalizando loop.
Total de entradas obtenidas: 773
--------------------------
$bash> 
```
