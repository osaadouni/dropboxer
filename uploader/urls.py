from rest_framework.routers import SimpleRouter
from django.urls import path 

from uploader.views import DropBoxViewset, image_upload


router = SimpleRouter()
router.register('accounts', DropBoxViewset)
urlpatterns = router.urls


# add 
urlpatterns += [
    path('upload/', image_upload, name='upload-file'), 
]
