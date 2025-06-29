import os
import base64
import flet as ft 
from fletcarousel import BasicAnimatedHorizontalCarousel as bc, HintLine, AutoCycle
import requests

def main(page: ft.Page):
    page.title = 'Menu'
    page.theme = ft.Theme()
    page.theme_mode = ft.ThemeMode.DARK

    link_mostrar_image = ''



    # cadastrar produto
    list_img_to_cadastrar = []
    file_picker = ft.FilePicker()
    page.overlay.append(file_picker)

    img_container = ft.Row(wrap=True, spacing=10, )
    frame_images_cadastro = ft.Container(
        content=img_container,
        width=200,
        visible=True
    )

    def on_files_selected(e: ft.FilePickerResultEvent):
        if e.files:
            for f in e.files:
                if len(list_img_to_cadastrar) < 4:
                    list_img_to_cadastrar.append(f)
                    print('lista criada')                    
                

    def on_upload_event(e: ft.FilePickerUploadEvent):
        print("Entramos na função de UPLOADS")
        print(e)

    file_picker.on_result = on_files_selected
    file_picker.on_upload = on_upload_event



    def add_images_to_cadastrar(e):
        if len(list_img_to_cadastrar) >= 4:
            page.snack_bar = ft.SnackBar(ft.Text('limite de 4 images atingido !'))
            page.snack_bar.open = True
            page.update()
        else:
            file_picker.pick_files(allow_multiple=True, allowed_extensions=["png","jpg", "jpeg"])

    btn_add_img_to_cadastrar = ft.Container(
        content=ft.Icon(name=ft.Icons.ADD, size=40),
        width=150,
        height=150,
        bgcolor=ft.Colors.GREY_200,
        alignment=ft.alignment.center,
        border_radius=10,
        margin=10,
        on_click=add_images_to_cadastrar
    )


    nome_produto_cadastro = ft.TextField(label='Nome do Produto', color='#ffffff')
    descricao_produto_cadastro = ft.TextField(label='Descrição do Produto', color='#ffffff', multiline=True)
    Valor_promocional = ft.TextField(label='Valor Promocional', color='#ffffff') #preço de venda
    codigo_produto = ft.TextField(label='Codigo Produto', color='#ffffff')
    unidade_de_medida = ft.TextField(label='Unidade de Media', color='#ffffff')
    quantidade_estoque = ft.TextField(label='Qntd. Estoque', color='#ffffff')
    link_produto = ft.TextField(label='Link produto', color='#ffffff')

    def cadastrar_produto(e):
        api_url = "https://api-flet.onrender.com/cadastrar_produto/" #Alterar o nome do Endpoint para Cadastrar Images, criar um Endpoint para cadastro Produto
        link_upload = []
        data = {
            'Cnome_produto': nome_produto_cadastro.value,
            'Cdescricao_produto_cadastro':descricao_produto_cadastro.value,
            'CValor_promocional': Valor_promocional.value, 
            'Ccodigo_produto': codigo_produto.value,
            'Cunidade_de_medida': unidade_de_medida.value,
            'Cquantidade_estoque': quantidade_estoque.value,
            'Clink_produto': link_produto.value,
            'Cimages':[]
        }
        
        for f in list_img_to_cadastrar:
            with open(f.path, 'rb') as file_obj:
                print('abriu o path')
                try:
                    files = {'file': (f.name, file_obj, 'application/octet-stream')}
                    response = requests.post(api_url, files=files)
            
                    if response.status_code == 200:
                        dados = response.json()
                        link_upload.append(dados['url'])
                        print(link_upload)
                        print('UPLOAD FEITO')
                    else:
                        print(f'O NOSSO CÓDIGO DE RESPOSTA FOI {response.status_code}')
                except Exception as e:
                    print(f'Erro ao enviar através do Path {e}')
            data['Cimages'] = link_upload
        
    


    frame_cadastro_produto = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                btn_add_img_to_cadastrar,
                                ft.ElevatedButton(text="Cadastrar Produto", on_click=cadastrar_produto)
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                        ft.Column(
                            controls=[
                                frame_images_cadastro,
                                nome_produto_cadastro,
                                descricao_produto_cadastro,
                                Valor_promocional,
                                codigo_produto
                            ]
                        ),
                        ft.Column(
                            controls=[
                                unidade_de_medida,
                                quantidade_estoque,
                                link_produto
                            ]
                        )
                    ]
                )
            ]
        ),
        visible=False,
        bgcolor='#838383',
        border_radius=30,
        width=890,
        margin=0
    )

    def show_cadastro(e):
        frame_cadastro_produto.visible = not frame_cadastro_produto.visible
        page.update()       

    #EDITAR PRODUTO  < ------------
    list_img_to_editar = []

    img_container_edit = ft.Row(wrap=True, spacing=10, )
    frame_images_edit = ft.Container(
        content=img_container_edit,
        width=200,
        visible=True
    )

    def on_files_selected_edit(e: ft.FilePickerResultEvent):
        if e.files:
            for f in e.files:
                if len(list_img_to_editar) < 4:
                    print('em edição')
                    
    
    file_picker.on_result = on_files_selected

    def add_images_to_editar(e):
        if len(list_img_to_editar) >= 4:
            page.snack_bar = ft.SnackBar(ft.Text('limite de 4 images atingido !'))
            page.snack_bar.open = True
            page.update()
        else:
            file_picker.pick_files(allow_multiple=True, allowed_extensions=["png","jpg", "jpeg"])

    btn_add_img_to_editar = ft.Container(
        content=ft.Icon(name=ft.Icons.ADD, size=40),
        width=150,
        height=150,
        bgcolor=ft.Colors.GREY_200,
        alignment=ft.alignment.center,
        border_radius=10,
        margin=10,
        on_click=add_images_to_editar
    )


    nome_produto_editar = ft.TextField(label='Nome do Produto', color='#ffffff')
    Valor_promocional_editar = ft.TextField(label='Valor Promocional', color='#ffffff')
    codigo_produto_editar = ft.TextField(label='Codigo Produto', color='#ffffff')
    
    def mudando_valor_no_dropdown_editar(e):
        frequencia_exibicao_edit.value = frequencia_exibicao_edit.value
        page.update()

    frequencia_exibicao_edit = ft.Dropdown(
        label='Frequência de exibição',
        hint_text='Selecione...',
        options=[
            ft.dropdown.Option("Aleatória"),
            ft.dropdown.Option("Agendada"),
            ft.dropdown.Option("Não exibir"),
            ft.dropdown.Option("Obrigatório"),
        ],
        on_change=mudando_valor_no_dropdown_editar
    )

    controle_visualizacao_edit = ft.Checkbox(label='Controle de Visualização')

    frame_editar_produto = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        btn_add_img_to_editar,
                        ft.Column(
                            controls=[
                                frame_images_edit,
                                nome_produto_editar,
                                Valor_promocional_editar,
                                codigo_produto_editar,
                                frequencia_exibicao_edit,
                                controle_visualizacao_edit
                            ]
                        )
                    ]
                )
            ]
        ),
        visible=False,
        bgcolor='#838383',
        border_radius=30,
        width=500
    )
    
    #função passada dentro do gerar lista produtos
    #NÃO TIRAR A DOCTRING ATÉ TER O DICT/JSON COMO PARAMETRO, POIS VAI GERAR UM ERRO
    def show_editar(e): # data <- data é igual a um dict/json com informação dos atos cadastrados <- add este parametro
        '''frame_images_edit.value = ''
        nome_produto_editar.value = ''
        Valor_promocional_editar.value = ''
        codigo_produto_editar.value = ''
        frequencia_exibicao_edit.value = ''
        controle_visualizacao_edit.value = '''''
        frame_editar_produto.visible = not frame_editar_produto.visible
        page.update()

    # BUSCAR PRODUTO < ------------
    def gerar_lista_produtos():
        carrosel = bc(
            page=page,
            items=[
                ft.Image(
                    src="https://picsum.photos/200/300",
                    height=300,
                    width=300,
                    fit=ft.ImageFit.CONTAIN,
                ),
            ],
            margin=10,
            border_radius=30
        )

        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Row(
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
                            )
                        ],
                        alignment=ft.MainAxisAlignment.START,
                    ),
                    ft.ElevatedButton('open', on_click=show_editar)
                    ],
                    spacing=80
                ),
                    bgcolor='#838383',
                    margin=10,
                    padding=0,
                    width=500,
                    border_radius=30)

    frame_lista_produtos = ft.Column(
        scroll=ft.ScrollMode.AUTO,
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
                ft.ElevatedButton(icon=ft.Icons.SEARCH, text='.', color=ft.Colors.WHITE, on_click=buscar_produto)
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
                ft.Row(
                    controls=[
                        frame_lista_produtos,
                        ft.Column(
                            controls=[
                                frame_cadastro_produto,
                                frame_editar_produto
                            ]
                        )
                    ],
                    alignment=ft.MainAxisAlignment.START

                ),
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
                ft.ElevatedButton(text='PRODUTOS', on_click=show_main_produtos, color=ft.Colors.WHITE, bgcolor='#222256', width=100, height=37),
                ft.ElevatedButton(text='USUÁRIOS', color=ft.Colors.WHITE, bgcolor='#222256', width=100, height=37),
                ft.ElevatedButton(text='CAMPANHAS', color=ft.Colors.WHITE, bgcolor='#222256', width=110, height=37),
                ft.ElevatedButton(text='AGENDA', color=ft.Colors.WHITE, bgcolor='#222256', width=100, height=37),
                ft.ElevatedButton(text='RELATÓRIOS', color=ft.Colors.WHITE, bgcolor='#222256', width=100, height=37),
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
ft.app(target=main, upload_dir='assets/uploads', assets_dir='assets')