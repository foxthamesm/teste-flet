import flet as ft
import base64

def landing_page_view(page: ft.Page):
    page.title = 'HareBlast'
    page.theme = ft.Theme()
    page.theme_mode = ft.ThemeMode.DARK

    with open("assets/resource/img/Logo-HareBlast-White.png", "rb") as img_file_white:
        b64_HareBlast_White = base64.b64encode(img_file_white.read()).decode()
    
    with open("assets/resource/img/Logo-HareBlast-Blue-Expand.png", "rb") as img_file_blue:
        b64_HareBlast_Blue = base64.b64encode(img_file_blue.read()).decode()

    def go_to_register(e):
        page.go("/cadastro")
    
    def go_to_login(e):
        page.go("/login")



    options_nav_bar = ft.Row(
        controls=[
            ft.TextButton(text='Home'),
            ft.TextButton(text='Quem somos'),
            ft.TextButton(text='Planos')
        ],
        spacing=10
    )

    options_logins = ft.Row(
        controls=[
            ft.ElevatedButton('Cadastre-se', on_click=go_to_register),
            ft.TextButton(text='Login', on_click=go_to_login)
        ]
    )

    frame_nav_bar = ft.Container(
        content=ft.Row(
            controls=[
                ft.Image(src=f'data:image/png;base64,{b64_HareBlast_White}'), # '/assets/resource/...'
                options_nav_bar,
                options_logins

            ],
            spacing=660
        ),
        margin=10
        
    )

    frame_section_1 = ft.Container(
        content=ft.Row(
            controls=[
                ft.Image(src=f'data:image/png;base64,{b64_HareBlast_Blue}')
            ]
        )
    )

    layout = ft.Column(
        controls=[
            frame_nav_bar,
            frame_section_1
        ]
    )

    page.add(layout)
