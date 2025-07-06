import flet as ft
import requests
from assets.resource.function.validacao import validar_cnpj

'''
    OS DADOS ESTÃO SENDO ENVIADOS CORRETAMENTE, SÓ SE FAZ NECESSARIO VALIDAR A PARTE DE PAGAMENTO, PASSANDO OS DADOS DO PLANO SELECIONADO E PROCESSANDO O PAGAMENTO


'''


url_api_cadastrar = "http://localhost:8000/empresa/cadastrar-empresa"

data_empresa = {
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

    def voltar_a_pagina_inicial(e):
        page.go("/")

    def ir_a_pagina_de_login(e):
        page.go("/login")

    frame_cabecalho = ft.Container(
        content=ft.Row(
            controls=[
                ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=voltar_a_pagina_inicial)
            ]
        )
    )


    nome_fantasia = ft.TextField(label='Nome Fantasia')
    razao_social = ft.TextField(label='Razão Social') 
    cnpj = ft.TextField(label='CNPJ', input_filter=ft.InputFilter(regex_string=r"[0-9]", replacement_string=""))
    endereco = ft.TextField(label='Endereço')
    telefone = ft.TextField(label='Telefone ex: (11) 0000 0000')
    email = ft.TextField(label='Email', keyboard_type=ft.KeyboardType.EMAIL, autofill_hints=["email"], autocorrect=False)
    status = 'true'

    def proximo_frame_cadastro_empresa(e):
        print('Entrei aqui { proximo frame cadastro empresa }')
        data_empresa['nome_fantasia'] = nome_fantasia.value
        data_empresa['razao_social'] = razao_social.value
        data_empresa['cnpj'] = cnpj.value
        data_empresa['endereco'] = endereco.value
        data_empresa['telefone'] = telefone.value
        data_empresa['email'] = email.value

        try:
            if validar_cnpj(data_empresa['cnpj']):
                print('cnpj validado')
                frame_cadastro_empresa.height = 90
                content_frame_cadastro.visible = False
                content_cadastro_plano.visible = True
                page.update()
            else:
                print('CNPJ invalido')
                cnpj.color = ft.Colors.RED
                cnpj.border_color = ft.Colors.RED
                page.update()
        except Exception as e:
            print(f'erro ao validar o CNPJ {e}')

        

    
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
            ],
            alignment=ft.MainAxisAlignment.CENTER,  # vertical
            horizontal_alignment=ft.CrossAxisAlignment.CENTER        
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
        print(data_empresa)
        content_cadastro_plano.visible = False
        page.update()

    def check_bronze_change(e):
        checkbox_plano_ouro.visible = not checkbox_plano_ouro.visible
        checkbox_plano_prata.visible = not checkbox_plano_prata.visible
        page.update() 
    
    checkbox_plano_bronze = ft.Checkbox(
        on_change= check_bronze_change
    )

    def check_prata_change(e):
        checkbox_plano_bronze.visible = not checkbox_plano_bronze.visible
        checkbox_plano_ouro.visible = not checkbox_plano_ouro.visible
        page.update()

    checkbox_plano_prata = ft.Checkbox(
        on_change= check_prata_change
    )

    def check_ouro_change(e):
        checkbox_plano_bronze.visible = not checkbox_plano_bronze.visible
        checkbox_plano_prata.visible = not checkbox_plano_prata.visible
        page.update()
    
    checkbox_plano_ouro = ft.Checkbox(
        on_change= check_ouro_change
    )

    content_plano_bronze = ft.Column(
        controls=[
            ft.Text('3 PROMOÇÕES ENVIADAS POR DIA'),
            ft.Text('PERMITIDO FUNCIONAR EM 1 GRUPO'),
            ft.Text('TAXA DE SETUP - R$500')

        ],
        spacing=1,
        alignment=ft.MainAxisAlignment.CENTER,  
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    plano_bronze = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text('Plano Bronze'),
                ft.Text('R$250/mês'),
                content_plano_bronze,
                checkbox_plano_bronze
            ],
            spacing=13,  
            alignment=ft.MainAxisAlignment.CENTER,  
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        border_radius=20,
        bgcolor=ft.Colors.BLUE_GREY_900,
        padding=ft.padding.only(top=10, left=10, right=10, bottom=10)
    )
    
    content_plano_prata = ft.Column(
        controls=[
            ft.Text('5 PROMOÇÕES ENVIADAS POR DIA'),
            ft.Text('PERMITIDO FUNCIONAR EM 2 GRUPOS'),
            ft.Text('TAXA DE SETUP - R$500')

        ],
        spacing=1,
        alignment=ft.MainAxisAlignment.CENTER,  
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    plano_prata = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text('Plano Prata'),
                ft.Text('R$300/mês'),
                content_plano_prata,
                checkbox_plano_prata
            ],
            spacing=13,  
            alignment=ft.MainAxisAlignment.CENTER,  
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        border_radius=20,
        bgcolor=ft.Colors.BLUE_GREY_900,
        padding=ft.padding.only(top=10, left=10, right=10, bottom=10)
    )

    content_plano_ouro = ft.Column(
        controls=[
            ft.Text('10 PROMOÇÕES ENVIADAS POR DIA'),
            ft.Text('PERMITIDO FUNCIONAR EM 3 GRUPOS'),
            ft.Text('TAXA DE SETUP - R$500')

        ],
        spacing=1,
        alignment=ft.MainAxisAlignment.CENTER,  
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        
    )

    plano_ouro = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text('Plano Ouro'),
                ft.Text('R$400/mês'),
                content_plano_ouro,
                checkbox_plano_ouro
            ],
            spacing=13,  
            alignment=ft.MainAxisAlignment.CENTER,  
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        border_radius=20,
        bgcolor=ft.Colors.BLUE_GREY_900,
        padding=ft.padding.only(top=10, left=10, right=10, bottom=10)
    )


    content_cadastro_plano = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        plano_bronze,
                        plano_prata,
                        plano_ouro
                    ],
                    spacing=14,
                    scroll=ft.ScrollMode.AUTO
                ),
                ft.ElevatedButton('Próximo', on_click=proximo_frame_cadastro_plano)
            ],
            spacing=5,
            alignment=ft.MainAxisAlignment.CENTER,  
            horizontal_alignment=ft.CrossAxisAlignment.CENTER 
            
        ),
        visible=False,
        padding=ft.padding.only(top=10)
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
        # try para fazer a requisiçao de cadastro na API e estamos tendo problemas com o Token
        try:
            response = requests.post(url_api_cadastrar, json=data_empresa)
            if response.status_code == 200:
                print(response.status_code)
                print(response.json())

            else:
                print(response.status_code)
        except Exception as e:
            print(f'Erro na hora de enviar dados: {e}')


            
    frame_cadastro_pagamento = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text('Pagamento', size=24, weight=ft.FontWeight.BOLD)
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



    # Centraliza o container na página
    page.add(
        ft.Row(
            controls=[
                ft.Column(
                    controls=[
                            frame_cabecalho,
                            ft.Column(
                                controls=[
                                    frame_cadastro_empresa,
                                    frame_cadastro_Plano,
                                    frame_cadastro_pagamento,
                                    ft.ElevatedButton('Efetuar Cadastro', on_click=cadastrar_empresa),
                                    ft.TextButton(text='Já tem cadastro? Efetue o LOGIN', on_click=ir_a_pagina_de_login)
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,  
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER
                            ),
                        ]
                    )
                ],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
        )
    )


