from flask import request
from flask import Flask
import json
import subprocess
import re

app = Flask(__name__)
@app.route('/', methods = ['POST'])
def index():
        data = json.loads(request.data.decode('utf'))
        try:
            commit = data['head_commit']['id']
            repo = data['repository']['name']
            # LaTeX unsafe: & % $ # _ { } ~ ^ \
            # sed unsafe / \ &
            message = re.sub('[/\&%$#_{}~^]', '', data['head_commit']['message'])
        except:
            return 'Invalid commit'

        print(commit)
        process = subprocess.Popen(['./buildpaper.sh', repo, commit], stdout=subprocess.PIPE)
        output, error = process.communicate()

        print(output)

        return 'OK'

if __name__ == "__main__":
        app.run(host='0.0.0.0', port = 9000)
