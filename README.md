# Test parser

A Python-based script for parsing login forms, promotions, and bonuses as part of a test task for the company "AzCode".

Follow the steps below to set up and run the script:

1. <a href="#virtual_environment">Create and active Virtual Environment</a><br>
2. <a href="#install_libraries">Install all libraries and dependencies</a><br>
3. <a href="#run_script">Run script</a><br>

***

<a id="virtual_environment"></a>
## 1. Create and active Virtual Environment:

```bash
pip install virtualenv
```

```bash
virtualenv -p python3 venv
```

```bash
source venv/bin/activate
```

<a id="install_libraries"></a>
## 2. Install all libraries and dependencies:

```bash
pip3 install -r requirements.txt
```

<a id="run_script"></a>
## 3. Run parser:

```bash
python3 slotimo.py
```

During execution, the script will create the following folders:

- bonuses
- login_forms
- promotions

Each folder will store the results related to its purpose.

Please note that the script can work in headless mode, to do this, change the value in the variable "headless_mode".