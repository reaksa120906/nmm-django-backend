from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    RegisterView, LoginView, ProfileView,
    ExpenseListCreateView, ExpenseDetailView,
    IncomeListCreateView, IncomeDetailView,
    SavingsListCreateView, SavingsDetailView,
)

urlpatterns = [
    # Auth
    path('register/',      RegisterView.as_view(),      name='register'),
    path('login/',         LoginView.as_view(),          name='login'),
    path('token/refresh/', TokenRefreshView.as_view(),   name='token-refresh'),
    path('profile/',       ProfileView.as_view(),        name='profile'),

    # Expenses
    path('expenses/',         ExpenseListCreateView.as_view(), name='expenses'),
    path('expenses/<int:pk>/', ExpenseDetailView.as_view(),    name='expense-detail'),

    # Income
    path('income/',         IncomeListCreateView.as_view(), name='income'),
    path('income/<int:pk>/', IncomeDetailView.as_view(),    name='income-detail'),

    # Savings
    path('savings/',         SavingsListCreateView.as_view(), name='savings'),
    path('savings/<int:pk>/', SavingsDetailView.as_view(),    name='savings-detail'),
]
