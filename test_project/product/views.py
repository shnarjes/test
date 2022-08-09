from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import generics, status, viewsets
from functools import partial

from django.shortcuts import get_object_or_404

from product.models import Product
from product.serializers import ProductSerializers


class ProductAddView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = ProductSerializers

    def post(self, request, *args,  **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()
        content = ProductSerializers(product, context=self.get_serializer_context()).data
        return Response(content, status=status.HTTP_201_CREATED)


class IsOwnerOrReadOnly(permissions.BasePermission):
    SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        else:
            return request.method in self.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        else:
            return request.method in self.SAFE_METHODS


class ProductAPIViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers
    permission_classes = (IsOwnerOrReadOnly,)

    def list(self, request):
        serializer = ProductSerializers(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializers(product)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_200_OK)
