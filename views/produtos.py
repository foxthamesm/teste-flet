import os
import shutil
import base64
import flet as ft 
from fletcarousel import BasicAnimatedHorizontalCarousel as bc, HintLine, AutoCycle
import requests

url_api = "http://127.0.0.1:8000"

# esta lista pode ser retirada, estava apenas simulando o recebimento de dados da api, função da linha 744
simulando_dados_recebido_api = [
    {
        "id": '1',
        "nome": 'Hare',
        "descricao": 'Capacete de moto personalizado',
        "codigo_produto": 10002,
        "unidade_medida": "cm",
        "preco_venda": 90,
        "qtd_estoque": 3,
        "link": 'produto.link',
        "url_imagem1": '',
    },
    {
        "id": '1',
        "nome": 'Hare',
        "descricao": 'Capacete de moto personalizado',
        "codigo_produto": 10002,
        "unidade_medida": "cm",
        "preco_venda": 90,
        "qtd_estoque": 3,
        "link": 'produto.link',
        "url_imagem1": '',
    },
    {
        "id": '1',
        "nome": 'Hare',
        "descricao": 'Capacete de moto personalizado',
        "codigo_produto": 10002,
        "unidade_medida": "cm",
        "preco_venda": 90,
        "qtd_estoque": 3,
        "link": 'produto.link',
        "url_imagem1": '',
    },
    {
        "id": '1',
        "nome": 'Hare',
        "descricao": 'Capacete de moto personalizado',
        "codigo_produto": 10002,
        "unidade_medida": "cm",
        "preco_venda": 90,
        "qtd_estoque": 3,
        "link": 'produto.link',
        "url_imagem1": '',
    },]



def produtos_view(page: ft.Page):
    page.title = 'Menu'
    page.theme = ft.Theme()
    page.theme_mode = ft.ThemeMode.DARK


    # cadastrar produto
    list_img_to_cadastrar = []
    file_picker = ft.FilePicker()
    page.overlay.append(file_picker)
    


    list_img_cadastro = ft.Row(controls=[
            
            ],
            scroll=ft.ScrollMode.AUTO
        )

    frame_images_cadastro = ft.Container(
        content=list_img_cadastro,
        width=200,
        visible=True
    )
    list_two = []


    def on_files_selected(e: ft.FilePickerResultEvent):
        if e.files:
            for f in e.files:
                if len(list_img_to_cadastrar) < 1:
                    list_img_to_cadastrar.append(f)
                    link_temporary = page.get_upload_url(f.name, expires=600)
                    list_two.append(ft.FilePickerUploadFile(
                        name=f.name,
                        upload_url=link_temporary
                    ))
                    file_picker.upload(list_two)
                    print('lista criada')                    
                

    def on_upload_event(e: ft.FilePickerUploadEvent):
        if e.progress == 1:
            try:
                file_name = e.file_name
                file_path = f"assets/uploads/{file_name}"

                if not os.path.exists(file_path):
                    print(f"Arquivo não encontrado: {file_path}")
                    return

                with open(file_path, "rb") as img_file:
                    img = base64.b64encode(img_file.read()).decode()

                extension = file_name.split(".", 1)[1].lower()

                img_format = ft.Container()

                def remove_img(ev):
                    # Remove da interface
                    list_img_cadastro.controls.remove(img_format)
                    list_img_cadastro.update()

                    # Remove da lista (opcional)
                    for f in list_img_to_cadastrar:
                        if f.name == file_name:
                            list_img_to_cadastrar.remove(f)
                            break   

                    # Remove o arquivo do sistema
                    try:
                        os.remove(file_path)
                        print(f"Arquivo removido: {file_path}")
                    except Exception as err:
                        print(f"Erro ao deletar o arquivo: {err}")

                img_format.content = ft.Column(
                    controls=[
                        ft.IconButton(icon=ft.Icons.DELETE, on_click=remove_img),
                        ft.Image(
                            src=f'data:image/{extension};base64,{img}',
                            width=100,
                            height=100
                        )
                    ]
                )

                img_format.margin = ft.margin.only(right=10, bottom=10)
                list_img_cadastro.controls.append(img_format)
                list_img_cadastro.update()

            except Exception as err:
                print(f"Erro ao processar imagem: {err}")

    file_picker.on_result = on_files_selected
    file_picker.on_upload = on_upload_event


    def add_images_to_cadastrar(e):
        if len(list_img_to_cadastrar) >= 4:
            page.snack_bar = ft.SnackBar(ft.Text('limite de 1 images atingido !'))
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
    Valor_promocional = ft.TextField(label='Valor Promocional', color='#ffffff') 
    codigo_produto = ft.TextField(label='Codigo Produto', color='#ffffff')


    unidade_de_medida = ft.Dropdown(
        label='Unidade de medida',
        color='#ffffff',
        options=[
            ft.dropdown.Option("kg"),
            ft.dropdown.Option("g"),
            ft.dropdown.Option("mg"),
            ft.dropdown.Option("ton"),
            ft.dropdown.Option("l"),
            ft.dropdown.Option("ml"),
            ft.dropdown.Option("m³"),
            ft.dropdown.Option("cm³"),
            ft.dropdown.Option("m"),
            ft.dropdown.Option("cm"),
            ft.dropdown.Option("mm"),
            ft.dropdown.Option("unidade"),
            ft.dropdown.Option("pacote"),
            ft.dropdown.Option("caixa"),
            ft.dropdown.Option("dúzia"),
        ],
        width=150
        
    )

    quantidade_estoque = ft.TextField(label='Qntd. Estoque', color='#ffffff')
    Link_produto = ft.TextField(label='Link Produto', color='#ffffff')

    def cadastrar_produto(e):
        # api_url_teste = "https://api-flet.onrender.com/cadastrar_produto/" # API render com cadastro no bunnynet 
        api_url_cadastro = f"{url_api}/produto/cadastrar-produto"  # API local Oficial para usar o Projeto

        '''
            A nossa lógica estava sendo enviar as imagens para o bunny e retonar as url em um dict e enviar para a outra api.
            mas vamos mudar, a partir de agora vamos gerar os file dos arquivos e enviar tudo de uma vez para a api oficial do HAREBLAST
            sendo assim ela vai gerar as url e ela mesmo vai cadastrar os dados no banco de dados

            Após colocar o sistema de LOGIN integrado com o banco de dados adicionar o um nome as images antes de prepara-las para o Upload
             ------>>> ex: f"{nome_empresa}_{nome_produto}_*colocar a ordem da imagem na lista (0,1,2,3)* 

            Ainda não testando para fazer o upload Com o APi do Enzo, pois, precisamos do login e do token de autenticação
        '''
        files_upload = []        
        data = {
            'Cnome_produto': nome_produto_cadastro.value,
            'Cdescricao_produto_cadastro':descricao_produto_cadastro.value,
            'CValor_promocional': Valor_promocional.value, 
            'Ccodigo_produto': codigo_produto.value,
            'Cunidade_de_medida': unidade_de_medida.value,
            'Cquantidade_estoque': quantidade_estoque.value,
            'Clink':Link_produto.value,
            'Cimages':[]
        }
        
        for f in list_img_to_cadastrar:
            upload_dir = 'assets/uploads/'
            try:
                with open(f'{upload_dir}{f.name}', 'rb') as f:
                    print('abriu o path')
                    files = {'file': (f.name, f, 'application/octet-stream')}
                    files_upload.append(files)
                    data['Cimages'] = files_upload
            except Exception as e:
                print(f'Erro ao gerar lista com os files ( line: 115 - main.py ): {e}')

        print(data)

        
        try:
            response = requests.post(api_url_cadastro, files=data)
            if response.status_code == 200:
                print('UPLOAD FEITO COM SUCESSO')
            else:
                print(f'Obtivemos um erro no upload (LINE 118 - main.py): {response.status_code}')
        except Exception as e:
            print(f"erro ao enviar os dados para API ( LINE 119 - main.py ): {e}")


        
    frame_cadastro_produto = ft.Container(
        content=ft.Container(
            ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            btn_add_img_to_cadastrar,
                            frame_images_cadastro
                        ]
                    ),
                    nome_produto_cadastro,
                    Valor_promocional,
                    codigo_produto,
                    unidade_de_medida,
                    quantidade_estoque,
                    descricao_produto_cadastro,
                    Link_produto,
                    ft.ElevatedButton(text="Cadastrar", on_click=cadastrar_produto)

                ],
                spacing=7,
            ),
            margin=10
        ),
        visible=False,
        bgcolor='#838383',
        border_radius=30,
        width=600,
        margin=10
    )

    def show_cadastro(e):
        frame_cadastro_produto.visible = not frame_cadastro_produto.visible
        page.update()       

    # EDITAR PRODUTO

    list_img_to_editarr = []
    file_picker_editar = ft.FilePicker()
    page.overlay.append(file_picker_editar)
    


    list_img_editar = ft.Row(controls=[
            
            ],
            scroll=ft.ScrollMode.AUTO
        )

    frame_images_editar = ft.Container(
        content=list_img_editar,
        width=200,
        visible=True
    )
    list_two_editar = []


    def on_files_selected(e: ft.FilePickerResultEvent):
        if e.files:
            for f in e.files:
                if len(list_img_to_editarr) < 1:
                    list_img_to_editarr.append(f)
                    link_temporary_editar = page.get_upload_url(f.name, expires=600)
                    list_two_editar.append(ft.FilePickerUploadFile(
                        name=f.name,
                        upload_url=link_temporary_editar
                    ))
                    file_picker.upload(list_two_editar)
                    print('lista criada')                    
                

    def on_upload_event(e: ft.FilePickerUploadEvent):
        if e.progress == 1:
            try:
                file_name = e.file_name
                file_path = f"assets/uploads/{file_name}"

                if not os.path.exists(file_path):
                    print(f"Arquivo não encontrado: {file_path}")
                    return

                with open(file_path, "rb") as img_file:
                    img = base64.b64encode(img_file.read()).decode()

                extension = file_name.split(".", 1)[1].lower()

                img_format = ft.Container()

                def remove_img(ev):
                    # Remove da interface
                    list_img_editar.controls.remove(img_format)
                    list_img_editar.update()

                    # Remove da lista (opcional)
                    for f in list_img_to_editarr:
                        if f.name == file_name:
                            list_img_to_editarr.remove(f)
                            break   

                    # Remove o arquivo do sistema
                    try:
                        os.remove(file_path)
                        print(f"Arquivo removido: {file_path}")
                    except Exception as err:
                        print(f"Erro ao deletar o arquivo: {err}")

                img_format.content = ft.Column(
                    controls=[
                        ft.IconButton(icon=ft.Icons.DELETE, on_click=remove_img),
                        ft.Image(
                            src=f'data:image/{extension};base64,{img}',
                            width=100,
                            height=100
                        )
                    ]
                )

                img_format.margin = ft.margin.only(right=10, bottom=10)
                list_img_editar.controls.append(img_format)
                list_img_editar.update()

            except Exception as err:
                print(f"Erro ao processar imagem: {err}")

    file_picker.on_result = on_files_selected
    file_picker.on_upload = on_upload_event


    def add_images_to_editar(e):
        if len(list_img_to_editarr) >= 4:
            page.snack_bar = ft.SnackBar(ft.Text('limite de 1 images atingido !'))
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
    descricao_produto_editar = ft.TextField(label='Descrição do Produto', color='#ffffff', multiline=True)
    Valor_promocional_editar = ft.TextField(label='Valor Promocional', color='#ffffff') 
    codigo_produto_editar = ft.TextField(label='Codigo Produto', color='#ffffff')


    unidade_de_medida_editar = ft.Dropdown(
        label='Unidade de medida',
        color='#ffffff',
        options=[
            ft.dropdown.Option("kg"),
            ft.dropdown.Option("g"),
            ft.dropdown.Option("mg"),
            ft.dropdown.Option("ton"),
            ft.dropdown.Option("l"),
            ft.dropdown.Option("ml"),
            ft.dropdown.Option("m³"),
            ft.dropdown.Option("cm³"),
            ft.dropdown.Option("m"),
            ft.dropdown.Option("cm"),
            ft.dropdown.Option("mm"),
            ft.dropdown.Option("unidade"),
            ft.dropdown.Option("pacote"),
            ft.dropdown.Option("caixa"),
            ft.dropdown.Option("dúzia"),
        ],
        width=150
        
    )

    quantidade_estoque_editar = ft.TextField(label='Qntd. Estoque', color='#ffffff')
    Link_produto_editar = ft.TextField(label='Link Produto', color='#ffffff')

    def editar_produto(e):
        api_url_editar = f"{url_api}/produto/"  # API local Oficial para usar o Projeto

        '''
            temos que fazer a conexão com a API do Enzo, essa parte eu não fiz 
        '''
        files_upload = []        
        data = {
            'Cnome_produto': nome_produto_editar.value,
            'Cdescricao_produto_cadastro':descricao_produto_editar.value,
            'CValor_promocional': Valor_promocional_editar.value, 
            'Ccodigo_produto': codigo_produto_editar.value,
            'Cunidade_de_medida': unidade_de_medida_editar.value,
            'Cquantidade_estoque': quantidade_estoque_editar.value,
            'Clink':Link_produto_editar.value,
            'Cimages':[]
        }
        
        for f in list_img_to_cadastrar:
            upload_dir = 'assets/uploads/'
            try:
                with open(f'{upload_dir}{f.name}', 'rb') as f:
                    print('abriu o path')
                    files = {'file': (f.name, f, 'application/octet-stream')}
                    files_upload.append(files)
                    data['Cimages'] = files_upload
            except Exception as e:
                print(f'Erro ao gerar lista com os files ( line: 115 - main.py ): {e}')

        print(data)

        # Essa função vai retonar um erro, tem que alterar o link da API
        try:
            response = requests.post('', files=data)
            if response.status_code == 200:
                print('UPLOAD FEITO COM SUCESSO')
            else:
                print(f'Obtivemos um erro no upload (LINE 118 - main.py): {response.status_code}')
        except Exception as e:
            print(f"erro ao enviar os dados para API ( LINE 119 - main.py ): {e}")


        
    frame_editar_produto = ft.Container(
        content=ft.Container(
            ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            btn_add_img_to_editar,
                            frame_images_editar
                        ]
                    ),
                    nome_produto_editar,
                    Valor_promocional_editar,
                    codigo_produto_editar,
                    unidade_de_medida_editar,
                    quantidade_estoque_editar,
                    descricao_produto_editar,
                    Link_produto_editar,
                    ft.ElevatedButton(text="Editar", on_click=editar_produto)

                ],
                spacing=7,
            ),
            margin=10
        ),
        visible=False,
        bgcolor='#838383',
        border_radius=30,
        width=600,
        margin=10
    )

    def limpar_pasta(caminho_pasta):
        for item in os.listdir(caminho_pasta):
            caminho_item = os.path.join(caminho_pasta, item)
            if os.path.isfile(caminho_item) or os.path.islink(caminho_item):
                os.remove(caminho_item)
            elif os.path.isdir(caminho_item):
                shutil.rmtree(caminho_item)
    
    def show_editar(e, data):
        nome_produto_editar.value = data['nome']
        Valor_promocional_editar.value = data['preco_venda']
        codigo_produto_editar.value = data['codigo_produto']
        unidade_de_medida_editar.value = data['unidade_medida']
        quantidade_estoque_editar.value = data['qtd_estoque']
        Link_produto_editar.value = data['link']

        file_path = data['url_imagem1']

        if not os.path.exists(file_path):
            print(f"Arquivo não encontrado: {file_path}")
            return

        with open(file_path, "rb") as img_file:
            img = base64.b64encode(img_file.read()).decode()

        extension = data['url_imagem1'].split(".", 1)[1].lower()

        img_format = ft.Container()

        def remove_img(ev):
            # Remove da interface
            list_img_editar.controls.remove(img_format)
            list_img_editar.update()

            # Remove da lista (opcional)
            for f in list_img_to_editarr:
                if f.name == data['url_imagem1']:
                    list_img_to_editarr.remove(f)
                    break   

            # Remove o arquivo do sistema
            try:
                os.remove(file_path)
                print(f"Arquivo removido: {file_path}")
            except Exception as err:
                print(f"Erro ao deletar o arquivo: {err}")

        img_format.content = ft.Column(
            controls=[
                ft.IconButton(icon=ft.Icons.DELETE, on_click=remove_img),
                ft.Image(
                    src=f'data:image/{extension};base64,{img}',
                    width=100,
                    height=100
                )
            ]
        )

        img_format.margin = ft.margin.only(right=10, bottom=10)
        list_img_editar.controls.append(img_format)
        list_img_editar.update()


        frame_editar_produto.visible = not frame_editar_produto.visible
        page.update()
        


    # BUSCAR PRODUTO < ------------
    def gerar_lista_produtos(data_list_product: dict):
        with open(data_list_product['url_imagem1'], 'rb') as img:
            img64_edit = base64.b64encode(img.read()).decode()
            extension = data_list_product['url_imagem1'].split(".", 1)[1].lower()
            print(f'extensão para buscar o produto {extension}')
        carrosel = bc(
            page=page,
            items=[
                ft.Image(
                    src=f'data:image/{extension};base64,{img64_edit}',
                    height=200,
                    width=200,
                    fit=ft.ImageFit.CONTAIN,
                ),
            ],
            margin=ft.margin.only(top=3),
            border_radius=40
        )

        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Row(
                        controls=[
                            carrosel,
                            ft.Column(
                                controls=[
                                    ft.Text(f"Nome: {data_list_product['nome']}    Cod. {data_list_product['codigo_produto']}"),
                                    ft.Text(f"Descrição: {data_list_product['descricao']}"),
                                    ft.Text(f"Valor: {data_list_product['preco_venda']}"),
                                    ft.Text(f"qntd. estoque: {data_list_product['qtd_estoque']}"),
                                    ft.ElevatedButton('open', on_click= lambda e: show_editar(e, data_list_product))
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                spacing=1,
                                
                            )
                        ],
                        alignment=ft.MainAxisAlignment.START,
                    )
                    ]
                ),
                bgcolor='#838383',
                margin=ft.margin.only(left=5, right=5),
                width=500,
                border_radius=30
                )

    frame_lista_produtos = ft.Column(
        scroll=ft.ScrollMode.AUTO,
    )
    
    search_produtos = ft.TextField(label='Pesquisar (ID)')

    unidade_de_medida_settings_filter = ft.Dropdown(
        label='Unidade de medida',
        color='#ffffff',
        options=[
            ft.dropdown.Option("kg"),
            ft.dropdown.Option("g"),
            ft.dropdown.Option("mg"),
            ft.dropdown.Option("ton"),
            ft.dropdown.Option("l"),
            ft.dropdown.Option("ml"),
            ft.dropdown.Option("m³"),
            ft.dropdown.Option("cm³"),
            ft.dropdown.Option("m"),
            ft.dropdown.Option("cm"),
            ft.dropdown.Option("mm"),
            ft.dropdown.Option("unidade"),
            ft.dropdown.Option("pacote"),
            ft.dropdown.Option("caixa"),
            ft.dropdown.Option("dúzia"),
        ],
        width=200
    )


    data_settings_filter = {
        'status':'default',
        'unidade_de_medida':unidade_de_medida_settings_filter.value,
        'ordem alfabética':'',
        'ordem numerica':'',
        'Quantidade':''
    }

    def btnbox_settings_filter_ordem_alfabetica():
        checkbox_settings_filter_ordem_numerica.visible = not checkbox_settings_filter_ordem_numerica.visible
        checkbox_settings_filter_quantidade.visible = not checkbox_settings_filter_quantidade.visible

        data_settings_filter['ordem alfabética'] = checkbox_settings_filter_ordem_alfabetica.value
        page.update()
    
    checkbox_settings_filter_ordem_alfabetica = ft.Checkbox(on_change=btnbox_settings_filter_ordem_alfabetica)
    
    def btnbox_settings_filter_ordem_numerica():
        checkbox_settings_filter_ordem_alfabetica.visible = not checkbox_settings_filter_ordem_alfabetica.visible
        checkbox_settings_filter_quantidade.visible = not checkbox_settings_filter_quantidade.visible

        data_settings_filter['ordem numerica'] = checkbox_settings_filter_ordem_numerica.value
        page.update()
    
    checkbox_settings_filter_ordem_numerica = ft.Checkbox(on_change=btnbox_settings_filter_ordem_numerica)
    
    def btnbox_settings_filter_quantidade():
        checkbox_settings_filter_ordem_numerica.visible = not checkbox_settings_filter_ordem_numerica.visible
        checkbox_settings_filter_ordem_alfabetica.visible = not checkbox_settings_filter_ordem_alfabetica.visible

        data_settings_filter['Quantidade'] = checkbox_settings_filter_quantidade.value
        page.update()

    checkbox_settings_filter_quantidade = ft.Checkbox(on_change=btnbox_settings_filter_quantidade)

    def fechar_popup_settings_filter(e):
        popup_settings_filter.open = False
        page.update()

    popup_settings_filter = ft.AlertDialog(
        content=ft.Column(
            controls=[
                ft.Text('FIltros'),
                unidade_de_medida_settings_filter,
                ft.Row(
                    controls=[
                        checkbox_settings_filter_ordem_alfabetica,
                        ft.Text('Ordem Alfabética')
                        
                    ]
                ),
                ft.Row(
                    controls=[
                        checkbox_settings_filter_ordem_numerica,
                        ft.Text('Ordem Numérica')
                    ]
                ),
                ft.Row(
                    controls=[
                        checkbox_settings_filter_quantidade,
                        ft.Text('Ordenar por Quantidade de estoque')
                    ]
                )
            ],
            spacing=10,
            height=400
        ),
        actions=[
            ft.TextButton(text='Fechar', on_click=fechar_popup_settings_filter)
        ],
        visible=False
    )

    page.add(popup_settings_filter)
    popup_settings_filter.open = True
    page.update()

    def show_settings_filter(e):
        popup_settings_filter.open = True
        popup_settings_filter.visible = not popup_settings_filter.visible
        page.update()

    def buscar_produto(e):
        frame_lista_produtos.controls.clear()
        try:
            print(page.client_storage.get('token'))
            if search_produtos.value:
                print('not null search')
                response = requests.get(f"{url_api}/produto/buscar-produto/{search_produtos.value}", params={'usuario_atual': page.client_storage.get('token')})
                print(response.status_code)
                print(response.json().get('status'))
                if data_settings_filter['status'] == 'default':
                    frame_lista_produtos.controls.append(gerar_lista_produtos(response.json().get('produtos')))
                    frame_lista_produtos.update()
                else:
                    list_produtos_search_produtos = simulando_dados_recebido_api #response.json().get('produtos')


                    if data_settings_filter['unidade_de_medida'] != '':
                        for i in list_produtos_search_produtos:
                            if i['unidade_medida'] == data_settings_filter['unidade_de_medida']:
                                frame_lista_produtos.controls.append(gerar_lista_produtos(i))
                    
                    if data_settings_filter['ordem alfabética'] != '':
                        produtos_ordenados = sorted(list_produtos_search_produtos, key=lambda x: x['nome'])

                        for produto in produtos_ordenados:
                            frame_lista_produtos.controls.append(gerar_lista_produtos(produto))
                    if data_settings_filter['ordem numerica'] != '':
                        produtos_ordenados = sorted(list_produtos_search_produtos, key=lambda x: x['id'])

                        for produto in produtos_ordenados:
                            frame_lista_produtos.controls.append(gerar_lista_produtos(produto))
                    
                    if data_settings_filter['Quantidade'] != '':
                        for i in list_produtos_search_produtos:
                            if str(i['qtd_estoque']) == str(data_settings_filter['Quantidade']):
                                frame_lista_produtos.controls.append(gerar_lista_produtos(i))
            else:
                print(f'Listar todos os produtos')
                try:
                    #response = requests.get(f"{url_api}/produto/listar-produtos", params={'usuario_atual': page.client_storage.get('token')})
                    #print(response.status_code)
                    #print(response.json().get('status'))
                    for i in simulando_dados_recebido_api:
                        frame_lista_produtos.controls.append(gerar_lista_produtos(i)) #response.json().get('produtos')
                        frame_lista_produtos.update()
                except Exception as e:
                    print(f'erro ao listar todos os produtos: {e}')
        except Exception as e:
            print('obtivemos um erro ao recuperar o token')

    
    frame_pesquisa = ft.Container(
        content=ft.Row(
            controls=[
                search_produtos,
                ft.IconButton(icon=ft.Icons.SEARCH, on_click=buscar_produto)
            ]
        ),
        margin=10
    )

    frame_manipular_produtos = ft.Column(
        controls=[
            ft.Row(
                    controls=[
                        frame_lista_produtos,
                        ft.Container(
                            content=ft.Row(
                                controls=[
                                    frame_cadastro_produto,
                                    frame_editar_produto
                                ]
                            )
                        )
                    ],
                    alignment=ft.MainAxisAlignment.START
                )
        ],
        scroll=ft.ScrollMode.AUTO,  # scroll ativado aqui
        expand=True  # faz o Column crescer dentro do Container
    )
    
    frame_main_produtos = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        frame_pesquisa,
                        ft.ElevatedButton(text='Filtros', on_click=show_settings_filter),
                        ft.ElevatedButton(text='Add Produto', on_click=show_cadastro)
                    ]
                ),
                frame_manipular_produtos
            ]
        ),
        visible=True,
        bgcolor='#151B38',
        border_radius=30,
        alignment=ft.alignment.center,
        margin=10,
        expand=True  # faz o Container crescer dentro do layout
    )
    
    def show_main_produtos(e):
        frame_main_produtos.visible = not frame_main_produtos.visible
        page.update()


    def show_main_usuarios(e):
        page.go("/usuarios")
    

    # cabeçalho - botões
    lista_buttons = ft.Container(
        content=ft.Row(
            controls=[
                ft.ElevatedButton(text='PRODUTOS', on_click=show_main_produtos, color=ft.Colors.WHITE, bgcolor='#222256', width=100, height=37),
                ft.ElevatedButton(text='USUÁRIOS', on_click=show_main_usuarios,color=ft.Colors.WHITE, bgcolor='#222256', width=100, height=37),
                ft.ElevatedButton(text='CAMPANHAS', color=ft.Colors.WHITE, bgcolor='#222256', width=110, height=37),
                ft.ElevatedButton(text='AGENDA', color=ft.Colors.WHITE, bgcolor='#222256', width=100, height=37),
                ft.ElevatedButton(text='RELATÓRIOS', color=ft.Colors.WHITE, bgcolor='#222256', width=100, height=37),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        margin=ft.margin.all(30)
    )
    
    layout = ft.Column(
        controls=[
            lista_buttons,
            frame_main_produtos
        ],
        expand=True  # para ocupar a tela toda e permitir scroll
    )

    page.add(layout)


