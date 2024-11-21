from django.urls import path,reverse
from .views import NewBook,ThanksView
from rest_framework_simplejwt.views import ( TokenObtainPairView, TokenRefreshView,TokenVerifyView)
from django.shortcuts import redirect
from .views import RegisterUser, BookManagement, BorrowBook, ReturnBook

urlpatterns = [
    path('register/', RegisterUser.as_view(), name='register'),
    path('books/', BookManagement.as_view(), name='books'),
    path('borrow/', BorrowBook.as_view(), name='borrow'),
    path('return/<int:borrowing_id>/', ReturnBook.as_view(), name='return'),
    path('jwt/create/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('jwt/create/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('jwt/create/verify/', TokenVerifyView.as_view(), name='token_verify')
    
    
]