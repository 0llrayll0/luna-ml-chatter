from transformers import pipeline
import speech_recognition as sr
import os
import pyttsx3
from googletrans import Translator
import pytesseract
from PIL import ImageGrab

engine = pyttsx3.init()
gerador_texto = pipeline("text-generation", model="EleutherAI/gpt-neo-1.3B")
tradutor = Translator()

comandos = {
    'oi luna': 'Iniciando conversa...',
    'luna n': 'Abrindo o navegador...',
    'luna kit': 'Abrindo o site do GitHub...',
    'luna pasta': 'Abrindo a pasta padrão...',
    'luna visual': 'Abrindo o Visual Studio Code...',
    'luna texto': 'Lendo a tela...',
    'luna console': 'abrindo a Cmd'
}

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def reconhecer_comando():
    reconhecedor = sr.Recognizer()
    with sr.Microphone() as source:
        print("Ajustando para o ruído ambiente. Por favor, aguarde...")
        reconhecedor.adjust_for_ambient_noise(source)
        print("Diga algo...")
        audio = reconhecedor.listen(source)

    try:
        comando = reconhecedor.recognize_google(audio, language="pt-BR")
        print(f"Você disse: {comando}")
        return comando.lower()
    except sr.UnknownValueError:
        print("Não entendi o que foi dito.")
        return ""
    except sr.RequestError as e:
        print(f"Erro ao se conectar ao serviço de reconhecimento de fala: {e}")
        return ""

def falar(resposta):
    engine.say(resposta)
    engine.runAndWait()

def abrir_pasta(caminho):
    try:
        os.startfile(caminho)
        print(f"Abrindo a pasta: {caminho}")
    except Exception as e:
        print(f"Erro ao abrir a pasta: {e}")

def ler_tela():
    screenshot = ImageGrab.grab()
    texto = pytesseract.image_to_string(screenshot, lang='por')
    print("Texto lido da tela:")
    print(texto)
    falar(texto)

def executar_acao(comando):
    if comando in comandos:
        print(comandos[comando])
        falar(comandos[comando])
        
        if comando == "oi luna":
            iniciar_conversa()
        elif comando == "luna n":
            print("Abrindo o navegador...")
            os.system("start chrome")
        elif comando == "luna kit":
            print("Abrindo o site do GitHub...")
            os.startfile("https://github.com")
        elif comando == "luna pasta":
            caminho_padrao = r"C:\Users\power\OneDrive\Área de Trabalho"
            abrir_pasta(caminho_padrao)
        elif comando == "luna visual":
            print("Abrindo o Visual Studio Code...")
            os.startfile(r"C:\Users\power\OneDrive\Área de Trabalho\Visual Studio Code.lnk")
        elif comando == "luna texto":
            ler_tela()
        elif comando == "luna console":
            print("Abrindo a Cmd...")
            os.startfile(r"C:\Users\power\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\System Tools\Command Prompt.lnk")
    else:
        print("Comando não reconhecido. Você pode adicionar novos comandos.")

def iniciar_conversa():
    while True:
        usuario_input = reconhecer_comando()
        if "luna sair" in usuario_input:
            print("Saindo da conversa.")
            break
            
        traducao_input = tradutor.translate(usuario_input, src='pt', dest='en').text
        resposta_en = gerador_texto(traducao_input, max_length=100, num_return_sequences=1)[0]['generated_text']
        resposta_pt = tradutor.translate(resposta_en, src='en', dest='pt').text

        print("luna:", resposta_pt)
        falar(resposta_pt)

if __name__ == "__main__":
    while True:
        comando = reconhecer_comando()
        if comando:
            executar_acao(comando)
        if "sair" in comando:
            print("Encerrando o programa.")
            break
