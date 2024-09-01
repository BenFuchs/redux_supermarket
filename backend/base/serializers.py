# serializers.py
from rest_framework import serializers
from .models import Profile, Product, Cart

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user', 'phone_number', 'address', 'age', 'gender']

    def validate_gender(self, value):
        GENDER_CHOICES = ['M', 'F', 'O', 'N']
        if value not in GENDER_CHOICES:
            raise serializers.ValidationError("Invalid gender choice")
        return value

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    productDesc = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'userID', 'productID', 'amount', 'productDesc', 'date']

    def get_productDesc(self, obj):
        return obj.productID.desc # this line implies that cart is getting the product desc from the Product model