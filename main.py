print('start')
from flask import Flask
from waitress import serve
from github_webhook import Github

app = Flask(__name__)

Github(app)

Github.new_handler('FosterToster/webhook_autoupdate_test', 'master', 'mas/prod', on_update=Github.update_itself, on_restart=Github.restart_itself)

@app.route('/')
def index():
    return 'OMG! It works!!!'


if __name__ == '__main__':
    serve(app, listen="*:5550")
    # app.run(host='0.0.0.0', port=5550)