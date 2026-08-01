"""
Constantes de referência para o sistema de provisionamento de garrafas.

Qualquer alteração de premissas do negócio (unidades por caixa, garrafas
por R, quantidade de R por palete etc.) deve ser feita apenas neste
arquivo, para manter os módulos de cálculo desacoplados das regras.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class FormatoGarrafa:
    """Representa as regras de empacotamento de um formato de garrafa."""

    nome: str                  # rótulo do formato, ex: "1000 ml"
    volume_ml: int              # volume unitário da garrafa, em ml
    unidades_por_caixa: int     # quantidade de garrafas em uma caixa
    r_por_palete: int           # quantidade de "R" que compõem um palete
    garrafas_por_r: int         # quantidade de garrafas em cada "R"

    @property
    def garrafas_por_palete(self) -> int:
        return self.r_por_palete * self.garrafas_por_r


# Catálogo central dos formatos suportados hoje.
# Para adicionar um novo formato de garrafa, basta incluir uma nova
# entrada aqui — os módulos de cálculo já sabem lidar com qualquer
# formato cadastrado neste dicionário.
FORMATOS: dict[str, FormatoGarrafa] = {
    "1000ml": FormatoGarrafa(
        nome="1000 ml",
        volume_ml=1000,
        unidades_por_caixa=6,
        r_por_palete=7,
        garrafas_por_r=217,
    ),
    "414ml": FormatoGarrafa(
        nome="414 ml",
        volume_ml=414,
        unidades_por_caixa=12,
        r_por_palete=8,
        garrafas_por_r=440,
    ),
}


def obter_formato(codigo: str) -> FormatoGarrafa:
    """Busca um formato pelo código (ex: '1000ml' ou '414ml').

    Lança ValueError com uma mensagem amigável se o código não existir,
    para que as camadas de CLI/web possam apenas repassar a mensagem.
    """
    try:
        return FORMATOS[codigo]
    except KeyError as exc:
        disponiveis = ", ".join(FORMATOS.keys())
        raise ValueError(
            f"Formato de garrafa '{codigo}' não reconhecido. "
            f"Formatos disponíveis: {disponiveis}."
        ) from exc
