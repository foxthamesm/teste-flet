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



def menu(page: ft.Page):
    page.title = 'Menu'
    page.theme = ft.Theme()
    page.theme_mode = ft.ThemeMode.DARK

    def show_main_produtos(e):
        page.go("/produtos")

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
            lista_buttons
        ],
        expand=True  # para ocupar a tela toda e permitir scroll
    )

    page.add(layout)


