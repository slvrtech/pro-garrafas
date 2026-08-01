"""
Módulo 2 — Cálculo de garrafas provisionadas para a linha de produção.

Regra de negócio:
    1. R total = (quantidade de paletes × R por palete do formato)
                 + R que sobraram do dia anterior
    2. garrafas provisionadas = (R total × garrafas por R)
                 + garrafas de retorno do dia anterior (se existirem)
"""

from dataclasses import dataclass

from constantes import FormatoGarrafa, obter_formato


@dataclass(frozen=True)
class ResultadoProvisionamento:
    """Resultado detalhado do cálculo de garrafas provisionadas."""

    formato: FormatoGarrafa
    paletes: int
    r_por_palete: int
    r_sobra_dia_anterior: int
    r_total: int
    garrafas_por_r: int
    garrafas_calculadas: int
    garrafas_retorno_dia_anterior: int
    garrafas_provisionadas: int

    def resumo(self) -> str:
        return (
            f"Formato: {self.formato.nome}\n"
            f"Paletes informados: {self.paletes}\n"
            f"R por palete: {self.r_por_palete}\n"
            f"R que sobraram do dia anterior: {self.r_sobra_dia_anterior}\n"
            f"R total: {self.r_total}\n"
            f"Garrafas por R: {self.garrafas_por_r}\n"
            f"Garrafas calculadas (R total × garrafas/R): {self.garrafas_calculadas}\n"
            f"Garrafas de retorno do dia anterior: {self.garrafas_retorno_dia_anterior}\n"
            f"Garrafas provisionadas (resultado final): {self.garrafas_provisionadas}"
        )


def calcular_garrafas_provisionadas(
    codigo_formato: str,
    paletes: int,
    r_sobra_dia_anterior: int = 0,
    garrafas_retorno_dia_anterior: int = 0,
) -> ResultadoProvisionamento:
    """Calcula a quantidade de garrafas provisionadas para a linha de produção.

    Args:
        codigo_formato: chave do formato em `constantes.FORMATOS`
            (ex.: "1000ml" ou "414ml").
        paletes: quantidade de paletes provisionados no dia. Deve ser
            um inteiro maior ou igual a zero.
        r_sobra_dia_anterior: quantidade de R que sobraram do dia
            anterior (0 se não houver sobra).
        garrafas_retorno_dia_anterior: quantidade de garrafas de
            retorno do dia anterior (0 se não houver retorno).

    Returns:
        ResultadoProvisionamento com todos os valores intermediários e
        o resultado final de garrafas provisionadas.

    Raises:
        ValueError: se o formato não existir ou se algum dos valores
            numéricos for negativo.
    """
    if paletes < 0:
        raise ValueError("A quantidade de paletes não pode ser negativa.")
    if r_sobra_dia_anterior < 0:
        raise ValueError("A sobra de R do dia anterior não pode ser negativa.")
    if garrafas_retorno_dia_anterior < 0:
        raise ValueError("As garrafas de retorno não podem ser negativas.")

    formato = obter_formato(codigo_formato)

    r_total = (paletes * formato.r_por_palete) + r_sobra_dia_anterior
    garrafas_calculadas = r_total * formato.garrafas_por_r
    garrafas_provisionadas = garrafas_calculadas + garrafas_retorno_dia_anterior

    return ResultadoProvisionamento(
        formato=formato,
        paletes=paletes,
        r_por_palete=formato.r_por_palete,
        r_sobra_dia_anterior=r_sobra_dia_anterior,
        r_total=r_total,
        garrafas_por_r=formato.garrafas_por_r,
        garrafas_calculadas=garrafas_calculadas,
        garrafas_retorno_dia_anterior=garrafas_retorno_dia_anterior,
        garrafas_provisionadas=garrafas_provisionadas,
    )


if __name__ == "__main__":
    # Exemplo rápido de uso direto do módulo
    resultado = calcular_garrafas_provisionadas(
        "1000ml", paletes=10, r_sobra_dia_anterior=3, garrafas_retorno_dia_anterior=120
    )
    print(resultado.resumo())
