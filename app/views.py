from app import app
from flask import jsonify
from flask import request
from flask import render_template
from pathlib import Path
import json

@app.route('/prof', methods=['GET'])
def prof():
     return render_template("index.html", name = 'prof', title = '1С Платформа')

@app.route('/do', methods=['GET'])
def do():
     return render_template("index.html", name = 'do', title = '1С Документооборот')

@app.route('/api', methods=['GET'])
def get_data():
    return get_data_int()

@app.route('/api/all', methods=['GET'])
def get_data_all():
    return get_data_int(True)
    
def get_data_int(all=False):
    username = get_user_name()
    name = request.args.get('name')
    
    data_file_name = "data/" + name + "/" + username
    data_file = Path(data_file_name)
    
    if data_file.is_file():
        with open(data_file_name, 'r') as fp:
            # считываем сразу весь файл
            data = json.load(fp)
    else:
        data = []
        
    result = []
    for question_key in data.keys():   
        if all:
            result.append(question_key)
        else:
            if data[question_key] < 3:
                result.append(question_key)

    return jsonify(result)


def get_user_name():
    username = request.environ.get('REMOTE_USER')
    # Раскоментировать при тестироватие и запуске не на сервере
    #username = "larin"
    return username
    
@app.route('/api', methods=['POST'])
def set_data():
    username = get_user_name()
    request_data = request.json
    
    data_dir_name = "data/" + request_data["test"]
    data_file_name = data_dir_name + "/" + username
    data_file = Path(data_file_name)
    data_dir = Path(data_dir_name)
    
    if not data_dir.is_dir():
        data_dir.mkdir(parents=True)
    
    if data_file.is_file():
        with open(data_file_name, 'r') as fp:
            # считываем сразу весь файл
            data = json.load(fp)
    else:
        data = {}

    question_data = data.get(request_data["question"])
    
    if request_data["result"]:
        if question_data is not None:
            question_data = question_data + 1
            data[request_data["question"]] = question_data
    else:
        # Ошибка, Сбрасываем правильные ответы в 0
        data[request_data["question"]] = 0
                
    with open(data_file_name, 'w') as fp:
        json.dump(data, fp)
        
    return jsonify(data.get(request_data["question"], ""))
