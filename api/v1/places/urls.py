from django.urls import path,include
from api.v1.places import views

urlpatterns = [
    path('',views.places),
    path('view/<int:pk>',views.place),
    path('protected/<int:pk>',views.protected),
    path(' <int:pk>',views.create_comments),
    path('comments/view/<int:pk>',views.view_comments),
    path('likes/<int:pk>',views.like),
]
   