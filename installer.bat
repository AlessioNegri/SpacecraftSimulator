@echo OFF

rem pyinstaller --icon=img\icon.ico --windowed --exclude-module _bootlocale --name SpacecraftSimulator2 main.py
rem pyinstaller --onefile --icon=img\icon.ico --windowed --exclude-module _bootlocale --name SpacecraftSimulator main.py
rem pyinstaller --onedir --windowed --exclude-module _bootlocale --name SpacecraftSimulator main.py

pyinstaller SpacecraftSimulator.spec --noconfirm