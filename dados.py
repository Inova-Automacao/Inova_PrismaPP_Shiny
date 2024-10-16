import pandas as pd 

df_cnab_desc =  pd.read_pickle('assets/df_cnab_desc.pkl') #igual ao df_cnab
df_cnab_valor =  pd.read_pickle('assets/df_cnab_valor.pkl') #totaç de transações em cada cnab
df_cnab = pd.read_pickle('assets/df_cnab_desc.pkl') #descricao do código cnab
df_empresa_cnab_valor = pd.read_pickle('assets/df_empresa_cnab_valor.pkl') # empresa - transacao feita - tipo de transacao (cnab)
df_empresa_cnab =  pd.read_pickle('assets/df_empresa_cnab.pkl') #transações que cada empresa mais realizou )?)
df_empresa = pd.read_pickle('assets/df_empresa.pkl') #nome de cada empresa
df_empresas_valores = pd.read_pickle('assets/df_empresas_valores.pkl') #transacoes feitas por cada empresa 
df_empresas_valores['VALOR_TRANSACAO'] = df_empresas_valores['VALOR_TRANSACAO'].apply(lambda x: "{:,.2f}".format(x))
df = pd.read_pickle('assets/df_filtrado.pkl') #cheio de coisa

df_maioresgraf = pd.read_pickle('assets/df_maiores_reset.pkl') #top 10 empresas com maior valor total de transações realizadas
df_maioresgraf['Valor']=df_maioresgraf['Valor'].astype(float).apply(round) #exibido no grafico
df_maiores = pd.read_pickle('assets/df_maiores_reset.pkl') #top 10 empresas com maior valor total de transações realizadas
df_maiores['Valor'] = df_maiores['Valor'].apply(lambda x: "{:,.2f}".format(x)) #exibido na tabela
df_maiores_reset_20 = pd.read_pickle('assets/df_maiores_reset_20.pkl') #nao entendi a diferenca desse pro maiores_reset
df_valor_total = pd.read_pickle('assets/df_valor_total.pkl')

# Preparar choices dinamicos para input_select
choices_anos = sorted([str(ano) for ano in pd.to_datetime(df['DATA_LANCAMENTO']).dt.year.unique()])
choices_empresa = [nome for nome in df_empresa['NOME_PESSOA_OD'].unique()]
choices_titular = [nome for nome in df['NOME_TITULAR'].unique()]
choices_cnab = [descricao for descricao in df_cnab['descricao'].unique()]
choices_nome_titular = [nome for nome in df['NOME_TITULAR'].unique()]

# Preparar choices estaticos para input_select
choices_tipo_transacao_conta = ["Transações com contas privadas", "Transações entre contas públicas"]
choices_tipo_natureza = ["Débito", "Crédito"]
choices_tipo_pessoa = ["CPF", "CNPJ", "Não informado"]

cnab_numeros = [0,
    101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 
    111, 112, 113, 114, 115, 117, 118, 119, 120, 121, 
    122, 123, 124, 125, 126, 127, 201, 202, 203, 204, 
    205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 
    215, 216, 217, 218, 219, 220, 221, 222, 223
]

cnab_titulos = ["Selecionar",
    "101-CHEQUE COMPENSADO",
    "102-ENCARGOS",
    "103-ESTORNOS",
    "104-LANÇAMENTO AVISADO",
    "105-TARIFAS",
    "106-APLICAÇÃO",
    "107-EMPRÉSTIMO / FINANCIAMENTO",
    "108-CÂMBIO",
    "109-CPMF",
    "110-IOF",
    "111-IMPOSTO DE RENDA",
    "112-PAGAMENTOS FORNECEDORES",
    "113-PAGAMENTOS SALÁRIO",
    "114-SAQUE ELETRÔNICO",
    "115-AÇÕES",
    "117-TRANSFERÊNCIA ENTRE CONTAS",
    "118-DEVOLUÇÃO DA COMPENSAÇÃO",
    "119-DEVOLUÇÃO DE CHEQUE DEPOSITADO",
    "120-TRANSFERÊNCIA INTERBANCÁRIA (DOC, TED, PIX)",
    "121-ANTECIPAÇÃO A FORNECEDORES",
    "122-OC / AEROPS",
    "123-SAQUE EM ESPÉCIE",
    "124-CHEQUE PAGO",
    "125-PAGAMENTOS DIVERSOS",
    "126-PAGAMENTO DE TRIBUTOS",
    "127-CARTÃO DE CRÉDITO - PAGAMENTO DE FATURA DE...",
    "201-DEPÓSITO EM CHEQUE",
    "202-CRÉDITO DE COBRANÇA",
    "203-DEVOLUÇÃO DE CHEQUES",
    "204-ESTORNOS",
    "205-LANÇAMENTO AVISADO",
    "206-RESGATE DE APLICAÇÃO",
    "207-EMPRÉSTIMO / FINANCIAMENTO",
    "208-CÂMBIO",
    "209-TRANSFERÊNCIA INTERBANCÁRIA (DOC, TED, PIX)",
    "210-AÇÕES",
    "211-DIVIDENDOS",
    "212-SEGURO",
    "213-TRANSFERÊNCIA ENTRE CONTAS",
    "214-DEPÓSITOS ESPECIAIS",
    "215-DEVOLUÇÃO DA COMPENSAÇÃO",
    "216-OCT",
    "217-PAGAMENTOS FORNECEDORES",
    "218-PAGAMENTOS DIVERSOS",
    "219-RECEBIMENTO DE SALÁRIO",
    "220-DEPÓSITO EM ESPÉCIE",
    "221-PAGAMENTO DE TRIBUTOS",
    "222-CARTÃO DE CRÉDITO - RECEBÍVEIS DE CARTÃO D...",
    "223-CRÉDITO PIX VIA QRCODE"
]


def obter_choices_cnab_recorrente(df):
    cnab_counts = df['CNAB'].value_counts()

    # Seleciona os 10 CNABs mais frequentes e suas quantidades
    top_cnabs = cnab_counts.nlargest(10)

    # Cria a lista de CNABs ordenados por quantidade de ocorrências
    choices_cnab_recorrente = top_cnabs.index.tolist()

    return choices_cnab_recorrente