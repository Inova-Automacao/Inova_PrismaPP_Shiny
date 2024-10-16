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

with ui.nav_panel("CNAB"):
    with ui.layout_columns(col_widths=[4, 4, 4]):

        with ui.card(full_screen=True):
            ui.card_header("CNAB")
            ui.input_select("tipocnab", "Escolha o tipo de transação e veja o total transacionado por empresa:", choices=cnab_titulos)

            @render.data_frame
            def tb_transacao_tipo_transacao():
                transacao_tipo_transacao = obter_total_transacoes_por_empresa(df, str(input.tipocnab()))
                return exibe_tabela(transacao_tipo_transacao)

            ui.input_select("empresa", "Escolha a empresa e veja o total transacionado em cada CNAB:", choices=choices_empresa)

            @render.data_frame
            def tb_transacao_cnab_empresa():
                transacao_cnab_empresa = top_5_cnabs_empresa(df, str(input.empresa()))
                return exibe_tabela(transacao_cnab_empresa)

        with ui.card(full_screen=True):
            ui.card_header("Top 10 EMPRESAS - CNAB")
            ui.input_select("cnab_escolha", "Escolha o CNAB:", choices=cnab_titulos)

            @render.data_frame
            def tb_transacao_cnab_escolha():
                tb_transacao_cnab_escolha = exibir_top_cnabs_ou_empresas(df, str(input.cnab_escolha()))
                return exibe_tabela(tb_transacao_cnab_escolha)
        
        with ui.card(full_screen=True):
            ui.card_header("Top 10 TITULARES - CNAB")
            ui.input_select("cnab_escolha_tit", "Escolha o CNA:", choices=cnab_titulos)

            @render.data_frame
            def tb_transacao_cnab_escolha_tit():
                tb_transacao_cnab_escolha_tit = exibir_top_cnabs_ou_titular(df, str(input.cnab_escolha_tit()))
                return exibe_tabela(tb_transacao_cnab_escolha_tit)




with ui.nav_panel("Empresa - Titular"): 
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

    with ui.layout_columns(col_widths=[6, 6, 6]):

        with ui.card(full_screen=True):
            ui.card_header("Total de transações por tipo de conta")
            ui.input_select("tipoconta", "Escolha o tipo de conta da transação:", choices=choices_tipo_transacao_conta)

            @render.data_frame
            def tb_transacao_tipo_conta():
                transacao_tipo_conta = filtrar_transacoes_por_tipo(df, str(input.tipoconta()))
                return exibe_tabela(transacao_tipo_conta)

        with ui.card(full_screen=True):
            ui.card_header("Total de transações por lançamento")
            ui.input_select("tipolancamento", "Escolha a empresa:", choices=choices_titular)

            @render.data_frame
            def tb_transacao_tipo_lancamento():
                transacao_tipo_lancamento = filtrar_por_titular(df, str(input.tipolancamento()))
                return exibe_tabela(transacao_tipo_lancamento)
            
            


# Terceiro painel de navegação
with ui.nav_panel("Gráficos"):  
    with ui.layout_columns(col_widths=[6,6,6]):

        with ui.card(full_screen=True):
            ui.card_header("Total de transações empresa - ano - Crédito")
            ui.input_select("ano_c", "Escolha um ano:", choices=choices_anos)

            @render_widget  
            def plot_C(): 

                fig = px.bar(
                    data_frame= top_10_titulares_natureza(df, str(input.ano_c()),'C'),
                    x='VALOR_TRANSACAO',
                    y='NOME_TITULAR',
                    text='VALOR_TRANSACAO',
                    orientation='h',
                    title="Total de Transações de CRÉDITO por Titular"
                )
                fig.update_layout(
                    yaxis={'categoryorder':'total ascending'},  # Garante que as barras sejam ordenadas corretamente
                    xaxis_title="Valor Total das Transações",
                    yaxis_title="Nome do Titular",
                    margin=dict(l=200, r=50, t=50, b=50),  # Ajuste das margens para dar mais espaço aos textos
                    height=400,  # Altura do gráfico para maior visibilidade
                )
                fig.update_traces(
                    texttemplate='%{text:,.2f}',  # Aplicar o formato com separador de milhar diretamente nos valores do gráfico
                    textposition='auto',
                    textfont_size=12
                )
                return fig
            
        with ui.card(full_screen=True):
            ui.card_header("Total de transações empresa - ano - Débito")
            ui.input_select("ano_d", "Escolha um ano:", choices=choices_anos)

            @render_widget  
            def plot_D(): 
                df_top_10 = top_10_titulares_natureza(df, str(input.ano_d()),'D')
                fig = px.bar(
                    data_frame= df_top_10,
                    x='VALOR_TRANSACAO',
                    y='NOME_TITULAR',
                    text='VALOR_TRANSACAO',
                    orientation='h',
                    title="Total de Transações de DÉBITO por Titular"
                )
                fig.update_layout(
                    yaxis={'categoryorder':'total ascending'},  # Garante que as barras sejam ordenadas corretamente
                    xaxis_title="Valor Total das Transações",
                    yaxis_title="Nome do Titular",
                    margin=dict(l=200, r=50, t=50, b=50),  # Ajuste das margens para dar mais espaço aos textos
                    xaxis_range=[0, df_top_10['VALOR_TRANSACAO'].max() * 1.1],
                )
                fig.update_traces(
                    texttemplate='%{text:,.2f}',  # Aplicar o formato com separador de milhar diretamente nos valores do gráfico
                    textposition='auto',
                    textfont_size=12
                )
                return fig


        with ui.card(full_screen=True):
            ui.card_header("Total de transações EMPRESA - ano - CNAB")
            ui.input_select("ano_cnab_emp", "Escolha um ano:", choices=choices_anos)

            @render.data_frame
            def tb_transacao_cnab_recorrente_emp():
                transacao_cnab_recorrente = empresas_top_por_cnab_empresa(df, str(input.ano_cnab_emp()),obter_choices_cnab_recorrente(df))
                return exibe_tabela(transacao_cnab_recorrente)

            @render_widget  
            def plot_EMP_CNAB(): 
                df_top_10 = empresas_top_por_cnab_empresa(df, str(input.ano_cnab_emp()),obter_choices_cnab_recorrente(df))
                fig = px.bar(
                    data_frame= df_top_10,
                    x='QUANTIDADE_TRANSACOES',
                    y='CNAB',
                    text='QUANTIDADE_TRANSACOES',
                    orientation='h',
                    title="Total de Transações por CNAB - EMPRESA"
                )
                fig.update_layout(
                    yaxis={'categoryorder':'total ascending'},  # Garante que as barras sejam ordenadas corretamente
                    xaxis_title="Quantidade de transações",
                    yaxis_title="CNAB",
                    margin=dict(l=200, r=50, t=50, b=50),  # Ajuste das margens para dar mais espaço aos textos
                    xaxis_range=[0, df_top_10['VALOR_TRANSACAO'].max() * 2],
                )
                fig.update_traces(
                    textposition='auto',
                    textfont_size=12
                )
        
                return fig

        with ui.card(full_screen=True):
            ui.card_header("Total de transações TITULAR - ano - CNAB")
            ui.input_select("ano_cnab_tit", "Escolha um ano:", choices=choices_anos)

            @render.data_frame
            def tb_transacao_cnab_recorrente_tit():
                transacao_cnab_recorrente = empresas_top_por_cnab_titular(df, str(input.ano_cnab_tit()),obter_choices_cnab_recorrente(df))
                return exibe_tabela(transacao_cnab_recorrente)

            @render_widget  
            def plot_TIT_CNAB(): 
                df_top_10 = empresas_top_por_cnab_titular(df, str(input.ano_cnab_tit()),obter_choices_cnab_recorrente(df))
                fig = px.bar(
                    data_frame= df_top_10,
                    x='QUANTIDADE_TRANSACOES',
                    y='CNAB',
                    text='QUANTIDADE_TRANSACOES',
                    orientation='h',
                    title="Total de Transações por CNAB - TITULAR"
                )
                fig.update_layout(
                    yaxis={'categoryorder':'total ascending'},  # Garante que as barras sejam ordenadas corretamente
                    xaxis_title="Quantidade de transações",
                    yaxis_title="CNAB",
                    margin=dict(l=200, r=50, t=50, b=50),  # Ajuste das margens para dar mais espaço aos textos
                    xaxis_range=[0, df_top_10['VALOR_TRANSACAO'].max() * 2],
                )
                fig.update_traces(
                    textposition='auto',
                    textfont_size=12
                )
        
                return fig
        


# Segundo painel de navegação
with ui.nav_panel("Filtros conjuntos"):  
    with ui.layout_columns(col_widths=[4, 4, 4]):
        with ui.card(full_screen=True):
            ui.input_select("tipoconta_", "Escolha o tipo de conta da transação:", choices=choices_tipo_transacao_conta)
        with ui.card(full_screen=True):
            ui.input_select("natureza_", "Escolha a natureza do lançamento:", choices=choices_tipo_natureza)
        with ui.card(full_screen=True):
            ui.input_select("cnab_", "Escolha um cnab:", choices=cnab_titulos)
            
    with ui.card(full_screen=True):
        @render.data_frame
        def tb_geral():
            total_geral = filtrar_transacoes_por_natureza_tipo_conta(df, str(input.natureza_()), str(input.tipoconta_()), str(input.cnab_()))
            return exibe_tabela(total_geral)