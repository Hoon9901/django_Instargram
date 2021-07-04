from django.urls import path
from .views import PhotoList, PhotoCreate, PhotoDelete, PhotoDetail, PhotoUpdate
from django.conf.urls.static import static
from django.conf import settings

app_name = 'photo'  # namespace 확보
urlpatterns = [
    # 클래스형 뷰 사용
    path('', PhotoList.as_view(), name = 'index'),
    path('create/', PhotoCreate.as_view(), name = 'create'),
    path('delete/<int:pk>/', PhotoDelete.as_view(), name = 'delete'),
    path('update/<int:pk>/', PhotoUpdate.as_view(), name = 'update'),
    path('detail/<int:pk>/', PhotoDetail.as_view(), name = 'detail'),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)