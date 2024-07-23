from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UploadImageForm
from .predict_num import get_num_avto
from django.conf import settings
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
            result, _ = get_num_avto(img)
            
            # Виведення результатів
            messages.success(request, f'Розпізнано номерний знак: {result}')
            return redirect('upload_image')
    else:
        form = UploadImageForm()
    
    return render(request, 'plate_recognition/upload.html', {'form': form})
