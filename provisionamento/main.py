"""
Programa de Provisionamento e Uso de Garrafas e Caixas
=======================================================

Ponto de entrada em linha de comando. Cada módulo de cálculo do negócio
vive em seu próprio arquivo (ex.: `modulo1_dep.py`) e é conectado aqui
por um item de menu — isso mantém o programa fácil de estender conforme
novos módulos forem sendo adicionados.

Uso:
    python main.py
"""

from constantes import FORMATOS
from modulo1_dep import calcular_r_dep
from modulo2_provisionamento import calcular_garrafas_provisionadas


def escolher_formato() -> str:
    print("\nFormatos de garrafa disponíveis:")
    codigos = list(FORMATOS.keys())
    for i, codigo in enumerate(codigos, start=1):
        f = FORMATOS[codigo]
        print(f"  {i}. {f.nome}  ({f.unidades_por_caixa} un/caixa, "
              f"{f.garrafas_por_r} garrafas/R, {f.r_por_palete} R/palete)")

    while True:
        escolha = input("Escolha o formato (número): ").strip()
        if escolha.isdigit() and 1 <= int(escolha) <= len(codigos):
            return codigos[int(escolha) - 1]
        print("Opção inválida, tente novamente.")


def ler_inteiro_nao_negativo(mensagem: str) -> int:
    while True:
        valor = input(mensagem).strip().replace(".", "")
        if valor.isdigit():
            return int(valor)
        print("Digite um número inteiro válido (>= 0).")


def modulo1_menu() -> None:
    print("\n=== Módulo 1: Quantidade de R para a máquina DEP ===")
    codigo_formato = escolher_formato()
    caixas = ler_inteiro_nao_negativo("Quantidade de caixas a produzir: ")

    resultado = calcular_r_dep(codigo_formato, caixas)

    print("\n--- Resultado ---")
    print(resultado.resumo())


def modulo2_menu() -> None:
    print("\n=== Módulo 2: Garrafas provisionadas para a linha de produção ===")
    codigo_formato = escolher_formato()
    paletes = ler_inteiro_nao_negativo("Quantidade de paletes: ")
    r_sobra = ler_inteiro_nao_negativo(
        "R que sobraram do dia anterior (0 se não houver): "
    )
    garrafas_retorno = ler_inteiro_nao_negativo(
        "Garrafas de retorno do dia anterior (0 se não houver): "
    )

    resultado = calcular_garrafas_provisionadas(
        codigo_formato, paletes, r_sobra, garrafas_retorno
    )

    print("\n--- Resultado ---")
    print(resultado.resumo())


def menu_principal() -> None:
    opcoes = {
        "1": ("Módulo 1 — Quantidade de R para a máquina DEP", modulo1_menu),
        "2": ("Módulo 2 — Garrafas provisionadas para a linha de produção", modulo2_menu),
        # Próximos módulos serão adicionados aqui.
    }

    while True:
        print("\n===============================================")
        print(" Provisionamento e Uso de Garrafas e Caixas")
        print("===============================================")
        for chave, (titulo, _) in opcoes.items():
            print(f"  {chave}. {titulo}")
        print("  0. Sair")

        escolha = input("Escolha uma opção: ").strip()
        if escolha == "0":
            print("Encerrando. Até a próxima!")
            break
        if escolha in opcoes:
            _, funcao = opcoes[escolha]
            funcao()
        else:
            print("Opção inválida, tente novamente.")


if __name__ == "__main__":
    menu_principal()
