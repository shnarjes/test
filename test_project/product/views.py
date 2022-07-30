from numpy import product
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework import generics, status ,viewsets

from django.shortcuts import get_object_or_404
from yaml import serialize

from product.models import Product
from product.serializers import ProductSerializers


class ProductAddView(generics.GenericAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = ProductSerializers

    def post(self, request, *args,  **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()
        content = ProductSerializers(product, context=self.get_serializer_context()).data
        return Response(content, status=status.HTTP_201_CREATED)


class ProductAPIViewSet(viewsets.ViewSet):

    def list(self, request):
        queryset = Product.objects.all()
        serializer = ProductSerializers(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Product.objects.all()
        product = get_object_or_404(queryset, pk=pk)
        serializer = ProductSerializers()
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        queryset = Product.objects.all()
        product = get_object_or_404(request, pk=pk)
        serializer = ProductSerializers()
        