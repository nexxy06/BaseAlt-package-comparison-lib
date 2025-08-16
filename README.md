# BaseAlt-package-comparison-lib

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
python -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -e .
```
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