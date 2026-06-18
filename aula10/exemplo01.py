import pandas as pd 
import numpy as np 
# pip install matplotlib
import matplotlib.pyplot as plt

try:
    print('Obtendo os dados...')
    ENDERECO_DADOS = 'https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv'

    # utf-8, iso-8859-1, latin1, cp1252
    df_ocorrencias = pd.read_csv(ENDERECO_DADOS, sep=';', encoding='iso-8859-1')

    # delimitando as variáveis
    df_roubo_veiculo = df_ocorrencias[['munic', 'roubo_veiculo']]
    # print(df_roubo_veiculo)

    # Totalizando os roubos pelos municípios
    df_roubo_veiculo = df_roubo_veiculo.groupby('munic', as_index=False)['roubo_veiculo'].sum()
    
    # ordenado o dataframe
    df_roubo_veiculo = df_roubo_veiculo.sort_values(by='roubo_veiculo', ascending=False)
    # print(df_roubo_veiculo.head(10))
    print(df_roubo_veiculo)

except Exception as e:
    print(f'Erro ao obter dados {e}')


# Obtendo a medidas
try:
    print('Calculando as medidas... ')
    array_roubo_veiculo = np.array(df_roubo_veiculo['roubo_veiculo'])

    media_roubo_veiculo = np.mean(array_roubo_veiculo)
    mediana_roubo_veiculo = np.median(array_roubo_veiculo)


    distancia = abs((media_roubo_veiculo - mediana_roubo_veiculo) / mediana_roubo_veiculo * 100)

    print('\nMedidas de Tendência Central')
    print(30*"=")
    print(f'Média: {media_roubo_veiculo}')
    print(f'Mediana: {mediana_roubo_veiculo}')
    print(f'Distancia: {distancia} %')

except Exception as e:
    print(f'Erro ao processar as medidas {e}')


# Obtendo a distribuição
try:
    print('Processando os quartis')

    q1 = np.quantile(array_roubo_veiculo, .25)
    q3 = np.quantile(array_roubo_veiculo, .75)

    print('\nQuartis')
    print(30*"=")
    print(f'Q1: {q1}')
    print(f'Mediana: {mediana_roubo_veiculo}')
    print(f'Q3: {q3}')


    # Municípios com menos roubos
    df_roubo_veiculo_menores = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] < q1]

    # Municípios com mais roubos
    df_roubo_veiculo_maiores = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] > q3]

    print('\nMunicípios com menos casos de roubos: ')
    print(30*"=")
    print(df_roubo_veiculo_menores.sort_values(by='roubo_veiculo', ascending=True))

    print('\nMunicípios com Mais Roubos: ')
    print(30*"=")
    print(df_roubo_veiculo_maiores)

except Exception as e:
    print(f'Erro ao obter a distribuição {e}')


# obtendo medidas de dispersão
try:
    # Amplitude Total
    # amplitude = maximo - minimo
    # Resultado: mais próximo do mínimo, baixa dispersão.
    # Se for 0, quer dizer que todos os dados são iguais.
    # Se mais próximo do maior valor, alta dispersão.
    maximo = np.max(array_roubo_veiculo)
    minimo = np.min(array_roubo_veiculo)
    amplitude = maximo - minimo

    print('\nMedidas de Dispersão')
    print(30*"=")
    print(f'Máximo: {maximo}')
    print(f'Mínimo: {minimo}')
    print(f'Amplitude Total: {amplitude}')

except Exception as e:
    print(f'Erro ao calcular medidas de dispersão: {e}')


# Calculando outliers
try:
    # iqr (Intervalo Interquartil) - Amplitude dos 50% dos dados mais centrais.
    # iqr = q3 - q1
    # Ele ignora os valores extremos. Max e Min estão fora do IQR
    # Não sofre interferência dos valores extremos.
    # Quanto mais próximo do zero, mais homogêneos são os dados
    # Quanto mais próximo do Q3, menos homogêneos são os dados
    iqr = q3 - q1

    # limite inferior: 
    # É uma medida que vai identificar como outliers, os valores abaixo dele.
    limite_inferior = q1 - (1.5 * iqr)

    # limite superior: 
    # É uma medida que vai identificar como outliers, os valores acima dele.
    limite_superior = q3 + (1.5 * iqr)


    print('\nMedidas ')
    print(30*"=")
    print(f'Mínimo: {minimo}')
    print(f'Limite Inferior: {limite_inferior}')
    print(f'Q1: {q1}')
    print(f'Mediana: {mediana_roubo_veiculo}')  # q2
    print(f'Q3: {q3}')
    print(f'Limite superior: {limite_superior}')
    print(f'Máximo: {maximo}')    

except Exception as e:
    print(f'Erro ao calcular os limites: {e}')


# Exibindo os outliers
try:
    # outliers superiores
    df_roubo_veiculo_outliers_superiores = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] > limite_superior]
    
    # outliers inferiores
    df_roubo_veiculo_outliers_inferiores = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] < limite_inferior]

    print('\nMunicípios c/ Outliers Inferiores ')
    print(30*"=")
    if len(df_roubo_veiculo_outliers_inferiores) == 0:
        print('Não existe outliers inferiores')
    else:
        print(df_roubo_veiculo_outliers_inferiores.sort_values(by='roubo_veiculo', ascending=True))



    print('\nMunicípios c/ Outliers Superiores ')
    print(30*"=")
    if len(df_roubo_veiculo_outliers_superiores) == 0:
        print('Não existe outliers superiores')
    else:
        print(df_roubo_veiculo_outliers_superiores.sort_values(by='roubo_veiculo', ascending=False))

except Exception as e:
    print(f'Erro ao Calular Outliers {e}')


# Visualizando os dados
try:
    
    plt.subplots(2, 2, figsize=(18, 10))

    # POSIÇÃO 01 - BOXPLOT
    plt.subplot(2, 2, 1)
    plt.boxplot(array_roubo_veiculo, vert=False, showmeans=True) # showfliers=False 
    plt.title('Boxplot da Distribuição')

    # POSIÇÃO 2 - MEDIDAS
    plt.subplot(2, 2, 2)
    plt.text(0.1, 0.9, f'Média: {media_roubo_veiculo}')
    plt.text(0.1, 0.8, f'Distância: {distancia}')
    plt.text(0.1, 0.7, f'Limite Inferior: {limite_inferior}')
    plt.text(0.1, 0.6, f'Mínimo: {minimo}')      
    plt.text(0.1, 0.5, f'Q1: {q1}')
    plt.text(0.1, 0.4, f'Mediana: {mediana_roubo_veiculo}')
    plt.text(0.1, 0.3, f'Q3: {q3}')
    plt.text(0.1, 0.2, f'Limite Superior: {limite_superior}')
    plt.text(0.1, 0.1, f'Máximo: {maximo}')
    plt.text(0.1, 0.0, f'Amplitude Total: {amplitude}')

    plt.axis('off')
    plt.title('Resumo Estatístico')


    # POSIÇÃO 3 - OUTLIERS
    plt.subplot(2, 2, 3)
    df_roubo_veiculo_outliers_superiores = (
        df_roubo_veiculo_outliers_superiores
        .head(10)
        .sort_values(by='roubo_veiculo', ascending=False)
    )

    plt.bar(
        #.str.slice(0, 10) - Corta as palavras "faz abreviações"
        df_roubo_veiculo_outliers_superiores['munic'],
        df_roubo_veiculo_outliers_superiores['roubo_veiculo'] 
    )

    # Espaço para afastar os valores, cada um de sua coluna
    deslocamento = max(df_roubo_veiculo_outliers_superiores['roubo_veiculo']) * 0.02

    for i, valor in enumerate(df_roubo_veiculo_outliers_superiores['roubo_veiculo']):
        # enumerate recupera os valores dos roubos e a posição de cada um na lista
        # No gráfico de Colunas usamos a posição em X p/ identificar as cada barra e
        # usamos os próprios valores dos roubos para das posição, vertical dos valores.
        plt.text(
            # i e valor, são usados como coordenadas q dão a posição dos valores no gráfico
            i, # posição X
            valor + deslocamento, # posição Y
            f'{valor:,}',
            ha='center'
        )

    plt.xticks(rotation=45, ha='right') # Rotaciona o texto do eixo X
    plt.title('Outliers Superiores')

    # POSIÇÃO 4 - OUTLIERS INFERIORES OU MENORES ROUBOS
    plt.subplot(2, 2, 4)
    
    if len(df_roubo_veiculo_outliers_inferiores) > 0:
        df_roubo_veiculo_outliers_inferiores = (
            df_roubo_veiculo_outliers_inferiores
            .sort_values(by='roubo_veiculo', ascending=True)
        )

        plt.barh(
            df_roubo_veiculo_outliers_inferiores['munic'],
            df_roubo_veiculo_outliers_inferiores['roubo_veiculo']
        )

        plt.title('Municípios c/ Outliers Inferiores')

    else:
        df_roubo_veiculo_menores = (
            df_roubo_veiculo_menores
            .sort_values(by='roubo_veiculo', ascending=True)
            .head(10)
            .sort_values(by='roubo_veiculo', ascending=False)
        )

        plt.barh(
            df_roubo_veiculo_menores['munic'],
            df_roubo_veiculo_menores['roubo_veiculo']
        )

        deslocamento = max(df_roubo_veiculo_menores['roubo_veiculo']) * 0.03

        # Rótulo dos dados:
        for i, valor in enumerate(df_roubo_veiculo_menores['roubo_veiculo']):
        # enumerate recupera os valores dos roubos e a posição de cada um na lista
        # No gráfico de Colunas usamos a posição em Y, que é i, p/ identificar as cada barra. E
        # usamos os próprios valores dos roubos para posiçionar os valores na horizontal.
            plt.text(
                valor +deslocamento, # posição X (soma o deslocamento para afastar o texto)
                i, # posição Y
                f'{valor:,}',
                ha='center'
            )
        
        plt.title('Municípios com Menores Roubos')

    plt.show()

except Exception as e:
    print(f'Erro ao plotar o gráfico: {e}')
