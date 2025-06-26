import sv_ttk
from tkinter import ttk

def setup_theme(app):
    """Инициализация темы приложения"""
    app.title_font = ("Segoe UI Semibold", 16)  # Уменьшенный размер
    app.input_font = ("Segoe UI Semibold", 12)  # Уменьшенный размер
    app.result_font = ("Segoe UI", 10)         # Уменьшенный размер
    app.angle_font = ("Segoe UI", 20, "bold")  # Уменьшенный размер
    
    sv_ttk.set_theme(app.current_theme)
    update_theme(app)

def toggle_theme(app):
    """Переключение между светлой и тёмной темой"""
    app.current_theme = "dark" if app.current_theme == "light" else "light"
    app.theme_button.config(text="☀️ Светлая тема" if app.current_theme == "dark" else "🌙 Тёмная тема")
    
    sv_ttk.set_theme(app.current_theme)
    update_theme(app)

def update_theme(app):
    """Обновление цветов в соответствии с текущей темой"""
    if app.current_theme == "light":
        app.root.configure(bg="#f5f5f5")
    else:
        app.root.configure(bg="#2a2b2e")
    
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
    style.configure('Accent.TButton', 
                   background='#1E90FF' if app.current_theme == "light" else '#d35400', 
                   foreground='white')