from flask import Blueprint, request
import json

git = Blueprint('git', 'git')

@git.route('/', methods=['POST'])
def index():
    with open('listing.json', 'w+') as f:
        f.write(json.dumps(request.json, indent=2))
        f.close()
    
    return 'asdf'