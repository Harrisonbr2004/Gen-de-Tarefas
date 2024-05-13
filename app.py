import PySimpleGUI as sg
import json

ARQUIVO_JSON = 'tarefas.json'

tarefas = []

def salvar_tarefas(arquivo):
    with open(arquivo, 'w') as f:
        json.dump(tarefas, f)
        
def carregar_tarefas(arquivo):
    try:
        with open(arquivo, 'r') as f:
            global tarefas
            tarefas = json.load(f)
    except FileNotFoundError:
        pass

carregar_tarefas(ARQUIVO_JSON)

def criar_janela_inicial(): 
    sg.theme('DarkTeal9')
    layout = [
        [sg.Text('Tarefas', font=('Helvetica', 20))],
        [sg.Listbox(values=tarefas, size=(80, 15), key='-LIST-', enable_events=True)],
        [sg.InputText(key='-TAREFA-'), sg.Button('Adicionar', key='-ADICIONAR-'),
         sg.Button('Editar', key='-EDITAR-'), sg.Button('Excluir', key='-EXCLUIR-')],
        [sg.Button('Resetar', key='-RESETAR-'), sg.Button('Salvar', key='-SALVAR-')]
    ]
    return sg.Window('Gen List', layout)
    
janela = criar_janela_inicial()

while True:
    event, values = janela.read()

    if event == sg.WIN_CLOSED:
        break  # Fechar a janela e sair do loop
    
    elif event == '-ADICIONAR-':
        tarefa = values['-TAREFA-'].strip()
        if tarefa:
            tarefas.append(tarefa)
            janela['-LIST-'].update(values=tarefas)
            janela['-TAREFA-'].update('')
            
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

salvar_tarefas(ARQUIVO_JSON)

janela.close()
