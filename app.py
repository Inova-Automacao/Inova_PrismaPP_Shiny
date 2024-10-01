from faicons import icon_svg as icon

from shinywidgets import render_plotly, render_widget, output_widget
import plotly.express as px
from shiny import reactive, App, Inputs, Outputs, Session, render, ui, req
from shiny.express import input, ui
import pandas as pd  

from exibicao import (
    exibe_tabela, 
    exibe_grafico_barras, 
    exibe_texto,)

from dados import *
from logica import *

ui.page_opts(title="Análise de transações públicas - São Fidélis")

with ui.nav_panel("Filtros específicos"):  # Primeiro painel de navegação
    with ui.layout_columns(col_widths=[4, 4, 4]):
        with ui.card(full_screen=True):
            ui.card_header("Empresa - Total de transações por ano")
            ui.input_select("ano", "Escolha um ano:", choices=choices_anos)

            @render.data_frame
            def tb_total_ano_escolhido():
                total_ano_escolhido = filtrar_gastos_por_ano(df, str(input.ano()))
                return exibe_tabela(total_ano_escolhido)

        with ui.card(full_screen=True):
            ui.card_header("Empresa - Total de transaçoes por natureza")
            ui.input_select("natureza", "Escolha a natureza do lançamento:", choices=choices_tipo_natureza)

            @render.data_frame
            def tb_total_natureza_escolhida():
                total_natureza_escolhida = calcular_total_por_natureza(df, str(input.natureza()))
                return exibe_tabela(total_natureza_escolhida)

        with ui.card(full_screen=True):
            ui.card_header("Total de transações por CPF/CNPJ")
            ui.input_select("tipopessoa", "Escolha o tipo de pessoa:", choices=choices_tipo_pessoa)

            @render.data_frame
            def tb_total_cpf_cnpj():
                total_cpf_cnpj = calcular_total_por_cpf_cnpj(df, str(input.tipopessoa()))
                return exibe_tabela(total_cpf_cnpj)
    
        with ui.card(full_screen=True):
            ui.card_header("Total de transações por tipo de conta")
            ui.input_select("tipoconta", "Escolha o tipo de conta da transação:", choices=choices_tipo_transacao_conta)

            @render.data_frame
            def tb_transacao_tipo_conta():
                transacao_tipo_conta = filtrar_transacoes_por_tipo(df, str(input.tipoconta()))
                return exibe_tabela(transacao_tipo_conta)

        with ui.card(full_screen=True):
            ui.card_header("Total de transações CNAB")
            ui.input_select("tipocnab", "Escolha o tipo de transação:", choices=cnab_titulos)

            @render.data_frame
            def tb_transacao_tipo_transacao():
                transacao_tipo_transacao = obter_total_transacoes_por_empresa(df, str(input.tipocnab()))
                return exibe_tabela(transacao_tipo_transacao)
            
    
        with ui.card(full_screen=True):
            ui.card_header("Total de transações por lançamento")
            ui.input_select("tipolancamento", "Escolha a empresa:", choices=choices_titular)

            @render.data_frame
            def tb_transacao_tipo_lancamento():
                transacao_tipo_lancamento = filtrar_por_titular(df, str(input.tipolancamento()))
                return exibe_tabela(transacao_tipo_lancamento)

# Segundo painel de navegação
with ui.nav_panel("Filtros gerais"):  
    with ui.layout_columns(col_widths=[4, 4, 4]):
        with ui.card(full_screen=True):
            ui.input_select("tipoconta_", "Escolha o tipo de conta da transação:", choices=choices_tipo_transacao_conta)
            ui.input_select("natureza_", "Escolha a natureza do lançamento:", choices=choices_tipo_natureza)
            ui.input_select("cnab_", "Escolha um cnab:", choices=cnab_titulos)
            
            @render.data_frame
            def tb_geral():
                total_geral = filtrar_transacoes_por_natureza_tipo_conta(df, str(input.natureza_()), str(input.tipoconta_()), str(input.cnab_()))
                return exibe_tabela(total_geral)

            
# Terceiro painel de navegação
with ui.nav_panel("---"):  
    with ui.layout_columns(col_widths=[6, 6, 6]):

        with ui.card(full_screen=True):
            ui.card_header("Total de transações empresa - ano - CNAB")
            ui.input_select("anos", "Escolha um ano:", choices=choices_anos)

            @render_widget  
            def plot(): 

                bar_chart = px.bar(
                    data_frame= top_10_titulares_credito(df, str(input.anos())),
                    x="NOME_TITULAR",
                    y="VALOR_TRANSACAO",
                    title="Total de Transações de Crédito por Titular"
                ).update_layout(
                    title={"text": "Total de Transações por Titular", "x": 0.5},
                    yaxis_title="Valor Total das Transações",
                    xaxis_title="Nome do Titular",
                )

                return bar_chart
                    