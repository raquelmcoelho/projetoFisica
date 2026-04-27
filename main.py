import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import ttkbootstrap as ttk_bs
from ttkbootstrap.constants import *

class SimuladorHallidayFinal:
    def __init__(self, root):
        self.root = root
        self.root.title("Halliday & Resnick - Cap 28.1")
        self.root.geometry("1500x900")
        self.style = ttk_bs.Style(theme="flatly")
        
        # Parâmetros Iniciais
        self.carga = tk.DoubleVar(value=1.0)
        self.velocidade = tk.DoubleVar(value=6.0)
        self.campo_b = tk.DoubleVar(value=1.2)
        self.angulo = tk.DoubleVar(value=45)
        self.massa = 1.0 
        
        self._setup_ui()
        self._atualizar()

    def _setup_ui(self):
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=BOTH, expand=True)
        
        # COLUNA 1: CONTROLES
        col1 = ttk.Frame(main_frame, width=400)
        col1.pack(side=LEFT, fill=Y, padx=10)
        
        ttk.Label(col1, text="CONTROLES", font=("Helvetica", 12, "bold")).pack(pady=10)
        
        self._create_slider(col1, "Carga (q)", self.carga, -2.0, 2.0, "C")
        self._create_slider(col1, "Velocidade (v)", self.velocidade, 1.0, 15.0, "m/s")
        self._create_slider(col1, "Campo B (T)", self.campo_b, 0.5, 4.0, "T")
        self._create_slider(col1, "Ângulo φ (°)", self.angulo, 1, 89, "°")

        # Painel Matemática
        self.info_box = ttk.LabelFrame(col1, text=" MATEMÁTICA DO CAPÍTULO ", padding=15)
        self.info_box.pack(fill=X, pady=20)
        self.lbl_calc = ttk.Label(self.info_box, text="", font=("Consolas", 11), justify=LEFT)
        self.lbl_calc.pack()

        # COLUNA 2: GRAFICO XY
        self.frame_xy = ttk.LabelFrame(main_frame, text=" Plano XY (Giro Circular) ")
        self.frame_xy.pack(side=LEFT, fill=BOTH, expand=True, padx=5)
        self.fig_xy, self.ax_xy = plt.subplots(figsize=(5, 5))
        self.canvas_xy = FigureCanvasTkAgg(self.fig_xy, master=self.frame_xy)
        self.canvas_xy.get_tk_widget().pack(fill=BOTH, expand=True)

        # COLUNA 3: GRAFICO YZ
        self.frame_yz = ttk.LabelFrame(main_frame, text=" Plano YZ (Avanço Helicoidal) ")
        self.frame_yz.pack(side=LEFT, fill=BOTH, expand=True, padx=5)
        self.fig_yz, self.ax_yz = plt.subplots(figsize=(5, 5))
        self.canvas_yz = FigureCanvasTkAgg(self.fig_yz, master=self.frame_yz)
        self.canvas_yz.get_tk_widget().pack(fill=BOTH, expand=True)

    def _create_slider(self, parent, label, var, v_min, v_max, unidade):
        frame = ttk.Frame(parent); frame.pack(fill=X, pady=8)
        top_row = ttk.Frame(frame); top_row.pack(fill=X)
        ttk.Label(top_row, text=label).pack(side=LEFT)
        val_label = ttk.Label(top_row, text=f"{var.get():.2f} {unidade}", font=("Helvetica", 9, "bold"), foreground="blue")
        val_label.pack(side=RIGHT)

        def on_slide(val):
            val_label.config(text=f"{float(val):.2f} {unidade}")
            self._atualizar()

        scale = ttk.Scale(frame, from_=v_min, to=v_max, variable=var, command=on_slide)
        scale.pack(fill=X)

    def _atualizar(self):
        self.ax_xy.clear()
        self.ax_yz.clear()
        
        q = self.carga.get()
        v = self.velocidade.get()
        B_val = self.campo_b.get()
        phi_deg = self.angulo.get()
        phi = np.radians(phi_deg)
        m = self.massa
        
        if abs(q) < 0.01: q = 0.01 
        
        # Decomposição da velocidade (Halliday)
        v_perp = v * np.sin(phi)
        v_paralela = v * np.cos(phi)
        
        # Frequência Angular (omega) e Raio (R)
        w = (q * B_val) / m 
        R = (m * v_perp) / (abs(q) * B_val) 
        
        t = np.linspace(0, 10, 500)
        x_pos = R * np.sin(w * t)
        y_pos = R * (1 - np.cos(w * t))
        z_pos = v_paralela * t

        # --- PLANO XY ---
        # Desenhar símbolos de campo entrando (⊗)
        for i in np.linspace(-15, 15, 6):
            for j in np.linspace(-5, 25, 6):
                self.ax_xy.text(i, j, '⊗', color='blue', alpha=0.1, ha='center', va='center')

        self.ax_xy.plot(x_pos, y_pos, 'k--', alpha=0.3, lw=1) 
        idx = 50 
        px, py = x_pos[idx], y_pos[idx]
        
        # Velocidade (Derivada: vx = dx/dt, vy = dy/dt)
        vx = v_perp * np.cos(w * t[idx])
        vy = v_perp * np.sin(w * t[idx])
        
        # FORÇA CENTRÍPETA (Sempre aponta para o centro da curva)
        # O centro instantâneo para esta parametrização está em (0, R)
        fx = -px 
        fy = (R - py)
        # Normalizando a seta para o desenho não ficar gigante
        f_mag = np.sqrt(fx**2 + fy**2)
        fx_alt, fy_alt = (fx/f_mag)*5, (fy/f_mag)*5

        self.ax_xy.quiver(px, py, vx, vy, color='green', scale=35, label='v')
        self.ax_xy.quiver(px, py, fx_alt, fy_alt, color='red', scale=35, label='Fb')
        self.ax_xy.plot(px, py, 'bo', markersize=10) 
        
        self.ax_xy.set_xlim(-15, 15); self.ax_xy.set_ylim(-5, 25)
        self.ax_xy.set_xlabel("X (m)"); self.ax_xy.set_ylabel("Y (m)")
        self.ax_xy.grid(True, linestyle=':', alpha=0.6); self.ax_xy.set_aspect('equal')

        # --- PLANO YZ ---
        for j in np.linspace(-5, 25, 5):
            self.ax_yz.arrow(0, j, 20, 0, color='blue', alpha=0.1, head_width=0.8)

        self.ax_yz.plot(z_pos, y_pos, color='purple', lw=2)
        self.ax_yz.quiver(0, 0, v_paralela, v_perp, color='green', scale=40)
        self.ax_yz.text(1, 1, f"φ={phi_deg:.0f}°", color='green', fontweight='bold')
        
        self.ax_yz.set_xlim(0, 25); self.ax_yz.set_ylim(-5, 25)
        self.ax_yz.set_xlabel("Z (Direção de B)"); self.ax_yz.set_ylabel("Y (Plano do Giro)")
        self.ax_yz.grid(True, linestyle=':', alpha=0.6)

        # PAINEL MATEMÁTICO
        txt = (
            f"Fb = |q|vB sen(φ)\n"
            f"Fb = {abs(q):.1f} * {v:.1f} * {B_val:.1f} * {np.sin(phi):.2f}\n"
            f"Fb = {abs(q)*v*B_val*np.sin(phi):.2f} N\n\n"
            f"R = (m * v * sen(φ)) / (|q| * B)\n"
            f"R = ({m} * {v:.1f} * {np.sin(phi):.2f}) / ({abs(q):.1f} * {B_val:.1f})\n"
            f"R = {abs(R):.2f} m"
        )
        self.lbl_calc.config(text=txt)
        
        self.canvas_xy.draw()
        self.canvas_yz.draw()

if __name__ == "__main__":
    root = ttk_bs.Window(themename="flatly")
    app = SimuladorHallidayFinal(root)
    root.mainloop()