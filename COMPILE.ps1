# Sample build command for PyInstaller to create an executable
./.venv/Scripts/pyinstaller --noconfirm --onefile --console --name "Prisma" --clean --add-data "./resources;resources/" "./main.py"