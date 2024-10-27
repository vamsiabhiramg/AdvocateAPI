from django.urls import path
from.import views
from .views import AdvocateDetail
from django.conf.urls import include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns=[
    path('', views.endpoints),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    #path('advocates/<str:username>/', AdvocateDetail.as_view(), name='advocate-detail'),

    path('advocates/',views.advocate_list, name="advocates"),
    #path('advocates/<str:username>/',views.advocate_detail),
    path('advocates/<str:username>/', AdvocateDetail.as_view(), name='advocate-detail'),
    #path('advocates/<str:username>/',views.AdvocateDetail.as_view()),
    
    #companies/
    path('companies/', views.companies_list)
    
    #companies/:id
    
    
    
]


