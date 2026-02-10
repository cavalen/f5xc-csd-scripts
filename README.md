# F5 Distributed Cloud - Client Side Defense Script exporter

This Python script queries the F5 Distributed Cloud API to retrieve information about scripts detected by the *Client Side Defense* service within a specific **Tenant** and **Namespace** over a defined time window.

The script automatically handles API pagination and allows you to export the results in **JSON** or **CSV** format.

## Prerequisites

* Python 3.6 or higher.
* Access to the F5 Distributed Cloud Console.
* A valid **API Token** generated from the console.

## Environment Setup (Installation)

Follow these steps to isolate dependencies and run the script safely.

### 1. Create a Virtual Environment (venv)

Open your terminal in the folder where you saved the script (`csd-logs.py`) and run:

**On Windows:**
```PowerShell
python -m venv path_to_venv
path_to_venv\bin\activate
```

**On Linux / macOS:**

```bash
python -m venv path_to_venv
source path_to_venv\bin\activate
```

### 2. Install Dependencies

The script requires the `requests` library. Install it by running:

```bash
pip install requests
```

### Authentication

The script uses an environment variable to read the security token.
Before running the script, you must export your token:

**Windows (PowerShell):**
```PowerShell
$env:APITOKEN="your_xc_token"
```

**Linux / macOS (bash/zsh):**
```bash
export APITOKEN="your_xc_token"
```

## Usage
The basic syntax is:

`python csd-logs.py -t <TENANT> -n <NAMESPACE> -hours <HOURS> [options]`

|Parameter|Long Name  |Required|Description                               |
----------|-----------|--------|------------------------------------------|
|-t       |--tenant   |Yes     |"Your Tenant Name" (e.g., my-company)     |
|-n       |--namespace|Yes     |"Namespace Name" (e.g., default, prod)    |
|-hours   |--hours    |Yes     |Number of hours to look back (time window)|
|-o       |--output   |No      |Output format: json (default) / csv       |
|-v       |--verbose  |No      |Shows debug logs at the end of execution  |
|-h       |--help     |No      |Quick help / Usage                        |


### Execution Examples
**1. Standard JSON Output (Default)**
Retrieves data from the last 24 hours and prints formatted JSON to the screen.

```bash
python csd-logs.py -t my-company -n default -hours 24
```

**2. Save JSON Output to a File**
You can use your operating system's redirection operator `>` to save the result.
```bash
python csd-logs.py -t my-company -n default -hours 24 > report.json
```

**3. CSV Output**
```bash
python csd-logs.py -t my-company -n default -hours 48 -o csv
```

**4. Verbose Mode (Debugging)**
```bash
python csd-logs.py -t my-company -n default -hours 12 -v
```
Verbose output example:
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
Configuracion: Tenant=my-company, Namespace=default
Ventana de tiempo: 2026-02-04 12:01:09 (1770224469) a 2026-02-09 12:01:09 (1770656469)
--- Iniciando Recoleccion de Datos ---
Consultando pagina 1...
  > Scripts encontrados en pagina 1: 500
  > Siguiente pagina detectada. Token: rieDz_ws-7XmcVmR4__S...
Consultando pagina 2...
  > Scripts encontrados en pagina 2: 273
  > No hay mas paginas (token vacio). Finalizando loop.
Total de entradas obtenidas: 773
--------------------------
$bash> 
```
