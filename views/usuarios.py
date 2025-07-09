import flet as ft
from datetime import datetime


usuarios = [{
            "nome": 'Danylo',
            "email": 'Dalejandropereira@gmail.com',
            "plano": "Basico",
            "data": datetime.now().strftime("%d/%m/%Y"),
            "permissoes": "planos[plano]"
        }]


planos = {
    "Básico": ["Visualizar Conteúdo"],
    "Profissional": ["Visualizar", "Editar"],
    "Premium": ["Visualizar", "Editar", "Administração"]
}

def usuarios_view(page: ft.Page):
    page.title = "Cadastro de Usuários"
    page.scroll = "AUTO"
    
    nome_input = ft.TextField(label="Nome do Usuário", width=300)
    email_input = ft.TextField(label="E-mail/Login", width=300)
    plano_dropdown = ft.Dropdown(
        label="Plano de Assinatura",
        options=[ft.dropdown.Option(p) for p in planos.keys()],
        width=300
    )

    data_label = ft.Text(f"Data de Cadastro: {datetime.now().strftime('%d/%m/%Y')}")
    msg_alert = ft.Text(value="", color=ft.Colors.RED)

    usuarios_list_view = ft.Column()

    def atualizar_lista():
        usuarios_list_view.controls.clear()
        for u in usuarios:
            print(u)
            usuarios_list_view.controls.append(render_usuario(u))
        page.update()

    def cadastrar_usuario(e):
        nome = nome_input.value.strip()
        email = email_input.value.strip().lower()
        plano = plano_dropdown.value

        if not nome or not email or not plano:
            msg_alert.value = "Todos os campos são obrigatórios."
            page.update()
            return

        if any(u['email'] == email for u in usuarios):
            msg_alert.value = "E-mail já cadastrado."
            page.update()
            return

        usuario = {
            "nome": nome,
            "email": email,
            "plano": plano,
            "data": datetime.now().strftime("%d/%m/%Y"),
            "permissoes": planos[plano]
        }
        usuarios.append(usuario)
        msg_alert.value = ""
        nome_input.value = ""
        email_input.value = ""
        plano_dropdown.value = None
        plano_dropdown.label = "Plano de Assinatura"
        atualizar_lista()

    def excluir_usuario(u):
        def confirmar_exclusao(e):
            usuarios.remove(u)
            page.dialog.open = False
            atualizar_lista()

        dialog = ft.AlertDialog(
            title=ft.Text("Confirmar Exclusão"),
            content=ft.Text(f"Tem certeza que deseja excluir o usuário {u['nome']}?"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda _: setattr(page.dialog, "open", False)),
                ft.TextButton("Excluir", on_click=confirmar_exclusao)
            ],
            open=True
        )
        page.dialog = dialog
        page.dialog.open = True
        page.update()

    def editar_usuario(u):
        nome_input.value = u['nome']
        email_input.value = u['email']
        plano_dropdown.value = u['plano']
        usuarios.remove(u)
        if frame_cadastro_usuarios.visible != True:
            frame_cadastro_usuarios.visible = not frame_cadastro_usuarios.visible
            page.update()
        atualizar_lista()

    def render_usuario(u):
        return ft.Container(
            content=
            ft.Column(
                controls=[
                    ft.Text(f"{u['nome']} ({u['email']})"),
                    ft.Text(f"Plano: {u['plano']} | Cadastro: {u['data']}"),
                    ft.Row([
                    ft.IconButton(icon=ft.Icons.EDIT, on_click=lambda e: editar_usuario(u)),
                    ft.IconButton(icon=ft.Icons.DELETE, on_click=lambda e: excluir_usuario(u)),
                    ])
                ]
                
            ),
            padding=20,
            bgcolor='#838383',
            border_radius=20    

                
        )
        

    frame_cadastro_usuarios = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Cadastro de Usuário", size=24, weight="bold"),
                nome_input,
                email_input,
                plano_dropdown,
                data_label,
                ft.ElevatedButton("Cadastrar", on_click=cadastrar_usuario)
            ]
        ),
        visible=False,
        bgcolor='#838383',
        padding=ft.padding.only(top=20, left=20, bottom=20, right=20),
        border_radius=20
    )

    frame_listar_usuarios = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Usuários Cadastrados", size=20),
                usuarios_list_view        
            ]
        ),
        visible=False
    )

    def show_listar_usuarios(e):
        atualizar_lista()
        frame_listar_usuarios.visible = not frame_listar_usuarios.visible
        page.update()

    def show_cadastro_usuarios(e):
        frame_cadastro_usuarios.visible = not frame_cadastro_usuarios.visible
        page.update()

    frame_main_usuarios= ft.Container(
        content=ft.Column(
            controls=[
            ft.Row(
                controls=[
                    ft.ElevatedButton(text='Usuarios', on_click= show_listar_usuarios),
                    ft.ElevatedButton(text='Cadastrar usuarios', on_click= show_cadastro_usuarios)
                ]
            ),
            ft.Container(
                content=ft.Row(
                    controls=[
                        frame_listar_usuarios,
                        frame_cadastro_usuarios
                    ],
                    spacing=100
                )
            )]
        ),
        bgcolor='#151B38',
        border_radius=20,
        padding= ft.padding.only(top=20, left=20)
    )
    
    def show_main_produtos(e):
        page.go("/produtos")

    def show_main_relatorio(e):
        page.go("/relatorio")
    
    def show_main_agendamento(e):
        page.go("/agendamento")

    def show_main_usuarios(e):
        frame_main_usuarios.visible = not frame_main_usuarios.visible
        page.update()

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
            frame_main_usuarios
        ],
        expand=True  # para ocupar a tela toda e permitir scroll
    )
    page.add(layout)

