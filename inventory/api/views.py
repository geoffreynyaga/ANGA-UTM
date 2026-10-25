from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import SAFE_METHODS, BasePermission, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from inventory.api.serializers import (
    AddStockSerializer,
    AircraftModelSerializer,
    ComponentRequestSerializer,
    ComponentTypeDetailSerializer,
    ComponentTypeSerializer,
    ComponentUnitSerializer,
    RpasSerializer,
    StockLotSerializer,
)
from inventory.models import (
    AircraftModel,
    ComponentRequest,
    ComponentType,
    ComponentUnit,
    StockLot,
    Tag,
    can_approve,
    is_read_only,
)
from rpas.models import Rpas


class InventoryPermission(BasePermission):
    """Organization members can read and write; CAA and MOD users can only read."""

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return not is_read_only(request.user)


class InventoryAPIView:
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated, InventoryPermission]
    pagination_class = None

    @property
    def organization(self):
        return self.request.user.userprofile.organization

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["organization"] = self.organization
        return context

    def require_organization(self):
        if self.organization is None:
            raise ValidationError("Your account is not linked to an organization.")


def run_model_action(action, *args, **kwargs):
    """Turn model validation errors into 400 responses."""
    try:
        return action(*args, **kwargs)
    except DjangoValidationError as error:
        raise ValidationError(error.messages)


class CurrentUserAPIView(InventoryAPIView, APIView):
    def get(self, request, *args, **kwargs):
        return Response(
            {
                "id": request.user.pk,
                "can_approve": can_approve(request.user),
                "read_only": is_read_only(request.user),
            }
        )


class AircraftModelListAPIView(InventoryAPIView, generics.ListAPIView):
    queryset = AircraftModel.objects.all()
    serializer_class = AircraftModelSerializer


class TagListAPIView(InventoryAPIView, APIView):
    def get(self, request, *args, **kwargs):
        return Response(Tag.objects.values_list("name", flat=True))


class OrganizationRpasListAPIView(InventoryAPIView, generics.ListAPIView):
    serializer_class = RpasSerializer

    def get_queryset(self):
        return Rpas.objects.filter(organization=self.organization)


class ComponentTypeListCreateAPIView(InventoryAPIView, generics.ListCreateAPIView):
    serializer_class = ComponentTypeSerializer

    def get_queryset(self):
        return (
            ComponentType.objects.with_stock(self.organization)
            .select_related("parent")
            .prefetch_related("tags", "aircraft_models")
        )

    def perform_create(self, serializer):
        # New types from organizations wait for a platform admin to review them
        self.require_organization()
        serializer.save(status=ComponentType.PENDING, proposed_by=self.request.user)


class ComponentTypeDetailAPIView(InventoryAPIView, generics.RetrieveUpdateAPIView):
    serializer_class = ComponentTypeDetailSerializer

    def get_queryset(self):
        return ComponentType.objects.with_stock(self.organization)

    def get_serializer(self, *args, **kwargs):
        # Organization users may only change tags on shared catalog entries
        if self.request.method not in SAFE_METHODS and not self.request.user.is_staff:
            data = kwargs.get("data")
            if data is not None:
                kwargs["data"] = {"tags": data.get("tags", [])}
                kwargs["partial"] = True
        return super().get_serializer(*args, **kwargs)


class AddStockAPIView(InventoryAPIView, APIView):
    def post(self, request, *args, **kwargs):
        self.require_organization()
        serializer = AddStockSerializer(
            data=request.data, context={"organization": self.organization}
        )
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        component_type = data["component_type"]
        common = {
            "organization": self.organization,
            "component_type": component_type,
            "condition": data["condition"],
            "origin": data["origin"],
            "source_rpas": data.get("source_rpas"),
            "created_by": request.user,
        }

        if component_type.is_serialized:
            with transaction.atomic():
                units = [
                    ComponentUnit.objects.create(
                        serial_number=serial,
                        last_serviced=data.get("last_serviced"),
                        **common,
                    )
                    for serial in data["serial_numbers"]
                ]
            body = {"units": ComponentUnitSerializer(units, many=True).data}
        else:
            lot = run_model_action(StockLot.add, quantity=data["quantity"], **common)
            body = {"lot": StockLotSerializer(lot).data}
        return Response(body, status=status.HTTP_201_CREATED)


class ComponentUnitUpdateAPIView(InventoryAPIView, generics.UpdateAPIView):
    serializer_class = ComponentUnitSerializer

    def get_queryset(self):
        return ComponentUnit.objects.filter(organization=self.organization)


class ComponentRequestListCreateAPIView(InventoryAPIView, generics.ListCreateAPIView):
    serializer_class = ComponentRequestSerializer

    def get_queryset(self):
        return ComponentRequest.objects.filter(
            organization=self.organization
        ).select_related(
            "component_type", "rpas", "unit", "requested_by", "decided_by"
        )

    def perform_create(self, serializer):
        self.require_organization()
        data = serializer.validated_data
        serializer.instance = run_model_action(
            ComponentRequest.place,
            requested_by=self.request.user,
            rpas=data["rpas"],
            quantity=data.get("quantity", 1),
            lot=data.get("lot"),
            unit=data.get("unit"),
            note=data.get("note", ""),
        )


class ComponentRequestActionAPIView(InventoryAPIView, APIView):
    ACTIONS = ("approve", "reject", "cancel")

    def post(self, request, pk, action, *args, **kwargs):
        if action not in self.ACTIONS:
            return Response(status=status.HTTP_404_NOT_FOUND)
        component_request = get_object_or_404(
            ComponentRequest, pk=pk, organization=self.organization
        )
        run_model_action(getattr(component_request, action), request.user)
        return Response(ComponentRequestSerializer(component_request).data)
