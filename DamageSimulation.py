import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
# import sys

class UniversalBalanceSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Damage Simulator")
        self.root.geometry("1200x800")
        
        # [종료 처리]
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.patch_widgets = []
        self.colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']

        # 1. 공통 환경 설정
        env_frame = ttk.LabelFrame(root, text="대상 설정")
        env_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(env_frame, text="대상 최대 체력:").pack(side="left", padx=5)
        self.entry_hp = ttk.Entry(env_frame, width=8)
        self.entry_hp.insert(0, "2000")
        self.entry_hp.pack(side="left", padx=5)

        ttk.Label(env_frame, text="대상 방어력:").pack(side="left", padx=5)
        self.entry_def = ttk.Entry(env_frame, width=8)
        self.entry_def.insert(0, "100") 
        self.entry_def.pack(side="left", padx=5)

        ttk.Label(env_frame, text="현재 체력 비율(%) :").pack(side="left", padx=5)
        self.entry_hp_ratio = ttk.Entry(env_frame, width=8)
        self.entry_hp_ratio.insert(0, "50") 
        self.entry_hp_ratio.pack(side="left", padx=5)

        ttk.Label(env_frame, text="스킬 레벨 별 시전자 공격력 :").pack(side="left", padx=5)
        self.entry_ap = ttk.Entry(env_frame, width=20)
        self.entry_ap.insert(0, "50, 150, 400")
        self.entry_ap.pack(side="left", padx=5)




        # 2. 패치안 리스트
        self.canvas_frame = ttk.LabelFrame(root, text="Patch Cases : 스킬 옵션 상세 설정")
        self.canvas_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.canvas = tk.Canvas(self.canvas_frame)
        self.scrollbar = ttk.Scrollbar(self.canvas_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # 3. 버튼 영역
        btn_frame = tk.Frame(root)
        btn_frame.pack(fill="x", padx=10, pady=5)

        ttk.Button(btn_frame, text="+ Case 추가", command=lambda: self.add_patch_row("New Case")).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="- 마지막 Case 제거", command=self.remove_patch_row).pack(side="left", padx=5)
        
        style = ttk.Style()
        style.configure("Bold.TButton", font=('Helvetica', 10, 'bold'))
        ttk.Button(btn_frame, text="▶ 시각화", style="Bold.TButton", command=self.visualize).pack(side="right", padx=10)

        # 4. 그래프 영역
        self.fig, self.ax = plt.subplots(figsize=(8, 4))
        self.graph_canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.graph_canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

        self.add_patch_row("Current Live")

    def on_closing(self):
        plt.close('all')
        self.root.quit()
        self.root.destroy()
        print("Simulator Closed Successfully.")

    def add_patch_row(self, default_name="New Case"):
        row_frame = ttk.Frame(self.scrollable_frame)
        row_frame.pack(fill="x", padx=5, pady=5)
        ttk.Separator(row_frame, orient='horizontal').pack(fill='x', pady=5)

        top_row = tk.Frame(row_frame)
        top_row.pack(fill="x", pady=2)
        
        ttk.Label(top_row, text="Name:").pack(side="left")
        entry_name = ttk.Entry(top_row, width=15)
        entry_name.insert(0, default_name)
        entry_name.pack(side="left", padx=5)

        ttk.Label(top_row, text="기본 피해량(Lv1,2,3...):").pack(side="left")
        entry_base = ttk.Entry(top_row, width=20)
        entry_base.insert(0, "100, 150, 200")
        entry_base.pack(side="left", padx=5)

        ttk.Label(top_row, text="공격력 계수").pack(side="left")
        entry_ratio = ttk.Entry(top_row, width=5)
        entry_ratio.insert(0, "1.0")
        entry_ratio.pack(side="left", padx=5)

        bot_row = tk.Frame(row_frame)
        bot_row.pack(fill="x", pady=2)

        ttk.Label(bot_row, text="[추가 옵션] 최대 체력 비례(%):").pack(side="left")
        entry_max = ttk.Entry(bot_row, width=5)
        entry_max.insert(0, "0")
        entry_max.pack(side="left", padx=5)

        ttk.Label(bot_row, text="현재 체력 비례(%)").pack(side="left")
        entry_cur = ttk.Entry(bot_row, width=5)
        entry_cur.insert(0, "0")
        entry_cur.pack(side="left", padx=5)

        ttk.Label(bot_row, text="잃은 체력 비례(%)").pack(side="left")
        entry_lost = ttk.Entry(bot_row, width=5)
        entry_lost.insert(0, "0")
        entry_lost.pack(side="left", padx=5)

        inputs = {
            'name': entry_name, 'base': entry_base, 'ratio': entry_ratio,
            'max_hp': entry_max, 'cur_hp': entry_cur, 'lost_hp': entry_lost
        }
        self.patch_widgets.append((row_frame, inputs))

    def remove_patch_row(self):
        if self.patch_widgets:
            frame, _ = self.patch_widgets.pop()
            frame.destroy()

    def calculate(self, inputs, t_hp, t_def, t_hp_ratio, c_ap_list):
        try:
            name = inputs['name'].get()
            base_dmgs = [float(x.strip()) for x in inputs['base'].get().split(',')]
            ratio = float(inputs['ratio'].get())
            max_hp_per = float(inputs['max_hp'].get())
            cur_hp_per = float(inputs['cur_hp'].get())
            lost_hp_per = float(inputs['lost_hp'].get())
        except ValueError:
            return None, None, None

        current_hp = t_hp * (t_hp_ratio / 100)
        lost_hp = t_hp - current_hp
        
        levels = range(1, len(base_dmgs) + 1)
        damages = []
        mitigation = 100 / (100 + t_def)

        for i, base in enumerate(base_dmgs):
            if i < len(c_ap_list):
                current_ap = c_ap_list[i]
            else:
                current_ap = c_ap_list[-1]

            flat_dmg = base + (current_ap * ratio)
            bonus_dmg = 0
            bonus_dmg += t_hp * (max_hp_per / 100)
            bonus_dmg += current_hp * (cur_hp_per / 100)
            bonus_dmg += lost_hp * (lost_hp_per / 100)
            
            final_dmg = (flat_dmg + bonus_dmg) * mitigation
            damages.append(final_dmg)

        return name, levels, damages

    def visualize(self):
        self.ax.clear()
        try:
            t_hp = float(self.entry_hp.get())
            t_def = float(self.entry_def.get())
            t_hp_ratio = float(self.entry_hp_ratio.get())
            
            raw_ap = self.entry_ap.get().split(',')
            c_ap_list = [float(x.strip()) for x in raw_ap]
        except ValueError:
            messagebox.showerror("Error", "숫자를 정확히 입력해주세요.")
            return

        valid = False
        for i, (_, inputs) in enumerate(self.patch_widgets):
            name, lv, dmg = self.calculate(inputs, t_hp, t_def, t_hp_ratio, c_ap_list)
            
            if name:
                valid = True
                color = self.colors[i % len(self.colors)]
                self.ax.plot(lv, dmg, marker='o', label=name, color=color, linewidth=2, alpha=0.8)
                
                for j, val in enumerate(dmg):
                    # 현재 포인트에 적용된 능력치 찾기
                    if j < len(c_ap_list):
                        applied_ap = c_ap_list[j]
                    else:
                        applied_ap = c_ap_list[-1]

                    # 1. 데미지 수치 (기존, 진하게)
                    self.ax.annotate(f"{int(val)}", (lv[j], dmg[j]), 
                                     textcoords="offset points", xytext=(0, 6), 
                                     ha='center', fontsize=9, color=color, fontweight='bold')
                    
                    # 2. 적용된 능력치 수치 (회색, 작게, 위쪽에)
                    self.ax.annotate(f"(AD:{int(applied_ap)})", (lv[j], dmg[j]), 
                                     textcoords="offset points", xytext=(0, 18), 
                                     ha='center', fontsize=7, color='gray')

        self.ax.set_title(f"Damage Analysis \n Enable Def : {t_def} -> ({100/(100+t_def)*100:.1f}% Dmg Received)")
        self.ax.set_xlabel("Skill Level")
        self.ax.set_ylabel("Post-Mitigation Damage")
        
        if valid:
            self.ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
            self.ax.legend()
            self.ax.grid(True, linestyle='--', alpha=0.4)

        self.graph_canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = UniversalBalanceSimulator(root)
    root.mainloop()