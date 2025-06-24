import sv_ttk
from tkinter import ttk
import matplotlib.pyplot as plt

def setup_theme(app):
    """Инициализация темы приложения"""
    app.title_font = ("Segoe UI Semibold", 20)
    app.subtitle_font = ("Segoe UI", 12)
    app.input_font = ("Segoe UI Semibold", 15)
    app.result_font = ("Segoe UI", 11)
    app.button_font = ("Segoe UI Semibold", 10)
    app.info_font = ("Consolas", 10)
    app.angle_font = ("Segoe UI", 24, "bold")
    
    sv_ttk.set_theme(app.current_theme)
    update_theme(app)

def toggle_theme(app):
    """Переключение между светлой и тёмной темой"""
    app.current_theme = "dark" if app.current_theme == "light" else "light"
    app.theme_button.config(text="☀️ Светлая тема" if app.current_theme == "dark" else "🌙 Тёмная тема")
    
    sv_ttk.set_theme(app.current_theme)
    update_theme(app)
    
    # Перерисовка графика
    if hasattr(app, 'fig_traj') and app.fig_traj:
        app.calculate()

def update_theme(app):
    """Обновление цветов в соответствии с текущей темой"""
    if app.current_theme == "light":
        app.root.configure(bg="#f5f5f5")
        if hasattr(app, 'ballistics_text'):
            app.ballistics_text.config(bg='white', fg='black')
        
        # Настройка цветов графиков
        plt.rcParams.update({
            'axes.facecolor': 'white',
            'axes.edgecolor': 'black',
            'axes.labelcolor': 'black',
            'xtick.color': 'black',
            'ytick.color': 'black',
            'text.color': 'black',
            'figure.facecolor': 'white',
            'grid.color': '#e0e0e0'
        })
        
        # Стили для кнопок
        style = ttk.Style()
        style.configure('Accent.TButton', background='#1E90FF', foreground='white')
        style.map('Accent.TButton', 
                 background=[('active', '#4682B4'), ('pressed', '#4169E1')])
    else:
        app.root.configure(bg="#2a2b2e")
        if hasattr(app, 'ballistics_text'):
            app.ballistics_text.config(bg='#2a2b2e', fg='#e0e0e0')
        
        # Настройка цветов графиков
        plt.rcParams.update({
            'axes.facecolor': '#2a2b2e',
            'axes.edgecolor': '#e0e0e0',
            'axes.labelcolor': '#e0e0e0',
            'xtick.color': '#e0e0e0',
            'ytick.color': '#e0e0e0',
            'text.color': '#e0e0e0',
            'figure.facecolor': '#1e1f22',
            'grid.color': '#444444'
        })
        
        # Стили для кнопок
        style = ttk.Style()
        style.configure('Accent.TButton', background='#d35400', foreground='white')
        style.map('Accent.TButton', 
                 background=[('active', '#e67e22'), ('pressed', '#bf360c')])
    
    # Обновление стилей фреймов
    if hasattr(app, 'setup_styles'):
        app.setup_styles()

def setup_styles(app):
    """Настройка стилей элементов"""
    style = ttk.Style()
    style.configure('TFrame', background='#f5f5f5' if app.current_theme == "light" else '#2a2b2e')
    style.configure('TLabelframe', 
                   background='#f5f5f5' if app.current_theme == "light" else '#2a2b2e', 
                   foreground='black' if app.current_theme == "light" else '#e0e0e0')
    style.configure('TLabelframe.Label', 
                   background='#f5f5f5' if app.current_theme == "light" else '#2a2b2e', 
                   foreground="#272727" if app.current_theme == "light" else "#ffaa44")