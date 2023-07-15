# psa_dispay_configurator
PSA matrix display configurator

### Installation

>python -m pip install virtualenv
***
>.\venv\Scripts\activate
***
Выполнить установку requirements.txt

pyinstaller --clean --windowed --onedir --add-data helloGUI.ui;. qt_code.py
pyinstaller -w -F -i "icon.ico" script.py
pyinstaller --onefile --clean --windowed --icon=logo.ico main.py


Then later can eg pack it with eg Inno Setup https://jrsoftware.org/isinfo.php then get single setup.exe which has a installer.
Or can just .zip to one file,and share that.
It depend one use case a singe .exe is easy to share a,but many will not a run a executable .exe if not sure what is.
A installer(that also has a uninstaller) also make some Doc,is the professional looking way if want to share in a larger scale. 