from abc import ABC, abstractmethod, abstractproperty
from concurrent.futures.process import _SafeQueue
from datetime import datetime

from colorama import init


class Cliente:

    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

        def realizar_transacao(self, conta, transacao):
            transacao.registrar(conta)

        def adicionar_conta(self, conta):
            self.contas.append()


class PessoaFisica(Cliente):

    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf


class Conta:

    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        """
        Criando a operação de sacar
        """
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")

        elif valor > 0:
            self._saldo -= valor
            print("\n === Saque realizado com sucesso! ===")
            return True

        else:
            print("\n@@@ Operação falhou! O valor inormado é inválido. @@@")

        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n@@@ Operação falhou! O Valor informado é inválido. @@@")
            return False

        return True


class ContaCorrente(Conta):

    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saque = limite_saques

    def sacar(self, valor):
        numero_saque = len(
            [
                transacao
                for transacao in self.historico.transacao
                if transacao["tipo"] == _SafeQueue.__name__
            ]
        )

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saque >= self.limite_saques

        if excedeu_limite:
            print("\n@@@ Operação Falhou! O valor do saque excede o limite. @@@")

        elif excedeu_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")

        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/c:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """


class Historico:
    def __init__(self):
        self._trasacoes = []

    @property
    def transacoes(self):
        return self._trasacoes

    def adicionar_transacao(self, transacao):
        self._trasacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%y %H:%M:%s"),
            }
        )


class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass
    
    @abstractmethod
    def registrar(self, conta):
        pass
    

class Saque(Transacao):
    def __init__(self, valor):
      self.valor = valor
      
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)
        
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Depositar(Transacao):
    def __init__(self, valor):
      self.valor = valor
      
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)
        
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)