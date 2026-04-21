# BanRep TRM (COP/USD) Access Methods

## Primary Option: datos.gov.co (Recommended)

**API**: Socrata Open Data API (REST)  
**URL**: `https://www.datos.gov.co/Econom-a-y-Finanzas/Tasa-de-Cambio-Representativa-del-Mercado-Historic/mcec-87by`  
**Method**: GET — historical dataset, SOQL filters for date range

```python
import requests
import json
from datetime import datetime

# Socrata API endpoint (histórico)
url = "https://www.datos.gov.co/resource/mcec-87by.json"

# Query Oct 2024 - Apr 2026
params = {
    "$where": "fecha >= '2024-10-01' AND fecha <= '2026-04-02'",
    "$order": "fecha ASC",
    "$limit": 50000
}

response = requests.get(url, params=params)
data = response.json()

# Extract: date, valor (TRM rate)
for record in data:
    print(f"{record['fecha']}: {record['valor']} COP/USD")
```

**Coverage**: Full daily history available

---

## Secondary: BanRep Statistics Portal

**URL**: `https://totoro.banrep.gov.co/estadisticas-economicas/`  
**Method**: Web scraping or direct data export  
**Note**: HTML-based, less programmatic. Export CSV available.

---

## Tertiary: Superfinanciera SFC

**URL**: `https://www.superfinanciera.gov.co/publicaciones/60819/`  
**Method**: SOAP API (legacy)  
**Note**: Official certifier but SOAP integration is more complex

---

## Quick Start (Python)

Use **datos.gov.co** with `requests` + `pandas`:

```python
import requests
import pandas as pd

url = "https://www.datos.gov.co/resource/mcec-87by.json"
params = {"$limit": 50000, "$where": "fecha >= '2024-10-01'"}
df = pd.DataFrame(requests.get(url, params=params).json())
df['fecha'] = pd.to_datetime(df['fecha'])
df.to_csv('trm_history.csv', index=False)
```

**Status**: ✓ Verified, free, no API key needed.
