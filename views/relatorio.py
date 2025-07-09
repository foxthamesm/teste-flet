import flet as ft

def relatorio_view(page: ft.Page):
    page.title = "Relatórios e Análises"
    page.scroll = "AUTO"

    header = ft.Text("Relatórios e Análises", size=24, weight="bold")

    # Filtros da aba "Efetividade de Campanhas"
    filtro_envios = ft.Checkbox(label="Nº de Envios", value=True)
    filtro_entrega = ft.Checkbox(label="Taxa de Entrega", value=True)
    filtro_clique = ft.Checkbox(label="Taxa de Clique", value=True)
    filtro_conversao = ft.Checkbox(label="Conversão", value=True)

    search_input = ft.TextField(label="Pesquisar Campanha", width=300)
    tabela_resultado = ft.DataTable(
        columns=[ft.DataColumn(label=ft.Text("Campanha"))],
        rows=[],
        bgcolor='#151B38'
    )

    # Dados simulados
    campanhas = [
        {
            "nome": "Campanha X",
            "envios": "1200",
            "entrega": "98%",
            "clique": "15%",
            "conversao": "3%"
        },
        {
            "nome": "Campanha Y",
            "envios": "800",
            "entrega": "95%",
            "clique": "10%",
            "conversao": "5%"
        },
        {
            "nome": "Campanha Z",
            "envios": "1500",
            "entrega": "99%",
            "clique": "20%",
            "conversao": "7%"
        }
    ]

    def aplicar_filtros(e=None):
        filtro = search_input.value.strip().lower()

        # Define colunas com base nos filtros marcados
        colunas = [ft.DataColumn(label=ft.Text("Campanha"))]
        if filtro_envios.value:
            colunas.append(ft.DataColumn(label=ft.Text("Nº de Envios")))
        if filtro_entrega.value:
            colunas.append(ft.DataColumn(label=ft.Text("Taxa de Entrega")))
        if filtro_clique.value:
            colunas.append(ft.DataColumn(label=ft.Text("Taxa de Clique")))
        if filtro_conversao.value:
            colunas.append(ft.DataColumn(label=ft.Text("Conversão")))

        # Cria as linhas com base nos dados e filtros
        rows = []
        for campanha in campanhas:
            if filtro in campanha["nome"].lower():
                cells = [ft.DataCell(ft.Text(campanha["nome"]))]
                if filtro_envios.value:
                    cells.append(ft.DataCell(ft.Text(campanha["envios"])))
                if filtro_entrega.value:
                    cells.append(ft.DataCell(ft.Text(campanha["entrega"])))
                if filtro_clique.value:
                    cells.append(ft.DataCell(ft.Text(campanha["clique"])))
                if filtro_conversao.value:
                    cells.append(ft.DataCell(ft.Text(campanha["conversao"])))
                rows.append(ft.DataRow(cells=cells))

        tabela_resultado.columns = colunas
        tabela_resultado.rows = rows
        page.update()

    botao_buscar = ft.ElevatedButton("Buscar", on_click=aplicar_filtros)

    filtros = ft.Row([
        filtro_envios,
        filtro_entrega,
        filtro_clique,
        filtro_conversao
    ])

    aba_efetividade = ft.Container(
        content = ft.Column(
            controls=[
                ft.Row([search_input, botao_buscar]),
                filtros,
                tabela_resultado
            ]
        ),
        bgcolor='#151B38'
        )

    # Tabela para aba "Produtos Promovidos"
    produtos_table = ft.DataTable(
        columns=[
            ft.DataColumn(label=ft.Text("Produto")),
            ft.DataColumn(label=ft.Text("Frequência em Campanhas")),
            ft.DataColumn(label=ft.Text("Tipo de Exibição")),
        ],
        rows=[
            ft.DataRow(cells=[
                ft.DataCell(ft.Text("Produto A")),
                ft.DataCell(ft.Text("10x")),
                ft.DataCell(ft.Text("Agendada")),
            ])
        ],
        bgcolor='#151B38'
    )

    # Tabela para aba "Relatório por Usuário"
    usuario_table = ft.DataTable(
        columns=[
            ft.DataColumn(label=ft.Text("Usuário")),
            ft.DataColumn(label=ft.Text("Campanhas Criadas")),
            ft.DataColumn(label=ft.Text("Produtos Cadastrados")),
            ft.DataColumn(label=ft.Text("Atividades Recentes")),
            ft.DataColumn(label=ft.Text("Consumo do Plano")),
        ],
        rows=[
            ft.DataRow(cells=[
                ft.DataCell(ft.Text("usuario_1")),
                ft.DataCell(ft.Text("5")),
                ft.DataCell(ft.Text("20")),
                ft.DataCell(ft.Text("Editou campanha X")),
                ft.DataCell(ft.Text("80%")),
            ])
        ],
        bgcolor='#151B38',
    )

    colum_product_table = ft.Column([produtos_table])
    colum_usuario_table = ft.Column([usuario_table])

    tabs = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        tabs=[
            ft.Tab(text="Efetividade de Campanhas", content=aba_efetividade),
            ft.Tab(text="Produtos Promovidos", content=colum_product_table),
            ft.Tab(text="Relatório por Usuário", content=colum_usuario_table)
        ]
        
    )

    frame_main_relatorio = ft.Container(
        content=ft.Column(
            controls=[
                header,
                tabs
            ]
        ),
        visible=True,
        margin=ft.margin.only(left=20, top=20),


    )


    def show_main_produtos(e):
        page.go("/produtos")

    def show_main_usuarios(e):
        page.go("/usuarios")
    
    def show_main_relatorio(e):
        frame_main_relatorio.visible = not frame_main_relatorio.visible
        page.update()

    def show_main_agendamento(e):
        page.go("/agendamento")


    lista_buttons = ft.Container(
        content=ft.Row(
            controls=[
                ft.ElevatedButton(text='PRODUTOS', on_click=show_main_produtos, color=ft.Colors.WHITE, bgcolor='#222256', width=100, height=37),
                ft.ElevatedButton(text='USUÁRIOS', on_click=show_main_usuarios,color=ft.Colors.WHITE, bgcolor='#222256', width=100, height=37),
                ft.ElevatedButton(text='CAMPANHAS', color=ft.Colors.WHITE, bgcolor='#222256', width=110, height=37),
                ft.ElevatedButton(text='AGENDA', on_click=show_main_agendamento,color=ft.Colors.WHITE, bgcolor='#222256', width=100, height=37),
                ft.ElevatedButton(text='RELATÓRIOS', on_click=show_main_relatorio,color=ft.Colors.WHITE, bgcolor='#222256', width=100, height=37),
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        margin=ft.margin.all(30)
    )


    layout = ft.Column(
        controls=[
            lista_buttons,
            frame_main_relatorio
        ],
        expand=True  # para ocupar a tela toda e permitir scroll
    )

    aplicar_filtros()
    page.add(layout)
  # Mostra os dados na primeira renderização


