# PyPI Browser

A simple package viewer that lets you look at information about packages on PyPI.

## Prerequisites
- **Python 3.9+**

## Setup
1. **Clone the repository:** `git clone https://github.com/canadaluke888/PyPIBrowser.git`
2. **Setup a virtual environment in the root of the project directory:** `python3 -m venv .venv` on Mac and Linux. `python -m venv .venv` on Windows
3. **Activate the virtual environment:** `source .venv/bin/activate` on Mac and Linux. `.venv/Scripts/Activate.ps1` on Windows.
4. **Install dependencies:** `pip install -r requirements.txt`
5. **Run the application:** `python3 main.py` on Mac and Linux. `python main.py` on Windows.

## Usage
- **Searching for packages:** Enter the search term or package at the top of the application in the search bar. Click the "Search" button and the results will be displayed below.
- **Viewing Information on a package:** Right click on a selected package and select "view package info" from the context menu. A window with more information should appear.
- **Copying the install commad for the package:** Right click on the selected package and click "copy install command" from the context menu. You can then paste this command into a terminal to install the package.