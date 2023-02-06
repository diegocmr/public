from vosk import Model, KaldiRecognizer, SetLogLevel
import pyttsx3
import datetime
import random
import sounddevice
import soundfile
import queue
import sys
import json
import time
import numpy as np

SetLogLevel(-1) #definindo vosk com verbose false

def voicegen(audio_str):
    voicegen = pyttsx3.init()
    voicegen.setProperty('voice', 'portugal')
    voicegen.say(audio_str)
    voicegen.runAndWait()

def boas_vindas():
    hora = datetime.datetime.now().hour
    if hora >= 6 and hora < 12 :
        inicio = 'Bom dia!'
    elif hora >= 12 and hora < 18:
        inicio = 'Boa tarde!'
    else:
        inicio = 'Boa noite!'

    atendentes = ['Carol', 'Gabi', 'Lia', 'Joana', 'Si', 'Rê']
    atendente = atendentes[random.randint(0,len(atendentes)-1)]
    
    string_boas_vindas = '{inicio} Aqui quem fala é a {atendente}, da i-Móvel! Vou te transferir agora... Só me diz qual setor você quer: Vendas, Aluguel, Administrativo ou Financeiro.'\
        .format(inicio = inicio, atendente = atendente)
    
    print ('> ATENDENTE <\n\t',string_boas_vindas)
    voicegen(string_boas_vindas)

def toca_som(beep=False):
    try:
        if beep:
            file = 'beep.wav'
        else:
            file = 'fur_elise.wav'
        data, fs = soundfile.read(file, dtype='float32')  
        sounddevice.play(data, fs)
        sounddevice.wait()
        if not beep:
            exit()
    except KeyboardInterrupt:
        print('saindo...')
        exit()

def atende_cliente():
    # obtendo informações de dispositivos de audio da maquina
    device_info = sounddevice.query_devices(sounddevice.default.device[0], 'input')
    samplerate = int(device_info['default_samplerate'])

    q = queue.Queue()

    def recordCallback(indata, frames, time, status):
        if status:
            print(status, file=sys.stderr)
        q.put(bytes(indata))
        
    # instanceando modelo ptbr
    model = Model('vosk-model-small-pt-0.3')
    recognizer = KaldiRecognizer(model, samplerate)
    recognizer.SetWords(False)
    try:
        with sounddevice.RawInputStream(dtype='int16',
                            channels=1,
                            callback=recordCallback):
            nao_entendido = False #variavel para soar a condicional else uma vez
            print("Fale agora...")
            toca_som(beep=True)
            while True:
                data = q.get()        
                if recognizer.AcceptWaveform(data):
                    dict_result = json.loads(recognizer.Result())
                    resposta = dict_result['text']
                    print ('resposta', resposta)
                    print ('>CLIENTE<\n\t',resposta)
                    for palavra in ['tchau', 'desligar', 'encerrar', 'bye', 'sair']: #palavras para encerrar programa
                        if palavra in resposta.split(' '):
                            string = 'Encerrando chamado! Agradecemos o contato.'
                            print ('> ATENDENTE <\n\t',string)
                            voicegen (string)
                            exit()
                    if 'aluguel' in resposta.split(' '):
                        string = 'OK! Estou te transferindo para o setor de aluguel.'
                        print ('> ATENDENTE <\n\t',string)
                        voicegen (string)
                        toca_som()
                    elif 'vendas' in resposta.split(' '):
                        string = 'OK! Estou te transferindo para Vendas!'
                        print ('> ATENDENTE <\n\t',string)
                        voicegen (string)
                        toca_som()
                    elif 'administrativo' in resposta.split(' '):
                        string = 'Transferindo agora para o Administrativo.'
                        print ('> ATENDENTE <\n\t',string)
                        voicegen (string)
                        toca_som()
                    elif 'financeiro' in resposta.split(' '):
                        string = 'Transferindo para o setor Financeiro! por favor aguarde...'
                        print ('> ATENDENTE <\n\t',string)
                        voicegen (string)
                        toca_som()
                    else:
                        q.task_done()
                        if nao_entendido:
                            string = 'Encerrando o contato por dificuldade de comunicação.'
                            print ('> ATENDENTE <\n\t',string)
                            voicegen (string)
                            exit()
                        else:
                            string = 'Pode repetir?'
                            print ('> ATENDENTE <\n\t',string)
                            voicegen (string)
                            nao_entendido = True
                            time.sleep(3)
                        data = q.get()
    except KeyboardInterrupt:
        print('saindo...')
        exit()
    except Exception as e:
        print(e)


boas_vindas()
atende_cliente()