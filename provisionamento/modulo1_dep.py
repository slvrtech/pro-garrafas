"""
Módulo 1 — Cálculo de quantidade de R para a máquina DEP.

Regra de negócio:
    1. quantidade de garrafas = caixas a produzir × garrafas por caixa
       (do formato escolhido)
    2. quantidade de R = quantidade de garrafas / garrafas por R
       (do formato escolhido)
    3. o resultado é arredondado para cima (próximo número inteiro)
"""

from dataclasses import dataclass
from math import ceil

from constantes import FormatoGarrafa, obter_formato


@dataclass(frozen=True)
class ResultadoDEP:
    """Resultado detalhado do cálculo de R para a máquina DEP."""

    formato: FormatoGarrafa
    caixas: int
    garrafas_totais: int
    garrafas_por_r: int
    r_exato: float
    r_necessario: int

    def resumo(self) -> str:
        return (
            f"Formato: {self.formato.nome}\n"
            f"Caixas a produzir: {self.caixas}\n"
            f"Garrafas por caixa: {self.formato.unidades_por_caixa}\n"
            f"Total de garrafas: {self.garrafas_totais}\n"
            f"Garrafas por R: {self.garrafas_por_r}\n"
            f"R exato (sem arredondar): {self.r_exato:.4f}\n"
            f"R necessário (arredondado p/ cima): {self.r_necessario}"
        )


def calcular_r_dep(codigo_formato: str, caixas: int) -> ResultadoDEP:
    """Calcula a quantidade de R necessária para a máquina DEP.

    Args:
        codigo_formato: chave do formato em `constantes.FORMATOS`
            (ex.: "1000ml" ou "414ml").
        caixas: quantidade de caixas que serão produzidas. Deve ser
            um inteiro maior ou igual a zero.

    Returns:
        ResultadoDEP com todos os valores intermediários e o resultado
        final já arredondado para cima.

    Raises:
        ValueError: se o formato não existir ou se `caixas` for negativo.
    """
    if caixas < 0:
        raise ValueError("A quantidade de caixas não pode ser negativa.")

    formato = obter_formato(codigo_formato)

    garrafas_totais = caixas * formato.unidades_por_caixa
    r_exato = garrafas_totais / formato.garrafas_por_r
    r_necessario = ceil(r_exato)

    return ResultadoDEP(
        formato=formato,
        caixas=caixas,
        garrafas_totais=garrafas_totais,
        garrafas_por_r=formato.garrafas_por_r,
        r_exato=r_exato,
        r_necessario=r_necessario,
    )


if __name__ == "__main__":
    # Exemplo rápido de uso direto do módulo
    resultado = calcular_r_dep("1000ml", 500)
    print(resultado.resumo())
