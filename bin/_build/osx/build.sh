pyinstaller hotwing-cli.py --onefile --icon=favicon.ico --clean

# Create temp directory to store packaged file
mkdir hotwing-cli

# Copy the files in bundle over to the package
cp bundle/* hotwing-cli

# Move the executable
mv dist/hotwing-cli hotwing-cli/hotwing-cli

# Chmod files
chmod +x hotwing-cli/hotwing-cli
chmod +x hotwing-cli/parse_config.command

# Remove the directories and files created by pyinstaller
rm -r build
rm -r dist
rm hotwing-cli.spec

# Zip the package
python zip_bundle.py

# Delete the package directory
rm -r hotwing-cli

# Move the packaged zip file to the bin directory
mv hotwing-cli-win.zip ../../hotwing-cli-osx.zip
