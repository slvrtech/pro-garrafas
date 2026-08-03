"""
Módulo 3 — Cálculo de garrafas perdidas no dia de produção.

Regra de negócio:
    1. garrafas utilizadas = caixas produzidas × garrafas por caixa (do formato)
    2. garrafas perdidas   = garrafas provisionadas para a linha
                              - garrafas utilizadas
                              - garrafas retornadas (se houver)

"Garrafas perdidas" representa o que foi provisionado mas não foi nem
embalado em caixas, nem retornado — ou seja, garrafas quebradas ou
jogadas fora ao longo do dia de produção.
"""

from dataclasses import dataclass

from constantes import FormatoGarrafa, obter_formato


@dataclass(frozen=True)
class ResultadoPerdas:
    """Resultado detalhado do cálculo de garrafas perdidas."""

    formato: FormatoGarrafa
    caixas_produzidas: int
    garrafas_utilizadas: int
    garrafas_provisionadas: int
    garrafas_retornadas: int
    garrafas_perdidas: int

    @property
    def inconsistente(self) -> bool:
        """True quando o resultado é negativo, ou seja, quando a soma de
        garrafas utilizadas + retornadas é maior do que o provisionado —
        sinal de que algum dos valores informados está incorreto."""
        return self.garrafas_perdidas < 0

    def resumo(self) -> str:
        linhas = [
            f"Formato: {self.formato.nome}",
            f"Caixas produzidas: {self.caixas_produzidas}",
            f"Garrafas por caixa: {self.formato.unidades_por_caixa}",
            f"Garrafas utilizadas (caixas × un./caixa): {self.garrafas_utilizadas}",
            f"Garrafas provisionadas para a linha: {self.garrafas_provisionadas}",
            f"Garrafas retornadas: {self.garrafas_retornadas}",
            f"Garrafas perdidas (quebradas/jogadas fora): {self.garrafas_perdidas}",
        ]
        if self.inconsistente:
            linhas.append(
                "AVISO: resultado negativo — a soma de garrafas utilizadas e "
                "retornadas é maior do que o provisionado. Confira os valores informados."
            )
        return "\n".join(linhas)


def calcular_garrafas_perdidas(
    codigo_formato: str,
    caixas_produzidas: int,
    garrafas_provisionadas: int,
    garrafas_retornadas: int = 0,
) -> ResultadoPerdas:
    """Calcula a quantidade de garrafas perdidas no dia de produção.

    Args:
        codigo_formato: chave do formato em `constantes.FORMATOS`
            (ex.: "1000ml" ou "414ml").
        caixas_produzidas: quantidade de caixas efetivamente produzidas
            no dia. Deve ser um inteiro maior ou igual a zero.
        garrafas_provisionadas: total de garrafas provisionadas para a
            linha de produção no dia (normalmente o resultado do
            Módulo 2). Deve ser um inteiro maior ou igual a zero.
        garrafas_retornadas: quantidade de garrafas retornadas no dia,
            se houver (0 caso não haja retorno).

    Returns:
        ResultadoPerdas com todos os valores intermediários e o
        resultado final de garrafas perdidas.

    Raises:
        ValueError: se o formato não existir ou se algum dos valores
            numéricos for negativo.
    """
    if caixas_produzidas < 0:
        raise ValueError("A quantidade de caixas produzidas não pode ser negativa.")
    if garrafas_provisionadas < 0:
        raise ValueError("A quantidade de garrafas provisionadas não pode ser negativa.")
    if garrafas_retornadas < 0:
        raise ValueError("A quantidade de garrafas retornadas não pode ser negativa.")

    formato = obter_formato(codigo_formato)

    garrafas_utilizadas = caixas_produzidas * formato.unidades_por_caixa
    garrafas_perdidas = garrafas_provisionadas - garrafas_utilizadas - garrafas_retornadas

    return ResultadoPerdas(
        formato=formato,
        caixas_produzidas=caixas_produzidas,
        garrafas_utilizadas=garrafas_utilizadas,
        garrafas_provisionadas=garrafas_provisionadas,
        garrafas_retornadas=garrafas_retornadas,
        garrafas_perdidas=garrafas_perdidas,
    )


if __name__ == "__main__":
    # Exemplo rápido de uso direto do módulo
    resultado = calcular_garrafas_perdidas(
        "1000ml",
        caixas_produzidas=2600,
        garrafas_provisionadas=15961,
        garrafas_retornadas=50,
    )
    print(resultado.resumo())
