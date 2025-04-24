from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets
from .serializer import *
from .models import *

class TransactionView(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()

class CategoryView(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()