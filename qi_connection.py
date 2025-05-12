import qi

session = None
qi_app = None

def QiConnection(robot_ip):
    global qi_app, session
    if session is None:  # Se ainda não existe uma sessão ativa, cria uma nova
        try:
            connection_url = f'tcp://{robot_ip}:9559'
            app_qi = qi.Application(['NaoQiApp', '--qi-url=' + connection_url])
            app_qi.start()
            session = app_qi.session
            print('Sessão com o robô iniciada!')
        except RuntimeError as e:
            print(f'Erro ao conectar ao robô: {e}')
            return None
    return session

def FirstInteraction(session):
    tts = session.service('ALTextToSpeech')
    tts.setLanguage('Brazilian')
    tts.setVolume(0.5)
    tts.say('Jano conectado! Pronto para personificar o assunto...')

def QiCloseSession(session, qi_app):
    session.close()
    qi_app.stop()
    session = None
    qi_app = None