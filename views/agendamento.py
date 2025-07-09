import flet as ft
import datetime

# Fake DBs
campanhas_fake_db = [
    {"id": 1, "nome": "Campanha Inverno", "ativa": True},
    {"id": 2, "nome": "Campanha Verão", "ativa": False},
    {"id": 3, "nome": "Campanha de Natal", "ativa": True}
]

templates_fake_db = [
    {"id": 1, "mensagem": "Aproveite nossa promoção especial!"},
    {"id": 2, "mensagem": "Descontos imperdíveis só essa semana!"},
    {"id": 3, "mensagem": "Compre 2 e leve 3! Confira agora!"}
]

produtos_fake_db = [
    {"id": 1, "nome": "Camisa Polo"},
    {"id": 2, "nome": "Calça Jeans"},
    {"id": 3, "nome": "Tênis Esportivo"},
    {"id": 4, "nome": "Jaqueta Corta Vento"},
    {"id": 5, "nome": "Bermuda Praia"},
    {"id": 6, "nome": "Camisa Social"},
    {"id": 7, "nome": "Tênis Casual"},
    {"id": 8, "nome": "Moletom Capuz"},
    {"id": 9, "nome": "Vestido Floral"},
    {"id": 10, "nome": "Blazer Slim"},
]

def agendamento_views(page: ft.Page):
    page.title = "Agendamento de Promoções via WhatsApp"
    page.scroll = ft.ScrollMode.AUTO

    # Campanhas ativas
    campanhas_ativas = [
        ft.dropdown.Option(c["nome"]) for c in campanhas_fake_db if c["ativa"]
    ]
    campanha_dropdown = ft.Dropdown(label="Selecione uma campanha", options=campanhas_ativas, width=400)

    # Campo de mensagem e template
    usar_template_checkbox = ft.Checkbox(label="Usar template de mensagem", value=False)
    mensagem_manual = ft.TextField(label="Escreva uma mensagem", multiline=True, width=400, max_lines=4)
    template_dropdown = ft.Dropdown(
        label="Selecione um template", 
        options=[ft.dropdown.Option(t["mensagem"]) for t in templates_fake_db],
        width=400,
        visible=False
    )

    def alternar_modo_mensagem(e):
        if usar_template_checkbox.value:
            mensagem_manual.visible = False
            template_dropdown.visible = True
        else:
            mensagem_manual.visible = True
            template_dropdown.visible = False
        page.update()

    usar_template_checkbox.on_change = alternar_modo_mensagem

    # Produtos
    checkboxes_produtos = []
    produtos_selecao_column = ft.Column()
    produtos_listview = ft.ListView(
        controls=produtos_selecao_column.controls,
        height=200,
        width=400,
        spacing=5,
        padding=10,
        auto_scroll=False
    )
    produtos_container = ft.Container(content=produtos_listview)

    def render_produtos(lista):
        checkboxes_produtos.clear()
        produtos_selecao_column.controls.clear()
        for produto in lista:
            checkbox = ft.Checkbox(label=produto["nome"], value=False)
            checkboxes_produtos.append(checkbox)
            produtos_selecao_column.controls.append(checkbox)
        produtos_listview.controls = produtos_selecao_column.controls
        page.update()

    render_produtos(produtos_fake_db)

    def filtrar_produtos(e):
        termo = pesquisa_produto.value.lower()
        filtrados = [p for p in produtos_fake_db if termo in p["nome"].lower()]
        render_produtos(filtrados)

    pesquisa_produto = ft.TextField(label="Buscar produto", width=400, on_change=filtrar_produtos)

    # Date & Time Picker
    data_picker = ft.DatePicker()
    hora_picker = ft.TimePicker()

    data_escolhida = ft.Text()
    hora_escolhida = ft.Text()

    def selecionar_data(e):
        page.dialog = data_picker
        data_picker.open = True
        page.update()

    def selecionar_hora(e):
        page.dialog = hora_picker
        hora_picker.open = True
        page.update()

    def data_confirmada(e):
        data_escolhida.value = f"📅 {data_picker.value.strftime('%d/%m/%Y')}"
        page.update()

    def hora_confirmada(e):
        hora_escolhida.value = f"⏰ {hora_picker.value.strftime('%H:%M')}"
        page.update()

    data_picker.on_change = data_confirmada
    hora_picker.on_change = hora_confirmada

    # Lista de agendamentos
    lista_campanhas = ft.Column()

    def agendar_disparo(e):
        nome = campanha_dropdown.value
        mensagem = template_dropdown.value if usar_template_checkbox.value else mensagem_manual.value
        produtos = [c.label for c in checkboxes_produtos if c.value]

        if not (nome and mensagem and data_escolhida.value and hora_escolhida.value and produtos):
            page.snack_bar = ft.SnackBar(ft.Text("Preencha todos os campos obrigatórios!"), open=True)
            page.update()
            return

        campanha_card = ft.Card(
            content=ft.ListTile(
                title=ft.Text(f"📣 {nome}"),
                subtitle=ft.Text(
                    f"{data_escolhida.value} {hora_escolhida.value}\n"
                    f"💬 {mensagem}\n"
                    f"📦 Produtos: {', '.join(produtos)}"
                )
            )
        )
        lista_campanhas.controls.append(campanha_card)

        # Resetar
        campanha_dropdown.value = None
        mensagem_manual.value = ""
        template_dropdown.value = None
        usar_template_checkbox.value = False
        data_escolhida.value = ""
        hora_escolhida.value = ""
        pesquisa_produto.value = ""
        render_produtos(produtos_fake_db)
        alternar_modo_mensagem(None)
        page.update()


    frame_main_agendamento = ft.Container(
        content = ft.Column(
            controls=[
                ft.Text("Agendamento de Promoções", size=24, weight="bold"),
                ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                campanha_dropdown,
                                ft.Text("Mensagem da Promoção", size=18, weight="bold"),
                                usar_template_checkbox,
                                mensagem_manual,
                                template_dropdown,
                                ft.Text("Data e Hora do Disparo", size=18, weight="bold"),
                                ft.Row([
                                    ft.ElevatedButton("Escolher Data", on_click=selecionar_data),
                                    ft.ElevatedButton("Escolher Hora", on_click=selecionar_hora)
                                ]),
                                ft.Row([data_escolhida, hora_escolhida]),

                                ft.ElevatedButton("Agendar Disparo", on_click=agendar_disparo, bgcolor=ft.Colors.GREEN, color=ft.Colors.WHITE),
                            ]
                        ),
                        ft.Column(
                            controls=[
                                ft.Text("Selecione os Produtos", size=18, weight="bold"),
                                pesquisa_produto,
                                produtos_container,   
                            ]
                        )
                        
                    ],
                    spacing=40
                ),
                ft.Divider(),
                ft.Text("Campanhas Agendadas", size=20, weight="bold"),
                lista_campanhas     
            ],
            
        ),
        visible=True,
        bgcolor='#151B38',
        padding=20,
        border_radius=20
    )


    
    def show_main_produtos(e):
        page.go("/produtos")

    def show_main_usuarios(e):
        page.go("/usuarios")
    
    def show_main_relatorio(e):
        page.go("/relatorio")
    
    def show_main_agendamentos(e):
        frame_main_agendamento.visible = not frame_main_agendamento.visible
        page.update()

    lista_buttons = ft.Container(
        content=ft.Row(
            controls=[
                ft.ElevatedButton(text='PRODUTOS', on_click=show_main_produtos, color=ft.Colors.WHITE, bgcolor='#222256', width=100, height=37),
                ft.ElevatedButton(text='USUÁRIOS', on_click=show_main_usuarios,color=ft.Colors.WHITE, bgcolor='#222256', width=100, height=37),
                ft.ElevatedButton(text='CAMPANHAS', color=ft.Colors.WHITE, bgcolor='#222256', width=110, height=37),
                ft.ElevatedButton(text='AGENDA', on_click=show_main_agendamentos,color=ft.Colors.WHITE, bgcolor='#222256', width=100, height=37),
                ft.ElevatedButton(text='RELATÓRIOS', on_click=show_main_relatorio,color=ft.Colors.WHITE, bgcolor='#222256', width=100, height=37),
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        margin=ft.margin.all(30)
    )

    # Montagem da página
    layout = ft.Column(
        controls=[
            lista_buttons,
            frame_main_agendamento
        ],
        expand=True  # para ocupar a tela toda e permitir scroll
    )
    page.add(layout)

    page.overlay.extend([data_picker, hora_picker])

