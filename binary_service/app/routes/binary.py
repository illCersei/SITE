from fastapi import APIRouter
from app.services.binary_service import ImageBase64Request, decode_base64_to_image, bradley_threshold, encode_image_to_base64

router = APIRouter()

@router.post("/binary_image")
def process_binary_image(request: ImageBase64Request):
    """ Принимает изображение в base64, бинаризует его и возвращает обратно в base64 """
    image = decode_base64_to_image(request.image_base64)  # Декодируем base64 в NumPy
    binary_image = bradley_threshold(image)  # Бинаризуем изображение
    binary_base64 = encode_image_to_base64(binary_image)  # Кодируем обратно в base64
    return {"binary_image_base64": binary_base64}  # Возвращаем результат