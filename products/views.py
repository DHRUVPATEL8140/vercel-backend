# products/views.py
from django.shortcuts import render
from rest_framework import viewsets, permissions, status, generics, serializers
from django.db.models import Q
from .models import Product, Order, CompanyInfo, Inquiry, Review, Pillow, EPESheet
from .serializers import ProductSerializer, OrderSerializer, CompanyInfoSerializer,UserSerializer, InquirySerializer, ReviewSerializer,PillowSerializer, EPESheetSerializer
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.permissions import IsAdminUser, AllowAny
from io import BytesIO
from django.http import HttpResponse

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by("-created_at")
    serializer_class = ProductSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [permissions.IsAuthenticatedOrReadOnly()]

    # search and filter example
    def get_queryset(self):
        qs = super().get_queryset()
        params = self.request.query_params

        # Exact filters
        density = params.get("density")
        color = params.get("color")
        size = params.get("size")
        if density:
            qs = qs.filter(density=density)
        if color:
            qs = qs.filter(color__iexact=color)
        if size:
            qs = qs.filter(size__iexact=size)

        # Price range
        min_price = params.get("min_price")
        max_price = params.get("max_price")
        if min_price:
            qs = qs.filter(price__gte=min_price)
        if max_price:
            qs = qs.filter(price__lte=max_price)

        # Search in name and description
        search = params.get("search") or params.get("q")
        if search:
            qs = qs.filter(Q(name__icontains=search) | Q(description__icontains=search))

        # Ordering
        ordering = params.get("ordering")
        if ordering in {"price", "-price", "density", "-density", "created_at", "-created_at"}:
            qs = qs.order_by(ordering)
        return qs

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all().order_by("-created_at")
        return Order.objects.filter(user=user).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CompanyInfoViewSet(viewsets.ModelViewSet):
    queryset = CompanyInfo.objects.all()
    serializer_class = CompanyInfoSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        return [IsAdminUser()]

    @action(detail=False, methods=["get"]) 
    def single(self, request):
        ci = self.get_queryset().first()
        if ci is None:
            return Response({}, status=status.HTTP_200_OK)
        serializer = self.get_serializer(ci)
        return Response(serializer.data)

class InquiryViewSet(viewsets.ModelViewSet):
    queryset = Inquiry.objects.all().order_by("-created_at")
    serializer_class = InquirySerializer
    permission_classes = [permissions.AllowAny]

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Review.objects.all().order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def product_reviews(self, request):
        product_id = request.query_params.get('product_id')
        if product_id:
            reviews = Review.objects.filter(product_id=product_id).order_by('-created_at')
            serializer = self.get_serializer(reviews, many=True)
            return Response(serializer.data)
        return Response([], status=status.HTTP_400_BAD_REQUEST)

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ("username","email","password")
    def validate_username(self, value):
        if len(value) < 4:
            raise serializers.ValidationError("Username must be at least 4 characters long")
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already taken")
        return value
    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long")
        return value
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email",""),
            password=validated_data["password"]
        )
        return user

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def company_analytics_chart(request):
    # Return JSON data instead of chart image for better performance
    data = {
        "months": ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"],
        "manufacturing": [120, 135, 150, 160, 170, 180, 175, 190, 200, 210, 205, 220],
        "sales": [100, 125, 140, 150, 165, 170, 168, 180, 190, 205, 198, 210]
    }
    return Response(data)





class PillowViewSet(viewsets.ModelViewSet):
    queryset = Pillow.objects.all().order_by("-created_at")
    serializer_class = PillowSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [permissions.IsAuthenticatedOrReadOnly()]

    def get_queryset(self):
        qs = super().get_queryset()
        params = self.request.query_params

        # Example filters (adjust if Pillow model fields differ)
        color = params.get("color")
        size = params.get("size")
        if color:
            qs = qs.filter(color__iexact=color)
        if size:
            qs = qs.filter(size__iexact=size)

        # Price range
        min_price = params.get("min_price")
        max_price = params.get("max_price")
        if min_price:
            qs = qs.filter(price__gte=min_price)
        if max_price:
            qs = qs.filter(price__lte=max_price)

        # Search
        search = params.get("search") or params.get("q")
        if search:
            qs = qs.filter(Q(name__icontains=search) | Q(description__icontains=search))

        return qs

 
class EPESheetViewSet(viewsets.ModelViewSet):
    queryset = EPESheet.objects.all().order_by("-created_at")
    serializer_class = EPESheetSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [permissions.IsAuthenticatedOrReadOnly()]

    def get_queryset(self):
        qs = super().get_queryset()
        params = self.request.query_params

        # Filtering
        size = params.get("size")
        if size:
            qs = qs.filter(size__iexact=size)

        # Price range
        min_price = params.get("min_price")
        max_price = params.get("max_price")
        if min_price:
            qs = qs.filter(price__gte=min_price)
        if max_price:
            qs = qs.filter(price__lte=max_price)

        # Search
        search = params.get("search") or params.get("q")
        if search:
            qs = qs.filter(Q(name__icontains=search) | Q(description__icontains=search))

        return qs
    



# products/views.py - Add this view
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def current_user(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)
