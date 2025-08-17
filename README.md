# BaseAlt-package-comparison-lib
Key Features:

    🔍 Compare packages between different ALT Linux branches (p9, p10, p11, Sisyphus)

    📊 Analyze version differences across architectures (x86_64, aarch64, etc.)

    🚀 CLI tool for quick branch comparisons

    📦 JSON output for easy integration with other tools

Makes a comparison of the received package lists and outputs JSON in which it will be displayed:
    
    all packages that are in the 1st but not in the 2nd
    
    all packages that are in the 2nd but are not in the 1st
    
    all packages whose version is greater in the 1st than in the 2nd
## Prerequisites
- Python 3.7 or higher
- pip 24.2 or higher
- git 2.49.0 or higher

## Installation
### 1. Clone repository
```bash
git clone https://github.com/nexxy06/BaseAlt-package-comparison-lib.git
cd BaseAlt-package-comparison-lib
```
### 2. Set up virtual environment(optional)
!!! When using venv, you will need to activate the environment in each new terminal. !!!
- Linux/macOS:
```bash
# Create virtual environment
python -m venv venv

# Activate environment
source venv/bin/activate
```

- Windows:
```bash
# Create virtual environment
python -m venv venv

# Activate environment  
venv\Scripts\activate
```
### 3. Installing dependencies
```bash
python -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade pip setuptools wheel
python -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple .
```
If the mirror is unavailable, try another one or without "-i https://pypi.tuna.tsinghua.edu.cn/simple".
### 4. Health check
```bash
altlinux-compare --help
altlinux-compare compare-branches p11 p10
```

## Uninstallation
```bash
pip uninstall altlinux-tools
```
If venv was used:
```bash
deactivate
```
```bash
rm -rf venv/
```