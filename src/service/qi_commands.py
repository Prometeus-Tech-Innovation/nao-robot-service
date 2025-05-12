import time
import json
import websockets
import asyncio
import base64

def QiAnimatedSpeech(session, resposta):
    tts = session.service("ALTextToSpeech")
    aas = session.service("ALAnimatedSpeech")
    arp = session.service("ALRobotPosture")
    
    aas.setBodyLanguageMode(2)
    arp.goToPosture("Stand", 1)
    tts.setVolume(0.5)
    
    if not resposta:
        tts.say("Desculpe, não recebi uma pergunta.")
        raise Exception('Empty response')

    aas.say(str(resposta))
    arp.goToPosture("Stand", 1)

async def QiListen(session):
    try:
        asr = session.service("ALAudioPlayer")
        asr.setInputDevice('Mic')
        asr.setSampleRate(16000)
        asr.setChannelsConfiguration('Front')
    except Exception as e:
        print(f"Erro ao configurar o microfone: {e}")
        raise

    websocket = websockets.Websocket
    websocket.accept()
    
    try:
        while True:
            data = asr.getFrontMicData()

            if data:
                encoded_data = base64.b64encode(data).decode('utf-8')
                await websocket.send(json.dumps({"audio": encoded_data}))

            await asyncio.sleep(0.01)

    except websockets.exceptions.ConnectionClosedOK:
        print("Cliente WebSocket desconectado.")
    except Exception as e:
        print(f"Erro ao enviar áudio: {e}")