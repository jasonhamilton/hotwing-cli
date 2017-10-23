:: Create temp directory to store packaged file
mkdir hotwing-cli

:: Copy the files in bundle over to the package
copy bundle\* hotwing-cli

:: Copy the hotwing file
copy ..\common\hotwing-cli.py .

:: Copy the config file
copy ..\..\..\sample-config.cfg hotwing-cli\config.txt

:: Copy the icon file
copy ..\common\favicon.ico .

:: Copy the zip_bundle script
copy ..\common\zip_bundle.py .

:: Create the executable
pyinstaller hotwing-cli.py --onefile --icon=favicon.ico --clean

:: Move the executable
move dist\hotwing-cli.exe hotwing-cli\hotwing-cli.exe

:: Remove the directories and files created by pyinstaller
rd build /s /q
rd dist /s /q
del hotwing-cli.spec

:: Zip the package
python zip_bundle.py

:: Delete the package directory
rd hotwing-cli /s /q

:: Delete the hotwing file
del hotwing-cli.py

:: Delete the icon file
del favicon.ico

:: Delete the zip_bundle script
del zip_bundle.py

:: Move the packaged zip file to the bin directory
move hotwing-cli-win.zip ../../hotwing-cli-win.zip
