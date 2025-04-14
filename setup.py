import os
import sys
from setuptools import setup, find_packages, Command

installRequires = [
    "PyQt6 >= 6.0",
    "mysql-connector-python >= 8.0",
    "python-dotenv >= 0.19.0"
]

defaultEnvContent = """\
DB_HOST = localhost
DB_USER = root
DB_PASSWORD = password
DB_NAME = pyqtwordquiz
"""

class InitCommand(Command):

    description = "Initialize environment (.env file) and create database table(s)"
    userOptions = []

    def initializeOptions(self):
        pass

    def finalizeOptions(self):
        pass

    def run(self):
        envPath = os.path.join(os.path.dirname(__file__), 'src', 'db', '.env')
        if not os.path.exists(envPath):
            self.announce("Creating .env file...", level = 3)
            with open(envPath, 'w') as f:
                f.write(defaultEnvContent)
            self.announce(".env file created successfully. Please edit it as necessary.", level = 3)
        else:
            self.announce(".env file already exists. Skipping creation.", level = 3)

        self.announce("Initializing database...", level = 3)
        try:
            os.environ['PYTHONPATH'] = os.path.abspath(os.path.dirname(__file__))
            from src.db.words import Database
            db = Database()
            db.createTable()
            db.commitChanges()
            db.close()
            self.announce("Database initialized successfully.", level = 3)
        except Exception as e:
            self.announce(f"Error initializing database: {e}", level = 3)
            sys.exit(1)

setup(
    name = "pyqtwordquiz",
    version = "0.1",
    description = "A PyQt6 Word Quiz Application with MySQL integration",
    author = "Your Name",
    author_email = "youremail@example.com",
    packages = find_packages(where = "src"),
    install_requires = installRequires,
    entry_points = {
        "console_scripts": [
            "pyqtwordquiz = mainPage:main",
        ],
    },
    cmdclass = {
        'init': InitCommand,
    },
    package_dir = {'': 'src'},
)
