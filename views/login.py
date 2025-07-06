import flet as ft


def login_view(page: ft.Page):
    page.title = "Login - HareBlast"
    page.theme = ft.Theme()
    page.theme_mode = ft.ThemeMode.DARK



    mensagem = ft.Text(color=ft.Colors.RED, bgcolor=ft.Colors.WHITE)

    usuario_input = ft.TextField(label="Usuário", color=ft.Colors.WHITE, border_color=ft.Colors.WHITE, width=600)
    senha_input = ft.TextField(label="Senha", password=True, can_reveal_password=True, color=ft.Colors.WHITE, border_color=ft.Colors.WHITE, width=600)

    def autenticar(e):
        usuario = usuario_input.value.strip()
        senha = senha_input.value.strip()
        print(f'{usuario} --- {senha}')
        page.client_storage.set('token', '12345') # Armazenar o token de login para poder usar nas chamadas da API posteriormente


        #logica para poder fazer o login
        '''if not usuario or not senha:
            mensagem.value = "⚠️ Preencha todos os campos."
        elif crud_sql.verificar_login(usuario, senha):
            mensagem.value = ""
            page.client_storage.set("usuario", usuario) 
            page.go("/menu")
        else:
            mensagem.value = "❌ Usuário ou senha incorretos."'''
        
        page.go("/menu") # após implementar o a função de login, retirar esta linha

    login_btn = ft.ElevatedButton("Entrar", on_click=autenticar)

    def page_cadastro(e=None):
        page.go("/cadastro")

    login_container = ft.Column(
        controls=[
            ft.Text("Login", size=30, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
            usuario_input,
            senha_input,
            login_btn,
            ft.TextButton(text='Não tem conta? Cadastre-se', on_click=page_cadastro),
            mensagem
        ],
        spacing=20,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    page.add(
        ft.Container(
            content=login_container,
            alignment=ft.alignment.center,
            expand=True
        )
    )