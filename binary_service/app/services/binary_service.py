import base64
import cv2
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class ImageBase64Request(BaseModel):
    image_base64: str  # Входящее изображение в base64

def decode_base64_to_image(base64_string: str) -> np.ndarray:
    """ Декодирует изображение из base64 в NumPy (OpenCV) """
    try:
        image_data = base64.b64decode(base64_string)
        np_arr = np.frombuffer(image_data, np.uint8)
        return cv2.imdecode(np_arr, cv2.IMREAD_GRAYSCALE)  # Загружаем в градациях серого
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid base64 image format")

def encode_image_to_base64(image: np.ndarray) -> str:
    """ Кодирует изображение NumPy в base64 """
    _, buffer = cv2.imencode('.png', image)
    return base64.b64encode(buffer).decode("utf-8")

def bradley_threshold(image: np.ndarray, S_div: int = 8, t: float = 0.15) -> np.ndarray:
    """ Реализация бинаризации изображения по алгоритму Брэдли с исправленным переполнением """
    height, width = image.shape[:2]
    S = width // S_div  # Размер локального окна
    s2 = S // 2

    # Вычисляем интегральное изображение
    integral_image = cv2.integral(image, sdepth=cv2.CV_64F)  # Изменяем тип данных на float64

    # Создаём выходное бинарное изображение
    binary_image = np.zeros_like(image, dtype=np.uint8)

    for y in range(height):
        for x in range(width):
            x1, x2 = max(0, x - s2), min(width - 1, x + s2)
            y1, y2 = max(0, y - s2), min(height - 1, y + s2)

            count = (x2 - x1) * (y2 - y1)
            sum_region = (
                integral_image[y2 + 1, x2 + 1]
                - integral_image[y1, x2 + 1]
                - integral_image[y2 + 1, x1]
                + integral_image[y1, x1]
            )

            # ✅ Исправляем переполнение
            if int(image[y, x]) * count < sum_region * (1.0 - t):
                binary_image[y, x] = 0
            else:
                binary_image[y, x] = 255

    return binary_image
