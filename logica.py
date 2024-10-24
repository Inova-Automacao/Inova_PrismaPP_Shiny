from dados import *
import pandas as pd
import plotly.express as px

# Retorna um dataframe com as transações feitas por cada empresa
def consulta(nome): 

    df_valor = df_valor_total[df_valor_total['Empresa'] == nome]

    df_transacoes = df_empresas_valores[df_empresas_valores['NOME_PESSOA_OD'] == nome]

    total_transacoes = df_transacoes.shape[0]

    valor_total = df_valor['Valor'].values[0] if not df_valor.empty else 0

    resultado = pd.DataFrame({
        'Empresa': [nome],
        'Valor': [valor_total],
        'Total de Transações': [total_transacoes]
    })

    return resultado

# Retorna um dataframe com o total transacionado por cada empresa no ano escolhido
def filtrar_gastos_por_ano(df, ano_escolhido):

    df['DATA_LANCAMENTO'] = pd.to_datetime(df['DATA_LANCAMENTO'], format='%Y-%m-%dT%H:%M:%S.%f')
  
    df_filtrado = df[df['DATA_LANCAMENTO'].dt.year == int(ano_escolhido)]
   
    df_total_gastos = df_filtrado.groupby('NOME_PESSOA_OD')['VALOR_TRANSACAO'].sum().reset_index()

    df_total_gastos = df_total_gastos.sort_values(by='VALOR_TRANSACAO', ascending=False)

    df_total_gastos['VALOR_TRANSACAO'] = df_total_gastos['VALOR_TRANSACAO'].apply(lambda x: "{:,.2f}".format(x))

    df_total_gastos.columns = ['Empresa', 'Total transacionado - Ano']
    
    return df_total_gastos

# Retorna um dataframe com o total transacionado por cada empresa na natureza escolhida
def calcular_total_por_natureza(df, tipo):

    natureza_mapeada = 'D' if tipo == 'Débito' else 'C'
    
    df_filtrado = df[df['NATUREZA_LANCAMENTO'] == natureza_mapeada]

    resultado = df_filtrado.groupby('NOME_PESSOA_OD')['VALOR_TRANSACAO'].sum().reset_index()

    resultado.rename(columns={'VALOR_TRANSACAO': 'TOTAL_GASTO'}, inplace=True)

    resultado.sort_values(by='TOTAL_GASTO', ascending=False, inplace=True)

    resultado['TOTAL_GASTO'] = resultado['TOTAL_GASTO'].apply(lambda x: f"{x:,.2f}")

    resultado.columns = ['Empresa', 'Total transacionado - Natureza']

    return resultado

# Formata o CPF e o CNPJ para uma exibição mais clara
def formatar_cpf_cnpj(cpf_cnpj, tipo):
    if tipo == 'CPF':
        return f"{cpf_cnpj[:3]}.{cpf_cnpj[3:6]}.{cpf_cnpj[6:9]}-{cpf_cnpj[9:]}"
    elif tipo == 'CNPJ':
        return f"{cpf_cnpj[:2]}.{cpf_cnpj[2:5]}.{cpf_cnpj[5:8]}/{cpf_cnpj[8:12]}-{cpf_cnpj[12:]}"
    return cpf_cnpj

# Retorna um dataframe com o total transacionado pelo CPF ou CNPJ
def calcular_total_por_cpf_cnpj(df, tipo):

    df['CPF_CNPJ_OD'] = df['CPF_CNPJ_OD'].astype(str)

    if tipo == 'CPF':
        df_filtrado = df[df['CPF_CNPJ_OD'].str.len() == 11]  # CPFs têm 11 dígitos
    elif tipo == 'CNPJ':  
        df_filtrado = df[df['CPF_CNPJ_OD'].str.len() == 14]  # CNPJs têm 14 dígitos
    else:
        df_filtrado = df[(df['CPF_CNPJ_OD'] == 'nan') | (df['CPF_CNPJ_OD'].isna())]

    resultado = df_filtrado.groupby('CPF_CNPJ_OD')['VALOR_TRANSACAO'].sum().reset_index()

    resultado.rename(columns={'VALOR_TRANSACAO': 'TOTAL_GASTO'}, inplace=True)

    resultado.sort_values(by='TOTAL_GASTO', ascending=False, inplace=True)

    resultado['TOTAL_GASTO'] = resultado['TOTAL_GASTO'].apply(lambda x: f"{x:,.2f}")

    resultado['CPF_CNPJ_OD'] = resultado['CPF_CNPJ_OD'].apply(lambda x: formatar_cpf_cnpj(x, tipo))

    resultado.columns = ['CPF/CNPJ', 'Total transacionado']

    return resultado

# Retorna um dataframe com o total gasto por tarnsações em contas publicas e privadas
def filtrar_transacoes_por_tipo(df, tipo_transacao):

    contas_privadas = df['NOME_TITULAR'].unique()

    if tipo_transacao == "Transações com contas privadas":
        df_filtrado = df[~df['NOME_PESSOA_OD'].isin(contas_privadas)]
    elif tipo_transacao == "Transações entre contas públicas":
        df_filtrado = df[df['NOME_PESSOA_OD'].isin(contas_privadas)]

    df_agrupado = df_filtrado.groupby('NOME_PESSOA_OD')['VALOR_TRANSACAO'].sum().reset_index()

    df_agrupado.columns = ['Nome Conta', 'Total transacionado']

    df_agrupado = df_agrupado.sort_values(by='Total transacionado', ascending=False)

    df_agrupado['Total transacionado'] = df_agrupado['Total transacionado'].astype(float).map('{:,.2f}'.format)
    
    return df_agrupado

# Retornar um DataFrame com o total de transações para cada empresa, baseado em um tipo específico de CNAB
def obter_total_transacoes_por_empresa(df, titulo_cnab):

    if titulo_cnab not in cnab_titulos:
        raise ValueError("Título do CNAB não encontrado.")
 
    numero_cnab = cnab_numeros[cnab_titulos.index(titulo_cnab)]

    df_filtrado = df[df['CNAB'] == numero_cnab]

    if df_filtrado.empty:
 
        return pd.DataFrame({
            'NOME_PESSOA_OD': ['Nenhuma transação encontrada'],
            'TOTAL_TRANSACOES': [0]
        })

    resultado = df_filtrado.groupby('NOME_PESSOA_OD')['VALOR_TRANSACAO'].sum().reset_index()
 
    resultado = resultado.sort_values(by='VALOR_TRANSACAO', ascending=False)

    resultado['VALOR_TRANSACAO'] = resultado['VALOR_TRANSACAO'].astype(float).map('{:,.2f}'.format)

    resultado.columns = ['Empresa', 'Total transacionado - CNAB']

    return resultado

# Retorna um DataFrame com o total de transações agrupadas por tipo de lançamento para um titular específico.
def filtrar_por_titular(df, nome_titular):

    df_filtrado = df[df['NOME_TITULAR'] == nome_titular]
 
    resultado = df_filtrado.groupby('DESCRICAO_LANCAMENTO', as_index=False)['VALOR_TRANSACAO'].sum()

    resultado = resultado.sort_values(by='VALOR_TRANSACAO', ascending=False)

    resultado['VALOR_TRANSACAO'] = resultado['VALOR_TRANSACAO'].astype(float).map('{:,.2f}'.format)

    resultado.columns = ['Lançamento', 'Total transacionado - lançamento']
    
    return resultado

# Retorna um DataFrame com as transações filtradas por débito ou crédito, tipo de conta e código CNAB, organizadas por valor de transação
def filtrar_transacoes_por_natureza_tipo_conta(df, natureza_lancamento, tipo_conta, cnab):

    contas_privadas = df['NOME_TITULAR'].unique()
 
    if tipo_conta == "Transações com contas privadas":
        df_filtrado = df[~df['NOME_PESSOA_OD'].isin(contas_privadas)]
    elif tipo_conta == "Transações entre contas públicas":
        df_filtrado = df[df['NOME_PESSOA_OD'].isin(contas_privadas)]

    if natureza_lancamento == 'Débito':
        natureza_mapeada = 'D' 
    else:
        natureza_mapeada = 'C'

    df_filtrado = df_filtrado[df_filtrado['NATUREZA_LANCAMENTO'] == natureza_mapeada]

    numero_cnab = cnab_numeros[cnab_titulos.index(cnab)]
    
    if numero_cnab != 0:
        df_filtrado = df_filtrado[df_filtrado['CNAB'] == numero_cnab]

    df_resultado = df_filtrado[['NOME_TITULAR', 'NOME_PESSOA_OD', 'CPF_CNPJ_OD', 'CNAB', 'VALOR_TRANSACAO', 'DATA_LANCAMENTO','NATUREZA_LANCAMENTO']]

    df_resultado = df_resultado.sort_values(by='VALOR_TRANSACAO', ascending=False)

    df_resultado['DATA_LANCAMENTO'] = pd.to_datetime(df_resultado['DATA_LANCAMENTO']).dt.strftime('%d/%m/%Y')

    df_resultado['VALOR_TRANSACAO'] = df_resultado['VALOR_TRANSACAO'].astype(float).map('{:,.2f}'.format)

    return df_resultado

# Retorna um DataFrame com os 10 titulares que realizaram as maiores transações de um determinado tipo de lançamento, filtradas por ano.
def top_10_titulares_natureza(df, ano, natureza):

    df['DATA_LANCAMENTO'] = pd.to_datetime(df['DATA_LANCAMENTO'], format='%Y-%m-%dT%H:%M:%S.%f')

    df_filtered = df[df['DATA_LANCAMENTO'].dt.year == int(ano)]

    df_credito = df_filtered[df_filtered['NATUREZA_LANCAMENTO'] == natureza]
    
    df_top_10 = df_credito.groupby('NOME_TITULAR')['VALOR_TRANSACAO'].sum().reset_index()

    df_top_10 = df_top_10.sort_values(by='VALOR_TRANSACAO', ascending=False).head(10)

    return df_top_10


# Função para obter o total de transações para uma empresa por CNAB
def top_5_cnabs_empresa(df,empresa):
    cnabs_desconsiderados = [203, 106, 102, 113]

    df_filtrado = df[
        (df['NOME_PESSOA_OD'] == empresa) &
        (~df['CNAB'].isin(cnabs_desconsiderados))
    ]

    df_filtrado['VALOR_TRANSACAO'] = pd.to_numeric(df_filtrado['VALOR_TRANSACAO'], errors='coerce')

    df_filtrado = df_filtrado.dropna(subset=['VALOR_TRANSACAO'])
 
    df_agrupado = df_filtrado.groupby('CNAB')['VALOR_TRANSACAO'].sum().reset_index()

    df_agrupado['VALOR_TRANSACAO'] = df_agrupado['VALOR_TRANSACAO'].astype(float).map('{:,.2f}'.format)

    df_agrupado = df_agrupado.sort_values(by='VALOR_TRANSACAO', ascending=False).head(5)
    
    return df_agrupado
    
# Retorna um DataFrame que mostra as empresas com o maior valor de transações para cada tipo de CNAB em um determinado ano
def empresas_top_por_cnab_empresa(df, ano, choices_cnab_recorrente):
    df['DATA_LANCAMENTO'] = pd.to_datetime(df['DATA_LANCAMENTO'], format='%Y-%m-%dT%H:%M:%S.%f')

    df_ano = df[df['DATA_LANCAMENTO'].dt.year == int(ano)]

    df_filtrado = df_ano[df_ano['CNAB'].isin(choices_cnab_recorrente)]

    transacoes = df_filtrado.groupby(['CNAB', 'NOME_PESSOA_OD']).agg(
        VALOR_TRANSACAO=('VALOR_TRANSACAO', 'sum'),  # Soma o valor transacionado
        QUANTIDADE_TRANSACOES=('VALOR_TRANSACAO', 'size')  # Conta o número de transações
    ).reset_index()

    idx = transacoes.groupby('CNAB')['VALOR_TRANSACAO'].idxmax()
    resultado_final = transacoes.loc[idx].reset_index(drop=True)

    resultado_final = resultado_final.sort_values(by='QUANTIDADE_TRANSACOES', ascending=False).reset_index(drop=True)

    resultado_final['VALOR_TRANSACAO'] = resultado_final['VALOR_TRANSACAO'].astype(float).map('{:,.2f}'.format)

    resultado_final['CNAB'] = resultado_final['CNAB'].astype(str)

    return resultado_final[['CNAB', 'QUANTIDADE_TRANSACOES', 'NOME_PESSOA_OD', 'VALOR_TRANSACAO']]

# Retorna um DataFrame que exibe os titulares com as maiores transações para cada tipo de CNAB em um determinado ano
def empresas_top_por_cnab_titular(df, ano, choices_cnab_recorrente):

    df['DATA_LANCAMENTO'] = pd.to_datetime(df['DATA_LANCAMENTO'], format='%Y-%m-%dT%H:%M:%S.%f')

    df_ano = df[df['DATA_LANCAMENTO'].dt.year == int(ano)]
    print(df_ano)

    df_filtrado = df_ano[df_ano['CNAB'].isin(choices_cnab_recorrente)]

    transacoes = df_filtrado.groupby(['CNAB', 'NOME_TITULAR']).agg(
        VALOR_TRANSACAO=('VALOR_TRANSACAO', 'sum'),  # Soma o valor transacionado
        QUANTIDADE_TRANSACOES=('VALOR_TRANSACAO', 'size')  # Conta o número de transações
    ).reset_index()

    idx = transacoes.groupby('CNAB')['VALOR_TRANSACAO'].idxmax()
    resultado_final = transacoes.loc[idx].reset_index(drop=True)
    resultado_final = resultado_final.sort_values(by='QUANTIDADE_TRANSACOES', ascending=False).reset_index(drop=True)

    resultado_final['VALOR_TRANSACAO'] = resultado_final['VALOR_TRANSACAO'].astype(float).map('{:,.2f}'.format)

    resultado_final['CNAB'] = resultado_final['CNAB'].astype(str)

    return resultado_final[['CNAB', 'QUANTIDADE_TRANSACOES', 'NOME_TITULAR', 'VALOR_TRANSACAO']]

# Retorna um DataFrame com as principais empresas e os valores de transações com base no tipo de CNAB selecionado ou em uma lista de tipos recorrentes de CNAB
def exibir_top_cnabs_ou_empresas(df, selecionado):

    numero_cnab = cnab_numeros[cnab_titulos.index(selecionado)]

    if numero_cnab == 0:
        df_filtrado = df[df['CNAB'].isin(obter_choices_cnab_recorrente(df))]

        top_empresas = df_filtrado.groupby('NOME_PESSOA_OD').agg(
            VALOR_TOTAL_TRANSACOES=('VALOR_TRANSACAO', 'sum'),
            QUANTIDADE_TRANSACOES=('VALOR_TRANSACAO', 'size')  # Conta as transações
        ).nlargest(10, 'VALOR_TOTAL_TRANSACOES')

        top_empresas_df = top_empresas.reset_index()

        top_empresas_df = top_empresas_df.sort_values(by='VALOR_TOTAL_TRANSACOES', ascending=False)

        top_empresas_df['VALOR_TOTAL_TRANSACOES'] = top_empresas_df['VALOR_TOTAL_TRANSACOES'].astype(float).map('{:,.2f}'.format)
        
        top_empresas_df.columns = ['Empresa', 'Total empresa', 'Quantidade geral CNAB']

        cnabs_correspondentes = df_filtrado['CNAB'].unique()  # Obtendo os CNABs únicos
        top_empresas_df.insert(0, 'CNAB', cnabs_correspondentes[:len(top_empresas_df)])  # Adicionando como primeira coluna

        return top_empresas_df

    else:
        df_filtrado = df[df['CNAB'] == numero_cnab]

        empresas_transacoes = df_filtrado.groupby('NOME_PESSOA_OD').agg(
            VALOR_TRANSACAO=('VALOR_TRANSACAO', 'sum'),
            QUANTIDADE_TRANSACOES=('VALOR_TRANSACAO', 'size')  # Conta as transações
        )

        top_empresas = empresas_transacoes.nlargest(10, 'VALOR_TRANSACAO').reset_index()
        top_empresas.columns = ['NOME_PESSOA_OD', 'VALOR_TRANSACAO', 'QUANTIDADE_TRANSACOES']  # Renomeia as colunas

        top_empresas = top_empresas.sort_values(by='VALOR_TRANSACAO', ascending=False)

        top_empresas['VALOR_TRANSACAO'] = top_empresas['VALOR_TRANSACAO'].astype(float).map('{:,.2f}'.format)

        return top_empresas[['NOME_PESSOA_OD', 'VALOR_TRANSACAO', 'QUANTIDADE_TRANSACOES']]  # Retorne o DataFrame de top empresas


# Retorna um DataFrame com as principais transações realizadas por titulares, agrupadas por nome do titular e ordenadas pelo valor total transacionado, com base em um tipo de CNAB selecionado.
def exibir_top_cnabs_ou_titular(df, selecionado):

    numero_cnab = cnab_numeros[cnab_titulos.index(selecionado)]

    if numero_cnab == 0:
        df_filtrado = df[df['CNAB'].isin(obter_choices_cnab_recorrente(df))]

        top_empresas = df_filtrado.groupby('NOME_TITULAR').agg(
            VALOR_TOTAL_TRANSACOES=('VALOR_TRANSACAO', 'sum'),
            QUANTIDADE_TRANSACOES=('VALOR_TRANSACAO', 'size')  # Conta as transações
        ).nlargest(10, 'VALOR_TOTAL_TRANSACOES')

        top_empresas_df = top_empresas.reset_index()

        top_empresas_df = top_empresas_df.sort_values(by='VALOR_TOTAL_TRANSACOES', ascending=False)

        top_empresas_df['VALOR_TOTAL_TRANSACOES'] = top_empresas_df['VALOR_TOTAL_TRANSACOES'].astype(float).map('{:,.2f}'.format)

        top_empresas_df.columns = ['Titular', 'Total titular', 'Quantidade geral CNAB']
        return top_empresas_df  # Retorne o DataFrame de top empresas

    else:
        df_filtrado = df[df['CNAB'] == numero_cnab]

        empresas_transacoes = df_filtrado.groupby('NOME_TITULAR').agg(
            VALOR_TRANSACAO=('VALOR_TRANSACAO', 'sum'),
            QUANTIDADE_TRANSACOES=('VALOR_TRANSACAO', 'size')  # Conta as transações
        )

        top_empresas = empresas_transacoes.nlargest(10, 'VALOR_TRANSACAO').reset_index()
        top_empresas.columns = ['NOME_TITULAR', 'VALOR_TRANSACAO', 'QUANTIDADE_TRANSACOES']  # Renomeia as colunas
        top_empresas = top_empresas.sort_values(by='VALOR_TRANSACAO', ascending=False)

        top_empresas['VALOR_TRANSACAO'] = top_empresas['VALOR_TRANSACAO'].astype(float).map('{:,.2f}'.format)

        return top_empresas[['NOME_TITULAR', 'VALOR_TRANSACAO', 'QUANTIDADE_TRANSACOES']]  # Retorne o DataFrame de top empresas

# Retorna um DataFrame com as transações filtradas por débito ou crédito, tipo de conta código CNAB e unidade gestora organizadas por valor de transação
def filtrar_transacoes_por_natureza_tipo_conta_unidade_gestora(df, natureza_lancamento, tipo_conta, cnab, unidade_gestora, **kwargs):

    contas_privadas = df['NOME_TITULAR'].unique()
 
    if tipo_conta == "Transações com contas privadas":
        df_filtrado = df[~df['NOME_PESSOA_OD'].isin(contas_privadas)]
        if 'empresa' in kwargs:
            df_filtrado = df_filtrado[df_filtrado['NOME_PESSOA_OD'].isin([kwargs['empresa']])]
        
    elif tipo_conta == "Transações entre contas públicas":
        df_filtrado = df[df['NOME_PESSOA_OD'].isin(contas_privadas)]
    elif tipo_conta == "Aplicação":
        df_filtrado = df[df['CNAB'] == 106]

    if natureza_lancamento == 'Débito':
        natureza_mapeada = 'D' 
    else:
        natureza_mapeada = 'C'

    df_filtrado = df_filtrado[df_filtrado['NATUREZA_LANCAMENTO'] == natureza_mapeada]

    if tipo_conta != "Aplicação":
        df_filtrado = df_filtrado[df_filtrado['NOME_PESSOA_OD'] == unidade_gestora]

    numero_cnab = cnab_numeros[cnab_titulos.index(cnab)]
    
    if numero_cnab != 0:
        df_filtrado = df_filtrado[df_filtrado['CNAB'] == numero_cnab]

    df_resultado = df_filtrado[['NOME_TITULAR', 'NOME_PESSOA_OD', 'CPF_CNPJ_OD', 'CNAB', 'VALOR_TRANSACAO', 'DATA_LANCAMENTO','NATUREZA_LANCAMENTO']]

    df_resultado = df_resultado.sort_values(by='VALOR_TRANSACAO', ascending=False)

    df_resultado['DATA_LANCAMENTO'] = pd.to_datetime(df_resultado['DATA_LANCAMENTO']).dt.strftime('%d/%m/%Y')

    df_resultado['VALOR_TRANSACAO'] = df_resultado['VALOR_TRANSACAO'].astype(float).map('{:,.2f}'.format)

    return df_resultado