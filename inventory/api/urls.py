from django.urls import path

from inventory.api import views

urlpatterns = [
    path("v1/me/", views.CurrentUserAPIView.as_view(), name="inventory_me_api"),
    path(
        "v1/aircraft-models/",
        views.AircraftModelListAPIView.as_view(),
        name="inventory_aircraft_models_api",
    ),
    path("v1/tags/", views.TagListAPIView.as_view(), name="inventory_tags_api"),
    path(
        "v1/rpas/",
        views.OrganizationRpasListAPIView.as_view(),
        name="inventory_rpas_api",
    ),
    path(
        "v1/components/",
        views.ComponentTypeListCreateAPIView.as_view(),
        name="inventory_components_api",
    ),
    path(
        "v1/components/<int:pk>/",
        views.ComponentTypeDetailAPIView.as_view(),
        name="inventory_component_detail_api",
    ),
    path("v1/stock/", views.AddStockAPIView.as_view(), name="inventory_add_stock_api"),
    path(
        "v1/units/<int:pk>/",
        views.ComponentUnitUpdateAPIView.as_view(),
        name="inventory_unit_api",
    ),
    path(
        "v1/requests/",
        views.ComponentRequestListCreateAPIView.as_view(),
        name="inventory_requests_api",
    ),
    path(
        "v1/requests/<int:pk>/<str:action>/",
        views.ComponentRequestActionAPIView.as_view(),
        name="inventory_request_action_api",
    ),
]
