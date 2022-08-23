from rest_framework import serializers

from product.models.products import Product


class ProductSerializers(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = [
            'name',
            'image',
            'image1',
            'image2',
            'price',
            'capacity',
            'discription',
            'color',
            'brand',
            'cat',
        ]
