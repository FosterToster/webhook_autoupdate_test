from flask import Flask
from waitress import serve
from github_webhook import Github

app = Flask(__name__)

Github(app)

Github.new_handler('FosterToster/webhook_autoupdate_test','master')

@app.route('/')
def index():
    return 'Test merge !'


if __name__ == '__main__':
    serve(app, listen="*:5550")
    # app.run(host='0.0.0.0', port=5550)