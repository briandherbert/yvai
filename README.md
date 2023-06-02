# Flask App to hit ChatGPT
Designed to pull in prompt engineering and config from a remote source. GSheets for now.

To get this thing working generally

```
pip3 install .
export FLASK_APP=yvai.py
export OPENAI_API_KEY=
export PASSARG=
export SHEETID=
```

`SHEETID` is the Google Sheet with config params. Modify DB_gsheets.py as needed

`PASSARG` is a simple way to require a passcode to hit this. You set it as an env var, then requests must also pass the same thing as a JSON arg

There are a couple endpoints, they all take a prompt payload like

```
curl --request GET \
  --url http://haxrox.pythonanywhere.com/ask \
  --header 'Content-Type: application/json' \
  --data '{"prompt":"who are you", "PASSARG": "mypass"}'
```

## PythonAnywhere
1. Start a console with Python3.9
2. Clone this repo there
3. Follow steps here: https://help.pythonanywhere.com/pages/Flask/ , namely
    - Set venv stuff
    - WSGI (see below for full code)
4. In the console, add the above env vars by running, for example `echo "export PASSARG=mypass" >> .env`
5. In the console, from the yvai dir, run `pip install .`
6. Under **WEB** tab, click the big button 'Reload subdomain.pythonanywhere.com'

**wsgi.py**
```
# make env vars accessible
import os
from dotenv import load_dotenv
project_folder = os.path.expanduser('~/yvai')
load_dotenv(os.path.join(project_folder, '.env'))

import sys

path = '/home/haxrox/yvai'
if path not in sys.path:
    sys.path.append(path)

from yvai import app as application  # noqa
```

## Troubleshooting
Any code changes require re-running `pip install .` and clicking the web tab reload button.
