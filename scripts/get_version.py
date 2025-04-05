import tomllib
import os

with open('pyproject.toml', 'rb') as file:
    data = tomllib.load(file)

env_file = os.getenv('GITHUB_ENV')

with open(env_file, "a") as myfile:
    myfile.write(f"VERSION=v{data['project']['version']}\nRAW_VERSION={data['project']['version']}\n")
