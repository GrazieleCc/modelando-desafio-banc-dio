class Cliente:
    def __init__(self, nome, data_nascimento, cpf, endereco):
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf
        self.endereco = endereco
        self.contas = []

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class Registro:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)

class Conta:
    def __init__(self, cliente, numero, agencia="0001"):
        self.saldo = 0.0
        self.numero = numero
        self.agencia = agencia
        self.cliente = cliente
        self.registro = Registro()
        cliente.adicionar_conta(self)

    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            self.registro.adicionar_transacao(f"Depósito: R$ {valor:.2f}")
        else:
            print("Valor inválido para depósito.")

    def sacar(self, valor):
        if valor > self.saldo:
            print("Saldo insuficiente.")
        elif valor > 0:
            self.saldo -= valor
            self.registro.adicionar_transacao(f"Saque: R$ {valor:.2f}")
        else:
            print("Valor inválido para saque.")

    def exibir_extrato(self):
        for transacao in self.registro.transacoes:
            print(transacao)
        print(f"\nSaldo: R$ {self.saldo:.2f}")

class ContaCorrente(Conta):
    def __init__(self, cliente, numero):
        super().__init__(cliente, numero)
        self.limite = 500.0
        self.limite_saques = 3
        self.saques_realizados = 0

    def sacar(self, valor):
        if self.saques_realizados >= self.limite_saques:
            print("Limite diário de saques alcançado.")
        elif valor > self.limite:
            print("Valor do saque ultrapassa o limite.")
        else:
            super().sacar(valor)
            self.saques_realizados += 1

def criar_cliente(usuarios):
    nome = input("Digite o nome do cliente: ")
    data_nascimento = input("Digite a data de nascimento (DD/MM/AAAA): ")
    cpf = input("Digite o CPF do cliente: ")
    endereco = input("Digite o endereço do cliente (logradouro, número - bairro - cidade/estado): ")
    cpf_numeros = ''.join(filter(str.isdigit, cpf))
    if any(u.cpf == cpf_numeros for u in usuarios):
        print("CPF já cadastrado!")
        return None
    return Cliente(nome, data_nascimento, cpf_numeros, endereco)

def cadastrar_conta(usuarios, contas):
    cpf = input("Digite o CPF do cliente para associar a conta: ")
    cpf_numeros = ''.join(filter(str.isdigit, cpf))
    cliente = next((u for u in usuarios if u.cpf == cpf_numeros), None)
    if cliente:
        numero_conta = len(contas) + 1
        conta = ContaCorrente(cliente, numero_conta)
        contas.append(conta)
        print(f"Conta criada com sucesso para o cliente {cliente.nome}!")
        return conta
    else:
        print("Cliente não encontrado!")

def listar_clientes(usuarios):
    if not usuarios:
        print("Não há clientes cadastrados.")
    else:
        print("Lista de Clientes:")
        for idx, cliente in enumerate(usuarios, start=1):
            print(f"{idx}. Nome: {cliente.nome} | CPF: {cliente.cpf} | Endereço: {cliente.endereco}")

def realizar_deposito(contas):
    if not contas:
        print("Não há contas cadastradas.")
        return

    numero_conta = int(input("Digite o número da conta para realizar o depósito: "))
    conta = next((c for c in contas if c.numero == numero_conta), None)
    if conta:
        valor_deposito = float(input('Informe o valor do depósito: '))
        conta.depositar(valor_deposito)
        print("Depósito realizado com sucesso!")
    else:
        print("Conta não encontrada.")

def realizar_saque(contas):
    if not contas:
        print("Não há contas cadastradas.")
        return

    numero_conta = int(input("Digite o número da conta para realizar o saque: "))
    conta = next((c for c in contas if c.numero == numero_conta), None)
    if conta:
        valor_saque = float(input("Informe o valor a ser sacado: "))
        conta.sacar(valor_saque)
    else:
        print("Conta não encontrada.")

def exibir_extrato(contas):
    if not contas:
        print("Não há contas cadastradas.")
        return

    numero_conta = int(input("Digite o número da conta para exibir o extrato: "))
    conta = next((c for c in contas if c.numero == numero_conta), None)
    if conta:
        conta.exibir_extrato()
    else:
        print("Conta não encontrada.")

def menu_principal():
    usuarios = []
    contas = []

    while True:
        print("\n===== MENU PRINCIPAL =====")
        print("1 - Criar cliente")
        print("2 - Criar conta")
        print("3 - Realizar depósito")
        print("4 - Realizar saque")
        print("5 - Exibir extrato")
        print("6 - Listar clientes")
        print("0 - Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            novo_cliente = criar_cliente(usuarios)
            if novo_cliente:
                usuarios.append(novo_cliente)
        elif opcao == "2":
            if usuarios:
                cadastrar_conta(usuarios, contas)
            else:
                print("Não há clientes cadastrados!")
        elif opcao == "3":
            realizar_deposito(contas)
        elif opcao == "4":
            realizar_saque(contas)
        elif opcao == "5":
            exibir_extrato(contas)
        elif opcao == "6":
            listar_clientes(usuarios)
        elif opcao == "0":
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    menu_principal()
