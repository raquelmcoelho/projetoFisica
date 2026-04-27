# Simulação de Campos Magnéticos e Definição de B (Cap. 28-1)

**Trabalho de Física - Eletromagnetismo** **Baseado no livro:** *Halliday, Resnick & Walker - 10ª Edição*

## Objetivo
Este software simula a interação entre uma partícula carregada e um **campo magnético uniforme**. O objetivo é demonstrar visualmente como a **Força de Lorentz** atua como uma força centrípeta, criando trajetórias circulares ou helicoidais (em hélice).

---

## O Que é Simulado?

Diferente de um campo elétrico, o campo magnético só exerce força em cargas que possuem **velocidade**. O simulador utiliza a decomposição do movimento em duas perspectivas para facilitar o entendimento:

1.  **Vista de Cima (Plano XY):** Foca no movimento de rotação (giro).
2.  **Vista Lateral (Plano YZ):** Revela o avanço da partícula, mostrando a formação da hélice.

### A Força de Lorentz
A base matemática do projeto é:
```math
\vec{F}_B = q(\vec{v} \times \vec{B})
```

Onde a força resultante ($\vec{F}_B$) é sempre perpendicular à velocidade ($\vec{v}$) e ao campo ($\vec{B}$).

---

## Como as Variáveis Influenciam o Gráfico?

Para entender o comportamento da partícula, observe como cada slider altera a física do sistema:

### 1. Carga ($q$)
* **Influência no Raio:** Quanto maior a carga, **menor** o raio (o giro fica mais "apertado").
* **Influência no Sentido:** Se a carga for **positiva** (Próton), ela gira para um lado. Se for **negativa** (Elétron), o sentido de giro inverte instantaneamente.
* **Fórmula:** $R \propto 1/q$

### 2. Velocidade ($v$) e Ângulo ($\phi$)
* **Influência no Raio:** Aumentar a velocidade torna o raio **maior**, pois a partícula ganha mais inércia para "fugir" da curva.
* **Ângulo de Entrada ($\phi$):** É o ângulo entre a velocidade e o campo.
    * Em **90°**: O movimento é um círculo perfeito (toda a velocidade é usada para girar).
    * Menor que **90°**: Surge a hélice. Uma parte da velocidade faz girar e a outra faz a partícula avançar.
* **Fórmula:** $R = \frac{m \cdot v \cdot \sin(\phi)}{q \cdot B}$

### 3. Campo Magnético ($B$)
* **Influência no Raio:** Quanto mais forte o campo, **menor** o raio. O campo magnético "obriga" a partícula a curvar com mais força.
* **No Gráfico:** Representado pelo símbolo $\otimes$ (entrando na tela) no plano XY.
* **Fórmula:** $R \propto 1/B$

---

## Interface e Legendas

A aplicação é dividida em 3 colunas estratégicas:

* **Coluna 1 (Cálculos):** Mostra a substituição dos valores reais na fórmula do Halliday. Útil para provar que a teoria bate com o desenho.
* **Coluna 2 (Plano XY):**
    * **Seta Verde:** Vetor Velocidade ($\vec{v}$).
    * **Seta Vermelha:** Vetor Força Magnética ($\vec{F}_B$). Note que ela aponta sempre para o **centro do círculo**.
* **Coluna 3 (Plano YZ):** Mostra a inclinação da entrada ($\phi$) e como a hélice se estica conforme o ângulo diminui.

---

## Instalação e Execução

### Dependências
Certifique-se de ter o Python instalado e as seguintes bibliotecas:
```bash
pip install numpy matplotlib ttkbootstrap
```

### Como rodar
```bash
python main.py
```

---

## Referências
* **Halliday, D., Resnick, R., Walker, J.** *Fundamentos de Física*, Vol. 3 (Eletromagnetismo).
* **Tópico:** 28-1 O que é um Campo Magnético e sua Definição.
