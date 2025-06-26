import tkinter as tk
from tkinter import ttk
from theme import setup_styles, toggle_theme

def setup_ui(app):
    """Инициализация пользовательского интерфейса"""
    main_frame = ttk.Frame(app.root)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
    
    # Заголовок
    header_frame = ttk.Frame(main_frame)
    header_frame.pack(fill=tk.X, pady=(0, 10))
    
    ttk.Label(header_frame, text="БЕГЕМОТ КАЛЬКУЛЯТОР", 
             font=app.title_font).pack(side=tk.LEFT)
    
    # Кнопка переключения темы
    app.theme_button = ttk.Button(
        header_frame, 
        text="🌙 Тёмная тема" if app.current_theme == "light" else "☀️ Светлая тема",
        command=lambda: toggle_theme(app),
        width=18
    )
    app.theme_button.pack(side=tk.RIGHT, padx=5)
    
    # Панель параметров стрельбы
    params_frame = ttk.LabelFrame(main_frame, text="ПАРАМЕТРЫ СТРЕЛЬБЫ", padding=10)
    params_frame.pack(fill=tk.X, pady=(0, 10))
    
    # Поле ввода дистанции
    input_row = ttk.Frame(params_frame)
    input_row.pack(fill=tk.X, pady=5)
    
    ttk.Label(input_row, text="Дистанция до цели (150-925м):", 
             font=app.input_font).pack(side=tk.LEFT, padx=(0, 10))
    
    app.entry_var = tk.StringVar(value="500")
    app.entry = ttk.Entry(input_row, textvariable=app.entry_var, width=10, 
                          font=app.input_font, justify=tk.CENTER)
    app.entry.pack(side=tk.LEFT)
    
    ttk.Button(input_row, text="РАССЧИТАТЬ", 
              command=app.calculate, 
              style="Accent.TButton",
              width=15).pack(side=tk.RIGHT, padx=10)
    
    # Параметры снаряда
    shell_frame = ttk.LabelFrame(params_frame, text="ПАРАМЕТРЫ СНАРЯДА", padding=5)
    shell_frame.pack(fill=tk.X, pady=5)
    
    shell_info = ttk.Frame(shell_frame)
    shell_info.pack(fill=tk.X, pady=3)
    
    ttk.Label(shell_info, text=f"Снаряд: ФАБ-500", 
             font=app.input_font).pack(side=tk.LEFT, padx=5)
    
    ttk.Label(shell_info, text=f"Скорость: {app.V0} м/с", 
             font=app.input_font).pack(side=tk.LEFT, padx=10)
    
    ttk.Label(shell_info, text=f"Масса: {app.MASS} кг", 
             font=app.input_font).pack(side=tk.LEFT, padx=10)
    
    # Панель результатов
    results_frame = ttk.LabelFrame(main_frame, text="РЕЗУЛЬТАТЫ РАСЧЕТА", padding=10)
    results_frame.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
    
    # Навесной огонь
    mortar_frame = ttk.Frame(results_frame)
    mortar_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
    
    ttk.Label(mortar_frame, text="НАВЕСНОЙ ОГОНЬ", 
             font=("Segoe UI Semibold", 11), foreground="#1E90FF").pack(pady=(0, 5))
    
    angle1_frame = ttk.Frame(mortar_frame)
    angle1_frame.pack(fill=tk.X, pady=3)
    ttk.Label(angle1_frame, text="Угол:", font=app.result_font).pack(side=tk.LEFT)
    app.angle1_var = tk.StringVar(value="0.00°")
    ttk.Label(angle1_frame, textvariable=app.angle1_var, 
             font=app.angle_font).pack(side=tk.RIGHT)
    
    time1_frame = ttk.Frame(mortar_frame)
    time1_frame.pack(fill=tk.X, pady=3)
    ttk.Label(time1_frame, text="Время полета:", font=app.result_font).pack(side=tk.LEFT)
    app.angle4_var = tk.StringVar(value="0 сек")
    ttk.Label(time1_frame, textvariable=app.angle4_var, 
             font=app.angle_font).pack(side=tk.RIGHT)
    
    # Прямой огонь
    direct_frame = ttk.Frame(results_frame)
    direct_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
    
    ttk.Label(direct_frame, text="ПРЯМОЙ ОГОНЬ", 
             font=("Segoe UI Semibold", 11), foreground="#DC143C").pack(pady=(0, 5))
    
    angle2_frame = ttk.Frame(direct_frame)
    angle2_frame.pack(fill=tk.X, pady=3)
    ttk.Label(angle2_frame, text="Угол:", font=app.result_font).pack(side=tk.LEFT)
    app.angle2_var = tk.StringVar(value="0.00°")
    ttk.Label(angle2_frame, textvariable=app.angle2_var, 
             font=app.angle_font).pack(side=tk.RIGHT)
    
    time2_frame = ttk.Frame(direct_frame)
    time2_frame.pack(fill=tk.X, pady=3)
    ttk.Label(time2_frame, text="Время полета:", font=app.result_font).pack(side=tk.LEFT)
    app.angle3_var = tk.StringVar(value="0 сек")
    ttk.Label(time2_frame, textvariable=app.angle3_var, 
             font=app.angle_font).pack(side=tk.RIGHT)
    
    # Настройка стилей
    setup_styles(app)