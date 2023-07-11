# psa_dispay_configurator
PSA matrix display configurator

### Installation

>python -m pip install virtualenv
***
>.\venv\Scripts\activate
***
Выполнить установку requirements.txt

pyinstaller --clean --windowed --onedir --add-data helloGUI.ui;. qt_code.py

Then later can eg pack it with eg Inno Setup https://jrsoftware.org/isinfo.php then get single setup.exe which has a installer.
Or can just .zip to one file,and share that.
It depend one use case a singe .exe is easy to share a,but many will not a run a executable .exe if not sure what is.
A installer(that also has a uninstaller) also make some Doc,is the professional looking way if want to share in a larger scale. 

fault_code 590209DF038708DF0A8809
fault_code 590209DF038708DF0A880890035409
fault_code 590209DF03870890035409

590209 - код ответчика
regex:
F\w\w\w = F03, F0A - ошибки
9\w\w\w = 9003 - ошибка защищённой конфигурации

22 f0 80 : 62F080967376838000299824142380FFFFFFFF0001FFFFFFFF
    hw id 62F08 09673768380
    0029 
    additional hw id 9824142380 
    FFFFFFFF0001FFFFFFFF

22 f0 fe - 96 031112 80

62F080967376838000299824142380FFFFFFFF0001FFFFFFFF
62F0FE95F2000029EC0A0311120000000A0311FE000000FE925365

hw_id = hex(cmd_ident[0].data[5])[2:].zfill(2) + "" + hex(cmd_ident[0].data[6])[2:].zfill(2) + "" + hex(
            cmd_ident[0].data[7])[2:].zfill(2) + "" + hex(cmd_ident[1].data[1])[2:].zfill(2) + "" + hex(
            cmd_ident[1].data[2])[2:].zfill(2)

        hw_id_2 = hex(cmd_ident[1].data[5])[2:].zfill(2) + "" + hex(cmd_ident[1].data[6])[2:].zfill(2) + "" + hex(
            cmd_ident[1].data[7])[2:].zfill(2) + "" + hex(cmd_ident[2].data[1])[2:].zfill(2) + "" + hex(
            cmd_ident[2].data[2])[2:].zfill(2)

        sw_id = "96" + hex(cmd_ident[5].data[5])[2:].zfill(2) + "" + hex(cmd_ident[5].data[6])[2:].zfill(2) + "" + hex(
            cmd_ident[5].data[7])[2:].zfill(2) + "80"

