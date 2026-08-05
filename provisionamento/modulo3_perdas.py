"""
Módulo 3 — Cálculo de garrafas retornadas no dia de produção.

Regra de negócio:
    1. garrafas produzidas = caixas produzidas × garrafas por caixa (do formato)
    2. SE o provisionamento do dia foi formado por mais de um lote
       (Módulo 2), primeiro se subtrai a quantidade de garrafas do
       PRIMEIRO lote das garrafas produzidas:
           garrafas produzidas (ajustada) = garrafas produzidas - garrafas do 1º lote
       Caso contrário (um único lote, ou a informação não se aplica),
       a quantidade de garrafas produzidas permanece a original.
    3. garrafas retornadas = garrafas provisionadas para a linha
                              - garrafas produzidas (ajustada)
                              - GR-Volta (garrafas retornadas do dia, se houver)

"GR-Volta" é a quantidade de garrafas que retornaram no próprio dia e
entra como uma subtração no cálculo. "Garrafas retornadas" (o resultado
final) representa o que foi provisionado mas não foi nem embalado em
caixas, nem contabilizado no GR-Volta.
"""

from dataclasses import dataclass

from constantes import FormatoGarrafa, obter_formato


@dataclass(frozen=True)
class ResultadoRetorno:
    """Resultado detalhado do cálculo de garrafas retornadas."""

    formato: FormatoGarrafa
    caixas_produzidas: int
    garrafas_produzidas: int
    garrafas_primeiro_lote: int
    garrafas_produzidas_ajustada: int
    garrafas_provisionadas: int
    gr_volta: int
    garrafas_retornadas: int

    @property
    def ajuste_aplicado(self) -> bool:
        """True quando a subtração do 1º lote foi aplicada (provisionamento
        formado por mais de um lote)."""
        return self.garrafas_primeiro_lote > 0

    @property
    def inconsistente(self) -> bool:
        """True quando o resultado é negativo — sinal de que algum dos
        valores informados está incorreto."""
        return self.garrafas_retornadas < 0

    def resumo(self) -> str:
        linhas = [
            f"Formato: {self.formato.nome}",
            f"Caixas produzidas: {self.caixas_produzidas}",
            f"Garrafas por caixa: {self.formato.unidades_por_caixa}",
            f"Garrafas produzidas (caixas × un./caixa): {self.garrafas_produzidas}",
        ]
        if self.ajuste_aplicado:
            linhas.append(
                f"- Garrafas do 1º lote (mais de um lote no provisionamento): "
                f"{self.garrafas_primeiro_lote}"
            )
            linhas.append(
                f"Garrafas produzidas (ajustada): {self.garrafas_produzidas_ajustada}"
            )
        linhas.append(f"Garrafas provisionadas para a linha: {self.garrafas_provisionadas}")
        linhas.append(f"GR-Volta (garrafas retornadas no dia): {self.gr_volta}")
        linhas.append(f"Garrafas Retornadas (resultado final): {self.garrafas_retornadas}")
        if self.inconsistente:
            linhas.append(
                "AVISO: resultado negativo — a soma de garrafas produzidas "
                "(ajustada) e GR-Volta é maior do que o provisionado. "
                "Confira os valores informados."
            )
        return "\n".join(linhas)


def calcular_garrafas_retornadas(
    codigo_formato: str,
    caixas_produzidas: int,
    garrafas_provisionadas: int,
    gr_volta: int = 0,
    garrafas_primeiro_lote: int = 0,
) -> ResultadoRetorno:
    """Calcula a quantidade de garrafas retornadas no dia de produção.

    Args:
        codigo_formato: chave do formato em `constantes.FORMATOS`
            (ex.: "1000ml" ou "414ml").
        caixas_produzidas: quantidade de caixas efetivamente produzidas
            no dia. Deve ser um inteiro maior ou igual a zero.
        garrafas_provisionadas: total de garrafas provisionadas para a
            linha de produção no dia (normalmente o total do Módulo 2,
            somando todos os lotes). Deve ser um inteiro maior ou
            igual a zero.
        gr_volta: quantidade de garrafas retornadas no dia (GR-Volta),
            se houver (0 caso não haja retorno).
        garrafas_primeiro_lote: quantidade de garrafas provisionadas
            apenas no PRIMEIRO lote do dia (Módulo 2). Informe este
            valor SOMENTE quando o provisionamento do dia foi formado
            por mais de um lote — nesse caso, ele é subtraído das
            garrafas produzidas antes do cálculo final. Deixe em 0 se
            houve um único lote (ou se a informação não existir).

    Returns:
        ResultadoRetorno com todos os valores intermediários e o
        resultado final de garrafas retornadas.

    Raises:
        ValueError: se o formato não existir ou se algum dos valores
            numéricos for negativo.
    """
    if caixas_produzidas < 0:
        raise ValueError("A quantidade de caixas produzidas não pode ser negativa.")
    if garrafas_provisionadas < 0:
        raise ValueError("A quantidade de garrafas provisionadas não pode ser negativa.")
    if gr_volta < 0:
        raise ValueError("O GR-Volta (garrafas retornadas no dia) não pode ser negativo.")
    if garrafas_primeiro_lote < 0:
        raise ValueError("A quantidade de garrafas do primeiro lote não pode ser negativa.")

    formato = obter_formato(codigo_formato)

    garrafas_produzidas = caixas_produzidas * formato.unidades_por_caixa

    if garrafas_primeiro_lote > 0:
        garrafas_produzidas_ajustada = garrafas_produzidas - garrafas_primeiro_lote
    else:
        garrafas_produzidas_ajustada = garrafas_produzidas

    garrafas_retornadas = (
        garrafas_provisionadas - garrafas_produzidas_ajustada - gr_volta
    )

    return ResultadoRetorno(
        formato=formato,
        caixas_produzidas=caixas_produzidas,
        garrafas_produzidas=garrafas_produzidas,
        garrafas_primeiro_lote=garrafas_primeiro_lote,
        garrafas_produzidas_ajustada=garrafas_produzidas_ajustada,
        garrafas_provisionadas=garrafas_provisionadas,
        gr_volta=gr_volta,
        garrafas_retornadas=garrafas_retornadas,
    )


if __name__ == "__main__":
    # Exemplo 1: provisionamento com um único lote (sem ajuste)
    r1 = calcular_garrafas_retornadas(
        "1000ml",
        caixas_produzidas=2600,
        garrafas_provisionadas=15961,
        gr_volta=50,
    )
    print(r1.resumo())
    print()

    # Exemplo 2: provisionamento com mais de um lote (com ajuste)
    r2 = calcular_garrafas_retornadas(
        "1000ml",
        caixas_produzidas=2600,
        garrafas_provisionadas=15961,
        gr_volta=50,
        garrafas_primeiro_lote=9885,
    )
    print(r2.resumo())
