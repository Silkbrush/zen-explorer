import tomllib
import os

with open('pyproject.toml', 'rb') as file:
    settings = tomllib.load(file)

env_file = os.getenv('GITHUB_ENV')

with open(env_file, "a") as myfile:
    myfile.write(f"VERSION={settings['project']['version']}\nRAW_VERSION={settings['project']['version']}\n")
