from dados import *
import pandas as pd

# Retorna um dataframe com as transações feitas por cada empresa
def consulta(nome): 

    # Filtra o dataframe para obter o valor transacionado pela empresa
    df_valor = df_valor_total[df_valor_total['Empresa'] == nome]

    # Filtra o dataframe para obter as transações da empresa
    df_transacoes = df_empresas_valores[df_empresas_valores['NOME_PESSOA_OD'] == nome]

    # Calcula o total de transações
    total_transacoes = df_transacoes.shape[0]

    # Extrai o valor total (supondo que o dataframe df_valor tem uma coluna chamada 'VALOR_TOTAL')
    valor_total = df_valor['Valor'].values[0] if not df_valor.empty else 0

    # Cria um novo dataframe com os resultados
    resultado = pd.DataFrame({
        'Empresa': [nome],
        'Valor': [valor_total],
        'Total de Transações': [total_transacoes]
    })

    return resultado

# Retorna um dataframe com o total transacionado por cada empresa no ano escolhido
def filtrar_gastos_por_ano(df, ano_escolhido):

    # Converte a coluna DATA_LANCAMENTO para o formato datetime
    df['DATA_LANCAMENTO'] = pd.to_datetime(df['DATA_LANCAMENTO'], format='%Y-%m-%dT%H:%M:%S.%f')
    
    # Filtra o dataframe pelo ano escolhido
    df_filtrado = df[df['DATA_LANCAMENTO'].dt.year == int(ano_escolhido)]
    
    # Agrupa os dados pelo nome da empresa (NOME_TITULAR) e soma o VALOR_TRANSACAO
    df_total_gastos = df_filtrado.groupby('NOME_PESSOA_OD')['VALOR_TRANSACAO'].sum().reset_index()

     # Ordena o dataframe do maior para o menor com base no TOTAL_GASTO
    df_total_gastos = df_total_gastos.sort_values(by='VALOR_TRANSACAO', ascending=False)

    # Formata a coluna TOTAL_GASTO para incluir separador de milhar e duas casas decimais
    df_total_gastos['VALOR_TRANSACAO'] = df_total_gastos['VALOR_TRANSACAO'].apply(lambda x: "{:,.2f}".format(x))

    # Renomear as colunas para uma visualização mais clara
    df_total_gastos.columns = ['Empresa', 'Total transacionado - Ano']
    
    return df_total_gastos

# Retorna um dataframe com o total transacionado por cada empresa na natureza escolhida
def calcular_total_por_natureza(df, tipo):

    # Mapeia o tipo para os valores correspondentes em NATUREZA_LANCAMENTO
    natureza_mapeada = 'D' if tipo == 'Débito' else 'C'
    
    # Filtra o dataframe de acordo com a natureza escolhida
    df_filtrado = df[df['NATUREZA_LANCAMENTO'] == natureza_mapeada]

    # Agrupa por NOME_PESSOA_OD e soma o VALOR_TRANSACAO
    resultado = df_filtrado.groupby('NOME_PESSOA_OD')['VALOR_TRANSACAO'].sum().reset_index()

    # Renomeia a coluna de total
    resultado.rename(columns={'VALOR_TRANSACAO': 'TOTAL_GASTO'}, inplace=True)

    # Ordena do maior para o menor
    resultado.sort_values(by='TOTAL_GASTO', ascending=False, inplace=True)

    # Formata a coluna TOTAL_GASTO
    resultado['TOTAL_GASTO'] = resultado['TOTAL_GASTO'].apply(lambda x: f"{x:,.2f}")

    # Renomear as colunas para uma visualização mais clara
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

    # Converte a coluna CPF_CNPJ_OD para string
    df['CPF_CNPJ_OD'] = df['CPF_CNPJ_OD'].astype(str)

    # Filtra os CPFs e CNPJs
    if tipo == 'CPF':
        df_filtrado = df[df['CPF_CNPJ_OD'].str.len() == 11]  # CPFs têm 11 dígitos
    elif tipo == 'CNPJ':  
        df_filtrado = df[df['CPF_CNPJ_OD'].str.len() == 14]  # CNPJs têm 14 dígitos
    else:
        # Filtra valores NaN na coluna CPF_CNPJ_OD
        df_filtrado = df[(df['CPF_CNPJ_OD'] == 'nan') | (df['CPF_CNPJ_OD'].isna())]

    # Agrupa por CPF_CNPJ_OD e soma o VALOR_TRANSACAO
    resultado = df_filtrado.groupby('CPF_CNPJ_OD')['VALOR_TRANSACAO'].sum().reset_index()

    # Renomeia a coluna de total
    resultado.rename(columns={'VALOR_TRANSACAO': 'TOTAL_GASTO'}, inplace=True)

    # Ordena do maior para o menor
    resultado.sort_values(by='TOTAL_GASTO', ascending=False, inplace=True)

    # Formata a coluna TOTAL_GASTO
    resultado['TOTAL_GASTO'] = resultado['TOTAL_GASTO'].apply(lambda x: f"{x:,.2f}")

    # Formata os CPFs ou CNPJs
    resultado['CPF_CNPJ_OD'] = resultado['CPF_CNPJ_OD'].apply(lambda x: formatar_cpf_cnpj(x, tipo))

    # Renomear as colunas para uma visualização mais clara
    resultado.columns = ['CPF/CNPJ', 'Total transacionado']

    return resultado

# Retorna um dataframe com o total gasto por tarnsações em contas publicas e privadas
def filtrar_transacoes_por_tipo(df, tipo_transacao):
    # Lista de nomes de contas privadas (NOME_TITULAR)
    contas_privadas = df['NOME_TITULAR'].unique()
    
    # Condicional para filtrar de acordo com a escolha do usuário
    if tipo_transacao == "Transações com contas privadas":
        # Filtrar transações onde a conta de origem/destino não está nas contas privadas
        df_filtrado = df[~df['NOME_PESSOA_OD'].isin(contas_privadas)]
    elif tipo_transacao == "Transações entre contas públicas":
        # Filtrar transações onde a conta de origem/destino está nas contas privadas
        df_filtrado = df[df['NOME_PESSOA_OD'].isin(contas_privadas)]
   
    # Agrupar o dataframe pelo nome da conta de origem/destino e somar os valores das transações
    df_agrupado = df_filtrado.groupby('NOME_PESSOA_OD')['VALOR_TRANSACAO'].sum().reset_index()
    
    # Renomear as colunas para uma visualização mais clara
    df_agrupado.columns = ['Nome Conta', 'Total transacionado']

    # Ordenar do maior para o menor total gasto
    df_agrupado = df_agrupado.sort_values(by='Total transacionado', ascending=False)

    # Formatar a coluna Total Gasto como decimal
    df_agrupado['Total transacionado'] = df_agrupado['Total transacionado'].astype(float).map('{:,.2f}'.format)
    
    return df_agrupado


def obter_total_transacoes_por_empresa(df, titulo_cnab):
    # Verifica se o título existe na lista
    if titulo_cnab not in cnab_titulos:
        raise ValueError("Título do CNAB não encontrado.")
    
    # Obtém o número correspondente do CNAB
    numero_cnab = cnab_numeros[cnab_titulos.index(titulo_cnab)]
    
    # Filtra o DataFrame para o CNAB correspondente
    df_filtrado = df[df['CNAB'] == numero_cnab]

    if df_filtrado.empty:
        # Retorna um DataFrame com uma mensagem
        return pd.DataFrame({
            'NOME_PESSOA_OD': ['Nenhuma transação encontrada'],
            'TOTAL_TRANSACOES': [0]
        })
    
    # Agrupa por empresa e soma as transações
    resultado = df_filtrado.groupby('NOME_PESSOA_OD')['VALOR_TRANSACAO'].sum().reset_index()
    
    # Ordenar do maior para o menor total gasto
    resultado = resultado.sort_values(by='VALOR_TRANSACAO', ascending=False)

    # Formatar a coluna Total Gasto como decimal
    resultado['VALOR_TRANSACAO'] = resultado['VALOR_TRANSACAO'].astype(float).map('{:,.2f}'.format)

    # Renomear as colunas para uma visualização mais clara
    resultado.columns = ['Empresa', 'Total transacionado - CNAB']

    return resultado

def filtrar_por_titular(df, nome_titular):

    # Filtra o dataframe pelo NOME_TITULAR
    df_filtrado = df[df['NOME_TITULAR'] == nome_titular]
    
    # Agrupa por DESCRICAO_LANCAMENTO e soma os VALOR_TRANSACAO
    resultado = df_filtrado.groupby('DESCRICAO_LANCAMENTO', as_index=False)['VALOR_TRANSACAO'].sum()

    # Ordenar do maior para o menor total gasto
    resultado = resultado.sort_values(by='VALOR_TRANSACAO', ascending=False)

    # Formatar a coluna Total Gasto como decimal
    resultado['VALOR_TRANSACAO'] = resultado['VALOR_TRANSACAO'].astype(float).map('{:,.2f}'.format)
    
    # Renomear as colunas para uma visualização mais clara
    resultado.columns = ['Lançamento', 'Total transacionado - lançamento']
    
    return resultado



def filtrar_transacoes_por_natureza_tipo_conta(df, natureza_lancamento, tipo_conta, cnab):

    # Lista de nomes de contas privadas (NOME_TITULAR)
    contas_privadas = df['NOME_TITULAR'].unique()
    
    # Condicional para filtrar de acordo com a escolha do usuário
    if tipo_conta == "Transações com contas privadas":
        # Filtrar transações onde a conta de origem/destino não está nas contas privadas
        df_filtrado = df[~df['NOME_PESSOA_OD'].isin(contas_privadas)]
    elif tipo_conta == "Transações entre contas públicas":
        # Filtrar transações onde a conta de origem/destino está nas contas privadas
        df_filtrado = df[df['NOME_PESSOA_OD'].isin(contas_privadas)]
   
   # Mapeia o tipo para os valores correspondentes em NATUREZA_LANCAMENTO
    if natureza_lancamento == 'Débito':
        natureza_mapeada = 'D' 
    else:
        natureza_mapeada = 'C'
    
    # Filtra o dataframe de acordo com a natureza escolhida
    df_filtrado = df_filtrado[df_filtrado['NATUREZA_LANCAMENTO'] == natureza_mapeada]

    # Obtém o número correspondente do CNAB
    numero_cnab = cnab_numeros[cnab_titulos.index(cnab)]
    
    if numero_cnab != 0:
    # Filtra o DataFrame para o CNAB correspondente
        df_filtrado = df_filtrado[df_filtrado['CNAB'] == numero_cnab]

    df_resultado = df_filtrado[['NOME_TITULAR', 'NOME_PESSOA_OD', 'CPF_CNPJ_OD', 'CNAB', 'VALOR_TRANSACAO', 'DATA_LANCAMENTO','NATUREZA_LANCAMENTO']]
    
    # Ordena pelo valor total transacionado (VALOR_TRANSACAO)
    df_resultado = df_resultado.sort_values(by='VALOR_TRANSACAO', ascending=False)

    # Formata a coluna DATA_LANCAMENTO no formato dia/mês/ano
    df_resultado['DATA_LANCAMENTO'] = pd.to_datetime(df_resultado['DATA_LANCAMENTO']).dt.strftime('%d/%m/%Y')

    # Formatar a coluna Total Gasto como decimal
    df_resultado['VALOR_TRANSACAO'] = df_resultado['VALOR_TRANSACAO'].astype(float).map('{:,.2f}'.format)

    return df_resultado


    

def top_10_titulares_credito(df, ano):
    # Converter a coluna DATA_LANCAMENTO para datetime
    df['DATA_LANCAMENTO'] = pd.to_datetime(df['DATA_LANCAMENTO'], format='%Y-%m-%dT%H:%M:%S.%f')

    # Filtrar transações por ano
    df_filtered = df[df['DATA_LANCAMENTO'].dt.year == int(ano)]
    
    # Filtrar apenas transações de crédito
    df_credito = df_filtered[df_filtered['NATUREZA_LANCAMENTO'] == 'C']

    # Agrupar por NOME_TITULAR e somar os valores das transações
    df_top_10 = df_credito.groupby('NOME_TITULAR')['VALOR_TRANSACAO'].sum().reset_index()
    
    # Ordenar do maior para o menor e selecionar os 10 primeiros
    df_top_10 = df_top_10.sort_values(by='VALOR_TRANSACAO', ascending=False).head(10)
    print(f"Top 10 titulares: {df_top_10}")  # Debugging
    return df_top_10