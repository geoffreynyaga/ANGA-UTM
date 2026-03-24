from datetime import datetime
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication

from flight_plans.api.serializers import (
    CheckListDetailSerializer,
    FlightLogListSerializer,
    CheckListTemplateListSerializer,
    WorkLogDetailSerializer,
    WorkLogListSerializer,
)
from flight_plans.models import ChecklistTemplate, DailyWorkLog
from rpas.models import RpasModel


class DailyWorkLogListAPIView(generics.ListAPIView):
    serializer_class = FlightLogListSerializer

    def get_queryset(self):
        """
        This view should return a list of all the logs
        for the currently authenticated user.
        """
        return DailyWorkLog.objects.filter(user=self.request.user).order_by("-id")


class CheckListDetailAPIView(generics.RetrieveAPIView):
    queryset = ChecklistTemplate.objects.all()
    serializer_class = CheckListDetailSerializer
    lookup_field = "pk"


class ChecklistTemplateListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]

    def get(self, request, *args, **kwargs):
        queryset = ChecklistTemplate.objects.filter(
            organization=self.request.user.userprofile.organization
        )
        serialized_data = CheckListTemplateListSerializer(queryset, many=True)
        return Response(serialized_data.data)


class CheckListTemplateCreateAPIView(APIView):
    """
    API View to create new ChecklistTemplate(s) from the React UI builder.
    It iterates over the 'checklist' object keys (e.g. Pre-Flight, Post-Flight)
    and saves each as a separate template.
    """

    def post(self, request, *args, **kwargs):
        data = request.data
        print(request.user, "user")
        checklist_data = data.get("checklist", {})

        if not checklist_data:
            return Response(
                {"error": "No checklist data provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        title = data.get("title", "Checklist")
        rpas_model_id = data.get("rpas_model_id")

        rpas_model = None
        if rpas_model_id:
            try:
                rpas_model = RpasModel.objects.get(id=rpas_model_id)
            except:
                pass

        created_ids = []

        # Mapping UI keys to model choices
        type_mapping = {
            "Pre-Flight": "PRE",
            "Post-Flight": "POS",
            "In-Flight": "INF",
            "Emergency": "EMR",
        }

        for key, items in checklist_data.items():
            ctype = type_mapping.get(key, "OTH")

            # Save each part as a separate template
            template = ChecklistTemplate.objects.create(
                title=f"{title} ({key})",
                checklist_type=ctype,
                checklist_data={key: items},  # Store the specific section
                rpas_model=rpas_model,
                created_by=request.user if request.user.is_authenticated else None,
            )
            created_ids.append(template.id)

        return Response(
            {
                "ids": created_ids,
                "message": f"Successfully created {len(created_ids)} checklist templates",
            },
            status=status.HTTP_201_CREATED,
        )


class WorkLogCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]

    def post(self, request, *args, **kwargs):
        data = request.data
        print(data, "data")

        # Parsing operation_date and time into a single datetime object
        # data examples: 'operation_date': '2026-03-22', 'time': '08:00 AM'
        op_date_str = data.get("operation_date")
        op_time_str = data.get("time")

        operation_datetime = None
        if op_date_str and op_time_str:
            try:
                # Combine date and time strings
                combined_str = f"{op_date_str} {op_time_str}"
                # Parse using the format: YYYY-MM-DD HH:MM AM/PM
                operation_datetime = datetime.strptime(
                    combined_str, "%Y-%m-%d %I:%M %p"
                )
            except Exception as e:
                print(f"Error parsing datetime: {e}")
                # Fallback to current time or handle as error
                pass

        project_id = data.get("project")
        rpas_id = data.get("rpas")

        # Prevent duplicate entries for the same RPAS on the same Project on the same Day
        if operation_datetime:
            existing_log = DailyWorkLog.objects.filter(
                project__id=project_id,
                rpas__id=rpas_id,
                operation_date__date=operation_datetime.date(),
            ).first()

            if existing_log:
                user_name = existing_log.user.first_name or existing_log.user.username
                return Response(
                    {
                        "error": f"User {user_name} has already added this RPAS to their daily log today"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

        x = DailyWorkLog.objects.create(
            user=request.user,
            # organization=request.user.userprofile.organization,
            project_id=project_id,
            rpas_id=rpas_id,
            preflight_template_id=data.get("preflight_template"),
            postflight_template_id=data.get("post_flight_template"),
            operation_date=operation_datetime,
        )

        return Response(
            {
                "id": x.id,
                "message": "Successfully created work log",
            },
            status=status.HTTP_201_CREATED,
        )


class WorkLogUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]

    def post(self, request, *args, **kwargs):
        data = request.data
        # print(data, "data")

        work_log_id = data.get("work_log_id")
        if not work_log_id:
            return Response(
                {"error": "work_log_id is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            work_log = DailyWorkLog.objects.get(id=work_log_id)
        except DailyWorkLog.DoesNotExist:
            return Response(
                {"error": "Work log not found"}, status=status.HTTP_404_NOT_FOUND
            )

        # Update Performance Metrics
        bags_spread = data.get("bags_spread")
        if bags_spread is not None:
            work_log.bags_spread = bags_spread

        acres_sprayed = data.get("acres_sprayed")
        if acres_sprayed is not None:
            work_log.acres_sprayed = acres_sprayed

        app_rate = data.get("application_rate_spraying")
        if app_rate is not None:
            work_log.application_rate_spraying = app_rate

        # Update Checklist Results
        results = data.get("results", {})
        preflight_data = results.get("Pre-Flight")
        postflight_data = results.get("Post-Flight")

        if preflight_data:
            work_log.preflight_results = preflight_data
            pre_saved_str = data.get("preflight_saved_at")
            work_log.preflight_saved_at = (
                parse_datetime(pre_saved_str) if pre_saved_str else timezone.now()
            )

        if postflight_data:
            work_log.postflight_results = postflight_data
            post_saved_str = data.get("postflight_saved_at")
            work_log.postflight_saved_at = (
                parse_datetime(post_saved_str) if post_saved_str else timezone.now()
            )

        # Mark as complete if we are saving post-flight or based on some condition
        # For now, let's assume if they sent it and it has results, it's progress
        if preflight_data and postflight_data:
            work_log.is_complete = True

        work_log.save()

        return Response(
            {
                "id": work_log.id,
                "message": "Successfully updated work log",
                "is_complete": work_log.is_complete,
            },
            status=status.HTTP_200_OK,
        )


class WorkLogDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]

    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")

        try:
            work_log = DailyWorkLog.objects.get(id=pk)

        except DailyWorkLog.DoesNotExist:
            return Response(
                {
                    "error": "Work log not found",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serialized_data = WorkLogDetailSerializer(work_log)

        return Response(serialized_data.data)


class WorkLogListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]

    def get(self, request, *args, **kwargs):
        queryset = DailyWorkLog.objects.filter(
            user=request.user,
            is_complete=False,
        )

        serialized_data = WorkLogListSerializer(queryset, many=True)

        return Response(serialized_data.data)
