from flask import Flask
from waitress import serve

app = Flask(__name__)
from gihub_webhook import git

app.register_blueprint(git, url_prefix="/github_webhook")

@app.route('/')
def index():
    return 'asdf'

if __name__ == '__main__':
    serve(app, listen="*:5550")
    # app.run(host='0.0.0.0', port=5550)