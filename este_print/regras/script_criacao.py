import re

def criar_arquivo_regra(nome_arquivo, conteudo):
    with open(nome_arquivo, 'w') as arquivo:
        for linha in conteudo:
            if 'commands' not in linha:
                # Remover a parte de definição da regra
                if linha.startswith('rule'):
                    continue
                # Remover espaços no início de cada linha
                linha_formatada = linha.strip()
                arquivo.write(linha_formatada + '\n')  # Adicionei '\n' para manter a quebra de linha

def main():
    with open('descricao.txt', 'r') as arquivo_origem:
        linhas = arquivo_origem.readlines()

    regras = []
    regra_atual = []

    for linha in linhas:
        if linha.startswith('rule'):
            if regra_atual:
                regras.append(regra_atual)
                regra_atual = []
        regra_atual.append(linha)

    if regra_atual:
        regras.append(regra_atual)

    for i, regra in enumerate(regras, start=1):
        nome_arquivo = f"{i}-{regra[0].split()[1][:-1]}.req"
        criar_arquivo_regra(nome_arquivo, regra)

if __name__ == "__main__":
    main()