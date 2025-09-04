# products/serializers.py
from rest_framework import serializers
from .models import Product, Order, CompanyInfo, Inquiry, Review, Pillow, EPESheet

from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    is_staff = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = User
        fields = ("id", "username", "email", "is_staff")

class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Review
        fields = "__all__"
        read_only_fields = ("user", "created_at", "updated_at")

class ProductSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    reviews = ReviewSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = "__all__"

    def get_image(self, obj):
        request = self.context.get("request")
        if obj.image:
            if request is not None:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None

    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews:
            return sum(review.rating for review in reviews) / len(reviews)
        return 0

    def get_review_count(self, obj):
        return obj.reviews.count()

class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = ("user","created_at")

class CompanyInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyInfo
        fields = "__all__"


class InquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inquiry
        fields = "__all__"


    
# pillows/serializers.py
from rest_framework import serializers
from .models import Pillow

class PillowSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Pillow
        fields = "__all__"

    def get_image(self, obj):
        request = self.context.get("request")
        if obj.image:
            if request is not None:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None
class EPESheetSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = EPESheet
        fields = "__all__"

    def get_image(self, obj):
        request = self.context.get("request")
        if obj.image:
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return None
    

class UserSerializer(serializers.ModelSerializer):
    is_staff = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = User
        fields = ("id", "username", "email", "is_staff")