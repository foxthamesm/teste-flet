import sys
import os
import requests
import flet as ft
from views.landing_page import landing_page_view
from views.login import login_view
from views.cadastro import cadastro_view
from views.menu import menu
from views.produtos import produtos_view
from views.usuarios import usuarios_view




def main(page: ft.Page):
    def route_change(e):
        page.clean()

        if page.route == "/":
            landing_page_view(page)
        elif page.route == "/login":
            login_view(page)
        elif page.route == "/cadastro":
            cadastro_view(page)
        elif page.route == "/menu":
            menu(page)
        elif page.route == "/produtos":
            produtos_view(page)
        elif page.route == "/usuarios":
            usuarios_view(page)
        else:
            page.add(ft.Text("❌ Rota não encontrada."))

    page.on_route_change = route_change
    page.go("/") 

port = int(os.environ.get("PORT", 8080))
ft.app(target=main, view=ft.WEB_BROWSER,upload_dir='assets/uploads', assets_dir='assets')
