import numpy as np

def calculate_ballistics(distance, elevation, V0, MASS, DRAG_COEFFICIENT):
    """Расчет баллистической траектории"""
    g = 9.81
    dt = 0.05
    time = 0
    x, z = 0, 0
    
    # Начальные скорости
    elevation_rad = np.radians(elevation)
    vx = V0 * np.cos(elevation_rad)
    vz = V0 * np.sin(elevation_rad)
    
    # Параметры сопротивления воздуха
    rho = 1.225
    A = 0.5
    
    trajectory = []
    
    while z >= 0 and time < 60:
        v = np.sqrt(vx**2 + vz**2)
        drag_force = 0.5 * rho * v**2 * A * DRAG_COEFFICIENT
        drag_x = drag_force * (-vx / v)
        drag_z = drag_force * (-vz / v)
        
        ax = drag_x / MASS
        az = (drag_z / MASS) - g
        
        vx += ax * dt
        vz += az * dt
        x += vx * dt
        z += vz * dt
        
        trajectory.append((time, x, z, v))
        time += dt
    
    # Корректировка траектории
    trajectory = np.array(trajectory)
    if len(trajectory) > 0 and trajectory[-1, 1] > 0:
        scale_factor = distance / trajectory[-1, 1]
        trajectory[:, 1] *= scale_factor
    
    return trajectory