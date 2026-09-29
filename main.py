import json
import tkinter as tk
from tkinter import messagebox
import os
import sys


# LOCAL DO ARQUIVO DE CHAMADOS
if getattr(sys, "frozen", False):
    PASTA_PROGRAMA = os.path.dirname(sys.executable)
else:
    PASTA_PROGRAMA = os.path.dirname(os.path.abspath(__file__))

ARQUIVO_CHAMADOS = os.path.join(
    PASTA_PROGRAMA,
    "chamados.json"
)


# CORES
FUNDO = "#F2F2F2"
FUNDO_LISTA = "#FFFFFF"
AZUL = "#2563EB"
AMARELO = "#FFD43B"
BRANCO = "#FFFFFF"
CINZA = "#555555"
PRETO = "#222222"


def carregar_chamados():
    try:
        with open(
            ARQUIVO_CHAMADOS,
            "r",
            encoding="utf-8"
        ) as arquivo:
            return json.load(arquivo)

    except FileNotFoundError:
        return []


def salvar_chamados():
    with open(
        ARQUIVO_CHAMADOS,
        "w",
        encoding="utf-8"
    ) as arquivo:

        json.dump(
            chamados,
            arquivo,
            indent=4,
            ensure_ascii=False
        )


def atualizar_lista():
    lista.delete(0, tk.END)

    if len(chamados) == 0:
        lista.insert(
            tk.END,
            "Nenhum chamado cadastrado."
        )
        return

    for chamado in chamados:

        texto = (
            f'#{chamado["id"]} | '
            f'{chamado["titulo"]} | '
            f'{chamado["status"]}'
        )

        lista.insert(
            tk.END,
            texto
        )


def efeito_mouse(botao):

    botao.bind(
        "<Enter>",
        lambda evento: botao.config(
            bg=AMARELO,
            fg=PRETO
        )
    )

    botao.bind(
        "<Leave>",
        lambda evento: botao.config(
            bg=AZUL,
            fg=BRANCO
        )
    )


def efeito_lista(evento):
    lista.config(
        bg="#FFFBEA"
    )


def sair_lista(evento):
    lista.config(
        bg=FUNDO_LISTA
    )


def criar_chamado():

    janela_chamado = tk.Toplevel(janela)

    janela_chamado.title(
        "Novo chamado"
    )

    janela_chamado.geometry(
        "450x350"
    )

    janela_chamado.configure(
        bg=FUNDO
    )

    janela_chamado.resizable(
        False,
        False
    )


    tk.Label(
        janela_chamado,
        text="Título do chamado:",
        bg=FUNDO,
        fg=PRETO,
        font=("Arial", 11, "bold")
    ).pack(
        pady=(20, 5)
    )


    entrada_titulo = tk.Entry(
        janela_chamado,
        width=50
    )

    entrada_titulo.pack()


    tk.Label(
        janela_chamado,
        text="Descrição:",
        bg=FUNDO,
        fg=PRETO,
        font=("Arial", 11, "bold")
    ).pack(
        pady=(15, 5)
    )


    entrada_descricao = tk.Text(
        janela_chamado,
        width=50,
        height=10
    )

    entrada_descricao.pack()


    def salvar_novo_chamado():

        titulo = entrada_titulo.get().strip()

        descricao = entrada_descricao.get(
            "1.0",
            tk.END
        ).strip()


        if not titulo:

            messagebox.showwarning(
                "Atenção",
                "Digite um título."
            )

            return


        if not descricao:

            messagebox.showwarning(
                "Atenção",
                "Digite uma descrição."
            )

            return


        if len(chamados) == 0:

            novo_id = 1

        else:

            novo_id = chamados[-1]["id"] + 1


        chamado = {

            "id": novo_id,

            "titulo": titulo,

            "descricao": descricao,

            "status": "Aberto"

        }


        chamados.append(
            chamado
        )


        salvar_chamados()

        atualizar_lista()


        messagebox.showinfo(
            "Sucesso",
            f"Chamado #{novo_id} criado com sucesso!"
        )


        janela_chamado.destroy()


    botao_criar = tk.Button(

        janela_chamado,

        text="Criar chamado",

        width=20,

        bg=AZUL,

        fg=BRANCO,

        cursor="hand2",

        command=salvar_novo_chamado

    )


    botao_criar.pack(
        pady=15
    )


    efeito_mouse(
        botao_criar
    )


def ver_chamado():

    selecao = lista.curselection()


    if not selecao:

        messagebox.showwarning(
            "Atenção",
            "Selecione um chamado na lista."
        )

        return


    indice = selecao[0]


    if indice >= len(chamados):

        return


    chamado = chamados[indice]


    mensagem = (

        f'ID: #{chamado["id"]}\n\n'

        f'Título: {chamado["titulo"]}\n\n'

        f'Descrição:\n{chamado["descricao"]}\n\n'

        f'Status: {chamado["status"]}'

    )


    messagebox.showinfo(

        "Detalhes do chamado",

        mensagem

    )


def resolver_chamado():

    selecao = lista.curselection()


    if not selecao:

        messagebox.showwarning(

            "Atenção",

            "Selecione um chamado na lista."

        )

        return


    indice = selecao[0]


    if indice >= len(chamados):

        return


    chamado = chamados[indice]


    if chamado["status"] == "Resolvido":

        messagebox.showinfo(

            "HelpFlow",

            "Esse chamado já foi resolvido."

        )

        return


    chamado["status"] = "Resolvido"


    salvar_chamados()

    atualizar_lista()


    messagebox.showinfo(

        "Sucesso",

        f'Chamado #{chamado["id"]} resolvido!'

    )


def excluir_chamado():

    selecao = lista.curselection()


    if not selecao:

        messagebox.showwarning(

            "Atenção",

            "Selecione um chamado na lista."

        )

        return


    indice = selecao[0]


    if indice >= len(chamados):

        return


    chamado = chamados[indice]


    if chamado["status"] != "Resolvido":

        messagebox.showwarning(

            "Não permitido",

            "Só é possível excluir chamados resolvidos."

        )

        return


    confirmacao = messagebox.askyesno(

        "Confirmar exclusão",

        f'Excluir o chamado #{chamado["id"]}?'

    )


    if confirmacao:

        chamados.remove(
            chamado
        )


        salvar_chamados()

        atualizar_lista()


        messagebox.showinfo(

            "Sucesso",

            "Chamado excluído com sucesso!"

        )


# JANELA PRINCIPAL

janela = tk.Tk()


janela.title(
    "HelpFlow"
)


janela.geometry(
    "700x560"
)


janela.configure(
    bg=FUNDO
)


janela.resizable(
    False,
    False
)


# TÍTULO

titulo = tk.Label(

    janela,

    text="HELPFLOW",

    font=("Arial", 28, "bold"),

    bg=FUNDO,

    fg=PRETO

)


titulo.pack(
    pady=(25, 5)
)


# SUBTÍTULO

subtitulo = tk.Label(

    janela,

    text="Sistema de gerenciamento de chamados",

    font=("Arial", 12),

    bg=FUNDO,

    fg=CINZA

)


subtitulo.pack(
    pady=(0, 20)
)


# INSTRUÇÃO

instrucao = tk.Label(

    janela,

    text="Selecione um chamado abaixo:",

    font=("Arial", 11, "bold"),

    bg=FUNDO,

    fg=PRETO

)


instrucao.pack(
    pady=(0, 8)
)


# LISTA

lista = tk.Listbox(

    janela,

    width=75,

    height=12,

    font=("Arial", 11),

    bg=FUNDO_LISTA,

    fg=PRETO,

    selectbackground=AZUL,

    selectforeground=BRANCO,

    relief="solid",

    borderwidth=1,

    cursor="hand2"

)


lista.pack()


lista.bind(
    "<Enter>",
    efeito_lista
)


lista.bind(
    "<Leave>",
    sair_lista
)


# BOTÕES

frame_botoes = tk.Frame(

    janela,

    bg=FUNDO

)


frame_botoes.pack(
    pady=20
)


botao_novo = tk.Button(

    frame_botoes,

    text="Abrir chamado",

    width=18,

    bg=AZUL,

    fg=BRANCO,

    cursor="hand2",

    command=criar_chamado

)


botao_novo.grid(

    row=0,

    column=0,

    padx=5

)


botao_ver = tk.Button(

    frame_botoes,

    text="Ver detalhes",

    width=18,

    bg=AZUL,

    fg=BRANCO,

    cursor="hand2",

    command=ver_chamado

)


botao_ver.grid(

    row=0,

    column=1,

    padx=5

)


botao_resolver = tk.Button(

    frame_botoes,

    text="Resolver",

    width=18,

    bg=AZUL,

    fg=BRANCO,

    cursor="hand2",

    command=resolver_chamado

)


botao_resolver.grid(

    row=0,

    column=2,

    padx=5

)


botao_excluir = tk.Button(

    frame_botoes,

    text="Excluir",

    width=18,

    bg=AZUL,

    fg=BRANCO,

    cursor="hand2",

    command=excluir_chamado

)


botao_excluir.grid(

    row=1,

    column=1,

    pady=10

)


botao_sair = tk.Button(

    janela,

    text="Sair",

    width=20,

    bg=AZUL,

    fg=BRANCO,

    cursor="hand2",

    command=janela.destroy

)


botao_sair.pack()


# EFEITO DOS BOTÕES

efeito_mouse(
    botao_novo
)

efeito_mouse(
    botao_ver
)

efeito_mouse(
    botao_resolver
)

efeito_mouse(
    botao_excluir
)

efeito_mouse(
    botao_sair
)


# RODAPÉ

rodape = tk.Label(

    janela,

    text="Desenvolvido por Anna Jhulie",

    font=("Arial", 9),

    bg=FUNDO,

    fg=CINZA

)


rodape.pack(

    side="bottom",

    pady=10

)


# CARREGAR CHAMADOS

chamados = carregar_chamados()


atualizar_lista()


janela.mainloop()