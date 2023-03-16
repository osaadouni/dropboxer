from rest_framework import viewsets, parsers

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render

from uploader.models import DropBox, DropBoxPrivate
from uploader.serializers import DropBoxSerializer


# API classes 
class DropBoxViewset(viewsets.ModelViewSet):

    queryset = DropBox.objects.all()
    serializer_class = DropBoxSerializer
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]
    http_method_names = ['get', 'post', 'patch', 'delete']



#
def image_upload(request):
    if request.method == 'POST':
        image_file = request.FILES['image_file']
        image_type = request.POST['image_type']

        print(f"Uploading file [name={image_file.name}, type={image_type}]")

        if settings.USE_S3:
            if image_type == 'privafe':
                upload = DropBoxPrivate(document=image_file)
            else:
                upload = DropBox(document=image_file)
            upload.save()
            image_url = upload.document.url 
        else:
            fs = FileSystemStorage()
            filename = fs.save(image_file.name, image_file)
            image_url = fs.url(filename)
        return render(request, 'uploader/upload_form.html', {
            'image_url': image_url
        })


    return render(request, 'uploader/upload_form.html')

