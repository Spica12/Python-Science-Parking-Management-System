from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import LicensePlate
from .utils import get_num_auto_png_io

@csrf_exempt
def upload_image(request):
    if request.method == 'POST':
        if 'image' in request.FILES:
            image_file = request.FILES['image']
            result = get_num_auto_png_io(image_file.read())
            if result:
                plate_number = result.get('num_avto_str', '')
                accuracy = result.get('accuracy', 0)
                image_path = result.get('num_img', None)
                if plate_number and accuracy > 0 and image_path:
                    license_plate = LicensePlate.objects.create(
                        plate_number=plate_number,
                        accuracy=accuracy,
                        image=image_file
                    )
                    return JsonResponse({'status': 'success', 'plate_number': plate_number, 'accuracy': accuracy})
    return render(request, 'upload.html')
