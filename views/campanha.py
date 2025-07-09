import flet as ft
from datetime import date


"""
    CORRIGIR: a parte de selecionar as data que eu fiquei cansado e nao consigo mais racioncinar em nada 

    Falar com o Enzo e ver se ele nao consegue colocar API dele para rodar via NGROK para que eu possa fazer as integrações, pois as telas já estão prontas, mas estãos seguindo
    o documento pdf que foi me mandando da primeira vez



"""




def main(page: ft.Page):
    page.title = "Cadastro de Campanha Promocional"
    page.scroll = ft.ScrollMode.AUTO
    page.theme_mode = ft.ThemeMode.LIGHT

    campanhas = []  # Lista mock (para substituir por dados do banco)

    # === CAMPOS DE CADASTRO ===
    nome_campanha = ft.TextField(label="Nome da Campanha", width=400)

    data_inicio = ft.DatePicker()
    data_fim = ft.DatePicker()

    produtos_selecionados = ft.Dropdown(
        label="Produtos Promocionais",
        options=[
            ft.dropdown.Option("Produto A"),
            ft.dropdown.Option("Produto B"),
            ft.dropdown.Option("Produto C"),
        ],
        width=300
    )

    valor_promocional = ft.TextField(label="Valor Promocional", width=200)

    # === Validação para datas ===
    def validar_datas(e):
        if data_inicio.value and data_fim.value:
            if data_fim.value < data_inicio.value:
                page.snack_bar = ft.SnackBar(
                    ft.Text("Data fim não pode ser menor que data início", color="white"),
                    bgcolor="red"
                )
                page.snack_bar.open = True
                page.update()

    data_inicio.on_change = validar_datas
    data_fim.on_change = validar_datas

    # === AÇÕES ===
    def cadastrar_campanha(e):
        if not nome_campanha.value or not data_inicio.value or not data_fim.value or not produtos_selecionados.value:
            page.snack_bar = ft.SnackBar(
                ft.Text("Preencha todos os campos obrigatórios!", color="white"),
                bgcolor="red"
            )
            page.snack_bar.open = True
            page.update()
            return
        if data_fim.value < data_inicio.value:
            page.snack_bar = ft.SnackBar(
                ft.Text("Data fim não pode ser menor que data início", color="white"),
                bgcolor="red"
            )
            page.snack_bar.open = True
            page.update()
            return

        nova = {
            "nome": nome_campanha.value,
            "inicio": data_inicio.value,
            "fim": data_fim.value,
            "produto": produtos_selecionados.value,
            "valor": valor_promocional.value,
        }

        campanhas.append(nova)
        atualizar_lista()
        limpar_campos()
        page.snack_bar = ft.SnackBar(
            ft.Text("Campanha cadastrada com sucesso!", color="white"),
            bgcolor="green"
        )
        page.snack_bar.open = True
        page.update()

    def limpar_campos():
        nome_campanha.value = ""
        data_inicio.value = None
        data_fim.value = None
        produtos_selecionados.value = None
        valor_promocional.value = ""
        page.update()

    def excluir_campanha(index):
        def confirmar_exclusao(e):
            campanhas.pop(index)
            atualizar_lista()
            dialog.open = False
            page.update()

        def cancelar_exclusao(e):
            dialog.open = False
            page.update()

        dialog = ft.AlertDialog(
            title=ft.Text("Confirmar Exclusão"),
            content=ft.Text("Tem certeza que deseja excluir esta campanha?"),
            actions=[
                ft.TextButton("Cancelar", on_click=cancelar_exclusao),
                ft.TextButton("Confirmar", on_click=confirmar_exclusao),
            ],
        )
        page.dialog = dialog
        dialog.open = True
        page.update()

    # === LISTAGEM ===
    lista_campanhas = ft.Column()

    def atualizar_lista():
        lista_campanhas.controls.clear()
        for index, c in enumerate(campanhas):
            lista_campanhas.controls.append(
                ft.Card(
                    content=ft.ListTile(
                        title=ft.Text(c["nome"]),
                        subtitle=ft.Text(f'{c["inicio"]} até {c["fim"]} - Produto: {c["produto"]}'),
                        trailing=ft.Row(
                            controls=[
                                ft.IconButton(icon=ft.icons.EDIT),
                                ft.IconButton(
                                    icon=ft.icons.DELETE,
                                    on_click=lambda e, i=index: excluir_campanha(i)
                                ),
                            ]
                        )
                    )
                )
            )
        page.update()

    # === LAYOUT ===
    page.add(
        ft.Column([
            ft.Text("Cadastro de Campanha", size=24, weight="bold"),
            nome_campanha,
            ft.Row([
                ft.Column([
                    ft.Text("Data Início"),
                    data_inicio,
                ]),
                ft.Column([
                    ft.Text("Data Fim"),
                    data_fim,
                ]),
            ]),
            produtos_selecionados,
            valor_promocional,
            ft.Row([
                ft.ElevatedButton("Cadastrar Campanha", on_click=cadastrar_campanha),
                ft.OutlinedButton("Limpar Campos", on_click=limpar_campos),
            ]),
            ft.Divider(),
            ft.Text("Campanhas Cadastradas", size=20),
            lista_campanhas
        ])
    )

ft.app(target=main)
