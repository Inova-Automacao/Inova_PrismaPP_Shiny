
with ui.card(full_screen=True):
    ui.card_header("Relação empresa - transação")

    @render.data_frame
    def tb_empresas_valores():
        return exibe_tabela(df_empresas_valores)

with ui.card(full_screen=True):
    ui.card_header("Empresa e pessoas que mais receberam")

    @render.data_frame
    def tb_maiores_reset():
        return exibe_tabela(df_maiores)

with ui.card(full_screen=True):
    ui.card_header("Empresa e pessoas que mais receberam")

    @render_plotly
    def grafico_barras():
        return exibe_grafico_barras(df_maioresgraf, "Empresa", "Valor")