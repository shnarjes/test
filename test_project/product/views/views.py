from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status, viewsets
from django.core.cache import cache

from product.models.products import Product
from product.serializers.serializers import ProductSerializers


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
    serializer_class = ProductSerializers
    permission_classes = (IsOwnerOrReadOnly,)

    def get_queryset(self):
        queryset = Product.objects.prefetch_related('color').select_related('cat').all()
        return queryset

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request):
        queryset = cache.get('product')
        if queryset is None:
            queryset = self.get_queryset()
            cache.set('product', queryset, 5 * 60)
        serializer = ProductSerializers(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        key = "product" + str(pk)
        queryset = cache.get(key)
        if queryset is None:
            queryset = Product.objects.filter(pk=pk).prefetch_related('color').select_related('cat').first()
            cache.set(key, queryset, 5 * 60)
        serializer = ProductSerializers(queryset)
        return Response(serializer.data)

    def update(self, request):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request):
        breakpoint()
        instance = self.get_object()
        key = "product" + str(instance.id)
        cache.delete('product')
        cache.delete(key)
        instance.delete()
        return Response(status=status.HTTP_200_OK)
