from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UploadImageForm
from .predict_num import get_num_avto
from django.conf import settings
from datetime import datetime
import os

def upload_image(request):
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            image_file = request.FILES['image']
            img_path = os.path.join(settings.MEDIA_ROOT, 'uploaded_image.jpg')
            with open(img_path, 'wb+') as destination:
                for chunk in image_file.chunks():
                    destination.write(chunk)
            
            # Завантаження зображення
            from django.core.files.images import ImageFile
            from PIL import Image
            img = Image.open(img_path)

            # Обробка зображення
            plate_number, image_with_plate = get_num_avto(img)
            
            # Збереження зображення з номерним знаком
            plate_image_path = os.path.join(settings.MEDIA_ROOT, 'plate_image.jpg')
            image_with_plate.save(plate_image_path)

            # Виведення результатів
            messages.success(request, f'Розпізнано номерний знак: {plate_number}')
            messages.success(request, f'Час розпізнавання: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
            
            # Перехід до сторінки з результатами
            context = {
                'form': form,
                'plate_number': plate_number,
                'plate_image_url': plate_image_path,
            }
            return render(request, 'plate_recognition/results.html', context)
    else:
        form = UploadImageForm()
    
    return render(request, 'plate_recognition/upload.html', {'form': form})
