# Stock Trend Analysis (Modular)

## Setup
```bash
python -m venv .venv
# Windows PowerShell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
# Windows:
.venv\Scripts\activate

# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```
## Run

### Show Static Anaylsis
```bash
python main.py
```

### Web App Interactive Analysis
`` bash
streamlit run app.py
```

Edit main.py config at the top (ticker, period, interval, SMA window).
