from flask import Flask, request, redirect
from gevent.pywsgi import WSGIServer
import os, json, datetime, hashlib

app = Flask(__name__)
version = 'V0001'
version_key = '.s/f21d31c653#4$#!@(CJ)kd*2!_e49605253bf'
secret_key = '!;lO)DS!lsdfikLOIn*%&29431-0679823vcxlk11,dn'


@app.route('/', methods=['POST', 'GET'])
def index():
    ctime = datetime.datetime.now()
    if request.method == 'POST':
        response = ''
        try:
            if request.json['userId'] is not None:
                data = request.json
                try:
                    try:
                        os.mkdir('post_data/' + data['userId'], 0o755)
                    except:
                        pass
                    try:
                        os.mkdir('post_data/' + data['userId'] + '/' + str(ctime.strftime('%Y-%m-%d')), 0o755)
                    except:
                        pass
                except OSError:
                    pass

                with open('post_data/' + data['userId'] + '/' + str(ctime.strftime('%Y-%m-%d')) + '/' +
                          str(ctime.strftime('%H-%M-%S')) + '_data.json', 'w') as f:
                    json.dump(request.json, f, indent=4)
                response = {
                    'secret': hashlib.md5(
                        json.dumps(data, sort_keys=True).encode('utf-8') + secret_key.encode('utf-8')).hexdigest()
                }
                return json.dumps(response)


        except:
            response = 'Data is corrupted!'

        try:
            if request.json['version'] is not None:
                data = version + version_key
                response = {
                    'secret_ver': str(hashlib.md5(json.dumps(data, sort_keys=True).encode('utf-8')).hexdigest())
                }
                return json.dumps(response)
        except:
            response = 'Data is corrupted!'
        return response
    else:
        return redirect("https://www.rupsa.ru", code=302)


if __name__ == '__main__':
    http_server = WSGIServer(('', 1234), app)
    http_server.serve_forever()
