# Provisionamento de Garrafas e Caixas

Sistema para cálculo de provisionamento e uso de garrafas e caixas de garrafas
em linha de engarrafamento, com um programa em Python e um site estático para
acesso interativo.

## 🔗 Site publicado

> Depois de ativar o GitHub Pages, cole aqui a URL gerada, por exemplo:
> `https://seuusuario.github.io/provisionamento-garrafas/`

## 📦 Premissas do negócio

| Formato | Garrafas por caixa | R por palete | Garrafas por R |
|---|---|---|---|
| 1000 ml | 6 | 7 | 217 |
| 414 ml | 12 | 8 | 440 |

Essas premissas estão centralizadas em [`provisionamento/constantes.py`](provisionamento/constantes.py)
e replicadas no site (`index.html`) para que os dois cálculos fiquem sempre consistentes.

## 🧮 Módulos disponíveis

### Módulo 1 — Quantidade de R para a máquina DEP
Calcula quantos "R" são necessários para atender uma produção:

```
garrafas totais   = caixas a produzir × garrafas por caixa
R necessário      = arredondar_para_cima(garrafas totais ÷ garrafas por R)
```

Implementado em [`provisionamento/modulo1_dep.py`](provisionamento/modulo1_dep.py).

### Módulo 2 — Garrafas provisionadas para a linha de produção
Calcula quantas garrafas estão provisionadas para a linha, considerando
sobras e retorno do dia anterior:

```
R total                = (paletes × R por palete) + R sobra do dia anterior
garrafas provisionadas = (R total × garrafas por R) + garrafas de retorno do dia anterior
```

Implementado em [`provisionamento/modulo2_provisionamento.py`](provisionamento/modulo2_provisionamento.py).

### Próximos módulos
- Módulo 3 — Uso & Consumo *(em breve)*

## 🖥️ Usando o site

O site (`index.html`) não precisa de instalação nem de servidor: é um arquivo
único em HTML/CSS/JavaScript. Basta abrir no navegador (localmente com duplo
clique, ou pela URL publicada no GitHub Pages).

1. Escolha o formato da garrafa (1000 ml ou 414 ml)
2. Informe a quantidade de caixas a produzir
3. Clique em **Calcular R**
4. Veja o resultado, o passo a passo do cálculo e a ocupação visual por palete

## 🐍 Usando o programa Python

Requer apenas Python 3.10+ (nenhuma dependência externa).

```bash
cd provisionamento
python main.py
```

O menu interativo guia pela escolha do módulo, formato e quantidade de caixas.

Também é possível usar as funções diretamente em outro script:

```python
from provisionamento.modulo1_dep import calcular_r_dep

resultado = calcular_r_dep("1000ml", caixas=500)
print(resultado.resumo())
```

## 📁 Estrutura do repositório

```
.
├── index.html                    # Site (front-end) — publicado via GitHub Pages
├── README.md
└── provisionamento/
    ├── constantes.py             # Premissas de negócio (formatos, caixas, paletes)
    ├── modulo1_dep.py            # Módulo 1: cálculo de R para a máquina DEP
    └── main.py                   # Menu de linha de comando
```

## ⚠️ Observação sobre o GitHub Pages

O GitHub Pages publica apenas arquivos estáticos. O `index.html` funciona
normalmente porque o cálculo do Módulo 1 é feito em JavaScript, no próprio
navegador. Os arquivos `.py` ficam disponíveis no repositório como
código-fonte, mas não são executados pelo site publicado.
