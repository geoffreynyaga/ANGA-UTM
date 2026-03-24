from django.urls import path
from .views import (
    FieldExpenseListCreateAPIView,
    FieldExpenseRetrieveUpdateDestroyAPIView,
    FieldRequisitionListCreateAPIView,
    FieldRequisitionRetrieveUpdateDestroyAPIView,
    FieldExpenseCreateAPIView,
    FieldExpensesForProjectAPIView,
)

app_name = "administration_api"

urlpatterns = [
    path(
        "v1/field-expenses/create/",
        FieldExpenseCreateAPIView.as_view(),
        name="field-expense-create",
    ),
    path(
        "v1/field-expenses/",
        FieldExpenseListCreateAPIView.as_view(),
        name="field-expense-list",
    ),
    path(
        "v1/field-expenses/<int:pk>/list/",
        FieldExpensesForProjectAPIView.as_view(),
        name="field-expenses-for-project",
    ),
    path(
        "field-expenses/<int:pk>/",
        FieldExpenseRetrieveUpdateDestroyAPIView.as_view(),
        name="field-expense-detail",
    ),
    path(
        "field-requisitions/",
        FieldRequisitionListCreateAPIView.as_view(),
        name="field-requisition-list",
    ),
    path(
        "field-requisitions/<int:pk>/",
        FieldRequisitionRetrieveUpdateDestroyAPIView.as_view(),
        name="field-requisition-detail",
    ),
]
