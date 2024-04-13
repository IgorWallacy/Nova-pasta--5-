import os
from tkinter import *
from tkinter.ttk import *
import fundo_base64 
import tkinter as tk
from tkinter import ttk
import locale
from PIL import Image, ImageTk
import io
import sys
import subprocess
import socket
import base64
from io import BytesIO
from PIL import Image
from datetime import datetime
import time
import psutil
import psycopg2
from psycopg2 import Error


# pyinstaller --onefile -w seu_script.py

# Variável global para armazenar a referência da imagem
global_image_reference = None

# Define a localização para português do Brasil
locale.setlocale(locale.LC_TIME, 'pt_BR')

def restart_program():
    python = sys.executable
    os.execl(python, python, *sys.argv)

def conectar_postgresql(usuario, senha, host, porta, banco_dados):
    try:
        # Conectar ao banco de dados PostgreSQL
        connection = psycopg2.connect(user=usuario,
                                      password=senha,
                                      host=host,
                                      port=porta,
                                      database=banco_dados)
        print("Conexão ao PostgreSQL bem-sucedida")
        return connection

    except (Exception, Error) as error:
        print("Erro ao conectar ao PostgreSQL:", error)
        return None

def executar_consulta(connection, consulta):
    try:
        # Criar um cursor
        cursor = connection.cursor()

        # Executar a consulta SQL
        cursor.execute(consulta)

        # Obter resultados, se houver
        records = cursor.fetchall()
        return records

    except (Exception, Error) as error:
        print("Erro ao executar a consulta:", error)
        return None

    finally:
        # Fechar o cursor
        if cursor:
            cursor.close()

def fechar_conexao(connection):
    try:
        # Fechar a conexão com o banco de dados
        if connection:
            connection.close()
            print("Conexão ao PostgreSQL fechada")

    except (Exception, Error) as error:
        print("Erro ao fechar a conexão:", error)



# Exemplo de uso
def atualizarIP():
    
    global server_ip  # Declare server_ip como global
    global tipo_servidor
    global filial
    global pdv
    
    server_ip = None
    tipo_servidor = None
    filial = None
    pdv = None
    
    conexao = conectar_postgresql("postgres", "postgres", "localhost", "5432", "unico")
    if conexao:
        
        resultado = executar_consulta(conexao, "SELECT valor FROM configuracaopdv WHERE chave='BaseRemota.Url' AND perfil='default';")
        resultadoTipoServidor = executar_consulta(conexao, "SELECT valor FROM configuracaopdv WHERE chave='Pdv.TipoServidor' AND perfil='default';")
        resultadoFilial = executar_consulta(conexao, "SELECT valor FROM configuracaopdv WHERE chave='Pdv.Filial' AND perfil='default';")
        resultadoPdv = executar_consulta(conexao, "SELECT valor FROM configuracaopdv WHERE chave='Pdv.Numero' AND perfil='default';")
        
        if resultado:
            # Acessando o primeiro elemento da primeira tupla retornada
            server_ip = str(resultado[0][0])  # Convertendo para string
        if resultadoTipoServidor:
            # Acessando o primeiro elemento da primeira tupla retornada
            tipo_servidor = resultadoTipoServidor[0][0]  
        if resultadoFilial:
            # Acessando o primeiro elemento da primeira tupla retornada
            filial = resultadoFilial[0][0] 
        if resultadoPdv:
            # Acessando o primeiro elemento da primeira tupla retornada
            pdv = resultadoPdv[0][0]   
            
    fechar_conexao(conexao)

# Chame a função atualizarIP() para atribuir o valor de server_ip
atualizarIP()


def switch_case(tipo):
    switcher = {
        "0": {"descricao": "Servidor PDV", "porta": "1099"},
        "1": {"descricao": "Servidor YODA", "porta": "8443"},
        "2": {"descricao": "Servidor Web Cloud", "porta": "8443"},
        "3": {"descricao": "Servidor Web Local", "porta": "8080"}
    }
    return switcher.get(tipo, {"descricao": "Tipo de Servidor inválido", "porta": ""})


# def load_server_ip():
#   try:
# Tenta carregar a variável de ambiente
#      ip_servidor = os.environ.get("ip_servidor_JJ")
#     if ip_servidor:
#        return ip_servidor.strip()  # Remove espaços em branco extras
#   else:
# Se a variável de ambiente não existir, retorne None
#      return None
# except Exception as e:
#    print("Erro ao carregar a variável de ambiente:", e)
#    return None

def atualizar_data_hora():
    
    # Obter a data e hora atual
    data_hora_atual_ = datetime.now().strftime("%d/%m/%Y - %H:%M:%S - %A")
    
    # Atualizar o rótulo com a nova data e hora
    label_hora.config(text="| Hoje é " + data_hora_atual_ + " |")
    
    # Chamar esta função novamente após 1000 milissegundos (1 segundo)
    root.after(1000, atualizar_data_hora)

def check_network_connection(server_ip):
    servidor = switch_case(tipo_servidor)
   # print(servidor["porta"])
    
    try:
            ip_address = socket.gethostbyname(server_ip)
            socket.create_connection((server_ip, servidor["porta"]))
            with socket.create_connection((ip_address, servidor["porta"]), timeout=5) as sock:
                return "Conectado"
    except OSError:
        return "Desconectado"

def check_internet_connection(ip):
    try:
        socket.create_connection((ip, 80))
        return True
    except OSError:
        return False

def get_computer_name():
    return socket.gethostname()

def get_local_ip():
    try:
        # Obtém o endereço IP da primeira interface de rede que não seja loopback
        local_ip = socket.gethostbyname(socket.gethostname())
        return local_ip
    except socket.gaierror:
        return "Não disponível"



# Função para verificar se o processo está em execução
def verificar_processo(process_name):
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == process_name:
            return True
    return False

# Função para iniciar o aplicativo
def iniciar_aplicativo(aplicativo_path):
    subprocess.Popen(aplicativo_path)
    


# Função para redimensionar a imagem para o tamanho da tela
def redimensionar_imagem(image, width, height):
    return image.resize((width, height), Image.FIXED)

# Função para exibir uma janela com um cronômetro
def exibir_cronometro():
    root = tk.Tk()
    #root.title("Cronômetro - Verificando se o PDV está em execução!")

    # Configurando a janela para tela cheia
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.attributes('-fullscreen', True)

    # Convertendo a imagem base64 para o formato de imagem do tkinter e redimensionando
    img_data = base64.b64decode(fundo_base64.background_base64)
    image = Image.open(io.BytesIO(img_data))
    image = redimensionar_imagem(image, screen_width, screen_height)
    background_image = ImageTk.PhotoImage(image)
   
    # Adicionando a imagem acima do cronômetro
    background_label = tk.Label(root, image=background_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Criando um frame para conter os widgets
    frame = tk.Frame(root, bg="#f0f0f0")
    frame.place(relx=0.5, rely=0.1, anchor="center")

    label = tk.Label(frame, text="O PDV não foi iniciado. Aguardando 45 segundos!", font=("Calibri", 16), bg="#f2f2f2")
    label.pack()

    segundos_restantes = 15
    while segundos_restantes > 0:
        label.config(text="Aguardando {} segundos para abrir automaticamente o software de vendas!".format(segundos_restantes), font=("Calibri", 24), bg="#f2f2f2")
        segundos_restantes -= 1
        root.update()
        time.sleep(1)

        if verificar_processo("UniNfce.exe"):
            label.config(text="UniNfce foi iniciado! Fechando o cronômetro...")
            root.update()
            time.sleep(2)
            root.destroy() 
            return

    label.config(text="Obrigado pela paciência! Iniciando o aplicativo...")
    root.update()
    time.sleep(2)
    root.destroy()
    segundos_restantes -= 1
    iniciar_aplicativo("E:/uniplus/uninfce.exe")

# Verificar se o processo está em execução
if not verificar_processo("UniNfce.exe"):
    # Se o processo não estiver em execução, exibir a janela com o cronômetro
    exibir_cronometro()

def update_status():
   
    atualizarIP()
   
    servidor = switch_case(tipo_servidor)
   
   

    if server_ip:
        # Se o IP do servidor foi carregado com sucesso
        if check_network_connection(server_ip) == "Conectado":
            status_label.config(text="Conectado ao "+ servidor["descricao"] , foreground="green")
           # icon_label.config(image=connected_icon)
            if check_internet_connection("www.google.com"):
                internet_status_label.config(text="| Conectado à internet |" , foreground="green")
                
            else:
                internet_status_label.config(text="| Desconectado da internet |" , foreground="red")
              
        else:
            status_label.config(text="Desconectado do "+servidor["descricao"], foreground="red")
           # icon_label.config(image=disconnected_icon)
            if check_internet_connection("www.google.com"):
                internet_status_label.config(text="| Conectado à internet |" , foreground="green")
            else:
                internet_status_label.config(text="| Desconectado da internet |", foreground="red")
               
           
    else:
       
        # Se houve algum erro ao carregar o IP do servidor
        status_label.config(text="Erro ao carregar o IP do servidor", foreground="red")

    # Verifica a conexão com a internet
     #   internet_status_label.config(text=check_internet_connection("www.google.com"))

    # Atualiza o nome do computador
    computer_name_label.config(text="|Computador:" + get_computer_name())

    # Atualiza o IP do servidor
    server_ip_label.config(text="|IP do servidor:" + str(server_ip))
    
    # Atualiza o IP local
    local_ip_label.config(text="|Meu ip:" + get_local_ip())
    
    # Atualiza a loja local
    local_filial_label.config(text="|Filial:" + filial )
    
    # Atualiza o IP local
    local_pdv_label.config(text="|PDV:" + pdv )

    
    ocultar_da_lista_alt_tab()
    
    # Agenda a próxima verificação após 60 segundos
    root.after(6000, update_status)

def ocultar_da_lista_alt_tab():
    root.attributes('-toolwindow', True)  # Define a janela como uma ferramenta (sem barra de título)
    root.lift()  # Eleva a janela para a frente
    style = Style()   

    # Define o estilo do ttk para 'alt'
    style.theme_use('alt')
    
    if verificar_processo("UniNfce.exe"):
    # Mostrar a janela
        root.deiconify()
    else:
    # Reiniciar toda a aplicação
       # root.destroy()
        restart_program()
    
      

# Função para converter base64 para imagem e redimensioná-la
def base64_to_resized_base64(base64_string, width, height):
    decoded_data = base64.b64decode(base64_string)
    image = Image.open(BytesIO(decoded_data))
    # Redimensiona a imagem para as dimensões desejadas
    resized_image = image.resize((width, height))
    # Converte a imagem redimensionada para bytes
    with BytesIO() as buffer:
        resized_image.save(buffer, format="PNG")
        resized_image_bytes = buffer.getvalue()
    # Converte os bytes para base64
    resized_base64 = base64.b64encode(resized_image_bytes).decode()
    return resized_base64

# Informe as imagens em base64 aqui
connected_base64 = fundo_base64.connected_base64
disconnected_base64 = fundo_base64.disconnected_base64

# Largura e altura desejadas para as imagens
image_width = 10
image_height = 10

root = Tk()  # Criar a janela principal
# Obter a largura da tela
largura_tela = root.winfo_screenwidth()
root.title("")
root.overrideredirect(True)  # Remove a barra de título da janela
# root.geometry("2000x22+0-1")  # Define a posição da janela 50 pixels acima do rodapé e alinhada à esquerda
# Calcule 90% da largura da tela
nova_largura = int(largura_tela * 100)
root.geometry(f"{nova_largura}x20+0+0")
root.overrideredirect(True) # Ocultar a janela da lista Alt+Tab
root.attributes('-topmost', True)
root.lift()  # Garante que a janela fique acima de todas as outras janelas
# root.wm_attributes("-transparentcolor", "black" )  # Define a cor branca como transparente
root.attributes('-alpha', 1.0)  # Define a opacidade da janela 
root['background'] = 'yellow'
# Defina a cor de fundo
background_color = "#D9D9D9"
# Definir a cor de fundo para todos os widgets ttk


root.configure(bg=background_color)


root.deiconify()
# Convertendo imagens para base64 redimensionadas
connected_base64_resized = base64_to_resized_base64(connected_base64, image_width, image_height)
connected_icon = PhotoImage(data=connected_base64_resized)
disconnected_base64_resized = base64_to_resized_base64(disconnected_base64, image_width, image_height)
disconnected_icon = PhotoImage(data=disconnected_base64_resized)

#icon_label = Label(root, image=connected_icon)
#icon_label.pack(side=LEFT, padx=0)

status_label = Label(root, text="Aguardando...", font=("Calibri", 12))
status_label.pack(side=LEFT, padx=0)

internet_status_label = Label(root, text="", font=("Calibri", 12))
internet_status_label.pack(side=LEFT, padx=0)

# Rótulo para o nome do computador
computer_name_label = Label(root, text="", font=("Calibri", 12))
computer_name_label.pack(side=LEFT, padx=0)

# Rótulo para o IP do servidor
server_ip_label = Label(root, text="", font=("Calibri", 12))
server_ip_label.pack(side=LEFT, padx=0)

# Rótulo para o IP local
local_ip_label = Label(root, text="", font=("Calibri", 12))
local_ip_label.pack(side=LEFT, padx=0)

# Rótulo para o PDV
local_pdv_label = Label(root, text="", font=("Calibri", 12))
local_pdv_label.pack(side=LEFT, padx=0)

# Rótulo para a Loja local
local_filial_label = Label(root, text="", font=("Calibri", 12))
local_filial_label.pack(side=LEFT, padx=0)

# Rótulo para a Hora
label_hora = Label(root, text="", font=("Calibri", 12))

label_hora.pack(side=LEFT,padx="0")

# Inicia a verificação de status
update_status()
atualizar_data_hora()


root.mainloop()

# setx ip_servidor_JJ "endereço_IP_do_servidor"
