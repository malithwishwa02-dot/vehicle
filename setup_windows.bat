@echo off
TITLE LUCID EMPIRE - WINDOWS BUILDER
COLOR 0A
echo [1] CREATING BINARY STRUCTURE...
mkdir bin
mkdir bin\firefox
echo [2] INSTALLING PYTHON DEPENDENCIES...
pip install flask pywebview pyinstaller playwright requests pysocks
echo [3] DOWNLOADING BROWSER ENGINE...
playwright install firefox
echo    -> NOTE: You must manually copy the firefox binary from
	echo       %LOCALAPPDATA%\ms-playwright\firefox-xxxx\firefox
	echo       into the .\bin\firefox\ folder for the EXE to work portably.
echo [4] INSTRUCTION:
if defined RUN_AS_DATE_URL (
    echo    Downloading RunAsDate from %RUN_AS_DATE_URL% ...
    powershell -ExecutionPolicy Bypass -File scripts\fetch_runasdate.ps1 -Url "%RUN_AS_DATE_URL%"
) else (
    echo    Please download RunAsDate.exe (x64) from NirSoft and place it in .\bin
)
echo    Then run: pyinstaller build_exe.spec
pause
