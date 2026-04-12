#  Simulação de Campos Magnéticos e definição de B

**Trabalho de Física - Tema: 28-1 Campos Magnéticos e a Definição de B**

##  Objetivo

Simular o comportamento de uma **partícula carregada** movendo-se em um **campo magnético uniforme**, demonstrando a **Força de Lorentz** através de uma interface interativa e dinâmica.

---

##  O Que É Simulado

### Força de Lorentz
A força magnética que atua sobre uma partícula carregada em movimento é dada por:

```
F = q(v × B)
```

Onde:
- **q** = carga da partícula (Coulombs)
- **v** = velocidade da partícula (m/s)
- **B** = campo magnético (Tesla)
- **×** = produto vetorial

Quando uma partícula carregada entra em um campo magnético perpendicular à sua velocidade, ela sofre uma **trajetória circular**.

### Parâmetros Calculados Automaticamente

1. **Raio de Curvatura (r)**
   ```
   r = (m × v) / (q × B)
   ```
   Quanto maior o raio, mais "aberta" é a trajetória.

2. **Frequência de Larmor (ω)**
   ```
   ω = q × B / m
   ```
   Frequência angular do movimento circular.

3. **Período (T)**
   ```
   T = 2π / ω
   ```
   Tempo para completar uma volta.

---


### Instalação de Dependências

```bash
pip install -r requirements.txt
```

### Executar a Simulação

```bash
python main.py
```

### Interface

A aplicação possui **dois painéis principais**:

#### Painel de Controles (Esquerda)
- **Sliders dinâmicos** para ajustar cada parâmetro
- Valores são **atualizados em tempo real** no gráfico
- **Informações calculadas** mostram raio, frequência e período

#### Painel de Visualização (Direita)
- **Gráfico interativo** da trajetória da partícula
- Ponto verde: posição inicial
- Estrela vermelha: posição final
- Pontos amarelos: representação do campo magnético

---

## Parâmetros Ajustáveis

| Parâmetro | Valor Padrão | Significado |
|-----------|-------------|-----------|
| **Carga (q)** | 1.6×10⁻¹⁹ C | Carga de um elétron |
| **Massa (m)** | 9.1×10⁻³¹ kg | Massa de um elétron |
| **Velocidade (v)** | 1×10⁶ m/s | Velocidade inicial da partícula |
| **Campo Magnético (B)** | 0.1 T | Intensidade do campo magnético |
| **Ângulo de Entrada** | 90° | Ângulo da velocidade inicial |
| **Tempo de Simulação** | 1×10⁻⁸ s | Duração da simulação |

---

## Exemplos de Uso

### Exemplo 1: Aumentar o Campo Magnético
- **Efeito**: Raio da órbita **diminui** (trajetória mais apertada)
- **Por quê**: r = mv / (qB) - quanto maior B, menor r

### Exemplo 2: Aumentar a Velocidade
- **Efeito**: Raio da órbita **aumenta**
- **Por quê**: r = mv / (qB) - quanto maior v, maior r

### Exemplo 3: Mudar o Ângulo de Entrada
- **Efeito**: Forma da trajetória muda
- **90°**: Movimento circular perfeito
- **0° ou 180°**: Sem deflexão (movimento reto)

---

## Física Envolvida

### O Que É Um Campo Magnético?

Um **campo magnético** é uma grandeza vetorial que exerce força em partículas carregadas em movimento. Representado por:
- **B** = intensidade (Tesla)
- **Direção** = perpendicular ao plano de simulação

### A Força Magnética

Diferente da força elétrica, a **força magnética**:
-  Age perpendicularmente à velocidade
-  Não realiza trabalho (energia cinética constante)
-  Causa mudança na **direção**, não na **velocidade**
-  Atua apenas em partículas em movimento

### Trajetória Circular

A força magnética atua como **força centrípeta**:
```
qvB = mv² / r

r = mv / (qB)
```

Portanto, a partícula se move em um **círculo** com velocidade constante.

---


- **Tema**: Dark Mode (TkBootstrap - Darkly)
- **Cores**:
  - 🟦 Cyan: Trajetória e valores de controle
  - 🟢 Verde: Informações calculadas
  - 🟥 Vermelho: Posição final
  - 🟨 Amarelo: Campo magnético

---

## Possíveis Extensões

1. **Adicionar campo elétrico** (combinação E e B)
2. **Múltiplas partículas** com cargas diferentes
3. **Campo magnético não-uniforme**
4. **Gráficos adicionais** (velocidade vs tempo, energia)
5. **Exportar dados** para análise

---

## Referências

- Halliday, Resnick & Walker - Fundamentos de Física
- Griffiths - Introduction to Electrodynamics
- Khan Academy - Magnetic Force on Moving Charges

---

**Desenvolvido com Python + Tkinter + Matplotlib**
