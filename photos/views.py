# photos/views.py
import time
import requests
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.files.storage import default_storage
from .models import UploadedImage
from .forms import ImageUploadForm
from dotenv import load_dotenv
import os
import json
from openai import OpenAI
import markdown
import base64


url = 'https://api.lightxeditor.com/external/api/v1/avatar'


def encode_image(image_path):
  image_path = "./media/uploads/" + os.path.basename(image_path)
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

def get_lightX_headers():
    load_dotenv(".env", override=True)
    LIGHTX_KEY = os.getenv("LIGHTX_KEY")
    headers = {
        'Content-Type': 'application/json',
        'x-api-key': LIGHTX_KEY
    }

    return headers


def get_gpt_description(image_path):
    # try:
    base64_image = encode_image(image_path)
    load_dotenv(".env", override=True)
    OPENAI_KEY = os.getenv("OPENAI_KEY")
    client = OpenAI(api_key=OPENAI_KEY, base_url="https://api.proxyapi.ru/openai/v1")
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text", 
                        "text": "What exercises should i do to gain more muscle mass?. Write answer in markdown format."
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                    }
                ]
            }
        ],
        max_tokens=100)

    return response.choices[0].message.content
    # except:
    #     return "Idk what to do :)"


def upload_image(request):
    form = ImageUploadForm(request.POST, request.FILES)
    if form.is_valid():
        headers = get_lightX_headers()

        data = {
        "imageUrl": None,  # Replace with the URL of your input image
        "styleImageUrl": "https//phantom-marca.unidadeditorial.es/052b50925b8b06aa421a1029e001b893/resize/990/f/webp/assets/multimedia/imagenes/2024/03/26/17114431722376.jpg",  # Replace with the URL of your input style image
        "textPrompt": "Imagine more stronger body, pay attention to the hairstyle, face, and individual features of human and save it"
        }

        # Save the uploaded image instance
        uploaded_image = form.save()
        uploaded_image.save()
        
        # Generate URL to the uploaded image
        image_url = request.build_absolute_uri(uploaded_image.original_image.url)
        print(image_url)

        data['imageUrl'] = image_url
        
        # Call external API to start processing the image
        response = requests.post(
            url,
            json=data,
            headers=headers
        )
        print(headers)
        if response.status_code == 200:
            data = response.json()
            if data["statusCode"] == 2000:
                print(data)
                uploaded_image.processing_id = data["body"]['orderId']
                uploaded_image.description_text = get_gpt_description(image_url)
                uploaded_image.save()
                # Redirect to status check page
                return redirect('check_status', image_id=uploaded_image.id)
        
        # Handle error if API request fails
        return JsonResponse(response.json(), status=500)
    else:
        form = ImageUploadForm()
    
    return render(request, 'photos/upload_photo.html', {'form': form})


def check_status(request, image_id):
    try:
        uploaded_image = UploadedImage.objects.get(id=image_id)
    except UploadedImage.DoesNotExist:
        return JsonResponse({'error': 'Image not found'}, status=404)
    
    # Check processing status
    headers = get_lightX_headers()
    payload = {"orderId": uploaded_image.processing_id}
    response = requests.post('https://api.lightxeditor.com/external/api/v1/order-status', headers=headers, data=json.dumps(payload))
    
    if response.status_code == 200:
        data = response.json()["body"]
        print(data)
        if data['status'] == 'active':
            # Save processed image URL and redirect to result page
            uploaded_image.processed_image_url = data['output']
            uploaded_image.save()
            
            return redirect('view_result', image_id=uploaded_image.id)
        elif data["status"] == 'init':
            # If still processing, wait and reload the page
            time.sleep(3.5)
            return redirect('check_status', image_id=image_id)
    
    return JsonResponse({'error': 'Failed to check status'}, status=500)


def view_result(request, image_id):
    try:
        uploaded_image = UploadedImage.objects.get(id=image_id)
    except UploadedImage.DoesNotExist:
        return JsonResponse({'error': 'Image not found'}, status=404)
    
    html_descr = markdown.markdown(uploaded_image.description_text)
    context = {
        'original_image_url': uploaded_image.original_image.url,
        'processed_image_url': uploaded_image.processed_image_url,
        "description": html_descr
    }
    return render(request, 'photos/photo_result.html', context)
