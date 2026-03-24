from rest_framework.authentication import SessionAuthentication
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from administration.models import FieldExpense, FieldRequisition
from applications.models import Project
from .serializers import FieldExpenseSerializer, FieldRequisitionSerializer
from django.utils.dateparse import parse_date


class FieldExpenseCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        data = request.data
        print(data)

        project_id = data.get("project")
        if not project_id:
            return Response(
                {"ResultDesc": "Project ID is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return Response(
                {"ResultDesc": "Project Not Found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        start_date_str = data.get("date")
        start_date = parse_date(start_date_str) if start_date_str else None

        try:
            field_expense = FieldExpense.objects.create(
                project=project,
                amount=data.get("amount", 0),
                category=data.get("category"),
                description=data.get("description"),
                start_date=start_date,
                user=request.user,
            )

        except Exception as e:
            print(f"Error creating field expense: {e}")
            return Response(
                {"ResultDesc": "Field Expense Not Created"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {"ResultDesc": "Field Expense Created successfully"},
            status=status.HTTP_201_CREATED,
        )


class FieldExpensesForProjectAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        try:
            project = Project.objects.get(id=pk)
        except Project.DoesNotExist:
            return Response(
                {"ResultDesc": "Project Not Found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        field_expenses = FieldExpense.objects.filter(project=project)
        serializer = FieldExpenseSerializer(field_expenses, many=True)
        return Response(serializer.data)


class FieldExpenseListCreateAPIView(generics.ListCreateAPIView):
    queryset = FieldExpense.objects.all()
    serializer_class = FieldExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FieldExpenseRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FieldExpense.objects.all()
    serializer_class = FieldExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]


class FieldRequisitionListCreateAPIView(generics.ListCreateAPIView):
    queryset = FieldRequisition.objects.all()
    serializer_class = FieldRequisitionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FieldRequisitionRetrieveUpdateDestroyAPIView(
    generics.RetrieveUpdateDestroyAPIView
):
    queryset = FieldRequisition.objects.all()
    serializer_class = FieldRequisitionSerializer
    permission_classes = [permissions.IsAuthenticated]
