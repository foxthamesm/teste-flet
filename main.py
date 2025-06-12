import os
import base64
import flet as ft 
from fletcarousel import BasicAnimatedHorizontalCarousel as bc


def main(page: ft.Page):
    page.title = 'Menu'
    page.theme = ft.Theme()
    page.theme_mode = ft.ThemeMode.DARK

    # cadastrar produto
    list_img_to_cadastrar = []
    file_picker = ft.FilePicker()
    page.overlay.append(file_picker)

    img_container = ft.Row(wrap=True, spacing=5)
    frame_images_cadastro = ft.Container(
        content=img_container,
        width=200,
        visible=True
    )

    def on_files_selected(e: ft.FilePickerResultEvent):
        if e.files:
            for f in e.files:
                if len(list_img_to_cadastrar) < 4:
                    file_bytes = f.read_bytes()
                    base64_str = base64.b64encode(file_bytes).decode("utf-8")
                    list_img_to_cadastrar.append(base64_str)
                    img_container.controls.append(ft.Image(src_base64=base64_str, width=100, height=100, fit=ft.ImageFit.COVER))
                    page.update()
    
    file_picker.on_result = on_files_selected

    def add_images_to_cadastrar(e):
        if len(list_img_to_cadastrar) >= 4:
            page.snack_bar = ft.SnackBar(ft.Text('limite de 4 images atingido !'))
            page.snack_bar.open = True
            page.update()
        else:
            file_picker.pick_files(allow_multiple=True, allowed_extensions=["png","jpg", "jpeg"])

    btn_add_img_to_cadastrar = ft.Container(
        content=ft.Icon(name=ft.icons.ADD, size=40),
        width=150,
        height=150,
        bgcolor=ft.colors.GREY_200,
        alignment=ft.alignment.center,
        border_radius=10,
        on_click=add_images_to_cadastrar
    )


    nome_produto_cadastro = ft.TextField(label='Nome do Produto', color='#ffffff')
    Valor_promocional = ft.TextField(label='Valor Promocional', color='#ffffff')
    codigo_produto = ft.TextField(label='Codigo Produto', color='#ffffff')
    
    def mudando_valor_no_dropdown_cadastro(e):
        frequencia_exibicao.value = frequencia_exibicao.value
        page.update()

    frequencia_exibicao = ft.Dropdown(
        label='Frequência de exibição',
        hint_text='Selecione...',
        options=[
            ft.dropdown.Option("Aleatória"),
            ft.dropdown.Option("Agendada"),
            ft.dropdown.Option("Não exibir"),
            ft.dropdown.Option("Obrigatório"),
        ],
        on_change=mudando_valor_no_dropdown_cadastro
    )

    controle_visualizacao = ft.Checkbox(label='Controle de Visualização')

    frame_cadastro_produto = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        btn_add_img_to_cadastrar,
                        ft.Column(
                            controls=[
                                frame_images_cadastro,
                                nome_produto_cadastro,
                                Valor_promocional,
                                codigo_produto,
                                frequencia_exibicao,
                                controle_visualizacao
                            ]
                        )
                    ]
                )
            ]
        ),
        visible=False,
        bgcolor='#838383'
    )

    def show_cadastro(e):
        frame_cadastro_produto.visible = not frame_cadastro_produto.visible
        page.update()

    # BUSCAR PRODUTO < ------------
    def gerar_lista_produtos():
        carrosel = bc(
            page=page,
            items=[
                ft.Image(
                    src="https://picsum.photos/200/300",
                    height=150,
                    fit=ft.ImageFit.CONTAIN,
                ),
            ],
            margin=10,
            border_radius=30
        )

        return ft.Container(
            content=ft.Row(
                controls=[
                    carrosel,
                    ft.Column(
                        controls=[
                            ft.Text('Tênis Nike'),
                            ft.Text('Código Promocional'),
                            ft.Text('Valor Promocional'),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=3
                    ),
                    ft.ElevatedButton('open')
                ],
                alignment=ft.MainAxisAlignment.START,
            ),
            bgcolor='#838383',
            margin=10,
            padding=0,
            width=500,
            border_radius=30
        )

    frame_lista_produtos = ft.Column(
        scroll=ft.ScrollMode.AUTO,
        expand=True
    )

    def buscar_produto(e):
        frame_lista_produtos.controls.clear()
        frame_lista_produtos.controls.append(gerar_lista_produtos())
        frame_lista_produtos.update()

    search_produtos = ft.TextField(label='Pesquisar')

    frame_pesquisa = ft.Container(
        content=ft.Row(
            controls=[
                search_produtos,
                ft.ElevatedButton(icon=ft.icons.SEARCH, text='.', color=ft.colors.WHITE, on_click=buscar_produto)
            ]
        ),
        margin=10
    )
    
    frame_main_produtos = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        frame_pesquisa,
                        ft.ElevatedButton(text='Filtros'),
                        ft.ElevatedButton(text='Add Produto', on_click=show_cadastro)
                    ]
                ),
                frame_lista_produtos,
                frame_cadastro_produto
            ]
        ),
        visible=False,
        bgcolor='#151B38',
        border_radius=30,
        alignment=ft.alignment.center,
        margin=10
    )
    
    def show_main_produtos(e):
        frame_main_produtos.visible = not frame_main_produtos.visible
        page.update()

    # cabeçalho - botões
    lista_buttons = ft.Container(
        content=ft.Row(
            controls=[
                ft.ElevatedButton(text='PRODUTOS', on_click=show_main_produtos, color=ft.colors.WHITE, bgcolor='#222256', width=100, height=37),
                ft.ElevatedButton(text='USUÁRIOS', color=ft.colors.WHITE, bgcolor='#222256', width=100, height=37),
                ft.ElevatedButton(text='CAMPANHAS', color=ft.colors.WHITE, bgcolor='#222256', width=110, height=37),
                ft.ElevatedButton(text='AGENDA', color=ft.colors.WHITE, bgcolor='#222256', width=100, height=37),
                ft.ElevatedButton(text='RELATÓRIOS', color=ft.colors.WHITE, bgcolor='#222256', width=100, height=37),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=50
        ),
        margin=ft.margin.all(30)
    )
    
    layout = ft.Column(
        controls=[
            lista_buttons,
            frame_main_produtos
        ]
    )

    page.add(layout)

port = int(os.environ.get("PORT", 8080))
ft.app(target=main, view=ft.WEB_BROWSER, port=port)