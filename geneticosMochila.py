import random

# Função para calcular o valor e o peso total de um cromossomo
def calcular_fitness(cromossomo, pesos_e_valores, peso_maximo):
    peso_total = valor_total = 0
    for i in range(len(cromossomo)):
        if cromossomo[i] == 1:
            peso_total += pesos_e_valores[i][0]
            valor_total += pesos_e_valores[i][1]
    # Penaliza cromossomos que excedem o peso máximo
    if peso_total > peso_maximo:
        return 0
    return valor_total

# Função para gerar um cromossomo aleatório
def gerar_cromossomo(tamanho):
    return [random.randint(0, 1) for _ in range(tamanho)]

# Função para selecionar dois pais para cruzamento
def selecionar_pais(populacao, aptidoes):
    return random.choices(populacao, weights=aptidoes, k=2)

# Função de cruzamento (crossover) entre dois cromossomos
def cruzamento(pai1, pai2):
    ponto_de_corte = random.randint(1, len(pai1) - 1)
    filho1 = pai1[:ponto_de_corte] + pai2[ponto_de_corte:]
    filho2 = pai2[:ponto_de_corte] + pai1[ponto_de_corte:]
    return filho1, filho2

# Função de mutação (troca aleatória em um cromossomo)
def mutacao(cromossomo, taxa_de_mutacao=0.01):
    for i in range(len(cromossomo)):
        if random.random() < taxa_de_mutacao:
            cromossomo[i] = 1 - cromossomo[i]

# Algoritmo genético para o problema da mochila
def algoritmo_genetico(pesos_e_valores, peso_maximo, num_cromossomos, num_geracoes):
    # Inicialização da população
    populacao = [gerar_cromossomo(len(pesos_e_valores)) for _ in range(num_cromossomos)]
    melhores_individuos_por_geracao = []

    for _ in range(num_geracoes):
        # Avaliação da aptidão de cada cromossomo
        aptidoes = [calcular_fitness(cromossomo, pesos_e_valores, peso_maximo) for cromossomo in populacao]

        # Seleciona os melhores indivíduos da geração atual
        melhor_fitness = max(aptidoes)
        melhor_cromossomo = populacao[aptidoes.index(melhor_fitness)]
        media_pesos = sum([pesos_e_valores[i][0] for i in range(len(melhor_cromossomo)) if melhor_cromossomo[i] == 1]) / len(melhor_cromossomo)
        melhores_individuos_por_geracao.append([media_pesos, melhor_cromossomo])

        # Nova geração
        nova_populacao = []
        while len(nova_populacao) < num_cromossomos:
            # Seleção dos pais
            pai1, pai2 = selecionar_pais(populacao, aptidoes)
            # Cruzamento
            filho1, filho2 = cruzamento(pai1, pai2)
            # Mutação
            mutacao(filho1)
            mutacao(filho2)
            # Adiciona os filhos à nova população
            nova_populacao.extend([filho1, filho2])

        # Atualiza a população
        populacao = nova_populacao[:num_cromossomos]

    return melhores_individuos_por_geracao

# Exemplo de uso
pesos_e_valores = [[2, 10], [4, 30], [6, 300], [8, 10], [8, 30], [8, 300], [12, 50], [25, 75], [50, 100], [100, 400]]
peso_maximo = 100
numero_de_cromossomos = 150
geracoes = 50

resultado = algoritmo_genetico(pesos_e_valores, peso_maximo, numero_de_cromossomos, geracoes)
for geracao in resultado:
    print(geracao)
