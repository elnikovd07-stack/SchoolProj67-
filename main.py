import math
from fastapi import FastAPI
import uvicorn

app = FastAPI()

# Изначальное состояние робота (глобальные переменные)
# Угол 90 градусов означает, что робот смотрит "вверх" по оси Y
robot_state = {
    "x": 0.0,
    "y": 0.0,
    "angle": 90.0  
}

@app.get('/robot')
def get_robot():
    """Возвращает текущие координаты робота и его направление в градусах."""
    return {
        "status": "Робот на экране",
        "position": [round(robot_state["x"], 2), round(robot_state["y"], 2)],
        "direction_degrees": round(robot_state["angle"] % 360, 2)
    }

@app.get('/turn')
def turn(deg: int):
    """Поворачивает робота на deg градусов вправо (по часовой стрелке)."""
    # Поворот вправо уменьшает угол на окружности
    robot_state["angle"] -= deg
    return {
        "message": f"Робот повернулся вправо на {deg} градусов",
        "current_direction": round(robot_state["angle"] % 360, 2)
    }

@app.get('/move')
def move(ln: int):
    """Шагает вперед (ln > 0) или назад (ln < 0) в направлении своего взгляда."""
    # Переводим текущий угол робота в радианы для функций math.cos и math.sin
    radians = math.radians(robot_state["angle"])
    
    # Шаг вперед (ln положительный) или назад (ln отрицательный)
    robot_state["x"] += ln * math.cos(radians)
    robot_state["y"] += ln * math.sin(radians)
    
    direction = "вперед" if ln >= 0 else "назад"
    return {
        "message": f"Робот шагнул {direction} на расстояние {abs(ln)}",
        "new_position": [round(robot_state["x"], 2), round(robot_state["y"], 2)]
    }

if __name__ == "__main__":
    uvicorn.run('main:app', host='0.0.0.0', port=10006)