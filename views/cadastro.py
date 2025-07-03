import flet as ft
import requests

'''

    ESTAMOS TRATANDO OS DADOS DO CNPJ NA FUNÇÃO proximo_frame_cadastro_empresa, COLOCAMOS UM END-POINT DENTRO DE auth LA NA API
    PARA QUE EU POSSA FAZER ESSA VALIDAÇÃO

    TEMOS QUE COLOCAR PARA QUE O CLIENTE POSSA ESCOLHER OS PLANOS QUE ELE QUER UTILIZAR NÃO SEI QUAIS SÃO OS PLANOS

'''


url_api_validar_cnpj = "http://localhost:8000/validar_cnpj/"
url_api_cadastrar = "http://localhost:8000/empresa/cadastrar-empresa/"

data = {
    'nome_fantasia':'',
    'razao_social':'',
    'cnpj':'',
    'endereco':'',
    'telefone':'',
    'email':'',
    'status': True
}

def cadastro_view(page: ft.Page):
    page.title = "Cadastro - HareBlast"
    page.theme = ft.Theme()
    page.theme_mode = ft.ThemeMode.DARK

    nome_fantasia = ft.TextField(label='Nome Fantasia')
    razao_social = ft.TextField(label='Razão Social') 
    cnpj = ft.TextField(label='CNPJ', input_filter=ft.InputFilter(regex_string=r"[0-9]", replacement_string=""))
    endereco = ft.TextField(label='Endereço')
    telefone = ft.TextField(label='Telefone ex: (11) 0000 0000')
    email = ft.TextField(label='Email', keyboard_type=ft.KeyboardType.EMAIL, autofill_hints=["email"], autocorrect=False)
    status = 'true'

    def proximo_frame_cadastro_empresa(e):
        print('Entrei aqui { proximo frame cadastro empresa }')
        data['nome_fantasia'] = nome_fantasia.value
        data['razao_social'] = razao_social.value
        data['cnpj'] = cnpj.value
        data['endereco'] = endereco.value
        data['telefone'] = telefone.value
        data['email'] = email.value

        try:

            payload = {'numero_cnpj': data['cnpj']}
            response = requests.post(url_api_validar_cnpj, json=payload)
            print(response.json())

            frame_cadastro_empresa.height = 90
            content_frame_cadastro.visible = False
            content_cadastro_plano.visible = True
            page.update()

        except Exception as e:
            print(f'Erro na hora de usar a API para validar o CNPJ: {e}')
    
    content_frame_cadastro = ft.Container(
        content=ft.Column(
            controls=[
                nome_fantasia,
                razao_social,
                cnpj,
                endereco,
                telefone,
                email,
                ft.ElevatedButton('Próximo', on_click=proximo_frame_cadastro_empresa)
            ]            
        ),
        visible=True
    )

    frame_cadastro_empresa = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text('Cadastro Empresa', size=24, weight=ft.FontWeight.BOLD),
                content_frame_cadastro
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.CENTER,  # vertical
            horizontal_alignment=ft.CrossAxisAlignment.CENTER  # horizontal
        ),
        border=ft.border.all(1, "white"),
        border_radius=10,
        bgcolor=ft.Colors.TRANSPARENT,
        width=550,
        height=550,
        padding=20
    )

    def proximo_frame_cadastro_plano(e):
        print(data)
        content_cadastro_plano.visible = False
        page.update()

    content_cadastro_plano = ft.Container(
        content=ft.Column(
            controls=[
                ft.ElevatedButton('Próximo', on_click=proximo_frame_cadastro_plano)
            ]
        ),
        visible=False
    )

    frame_cadastro_Plano = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text('Planos', size=24, weight=ft.FontWeight.BOLD),
                content_cadastro_plano
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.CENTER,  # vertical
            horizontal_alignment=ft.CrossAxisAlignment.CENTER  # horizontal
        ),
        border=ft.border.all(1, "white"),
        border_radius=10,
        bgcolor=ft.Colors.TRANSPARENT,
        width=550,
        padding=20
    )


    def cadastrar_empresa(e):
        '''  # try para fazer a requisiçao de cadastro na API e estamos tendo problemas com o Token

        try:
            response = requests.post(url_api_cadastrar, json=data)
            if response.status_code == 200:
                print(response.status_code)
                print(response.json())
            else:
                print(response.status_code)
        except Exception as e:
            print(f'Erro na hora de enviar dados: {e}')
        
        '''
        page.go("/")

    # Centraliza o container na página
    page.add(
        ft.Row(
            controls=[
                ft.Column(
                    controls=[
                            frame_cadastro_empresa,
                            frame_cadastro_Plano,
                            ft.ElevatedButton('Efetuar Cadastro', on_click=cadastrar_empresa)
                    ]
                )
                ],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True
        )
    )


