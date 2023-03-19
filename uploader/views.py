from rest_framework import viewsets, parsers

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse

from uploader.models import DropBox, DropBoxPrivate
from uploader.serializers import DropBoxSerializer

from project.storage_backends import MediaStorage


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


class FileUploadView(View):
    def post(self, request, **kwargs):
        file_obj = request.FILES.get('file', '')

        # do your validation here e.g. file size/type check 

        # organize a path for the file in bucket 
        file_directory_with_bucket = 'user_upload_files/{username}'.format(username=request.user)

        # synthesize a full file path; note that we included the filename
        file_path_within_bucket = os.path.join(
            file_directory_with_bucket, 
            file_obj.name
        )
    
        # get meida storage 
        media_storage =  MediaStorage()

        if not media_storage.exists(file_path_within_bucket): # avoid overwriting existing files
            media_storage.save(file_path_within_bucket, file_obj)
            file_url = media_storage.url(file_path_within_bucket)

            return JsonResponse({
                'message': 'OK', 
                'fileurl': file_url 
            })
        else:
            return JsonResponse({
                'message': 'Error: file {filename} already exists at {file_directory} in bucket {bucket_name}'.format(
                    filename=file_obj.name,
                    file_directory=file_directory_with_bucket,
                    bucket_name=media_storage.bucket_name)
            }, status=400)

