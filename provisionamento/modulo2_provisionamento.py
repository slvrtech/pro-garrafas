"""
Módulo 2 — Cálculo de garrafas provisionadas para a linha de produção.

O provisionamento do dia pode ser formado por um ou mais lotes de
paletes, cada um identificado por um código. O cálculo é feito
separadamente para cada lote:

    R do lote        = quantidade de paletes do lote × R por palete do formato
    garrafas do lote  = R do lote × garrafas por R do formato

A sobra de R e as garrafas de retorno do dia anterior são aplicadas
uma única vez, somente no PRIMEIRO lote informado:

    R do primeiro lote        += R que sobraram do dia anterior
    garrafas do primeiro lote += garrafas de retorno do dia anterior
"""

from dataclasses import dataclass
from typing import List

from constantes import FormatoGarrafa, obter_formato


@dataclass(frozen=True)
class LotePalete:
    """Um lote de paletes informado pelo usuário (código + quantidade)."""

    codigo: str
    paletes: int


@dataclass(frozen=True)
class ResultadoLote:
    """Resultado do cálculo de garrafas provisionadas para um único lote."""

    codigo_lote: str
    paletes: int
    r_por_palete: int
    r_sobra_aplicada: int
    r_total: int
    garrafas_por_r: int
    garrafas_calculadas: int
    garrafas_retorno_aplicada: int
    garrafas_provisionadas: int

    def resumo(self) -> str:
        linhas = [
            f"Lote: {self.codigo_lote}",
            f"  Paletes: {self.paletes} × {self.r_por_palete} R/palete = "
            f"{self.paletes * self.r_por_palete} R",
        ]
        if self.r_sobra_aplicada:
            linhas.append(f"  + R sobra do dia anterior: {self.r_sobra_aplicada}")
        linhas.append(f"  R total do lote: {self.r_total}")
        linhas.append(
            f"  Garrafas: {self.r_total} × {self.garrafas_por_r} garrafas/R = "
            f"{self.garrafas_calculadas}"
        )
        if self.garrafas_retorno_aplicada:
            linhas.append(
                f"  + Garrafas de retorno do dia anterior: {self.garrafas_retorno_aplicada}"
            )
        linhas.append(f"  Garrafas provisionadas do lote: {self.garrafas_provisionadas}")
        return "\n".join(linhas)


@dataclass(frozen=True)
class ResultadoProvisionamentoLotes:
    """Resultado consolidado do provisionamento por lotes."""

    formato: FormatoGarrafa
    lotes: List[ResultadoLote]

    @property
    def total_paletes(self) -> int:
        return sum(lote.paletes for lote in self.lotes)

    @property
    def total_r(self) -> int:
        return sum(lote.r_total for lote in self.lotes)

    @property
    def total_garrafas_provisionadas(self) -> int:
        return sum(lote.garrafas_provisionadas for lote in self.lotes)

    def resumo(self) -> str:
        partes = [f"Formato: {self.formato.nome}", ""]
        for lote in self.lotes:
            partes.append(lote.resumo())
            partes.append("")
        partes.append("--- Totais do dia ---")
        partes.append(f"Total de paletes: {self.total_paletes}")
        partes.append(f"Total de R: {self.total_r}")
        partes.append(f"Total de garrafas provisionadas: {self.total_garrafas_provisionadas}")
        return "\n".join(partes)


def calcular_garrafas_provisionadas_por_lotes(
    codigo_formato: str,
    lotes: List[LotePalete],
    r_sobra_dia_anterior: int = 0,
    garrafas_retorno_dia_anterior: int = 0,
) -> ResultadoProvisionamentoLotes:
    """Calcula as garrafas provisionadas, separadas por lote de paletes.

    A sobra de R e o retorno de garrafas do dia anterior são aplicados
    apenas ao último lote da lista.

    Args:
        codigo_formato: chave do formato em `constantes.FORMATOS`
            (ex.: "1000ml" ou "414ml").
        lotes: lista de lotes (código + quantidade de paletes), na
            ordem em que devem ser considerados. Deve conter ao menos
            um lote.
        r_sobra_dia_anterior: R que sobraram do dia anterior, aplicado
            somente ao primeiro lote (0 se não houver sobra).
        garrafas_retorno_dia_anterior: garrafas de retorno do dia
            anterior, aplicado somente ao primeiro lote (0 se não
            houver retorno).

    Returns:
        ResultadoProvisionamentoLotes com o detalhamento de cada lote
        e os totais consolidados do dia.

    Raises:
        ValueError: se não houver lotes, se algum código de lote for
            vazio, se algum valor numérico for negativo, ou se o
            formato não existir.
    """
    if not lotes:
        raise ValueError("Informe ao menos um lote de paletes.")
    if r_sobra_dia_anterior < 0:
        raise ValueError("A sobra de R do dia anterior não pode ser negativa.")
    if garrafas_retorno_dia_anterior < 0:
        raise ValueError("As garrafas de retorno não podem ser negativas.")

    formato = obter_formato(codigo_formato)

    resultados: List[ResultadoLote] = []
    indice_primeiro = 0

    for i, lote in enumerate(lotes):
        if not lote.codigo or not lote.codigo.strip():
            raise ValueError("Todo lote precisa de um código.")
        if lote.paletes < 0:
            raise ValueError(
                f"A quantidade de paletes do lote '{lote.codigo}' não pode ser negativa."
            )

        e_primeiro_lote = i == indice_primeiro
        r_sobra_aplicada = r_sobra_dia_anterior if e_primeiro_lote else 0
        garrafas_retorno_aplicada = garrafas_retorno_dia_anterior if e_primeiro_lote else 0

        r_total = (lote.paletes * formato.r_por_palete) + r_sobra_aplicada
        garrafas_calculadas = r_total * formato.garrafas_por_r
        garrafas_provisionadas = garrafas_calculadas + garrafas_retorno_aplicada

        resultados.append(
            ResultadoLote(
                codigo_lote=lote.codigo,
                paletes=lote.paletes,
                r_por_palete=formato.r_por_palete,
                r_sobra_aplicada=r_sobra_aplicada,
                r_total=r_total,
                garrafas_por_r=formato.garrafas_por_r,
                garrafas_calculadas=garrafas_calculadas,
                garrafas_retorno_aplicada=garrafas_retorno_aplicada,
                garrafas_provisionadas=garrafas_provisionadas,
            )
        )

    return ResultadoProvisionamentoLotes(formato=formato, lotes=resultados)


if __name__ == "__main__":
    # Exemplo rápido de uso direto do módulo
    resultado = calcular_garrafas_provisionadas_por_lotes(
        "1000ml",
        lotes=[
            LotePalete(codigo="LOTE-A", paletes=6),
            LotePalete(codigo="LOTE-B", paletes=4),
        ],
        r_sobra_dia_anterior=3,
        garrafas_retorno_dia_anterior=120,
    )
    print(resultado.resumo())
