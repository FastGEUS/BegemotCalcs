import tkinter as tk
from app import BegemotArtilleryCalculator

if __name__ == "__main__":
    root = tk.Tk()
    app = BegemotArtilleryCalculator(root)
    
    # Добавляем обработчик корректного закрытия окна
    def on_closing():
        root.destroy()
        root.quit()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    root.mainloop()
