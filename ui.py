import tkinter as tk
from tkinter import ttk, scrolledtext
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from theme import setup_styles, toggle_theme

def setup_ui(app):
    """Инициализация пользовательского интерфейса"""
    main_frame = ttk.Frame(app.root)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    # Заголовок
    header_frame = ttk.Frame(main_frame)
    header_frame.pack(fill=tk.X, pady=(0, 15))
    
    ttk.Label(header_frame, text="БЕГЕМОТ КАЛЬКУЛЯТОР", 
             font=app.title_font).pack(side=tk.LEFT)
    
    # Кнопка переключения темы
    app.theme_button = ttk.Button(
        header_frame, 
        text="🌙 Тёмная тема" if app.current_theme == "light" else "☀️ Светлая тема",
        command=lambda: toggle_theme(app)
    )
    app.theme_button.pack(side=tk.RIGHT, padx=10)
    
    # Панель параметров стрельбы
    top_panel = ttk.Frame(main_frame)
    top_panel.pack(fill=tk.X, pady=(0, 15))
    params_frame = ttk.LabelFrame(top_panel, text="ПАРАМЕТРЫ СТРЕЛЬБЫ", padding=15)
    params_frame.pack(fill=tk.X)
    
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
              style="Accent.TButton").pack(side=tk.LEFT, padx=10)
    
    # Параметры снаряда
    shell_frame = ttk.LabelFrame(params_frame, text="ПАРАМЕТРЫ СНАРЯДА", padding=10)
    shell_frame.pack(fill=tk.X, pady=15)
    
    shell_info = ttk.Frame(shell_frame)
    shell_info.pack(fill=tk.X)
    
    ttk.Label(shell_info, text=f"Снаряд: ФАБ-500", 
             font=app.input_font).pack(side=tk.LEFT, padx=5)
    
    ttk.Label(shell_info, text=f"Нач. скорость: {app.V0} м/с", 
             font=app.input_font).pack(side=tk.LEFT, padx=15)
    
    ttk.Label(shell_info, text=f"Масса: {app.MASS} кг", 
             font=app.input_font).pack(side=tk.LEFT, padx=15)
    
    # Панель углов возвышения
    angles_frame = ttk.Frame(main_frame)
    angles_frame.pack(fill=tk.X, pady=(0, 10))
    
    # Угол навесного огня
    angle1_frame = ttk.Frame(angles_frame)
    angle1_frame.pack(side=tk.LEFT, padx=20)
    ttk.Label(angle1_frame, text="НАВЕСНОЙ ОГОНЬ", 
             font=("Segoe UI Semibold", 11), foreground="#1E90FF").pack(pady=(0, 5))
    app.angle1_var = tk.StringVar(value="0.00°")
    ttk.Label(angle1_frame, textvariable=app.angle1_var, 
             font=app.angle_font).pack()

    # Время полёта снаряда навесного огня
    angle4_frame = ttk.Frame(angles_frame)
    angle4_frame.pack(side=tk.LEFT, padx=20)
    ttk.Label(angle4_frame, text="ВРЕМЯ ПОЛЁТА", 
             font=("Segoe UI Semibold", 11), foreground="#1E90FF").pack(pady=(0, 5))
    app.angle4_var = tk.StringVar(value="0 сек")
    ttk.Label(angle4_frame, textvariable=app.angle4_var, 
             font=app.angle_font).pack()
    
    # Угол прямого огня
    angle2_frame = ttk.Frame(angles_frame)
    angle2_frame.pack(side=tk.LEFT, padx=20)
    ttk.Label(angle2_frame, text="ПРЯМОЙ ОГОНЬ", 
             font=("Segoe UI Semibold", 11), foreground="#DC143C").pack(pady=(0, 5))
    app.angle2_var = tk.StringVar(value="0.00°")
    ttk.Label(angle2_frame, textvariable=app.angle2_var, 
             font=app.angle_font).pack()

    # Время полёта снаряда прямого огня
    angle3_frame = ttk.Frame(angles_frame)
    angle3_frame.pack(side=tk.LEFT, padx=20)
    ttk.Label(angle3_frame, text="ВРЕМЯ ПОЛЁТА", 
             font=("Segoe UI Semibold", 11), foreground="#DC143C").pack(pady=(0, 5))
    app.angle3_var = tk.StringVar(value="0 сек")
    ttk.Label(angle3_frame, textvariable=app.angle3_var, 
             font=app.angle_font).pack()
    
    # Центральная панель
    center_panel = ttk.Frame(main_frame)
    center_panel.pack(fill=tk.BOTH, expand=True)
    
    # График траектории
    traj_frame = ttk.LabelFrame(center_panel, text="ТРАЕКТОРИЯ ПОЛЕТА", padding=10)
    traj_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    app.fig_traj = plt.figure(figsize=(8, 4))
    app.ax_traj = app.fig_traj.add_subplot(111)
    app.canvas_traj = FigureCanvasTkAgg(app.fig_traj, master=traj_frame)
    app.canvas_traj.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    # Баллистические данные
    ballistics_frame = ttk.LabelFrame(center_panel, text="БАЛЛИСТИЧЕСКИЕ ДАННЫЕ", padding=15)
    ballistics_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False, padx=(10, 0))
    app.ballistics_text = scrolledtext.ScrolledText(
        ballistics_frame, 
        font=app.info_font,
        height=20, 
        relief=tk.FLAT
    )
    app.ballistics_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    app.ballistics_text.config(state=tk.DISABLED)
    
    # Настройка стилей
    setup_styles(app)