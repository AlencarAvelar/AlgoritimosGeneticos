import numpy as np


# Função alvo
def f(x):
    return x ** 3 - 6 * x + 14


# Função para converter um vetor binário em um número real
def binary_to_real(binary):
    # Converte a parte inteira do vetor binário para decimal
    decimal = int("".join(str(b) for b in binary), 2)
    # Normaliza para a faixa [-10, 10]
    return -10 + (decimal / (2 ** len(binary) - 1)) * 20


# Criação da população inicial
def initialize_population(pop_size, binary_length):
    return np.random.randint(0, 2, size=(pop_size, binary_length))


# Crossover de 1 ou 2 pontos
def crossover(parent1, parent2, points):
    if points == 1:
        point = np.random.randint(1, len(parent1) - 1)
        child1 = np.concatenate((parent1[:point], parent2[point:]))
        child2 = np.concatenate((parent2[:point], parent1[point:]))
        return child1, child2
    elif points == 2:
        point1, point2 = sorted(np.random.choice(range(1, len(parent1) - 1), 2, replace=False))
        child1 = np.concatenate((parent1[:point1], parent2[point1:point2], parent1[point2:]))
        child2 = np.concatenate((parent2[:point1], parent1[point1:point2], parent2[point2:]))
        return child1, child2
    return parent1, parent2  # Retorna os pais se não houver crossover


# Mutação
def mutate(individual, mutation_rate):
    for i in range(len(individual)):
        if np.random.rand() < mutation_rate:
            individual[i] = 1 - individual[i]  # Inverte o bit
    return individual


# Seleção por torneio
def tournament_selection(population, fitness, tournament_size):
    selected = np.random.choice(len(population), tournament_size, replace=False)
    winner = selected[np.argmin(fitness[selected])]  # Menor fitness é o melhor
    return population[winner]


# Algoritmo genético
def genetic_algorithm(pop_size=10, binary_length=20, mutation_rate=0.01,
                      crossover_points=1, tournament_size=3, elitism=False,
                      elitism_percentage=0.1, max_generations=100):
    # Inicializa a população
    population = initialize_population(pop_size, binary_length)

    for generation in range(max_generations):
        # Avalia a população
        fitness = np.array([f(binary_to_real(ind)) for ind in population])

        # Armazena os melhores indivíduos (elitismo)
        if elitism:
            num_elites = int(elitism_percentage * pop_size)
            elites_indices = np.argsort(fitness)[:num_elites]
            elites = population[elites_indices]

        new_population = []

        # Seleção, crossover e mutação
        while len(new_population) < pop_size:
            parent1 = tournament_selection(population, fitness, tournament_size)
            parent2 = tournament_selection(population, fitness, tournament_size)
            child1, child2 = crossover(parent1, parent2, crossover_points)
            child1 = mutate(child1, mutation_rate)
            child2 = mutate(child2, mutation_rate)
            new_population.append(child1)
            if len(new_population) < pop_size:
                new_population.append(child2)

        population = np.array(new_population)

        # Adiciona os elites, se habilitado
        if elitism:
            population[-num_elites:] = elites

        # Exibe o melhor resultado da geração
        best_fitness = np.min(fitness)
        best_individual = population[np.argmin(fitness)]
        print(f"Geração {generation + 1}: Melhor f(x) = {best_fitness}, x = {binary_to_real(best_individual)}")

    # Melhor resultado final
    final_fitness = np.array([f(binary_to_real(ind)) for ind in population])
    best_fitness_final = np.min(final_fitness)
    best_individual_final = population[np.argmin(final_fitness)]
    return binary_to_real(best_individual_final), best_fitness_final


# Parâmetros do algoritmo genético
best_x, best_value = genetic_algorithm(max_generations=50, elitism=True)
print(f"\nMelhor x encontrado: {best_x}, com f(x) = {best_value}")
