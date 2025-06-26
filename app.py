import pandas as pd
import tkinter as tk
from tkinter import messagebox
from ballistics import calculate_ballistics
from ui import setup_ui
from theme import setup_theme, toggle_theme
import numpy as np

class BegemotArtilleryCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Begemot Calculator - by SVET")
        self.root.geometry("600x400")  # Уменьшенный размер окна
        self.root.minsize(500, 350)    # Минимальный размер
        
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
            self.update_results(trajectory1, trajectory2)
            
        except ValueError:
            messagebox.showerror("Ошибка", "Введите числовое значение дистанции")
    
    def update_results(self, trajectory1, trajectory2):
        """Обновление результатов расчета"""
        # Расчет времени полета
        flight_time1 = trajectory1[-1, 0] if len(trajectory1) > 0 else 0
        flight_time2 = trajectory2[-1, 0] if len(trajectory2) > 0 else 0
        self.angle3_var.set(f"{flight_time2:.1f} с")
        self.angle4_var.set(f"{flight_time1:.1f} с")