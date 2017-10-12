pyinstaller hotwing-cli.py --onefile --icon=favicon.ico --clean

:: Create temp directory to store packaged file
mkdir hotwing-cli

:: Copy the files in bundle over to the package
copy bundle\* hotwing-cli

:: Move the executable
move dist\hotwing-cli.exe hotwing-cli\hotwing-cli.exe

:: Remove the directories and files created by pyinstaller
rd build /s /q
rd dist /s /q
del hotwing-cli.spec

:: Zip the package
python zip_bundle.py

:: Delete the package director
rd hotwing-cli /s /q

:: Move the packaged zip file to the bin directory
move hotwing-cli-win.zip ../hotwing-cli-win.zip
