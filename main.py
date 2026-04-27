import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import ttkbootstrap as ttk_bs
from ttkbootstrap.constants import *

class SimuladorHallidayDefinitivo:
    def __init__(self, root):
        self.root = root
        self.root.title("Halliday & Resnick - Cap 28.1: Análise Bi-Planar")
        self.root.geometry("1550x850")
        
        self.style = ttk_bs.Style(theme="flatly")
        
        # Variáveis
        self.carga = tk.DoubleVar(value=1.0)
        self.velocidade = tk.DoubleVar(value=6.0)
        self.campo_b = tk.DoubleVar(value=1.2)
        self.angulo = tk.DoubleVar(value=45)
        self.massa = 1.0 # Fixa para simplificar a escala visual
        
        self._setup_ui()
        self._atualizar()

    def _setup_ui(self):
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=BOTH, expand=True)
        
        # --- COLUNA 1: CONTROLES E MATEMÁTICA ---
        col1 = ttk.Frame(main_frame, width=380)
        col1.pack(side=LEFT, fill=Y, padx=10)
        
        ttk.Label(col1, text="PARÂMETROS DE ENTRADA", font=("Helvetica", 11, "bold")).pack(pady=10)
        
        self.lbl_q = self._create_slider(col1, "Carga (q)", self.carga, -2.0, 2.0)
        self.lbl_v = self._create_slider(col1, "Velocidade (v)", self.velocidade, 1.0, 10.0)
        self.lbl_b = self._create_slider(col1, "Campo B (T)", self.campo_b, 0.5, 3.0)
        self.lbl_phi = self._create_slider(col1, "Ângulo φ (°)", self.angulo, 1, 89)

        # Painel de Fórmulas
        self.info_box = ttk.LabelFrame(col1, text=" DEMONSTRAÇÃO MATEMÁTICA ", padding=15)
        self.info_box.pack(fill=X, pady=20)
        
        self.lbl_calc = ttk.Label(self.info_box, text="", font=("Consolas", 10), justify=LEFT)
        self.lbl_calc.pack()

        # --- COLUNA 2: PLANO XY ---
        col2 = ttk.LabelFrame(main_frame, text=" VISTA DE CIMA (Plano XY) ")
        col2.pack(side=LEFT, fill=BOTH, expand=True, padx=5)
        self.fig_xy, self.ax_xy = plt.subplots(figsize=(5, 5))
        self.canvas_xy = FigureCanvasTkAgg(self.fig_xy, master=col2)
        self.canvas_xy.get_tk_widget().pack(fill=BOTH, expand=True)

        # --- COLUNA 3: PLANO YZ ---
        col3 = ttk.LabelFrame(main_frame, text=" VISTA LATERAL (Plano YZ) ")
        col3.pack(side=LEFT, fill=BOTH, expand=True, padx=5)
        self.fig_yz, self.ax_yz = plt.subplots(figsize=(5, 5))
        self.canvas_yz = FigureCanvasTkAgg(self.fig_yz, master=col3)
        self.canvas_yz.get_tk_widget().pack(fill=BOTH, expand=True)

    def _create_slider(self, parent, label, var, v_min, v_max):
        frame = ttk.Frame(parent)
        frame.pack(fill=X, pady=5)
        
        header = ttk.Frame(frame)
        header.pack(fill=X)
        ttk.Label(header, text=label).pack(side=LEFT)
        val_lbl = ttk.Label(header, text=f"{var.get():.2f}", font=("Helvetica", 9, "bold"), foreground="#2c3e50")
        val_lbl.pack(side=RIGHT)

        def update_val(val):
            val_lbl.config(text=f"{float(val):.2f}")
            self._atualizar()

        scale = ttk.Scale(frame, from_=v_min, to=v_max, variable=var, command=update_val)
        scale.pack(fill=X)
        return val_lbl

    def _atualizar(self):
        self.ax_xy.clear()
        self.ax_yz.clear()
        
        q = self.carga.get()
        v = self.velocidade.get()
        B_val = self.campo_b.get()
        phi_deg = self.angulo.get()
        phi = np.radians(phi_deg)
        m = self.massa
        
        v_z = v * np.cos(phi)
        v_perp = v * np.sin(phi)
        
        if abs(q) < 0.01: q = 0.01 # Evitar erro
        omega = (q * B_val) / m
        R = v_perp / (abs(q) * B_val)
        
        t = np.linspace(0, 12, 600)
        x = R * np.sin(omega * t)
        y = R * (1 - np.cos(omega * t))
        z = v_z * t

        # --- PLANO XY (Vista de Cima) ---
        # Desenhar B (entrando)
        for i in np.linspace(-10, 10, 6):
            for j in np.linspace(-10, 10, 6):
                self.ax_xy.text(i, j, '⊗', color='blue', alpha=0.15, ha='center', va='center')
        
        self.ax_xy.plot(x, y, color='black', lw=1, alpha=0.5, ls='--')
        # Posição atual da partícula (ponto t=0.5 para ver os vetores)
        idx = 50 
        px, py = x[idx], y[idx]
        self.ax_xy.plot(px, py, 'ro', markersize=8, label='Carga')
        
        # Vetores v e F no plano XY
        vx_inst = v_perp * np.cos(omega * t[idx])
        vy_inst = v_perp * np.sin(omega * t[idx])
        # Fb = q(v x B). B é (0,0,-B). v x B = (-vyB, vxB, 0)
        fx = q * (vy_inst * B_val)
        fy = q * (-vx_inst * B_val)
        
        self.ax_xy.quiver(px, py, vx_inst, vy_inst, color='green', scale=40, label='v')
        self.ax_xy.quiver(px, py, fx, fy, color='red', scale=40, label='Fb')
        
        self.ax_xy.set_xlim(-10, 10); self.ax_xy.set_ylim(-10, 10)
        self.ax_xy.set_xlabel("X"); self.ax_xy.set_ylabel("Y")
        self.ax_xy.set_title("Giro em XY (B entrando)")

        # --- PLANO YZ (Vista Lateral) ---
        # Desenhar B (setas para direita/Z)
        for j in np.linspace(-10, 10, 5):
            self.ax_yz.quiver(0, j, 15, 0, color='blue', alpha=0.1, width=0.005)
            
        self.ax_yz.plot(z, y, color='cyan', lw=2)
        self.ax_yz.plot(z[idx], y[idx], 'ro')
        self.ax_yz.set_xlim(0, 20); self.ax_yz.set_ylim(-10, 10)
        self.ax_yz.set_xlabel("Z (Direção de B)"); self.ax_yz.set_ylabel("Y")
        self.ax_yz.set_title("Avanço em YZ (Hélice)")

        # --- PAINEL MATEMÁTICO ---
        txt = (
            f"1. FORÇA MAGNÉTICA:\n"
            f"Fb = q * (v_perp * B)\n"
            f"Fb = {abs(q):.1f} * ({v_perp:.1f} * {B_val:.1f})\n"
            f"Fb = {abs(q*v_perp*B_val):.2f} N\n\n"
            f"2. RAIO DA CURVATURA:\n"
            f"R = (m * v_perp) / (|q| * B)\n"
            f"R = ({m} * {v_perp:.2f}) / ({abs(q):.1f} * {B_val:.1f})\n"
            f"R = {abs(R):.2f} m\n\n"
            f"3. COMPONENTES VETORIAIS:\n"
            f"B = {B_val:.1f} k (T)\n"
            f"v_z (avanço) = {v_z:.2f} k (m/s)"
        )
        self.lbl_calc.config(text=txt)

        self.canvas_xy.draw()
        self.canvas_yz.draw()

if __name__ == "__main__":
    root = ttk_bs.Window(themename="flatly")
    app = SimuladorHallidayDefinitivo(root)
    root.mainloop()