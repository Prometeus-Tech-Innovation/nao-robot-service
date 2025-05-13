from flask import Flask, request, jsonify
from qi_connection import QiConnection, FirstInteraction, QiCloseSession
from qi_commands import QiAnimatedSpeech, QiListen
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://jano-plataform.vercel.app"}})
session = None
qi_app = None

@app.route('/ip', methods=['POST'])
def IpConnection():
    data = request.json
    
    robot_ip = data.get('robot_ip')
    if not robot_ip:
        return jsonify({'status': 'IP do robô não fornecido'}), 400
    
    session = QiConnection(robot_ip)
    if not session:
        return jsonify({'status': 'Falha na conexão com o robô'}), 500
    
    try:
        FirstInteraction(session)
    except Exception as e:
        return jsonify({'status': f'Erro ao interagir com o robô: {e}'}), 501
    
    return jsonify({'status': 'Conexão estabelecida com o robô'}), 200

@app.route('/ask', methods=['POST'])
def ResponseQuestion():
    data = request.json
    resposta = data.get('response', '')
    robot_ip = data.get('robot_ip')
    
    if not robot_ip:
        return jsonify({'status': 'IP do robô não fornecido'}), 400
    
    session = QiConnection(robot_ip)
    if not session:
        return jsonify({'status': 'Falha na conexão com o robô'}), 500
    
    try:
        QiAnimatedSpeech(session, resposta)
    except Exception as e:
        return jsonify({'status': f'Erro ao interagir com o robô: {e}'}), 502
    
    return jsonify({'response': resposta, 'robot_ip': robot_ip}), 201

@app.route('/shutdown', methods=['GET'])
def FinishSession():
    global qi_app, session
    if session:
        try:
            QiCloseSession(session, qi_app)
            return jsonify({'status': 'Sessão encerrada com sucesso'}), 202
        except Exception as e:
            return jsonify({'status': f'Erro ao encerrar a sessão: {e}'}), 503
    return jsonify({'status': 'Nenhuma sessão ativa'}), 401

@app.route('/listen', methods=['POST'])
def ListenQuestion():
    data = request.json
    robot_ip = data.get('robot_ip')

    if not robot_ip:
        return jsonify({'status': 'IP do robô não fornecido'}), 400
    
    session = QiConnection(robot_ip)
    if not session:
        return jsonify({'status': 'Falha na conexão com o robô'}), 500
    
    try:
        listen = QiListen(session)
    except Exception as e:
        return jsonify({'status': f'Erro ao interagir com o robô: {e}'}), 504
    
    return jsonify({'response': listen, 'robot_ip': robot_ip}), 203

