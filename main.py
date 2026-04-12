import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
import ttkbootstrap as ttk_bs
from ttkbootstrap.constants import *

class SimuladorCampoMagnetico:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulação de Campos Magnéticos - Força de Lorentz")
        self.root.geometry("1400x800")
        
        # Configuração de cores (tema dark bootstrap)
        style = ttk_bs.Style(theme="darkly")
        
        # Variáveis de controle
        self.carga = tk.DoubleVar(value=1.6e-19)  # Carga do elétron (C)
        self.massa = tk.DoubleVar(value=9.1e-31)   # Massa do elétron (kg)
        self.velocidade = tk.DoubleVar(value=1e6)  # Velocidade (m/s)
        self.campo_b = tk.DoubleVar(value=0.1)     # Campo magnético (T)
        self.angulo = tk.DoubleVar(value=90)       # Ângulo de entrada (graus)
        self.tempo_sim = tk.DoubleVar(value=1e-8)  # Tempo de simulação (s)
        
        self.animando = False
        self.trajetoria_x = []
        self.trajetoria_y = []
        
        self._criar_layout()
        self._criar_grafico()
        
    def _criar_layout(self):
        """Cria o layout principal da aplicação"""
        
        # Container principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        # ========== PAINEL DE CONTROLES (Esquerda) ==========
        controle_frame = ttk.LabelFrame(main_frame, text="⚙️ PARÂMETROS DE SIMULAÇÃO", padding=15)
        controle_frame.pack(side=LEFT, fill=BOTH, padx=(0, 10), pady=10)
        
        # Carga da Partícula
        ttk.Label(controle_frame, text="Carga (C):", font=("Helvetica", 10, "bold")).pack(anchor=W, pady=(10, 5))
        carga_scale = ttk.Scale(controle_frame, from_=1e-20, to=1e-18, variable=self.carga, 
                               orient=HORIZONTAL, command=lambda x: self._atualizar_grafico())
        carga_scale.pack(fill=X, pady=(0, 5))
        self.carga_label = ttk.Label(controle_frame, text=f"1.6e-19 C", foreground="cyan")
        self.carga_label.pack(anchor=W, pady=(0, 10))
        self.carga.trace("w", self._atualizar_labels)
        
        # Massa da Partícula
        ttk.Label(controle_frame, text="Massa (kg):", font=("Helvetica", 10, "bold")).pack(anchor=W, pady=(10, 5))
        massa_scale = ttk.Scale(controle_frame, from_=1e-31, to=1e-29, variable=self.massa, 
                               orient=HORIZONTAL, command=lambda x: self._atualizar_grafico())
        massa_scale.pack(fill=X, pady=(0, 5))
        self.massa_label = ttk.Label(controle_frame, text=f"9.1e-31 kg", foreground="cyan")
        self.massa_label.pack(anchor=W, pady=(0, 10))
        self.massa.trace("w", self._atualizar_labels)
        
        # Velocidade Inicial
        ttk.Label(controle_frame, text="Velocidade (m/s):", font=("Helvetica", 10, "bold")).pack(anchor=W, pady=(10, 5))
        vel_scale = ttk.Scale(controle_frame, from_=1e5, to=1e7, variable=self.velocidade, 
                             orient=HORIZONTAL, command=lambda x: self._atualizar_grafico())
        vel_scale.pack(fill=X, pady=(0, 5))
        self.vel_label = ttk.Label(controle_frame, text=f"1.0e+06 m/s", foreground="cyan")
        self.vel_label.pack(anchor=W, pady=(0, 10))
        self.velocidade.trace("w", self._atualizar_labels)
        
        # Campo Magnético
        ttk.Label(controle_frame, text="Campo Magnético B (T):", font=("Helvetica", 10, "bold")).pack(anchor=W, pady=(10, 5))
        campo_scale = ttk.Scale(controle_frame, from_=0.01, to=1.0, variable=self.campo_b, 
                               orient=HORIZONTAL, command=lambda x: self._atualizar_grafico())
        campo_scale.pack(fill=X, pady=(0, 5))
        self.campo_label = ttk.Label(controle_frame, text=f"0.1 T", foreground="cyan")
        self.campo_label.pack(anchor=W, pady=(0, 10))
        self.campo_b.trace("w", self._atualizar_labels)
        
        # Ângulo de Entrada
        ttk.Label(controle_frame, text="Ângulo de Entrada (°):", font=("Helvetica", 10, "bold")).pack(anchor=W, pady=(10, 5))
        angulo_scale = ttk.Scale(controle_frame, from_=0, to=180, variable=self.angulo, 
                                orient=HORIZONTAL, command=lambda x: self._atualizar_grafico())
        angulo_scale.pack(fill=X, pady=(0, 5))
        self.angulo_label = ttk.Label(controle_frame, text=f"90°", foreground="cyan")
        self.angulo_label.pack(anchor=W, pady=(0, 10))
        self.angulo.trace("w", self._atualizar_labels)
        
        # Tempo de Simulação
        ttk.Label(controle_frame, text="Tempo de Simulação (s):", font=("Helvetica", 10, "bold")).pack(anchor=W, pady=(10, 5))
        tempo_scale = ttk.Scale(controle_frame, from_=1e-9, to=1e-7, variable=self.tempo_sim, 
                               orient=HORIZONTAL, command=lambda x: self._atualizar_grafico())
        tempo_scale.pack(fill=X, pady=(0, 5))
        self.tempo_label = ttk.Label(controle_frame, text=f"1.0e-08 s", foreground="cyan")
        self.tempo_label.pack(anchor=W, pady=(0, 10))
        self.tempo_sim.trace("w", self._atualizar_labels)
        
        # Separador
        ttk.Separator(controle_frame, orient=HORIZONTAL).pack(fill=X, pady=15)
        
        # Botão Resetar
        ttk.Button(controle_frame, text="🔄 Resetar Simulação", 
                  command=self._resetar).pack(fill=X, pady=5)
        
        # ========== PAINEL DE INFORMAÇÕES ==========
        info_frame = ttk.LabelFrame(controle_frame, text="📊 INFORMAÇÕES CALCULADAS", padding=10)
        info_frame.pack(fill=X, pady=15)
        
        self.raio_label = ttk.Label(info_frame, text="Raio da órbita: -", foreground="lime")
        self.raio_label.pack(anchor=W, pady=3)
        
        self.freq_label = ttk.Label(info_frame, text="Frequência de Larmor: -", foreground="lime")
        self.freq_label.pack(anchor=W, pady=3)
        
        self.periodo_label = ttk.Label(info_frame, text="Período: -", foreground="lime")
        self.periodo_label.pack(anchor=W, pady=3)
        
        # ========== PAINEL DO GRÁFICO (Direita) ==========
        grafico_frame = ttk.LabelFrame(main_frame, text="📈 VISUALIZAÇÃO DA TRAJETÓRIA", padding=10)
        grafico_frame.pack(side=RIGHT, fill=BOTH, expand=True)
        
        self.canvas_frame = grafico_frame
        
    def _criar_grafico(self):
        """Cria o gráfico matplotlib"""
        self.fig, self.ax = plt.subplots(figsize=(8, 8), dpi=100, facecolor='#1e1e1e')
        self.ax.set_facecolor('#2d2d2d')
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.canvas_frame)
        self.canvas.get_tk_widget().pack(fill=BOTH, expand=True)
        
        self._atualizar_grafico()
        
    def _atualizar_labels(self, *args):
        """Atualiza os rótulos de valores"""
        self.carga_label.config(text=f"{self.carga.get():.2e} C")
        self.massa_label.config(text=f"{self.massa.get():.2e} kg")
        self.vel_label.config(text=f"{self.velocidade.get():.2e} m/s")
        self.campo_label.config(text=f"{self.campo_b.get():.2f} T")
        self.angulo_label.config(text=f"{self.angulo.get():.0f}°")
        self.tempo_label.config(text=f"{self.tempo_sim.get():.2e} s")
        
    def _calcular_trajetoria(self):
        """Calcula a trajetória da partícula em um campo magnético"""
        q = self.carga.get()
        m = self.massa.get()
        v = self.velocidade.get()
        B = self.campo_b.get()
        angulo_rad = np.radians(self.angulo.get())
        t_max = self.tempo_sim.get()
        
        # Componentes de velocidade
        vx = v * np.cos(angulo_rad)
        vy = v * np.sin(angulo_rad)
        
        # Raio de curvatura (r = mv / qB)
        if B > 0 and q > 0:
            raio = (m * v) / (q * B)
        else:
            raio = 1.0
        
        # Frequência ciclotron (ω = qB/m)
        omega = (q * B) / m if m > 0 else 1.0
        
        # Período (T = 2π/ω)
        periodo = (2 * np.pi) / omega if omega > 0 else 1.0
        
        # Número de passos
        n_passos = 1000
        dt = t_max / n_passos
        
        # Arrays para armazenar a trajetória
        x = np.zeros(n_passos)
        y = np.zeros(n_passos)
        
        # Integração numérica (método de Euler)
        vx_current = vx
        vy_current = vy
        
        for i in range(n_passos - 1):
            # Força de Lorentz: F = q(v × B)
            # Campo B está na direção z (perpendicular ao plano xy)
            ax = (q / m) * vy_current * B
            ay = -(q / m) * vx_current * B
            
            # Atualiza velocidade
            vx_current += ax * dt
            vy_current += ay * dt
            
            # Atualiza posição
            x[i + 1] = x[i] + vx_current * dt
            y[i + 1] = y[i] + vy_current * dt
        
        return x, y, raio, omega, periodo
    
    def _atualizar_grafico(self):
        """Atualiza o gráfico com a trajetória calculada"""
        self.ax.clear()
        
        x, y, raio, omega, periodo = self._calcular_trajetoria()
        
        # Plotar trajetória
        self.ax.plot(x * 1e10, y * 1e10, 'c-', linewidth=2, label='Trajetória da partícula')
        self.ax.plot(x[0] * 1e10, y[0] * 1e10, 'go', markersize=10, label='Início')
        self.ax.plot(x[-1] * 1e10, y[-1] * 1e10, 'r*', markersize=15, label='Fim')
        
        # Campo magnético (representado por símbolos)
        self._desenhar_campo_magnetico()
        
        # Configurações do gráfico
        self.ax.set_xlabel('X (Å)', color='white', fontsize=10)
        self.ax.set_ylabel('Y (Å)', color='white', fontsize=10)
        self.ax.set_title('Trajetória da Partícula Carregada em Campo Magnético', 
                         color='white', fontsize=12, fontweight='bold')
        self.ax.grid(True, alpha=0.2, color='white')
        self.ax.legend(loc='upper right', facecolor='#2d2d2d', edgecolor='white', labelcolor='white')
        
        # Cores dos eixos
        self.ax.spines['bottom'].set_color('white')
        self.ax.spines['left'].set_color('white')
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.tick_params(colors='white')
        
        # Atualizar informações calculadas
        self.raio_label.config(text=f"Raio da órbita: {self._converter_unidade(raio)} m")
        self.freq_label.config(text=f"Frequência de Larmor: {self._converter_unidade(omega)} rad/s")
        self.periodo_label.config(text=f"Período: {self._converter_unidade(periodo)} s")
        
        self.canvas.draw()
        
    def _desenhar_campo_magnetico(self):
        """Desenha representação do campo magnético"""
        # Campo magnético perpendicular à página (saindo = ●, entrando = ⊗)
        ax_lim = self.ax.get_xlim()
        ay_lim = self.ax.get_ylim()
        
        # Padrão de pontos/cruzes para representar campo B
        y_pos = np.linspace(ay_lim[0], ay_lim[1], 8)
        x_pos = np.linspace(ax_lim[0], ax_lim[1], 8)
        
        for x in x_pos:
            for y in y_pos:
                self.ax.plot(x, y, 'y.', markersize=3, alpha=0.3)
    
    def _converter_unidade(self, valor):
        """Converte valor para unidade apropriada com notação científica"""
        if abs(valor) < 1e-6:
            return f"{valor:.2e}"
        elif abs(valor) < 1e-3:
            return f"{valor:.2e}"
        else:
            return f"{valor:.2e}"
    
    def _resetar(self):
        """Reseta os valores aos padrões"""
        self.carga.set(1.6e-19)
        self.massa.set(9.1e-31)
        self.velocidade.set(1e6)
        self.campo_b.set(0.1)
        self.angulo.set(90)
        self.tempo_sim.set(1e-8)


def main():
    root = ttk_bs.Window(themename="darkly")
    app = SimuladorCampoMagnetico(root)
    root.mainloop()


if __name__ == "__main__":
    main()
