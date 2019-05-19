# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 22:43:54 2019

@author: Marcio Souza Filho

"""
import matplotlib.pyplot as plt
import numpy as np
import abc
import operator
from random import choice, sample

class ProblemaStrategyAbstract(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def calcula_fitness(self, ind):
        """Required Method"""

    @abc.abstractmethod
    def inicializa_limites(self, limite_inferior, limite_superior, n_variaveis):
        """Required Method"""

    @abc.abstractmethod
    def melhor_solucao(self, populacao):
        """Required Method"""

class RastriginStrategy(ProblemaStrategyAbstract):
    # limites [-5.12, 5.12]
    # f(x*) 0, x* = 0
    def calcula_fitness(self, ind):
        ind.fitness = 10*ind.n_variaveis
        for i in range(ind.n_variaveis):
            ind.fitness += (np.power(ind.variaveis[i], 2) -
                            10*np.cos(2*ind.variaveis[i]*np.pi))

    def inicializa_limites(self, n_variaveis):
        lim_inferior = [-5.12]*n_variaveis
        lim_superior = [5.12]*n_variaveis
        return(lim_inferior, lim_superior)

    def melhor_solucao(self, populacao):
        return populacao.solucao_menor_fitness()

class SchwefelStrategy(ProblemaStrategyAbstract):
    # limites [-500, 500]
    # f(x*) = 0 x* = 420.9687
    def calcula_fitness(self, ind):
        ind.fitness = 418.9829*ind.n_variaveis
        for i in range(ind.n_variaveis):
            ind.fitness -= ind.variaveis[i] * \
                np.sin(np.sqrt(abs(ind.variaveis[i])))

    def inicializa_limites(self, n_variaveis):
        lim_inferior = [-500]*n_variaveis
        lim_superior = [500]*n_variaveis
        return(lim_inferior, lim_superior)

    def melhor_solucao(self, populacao):
        return populacao.solucao_menor_fitness()

class DeJongSphereStrategy(ProblemaStrategyAbstract):
    # limites [-5.12, 5.12]
    # f(x*) 0, x* = 0
    def calcula_fitness(self, ind):
        ind.fitness = 0
        for i in range(ind.n_variaveis):
            ind.fitness += np.power(ind.variaveis[i], 2)

    def inicializa_limites(self, n_variaveis):
        lim_inferior = [-5.12]*n_variaveis
        lim_superior = [5.12]*n_variaveis
        return(lim_inferior, lim_superior)

    def melhor_solucao(self, populacao):
        return populacao.solucao_menor_fitness()

class DeJong5Strategy(ProblemaStrategyAbstract):
    # limites [-65.536, 65.536] e apenas 2 variaveis
    def calcula_fitness(self, ind):
        ind.fitness = 0.002
        a = [-32, -16, 0, 16, 32]
        for i in range(25):
            ind.fitness += 1 / \
                (i + np.power((ind.variaveis[0] - a[int(i % 5)]),
                              6) + np.power((ind.variaveis[1]-a[int(i/5)]), 6))

    def inicializa_limites(self, n_variaveis):
        lim_inferior = [-65.536]*n_variaveis
        lim_superior = [65.536]*n_variaveis
        return(lim_inferior, lim_superior)

    def melhor_solucao(self, populacao):
        return populacao.solucao_menor_fitness()

class RosenbrockStrategy(ProblemaStrategyAbstract):
    # limites [-5, 5]
    # f(x*) = 0, x* = 1
    def calcula_fitness(self, ind):
        ind.fitness = 0
        for i in range(ind.n_variaveis-1):
            ind.fitness += np.power((ind.variaveis[i]-1), 2) + 100*np.power(
                (ind.variaveis[i+1] - ind.variaveis[i]**2), 2)

    def inicializa_limites(self, n_variaveis):
        lim_inferior = [-5]*n_variaveis
        lim_superior = [5]*n_variaveis
        return(lim_inferior, lim_superior)

    def melhor_solucao(self, populacao):
        return populacao.solucao_menor_fitness()

class SelecionaIndividuosStrategyAbstract(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def seleciona_individuos(self, populacao):
        """Required Method"""

class SelecionaIndividuosAleatorioStrategy(SelecionaIndividuosStrategyAbstract):
    def seleciona_individuos(self, populacao):
        individuos = sample(populacao.individuos, 3)
        return individuos

class SelecionaSobreviventesStrategyAbstract(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def selecao_sobreviventes(self, pop_original, pop_mutante, tam_pop):
        """Required Method"""

class SelecionaSobreviventesDeterministicoStrategy(SelecionaSobreviventesStrategyAbstract):    
    def selecao_sobreviventes(self, pop_original, pop_mutante, tam_pop):
        for ind in range(tam_pop):
            if pop_original.individuos[ind].fitness > pop_mutante.individuos[ind].fitness:
                pop_original.individuos[ind] = pop_mutante.individuos[ind]

class Individuo:
    def __init__(self, n_variaveis):
        self.variaveis = []  # Variaveis do individuo
        self.n_variaveis = n_variaveis
        self.fitness = None

    def gera_individuo_aleatorio(self, lim_inferior, lim_superior):
        for i in range(self.n_variaveis):
            self.variaveis.append(np.random.uniform(
                lim_inferior[i], lim_superior[i]))

    def print(self):
        print(str(self.variaveis)+', '+str(self.fitness))

class Populacao:
    def __init__(self):
        self.individuos = []
        self.reta_prob = []

    def gera_populacao_aleatoria(self, n_variaveis, tam_pop, lim_inferior, lim_superior):
        for _ in range(tam_pop):
            individuo = Individuo(n_variaveis)
            individuo.gera_individuo_aleatorio(lim_inferior, lim_superior)
            self.individuos.append(individuo)

    # Ordena a populacao pelo fitness em ordem crescente
    def ordena(self):
        self.individuos.sort(key=operator.attrgetter('fitness'), reverse=False)

    def solucao_menor_fitness(self):
        return self.individuos[0]

    def solucao_maior_fitness(self):
        return self.individuos[-1]

    def print(self):
        for individuo in self.individuos:
            individuo.print()

class DE:
    def __init__(self, seleciona_individuos_strategy, seleciona_sobreviventes_strategy):
        self.seleciona_individuos_strategy = seleciona_individuos_strategy
        self.seleciona_sobreviventes_strategy = seleciona_sobreviventes_strategy

    def seleciona_individuos(self, populacao):
        return self.seleciona_individuos_strategy.seleciona_individuos(populacao)

    @staticmethod
    def mutacao(individuos, fator_escala):
        n_variaveis = len(individuos[0].variaveis)
        novo_individuo = Individuo(n_variaveis)
        n_var = len(individuos[0].variaveis)
        for i in range(n_var):
            x = individuos[0].variaveis[i] + fator_escala * \
                (individuos[1].variaveis[i]-individuos[2].variaveis[i])
            novo_individuo.variaveis.append(x)
        return novo_individuo

    # Confere se as solucoes mutantes estao saindo dos limites, caso estejam reflete
    @staticmethod
    def reflexao_limites(mutante, limite_inferior, limite_superior):
        variaveis = mutante.variaveis
        for i in range(mutante.n_variaveis):
            if variaveis[i] < limite_inferior[i]:
                variaveis[i] = limite_inferior[i] - (variaveis[i] - limite_inferior[i])
            elif variaveis[i] > limite_superior[i]:
                variaveis[i] = limite_superior[i] - (variaveis[i] - limite_superior[i])

    @staticmethod
    def recombinacao(sol_original, sol_mutante, prob_mutante):
        n_variaveis = sol_original.n_variaveis
        delta = np.random.randint(low=0, high=n_variaveis)
        for i in range(n_variaveis):
            if not(prob_mutante > np.random.rand() or i == delta):
                sol_mutante.variaveis[i] = sol_original.variaveis[i]

    def selecao_sobreviventes(self, pop_original, pop_mutante, tam_pop):
        self.seleciona_sobreviventes_strategy.selecao_sobreviventes(pop_original, pop_mutante, tam_pop)

class Problema:
    def __init__(self, problema_strategy):
        self.problema_strategy = problema_strategy

    def calcula_fitness(self, individuo):
        self.problema_strategy.calcula_fitness(individuo)

    def inicializa_limites(self, n_variaveis):
        return(self.problema_strategy.inicializa_limites(n_variaveis))

    def melhor_solucao(self, populacao):
        return(self.problema_strategy.melhor_solucao(populacao))

def run_DE():
    problema = Problema(RosenbrockStrategy())
    de = DE(SelecionaIndividuosAleatorioStrategy(), SelecionaSobreviventesDeterministicoStrategy())
    n_variaveis = 2
    tam_pop = 50
    max_iteracoes = 200*n_variaveis

    lim_inferior, lim_superior = problema.inicializa_limites(n_variaveis)

    precisao = 1e-12

    fator_escala = 0.5
    prob_mutante = 0.5

    # Inicializa populacao
    populacao = Populacao()
    populacao.gera_populacao_aleatoria(n_variaveis, tam_pop, lim_inferior, lim_superior)
    for individuo in populacao.individuos:
        problema.calcula_fitness(individuo)

    populacao_mutante = Populacao()
    melhor_fitness = populacao.individuos[0].fitness
    iteracao = 0
    while (iteracao < max_iteracoes) and (melhor_fitness > precisao):
        iteracao += 1
        for ind in range(tam_pop):
            selecionados = de.seleciona_individuos(populacao)
            mutante = de.mutacao(selecionados, fator_escala)
            de.reflexao_limites(mutante, lim_inferior, lim_superior)
            de.recombinacao(populacao.individuos[ind], mutante,  prob_mutante)
            problema.calcula_fitness(mutante)
            populacao_mutante.individuos.append(mutante)
        de.selecao_sobreviventes(populacao, populacao_mutante, tam_pop)
        populacao_mutante.individuos.clear()
        populacao.ordena()
        melhor_solucao_iteracao = problema.melhor_solucao(populacao)
        if melhor_solucao_iteracao.fitness < melhor_fitness:
            melhor_fitness = melhor_solucao_iteracao.fitness

    populacao.individuos[0].print()
    print('Rastrigin com n = ' + str(n_variaveis) + ': melhor solucao = ' +
          str(melhor_fitness) + 'em ' + str(iteracao) + ' iteracoes')
    return


run_DE()
