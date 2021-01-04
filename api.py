import flask
from flask import request
import json
import redis
import requests

r = redis.Redis(host='redis', port=6379)

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/report', methods=['GET'])
def home():
    keys = r.keys('*')
    print("keys: ",keys)
    data = []
    for key in keys:
        k_type = r.type(key)
        if k_type.decode('ascii') == "hash":
            value = r.hgetall(key.decode('ascii'))
            value = { y.decode('ascii'): value.get(y).decode('ascii') for y in value.keys() }
            for i in value:
                value[i] = int(value[i])
            value['ip'] = key.decode('ascii')
            print(value)
            data.append(value)
    print(data)
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/metrics', methods=['POST'])
def json_example():

    try:
        req_data = request.get_json()
        percentage_cpu_used = req_data['percentage_cpu_used']
        percentage_memory_used = req_data['percentage_memory_used']
        client_ip = request.remote_addr
        data = {}
        if(r.exists(client_ip)):
            old_value = r.hgetall(client_ip)
            old_value = { y.decode('ascii'): old_value.get(y).decode('ascii') for y in old_value.keys() }
            if(int(old_value['percentage_memory_used']) > int(percentage_memory_used)): percentage_memory_used = old_value['percentage_memory_used']
            if(int(old_value['percentage_cpu_used']) > int(percentage_cpu_used)): percentage_cpu_used = old_value['percentage_cpu_used']
            data = {"percentage_memory_used":percentage_memory_used, "percentage_cpu_used":percentage_cpu_used}
        else:
            data = {"percentage_memory_used":percentage_memory_used, "percentage_cpu_used":percentage_cpu_used}

        r.hmset(client_ip, data)
        value = r.hgetall(client_ip)
        return '''
            metrics have been inserted''', 200
    except Exception as e:
        print(e)
        return "Something went wrong",500

app.run(host='0.0.0.0', port=8080)