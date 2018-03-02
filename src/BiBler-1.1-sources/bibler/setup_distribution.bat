SET /p version="Change the version in __init__.py then press <Enter>..."

SET /p skip="Skip doc generation? (y/n) "
IF "%skip%"=="" GOTO Error
IF "%skip%"=="y" GOTO Setup
cd ..
"C:\Python27\Scripts\epydoc.py" --config BiBler\docs\config --verbose
pause
cd BiBler

:Setup
copy __init__.py bibler.py
py -3.4 setup.py py2exe
xcopy utils\resources\*.* dist\utils\resources /s/q/y
copy readme.txt dist\readme.txt
xcopy ext dist\external /s/q/y
del bibler.py
rename dist BiBler
SET /p zip="Now zip the BiBler folder to BiBler-VERSION then press <Enter>..."
rmdir /s/q BiBler

mkdir ..\BiBler-sources\app
mkdir ..\BiBler-sources\docs
mkdir ..\BiBler-sources\ext
mkdir ..\BiBler-sources\gui
mkdir ..\BiBler-sources\testApp
mkdir ..\BiBler-sources\utils\resources
mkdir ..\BiBler-sources\win_dll
copy app\*.py ..\BiBler-sources\app
xcopy docs\*.* ..\BiBler-sources\docs /s/q/y
REM copy docs\Scripts\*.* ..\BiBler-sources\docs\Scripts
copy ext\*.* ..\BiBler-sources\ext
copy gui\*.py ..\BiBler-sources\gui
copy testApp\*.py ..\BiBler-sources\testApp
copy utils\*.py ..\BiBler-sources\utils
copy utils\resources\*.* ..\BiBler-sources\utils\resources
copy win_dll\*.* ..\BiBler-sources\win_dll
copy readme.txt ..\BiBler-sources\readme.txt
copy __init__.py ..\BiBler-sources\__init__.py
copy setup.py ..\BiBler-sources\setup.py
copy setup_distribution.bat ..\BiBler-sources\setup_distribution.bat
SET /p zip="Now rename BiBler-sources to BiBler-VERSION-sources then zip it"
GOTO End

:Error
ECHO Unknown answer.
pause

:End
pause