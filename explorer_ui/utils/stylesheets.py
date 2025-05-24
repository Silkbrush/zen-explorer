import os

def load_css(directory):
    with open(f"{directory}/style.css", "r") as f:
        _style = f.read()
        if os.path.isfile(f"{directory}/variables.txt"):
            with open(f"{directory}/variables.txt", "r") as f:
                _variables = f.read()
                for line in _variables.splitlines():
                    line = line.replace(' ', '')
                    var = line.split(':')[0].strip()
                    val = line.split(':')[1].strip()
                    _style = _style.replace(f"{var}", val)
        return _style
