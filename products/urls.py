# products/urls.py
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import ProductViewSet, OrderViewSet, CompanyInfoViewSet, InquiryViewSet, ReviewViewSet, company_analytics_chart, PillowViewSet,EPESheetViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

router = DefaultRouter()
router.register("products", ProductViewSet)
router.register("pillows", PillowViewSet)        
router.register("epe-sheets", EPESheetViewSet, basename="epe-sheets")
router.register("orders", OrderViewSet, basename="orders")
router.register("company", CompanyInfoViewSet, basename="company")
router.register("inquiries", InquiryViewSet, basename="inquiries")
router.register("reviews", ReviewViewSet, basename="reviews")

urlpatterns = [
    path("", include(router.urls)),
    path("auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    # products/urls.py - Add this path
    path("auth/user/", views.current_user, name="current_user"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # register endpoint
    path("auth/register/", views.RegisterView.as_view(), name="register"),
    # analytics image
    path("company/analytics/chart/", company_analytics_chart, name="company_analytics_chart"),
]
