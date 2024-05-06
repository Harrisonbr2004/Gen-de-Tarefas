import PySimpleGUI as sg
import json

# Nome do arquivo JSON para salvar as tarefas
ARQUIVO_JSON = 'tarefas.json'

# Lista de tarefas inicial
tarefas = []

# Função para salvar tarefas
def salvar_tarefas(arquivo):
    
    # Salva a lista de tarefas em um arquivo JSON.

    with open(arquivo, 'w') as f:
        json.dump(tarefas, f)

# Função para carregar tarefas
def carregar_tarefas(arquivo):
    
    #Carrega a lista de tarefas de um arquivo JSON.
    
    try:
        with open(arquivo, 'r') as f:
            global tarefas  # Declare a variável global
            tarefas = json.load(f)
    except FileNotFoundError:
        pass  # Ignore o erro se o arquivo não existir

# Carregar tarefas ao iniciar o código
carregar_tarefas(ARQUIVO_JSON)

# Função para criar a janela inicial
def criar_janela_inicial():
    
    #Cria e retorna a janela principal da aplicação.
    
    sg.theme('DarkTeal9')
    layout = [
        [sg.Text('Tarefas', font=('Helvetica', 20))],
        [sg.Listbox(values=tarefas, size=(80, 15), key='-LIST-', enable_events=True)],
        [sg.InputText(key='-TAREFA-'), sg.Button('Adicionar', key='-ADICIONAR-'),
         sg.Button('Editar', key='-EDITAR-'), sg.Button('Excluir', key='-EXCLUIR-')],
        [sg.Button('Resetar', key='-RESETAR-'), sg.Button('Salvar', key='-SALVAR-')]
    ]
    return sg.Window('Gen List', layout)

# Criar a janela principal
janela = criar_janela_inicial()

# Loop de eventos da janela
while True:
    event, values = janela.read()

    # Verificar o tipo de evento
    if event == sg.WIN_CLOSED:
        break  # Fechar a janela e sair do loop
    
    elif event == '-ADICIONAR-':
        tarefa = values['-TAREFA-'].strip()
        if tarefa:
            tarefas.append(tarefa)
            janela['-LIST-'].update(values=tarefas)
            janela['-TAREFA-'].update('')  # Limpar campo de entrada
            
    elif event == '-EDITAR-':
        index = values['-LIST-'][0] if values['-LIST-'] else None
        if index is not None:
            index = tarefas.index(index)
            nova_tarefa = sg.popup_get_text('Editar Tarefa', default_text=tarefas[index])
            if nova_tarefa.strip():
                tarefas[index] = nova_tarefa
                janela['-LIST-'].update(values=tarefas)

    elif event == '-EXCLUIR-':
        index = values['-LIST-'][0] if values['-LIST-'] else None
        if index is not None:
            index = tarefas.index(index)
            if sg.popup_yes_no('Tem certeza que deseja excluir esta tarefa?') == 'Yes':
                del tarefas[index]
                janela['-LIST-'].update(values=tarefas)

    elif event == '-RESETAR-':
        janela.close()
        tarefas = []
        janela = criar_janela_inicial()
    elif event == '-SALVAR-':
        salvar_tarefas(ARQUIVO_JSON)

# Salvar tarefas antes de fechar a janela
salvar_tarefas(ARQUIVO_JSON)

# Fechar a janela principal
janela.close()
