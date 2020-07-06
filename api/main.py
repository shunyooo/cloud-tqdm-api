from datetime import datetime
from functools import partial
from flask import jsonify, make_response
import traceback

import time
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import firestore
from flask import jsonify

from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def call():
    return main(request)

cert_path = './data/cloud-tqdm-firebase-adminsdk-ojoma-57a051ae18.json'

if (not len(firebase_admin._apps)):
    cred = credentials.Certificate(cert_path)
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://cloud-tqdm.firebaseio.com/',
        'databaseAuthVariableOverride': {
            'uid': 'cloud-tqdm-service-worker'
        }
    })

## 参照
progress_ref = db.reference('/progress')

def validate_request(request):
    require_params = 'total description status elapsed'.split()
    assert request.args, f'please input {require_params}'

def set_if_in_args(progress_item, request, key, default_value=None):
    value = request.args.get(key)
    if value is not None:
        progress_item[key] = value
    elif default_value is not None:
        progress_item[key] = default_value

def main(request):
    try:
        validate_request(request)
        print(request.args)
        
        now = datetime.now().isoformat()
        progress_item = {}
        set_args = partial(set_if_in_args, progress_item, request)
        set_args('total')
        set_args('description')
        set_args('value', default_value=0)
        set_args('status')
        progress_item['updated_at'] = now

        progress_id = request.args.get('progress_id')
        if progress_id:
            progress_ref.child(progress_id).update(progress_item)
        else:
            progress_item['created_at'] = now
            progress_id = progress_ref.push(progress_item).key 

        progress_item['progress_id'] = progress_id

        return  jsonify({'message': 'success', 'res': progress_item}), 200
    except Exception as e:
        traceback_str = traceback.format_exc()
        print(f"ERROR: {str(e)}:{traceback_str}")
        return f"Internal Server Error:{str(e)}:{traceback_str}"
    
if __name__ == "__main__":
    app.run(debug=True)