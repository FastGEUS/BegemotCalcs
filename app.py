import pandas as pd
import tkinter as tk
from tkinter import messagebox
from ballistics import calculate_ballistics
from ui import setup_ui
from theme import setup_theme, toggle_theme, update_theme
import sv_ttk
import numpy as np
import matplotlib.pyplot as plt

class BegemotArtilleryCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Begemot Calculator - by SVET")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        # Параметры баллистики
        self.V0 = 95
        self.MASS = 500
        self.DRAG_COEFFICIENT = 0.15
        self.MIN_DISTANCE = 150
        self.MAX_DISTANCE = 925
        
        # Инициализация темы
        self.current_theme = "light"
        setup_theme(self)
        
        try:
            # Загрузка данных
            self.load_data()
            # Инициализация UI
            setup_ui(self)
            # Первоначальный расчет
            self.calculate()
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка инициализации: {str(e)}")
            self.root.destroy()
    
    def load_data(self):
        """Загрузка и предобработка данных из Excel"""
        self.df = pd.read_excel('data.xlsx')
        
        # Проверка необходимых колонок
        required_columns = ['Дистанция', 'Значение1', 'Значение2']
        if not all(col in self.df.columns for col in required_columns):
            raise ValueError("Файл должен содержать колонки 'Дистанция', 'Значение1', 'Значение2'")
            
        # Удаление строк с пропущенными значениями
        self.df = self.df.dropna(subset=required_columns)
        
        # Проверка наличия данных после очистки
        if self.df.empty:
            raise ValueError("Нет данных после очистки от пропусков")
        
        # Преобразование типов данных
        self.df['Дистанция'] = self.df['Дистанция'].astype(float)
        self.df['Значение1'] = self.df['Значение1'].astype(float)
        self.df['Значение2'] = self.df['Значение2'].astype(float)
        
        # Фильтрация данных (150-925 м)
        self.df = self.df[
            (self.df['Дистанция'] >= self.MIN_DISTANCE) & 
            (self.df['Дистанция'] <= self.MAX_DISTANCE)
        ]
    
    def calculate(self, event=None):
        """Основная функция расчета"""
        try:
            distance = float(self.entry_var.get())
            
            if distance < self.MIN_DISTANCE or distance > self.MAX_DISTANCE:
                messagebox.showwarning("Предупреждение", 
                    f"Дистанция должна быть в пределах {self.MIN_DISTANCE}-{self.MAX_DISTANCE} метров")
                return
            
            # Поиск ближайшего значения
            self.df['Разница'] = abs(self.df['Дистанция'] - distance)
            closest_idx = self.df['Разница'].idxmin()
            closest_row = self.df.loc[closest_idx]
            
            # Обновление углов
            angle1 = closest_row['Значение1']
            angle2 = closest_row['Значение2']
            self.angle1_var.set(f"{angle1:.2f}°")
            self.angle2_var.set(f"{angle2:.2f}°")
            
            # Расчет баллистики
            trajectory1 = calculate_ballistics(
                distance, angle1, 
                self.V0, self.MASS, self.DRAG_COEFFICIENT
            )
            trajectory2 = calculate_ballistics(
                distance, angle2, 
                self.V0, self.MASS, self.DRAG_COEFFICIENT
            )
            
            # Обновление информации
            self.update_results(trajectory1, trajectory2, distance, angle1, angle2)
            
        except ValueError:
            messagebox.showerror("Ошибка", "Введите числовое значение дистанции")
    
    def update_results(self, trajectory1, trajectory2, distance, angle1, angle2):
        """Обновление результатов расчета"""
        # Расчет времени полета
        flight_time1 = trajectory1[-1, 0] if len(trajectory1) > 0 else 0
        flight_time2 = trajectory2[-1, 0] if len(trajectory2) > 0 else 0
        self.angle3_var.set(f"{flight_time2:.1f} с")
        self.angle4_var.set(f"{flight_time1:.1f} с")
        
        # Расчет максимальной высоты
        max_height1 = np.max(trajectory1[:, 2]) if len(trajectory1) > 0 else 0
        max_height2 = np.max(trajectory2[:, 2]) if len(trajectory2) > 0 else 0
        
        # Обновление текстовой информации
        self.ballistics_text.config(state=tk.NORMAL)
        self.ballistics_text.delete(1.0, tk.END)
        
        info = "=== НАВЕСНОЙ ОГОНЬ ===\n"
        info += f"Угол возвышения: {angle1:.2f}°\n"
        info += f"Время полета: {flight_time1:.1f} с\n"
        info += f"Макс. высота: {max_height1:.0f} м\n"
        info += f"Дальность: {trajectory1[-1, 1] if len(trajectory1) > 0 else 0:.0f} м\n"
        
        info += "\n=== ПРЯМОЙ ОГОНЬ ===\n"
        info += f"Угол возвышения: {angle2:.2f}°\n"
        info += f"Время полета: {flight_time2:.1f} с\n"
        info += f"Макс. высота: {max_height2:.0f} м\n"
        info += f"Дальность: {trajectory2[-1, 1] if len(trajectory2) > 0 else 0:.0f} м\n"
        
        info += "\n=== ОБЩИЕ ПАРАМЕТРЫ ===\n"
        info += f"Дистанция до цели: {distance:.0f} м\n"
        info += f"Нач. скорость снаряда: {self.V0} м/с\n"
        info += f"Масса снаряда: {self.MASS} кг\n"
        info += f"Коэф. сопротивления: {self.DRAG_COEFFICIENT:.3f}"
        
        self.ballistics_text.insert(tk.END, info)
        self.ballistics_text.config(state=tk.DISABLED)
        
        # Обновление графика
        self.update_trajectory_plot(trajectory1, trajectory2, distance, angle1, angle2)
    
    def update_trajectory_plot(self, trajectory1, trajectory2, distance, angle1, angle2):
        """Обновление графика траекторий"""
        self.ax_traj.clear()
        
        # Определение цветов для текущей темы
        color1 = '#1E90FF' if self.current_theme == "light" else '#3498db'
        color2 = '#DC143C' if self.current_theme == "light" else '#e74c3c'
        
        # Отрисовка траекторий
        if len(trajectory1) > 0:
            self.ax_traj.plot(trajectory1[:, 1], trajectory1[:, 2], 
                             color=color1, linewidth=1.5, 
                             label=f'Навесной огонь ({angle1:.1f}°)')
            max_idx1 = np.argmax(trajectory1[:, 2])
            self.ax_traj.plot(trajectory1[max_idx1, 1], trajectory1[max_idx1, 2], 
                             'bo', markersize=4, alpha=0.7)
        
        if len(trajectory2) > 0:
            self.ax_traj.plot(trajectory2[:, 1], trajectory2[:, 2], 
                             color=color2, linewidth=1.5, 
                             label=f'Прямой огонь ({angle2:.1f}°)')
            max_idx2 = np.argmax(trajectory2[:, 2])
            self.ax_traj.plot(trajectory2[max_idx2, 1], trajectory2[max_idx2, 2], 
                             'ro', markersize=4, alpha=0.7)
        
        # Стартовая и конечная точки
        self.ax_traj.plot(0, 0, 'go', markersize=5, label='Орудие')
        self.ax_traj.plot(distance, 0, 'yo', markersize=5, label='Цель')
        
        # Настройки графика
        self.ax_traj.set_title(f'Траектории полета ФАБ-500 на {distance:.0f}м', fontsize=12)
        self.ax_traj.set_xlabel('Дистанция (м)', fontsize=9)
        self.ax_traj.set_ylabel('Высота (м)', fontsize=9)
        self.ax_traj.grid(True, linestyle='--', alpha=0.6)
        self.ax_traj.legend(fontsize=8, loc='upper right')
        self.ax_traj.set_ylim(bottom=0)
        self.ax_traj.set_xlim(left=0)
        self.ax_traj.set_xlim(right=max(distance * 1.1, 1000))
        
        # Сетка
        grid_color = '#cccccc' if self.current_theme == "light" else '#444444'
        self.ax_traj.grid(True, which='both', linestyle=':', color=grid_color, alpha=0.7)
        
        # Обновление фона
        self.ax_traj.set_facecolor(plt.rcParams['axes.facecolor'])
        self.fig_traj.set_facecolor(plt.rcParams['figure.facecolor'])
        
        self.canvas_traj.draw()