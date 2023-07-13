from flask import Flask, request
from gevent.pywsgi import WSGIServer
import os, json, datetime, hashlib

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
    ctime = datetime.datetime.now()
    if request.method == 'POST':
        try:
            if request.json['userId'] is not None:
                data = request.json
                try:
                    try:
                        os.mkdir('post_data/' + data['userId'], 0o755)
                    except:
                        pass
                    try:
                        os.mkdir('post_data/' + data['userId'] + '/' + str(ctime.year), 0o755)
                    except:
                        pass
                    try:
                        os.mkdir('post_data/' + data['userId'] + '/' + str(ctime.year) + '/' + str(ctime.month), 0o755)
                    except:
                        pass
                    try:
                        os.mkdir(
                            'post_data/' + data['userId'] + '/' + str(ctime.year) + '/' + str(ctime.month) + '/' + str(
                                ctime.day), 0o755)
                    except:
                        pass
                except OSError:
                    pass

                with open('post_data/'+ data['userId'] + '/' + str(ctime.year) + '/' + str(ctime.month) + '/' + str(ctime.day) + '/' +data['userId']+'_data.json', 'w') as f:
                    json.dump(request.json, f, indent=4)
                response = hashlib.md5(json.dumps(data, sort_keys=True).encode('utf-8')).hexdigest()
                return response
            else:
                return 'Use valid data'
        except:
            return 'Data is corrupted!'
    else:
        return 'Use POST requests'


if __name__ == '__main__':
    http_server = WSGIServer(('', 1234), app)
    http_server.serve_forever()