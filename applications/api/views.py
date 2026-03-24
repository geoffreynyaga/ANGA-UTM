from flight_plans.models import DailyWorkLog
from applications.api.serializers import (
    ProjectsListSerializer,
    ReserveAirspaceDetailSerializer,
    ReserveAirspaceListSerializer,
    DailyWorkLogForStatsSerializer,
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework import status
from django.db.models import Sum, Count
from rpas.models import Rpas

from applications.models import Project, ReserveAirspace
from administration.models import FieldExpense


class ProjectListExtraDetailsAPIView(APIView):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    queryset = Project.objects.all()

    def get(self, *args, **kwargs):
        org = self.request.user.userprofile.organization

        # Annotate each project with its aggregated metrics
        # We use the relationship name 'dailyworklog' (lowercase model name if not specified)
        projects = Project.objects.filter(organization=org).annotate(
            bags_spread_sum=Sum("dailyworklog__bags_spread"),
            acres_sprayed_sum=Sum("dailyworklog__acres_sprayed"),
            unique_rpas_count_per_project=Count("dailyworklog__rpas", distinct=True),
        )

        # Map annotated fields to serializer-friendly names if they differ
        for project in projects:
            project.bags_spread = project.bags_spread_sum or 0
            project.acres_sprayed = project.acres_sprayed_sum or 0
            project.unique_rpas_count = project.unique_rpas_count_per_project or 0

        projects_serialized = ProjectsListSerializer(projects, many=True).data

        return Response(
            {
                "projects": projects_serialized,
            },
            status=status.HTTP_200_OK,
        )


class ProjectDetailsAPIView(APIView):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, *args, **kwargs):
        project_id = self.kwargs["pk"]
        try:

            project = Project.objects.get(id=project_id)

        except Project.DoesNotExist:
            return Response(
                {"ResultDesc": "Project Not Found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        worklogs = DailyWorkLog.objects.filter(project=project)

        worklogs_serialized = DailyWorkLogForStatsSerializer(worklogs, many=True).data

        expenses = FieldExpense.objects.filter(project=project)
        total_expenses = expenses.aggregate(Sum("amount"))

        return Response(
            {
                "worklogs": worklogs_serialized,
                "total_expenses": total_expenses,
                "estimated_ops_budget": project.estimated_ops_budget,
            },
            status=status.HTTP_200_OK,
        )

class ProjectsListAPIView(ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectsListSerializer

    def get_queryset(self, *args, **kwargs):
        org = self.request.user.userprofile.organization
        queryset = Project.objects.filter(organization=org)
        return queryset

class ReserveCreateAPIView(APIView):
    permission_classes = (AllowAny,)
    # authentication_classes = (TokenAuthentication, SessionAuthentication)

    def post(self, request):
        import json

        print(request.data, "in API")
        project_id = request.data["project"]
        mission_type = request.data.get("mission_type", "OTH")
        geom = json.loads(request.data["geom"])
        rpas_ids = request.data["rpas"]
        start_day = request.data["start_day"]
        start_time = request.data["start_time"]
        end = request.data["end"]

        print(project_id, "project_id")
        print(geom, "geom")
        print(rpas_ids, "rpas_ids")
        print(start_day, "start_day")
        print(start_time, "start_time")
        print(end, "end")

        from datetime import datetime

        date_object = datetime.strptime(start_day, "%m/%d/%Y").date()
        start_time_object = datetime.strptime(start_time, "%I:%M %p").time()
        end_time_object = datetime.strptime(end, "%I:%M %p").time()

        from django.contrib.gis.geos import (
            GEOSGeometry,
            LineString,
            MultiLineString,
            Polygon,
        )

        # Handle GeoJSON FeatureCollection
        if geom.get("type") == "FeatureCollection":
            # Extract the first feature's geometry
            feature = geom["features"][0]
            geom_obj = GEOSGeometry(json.dumps(feature["geometry"]))
        else:
            geom_obj = GEOSGeometry(json.dumps(geom))

        x = ReserveAirspace.objects.create(
            geom=geom_obj,
            project_id=int(project_id),
            mission_type=mission_type,
            start_day=date_object,
            start_time=start_time_object,
            end=end_time_object,
            created_by=self.request.user,
        )
        if isinstance(rpas_ids, list):
            x.rpas.set(rpas_ids)
        else:
            x.rpas.add(int(rpas_ids))

        print(x, "x instance")
        try:
            x.full_clean()
            # The application_number is generated in save(), so we must save again
            # to ensure the finalized instance (with App #) is in the DB
            x.save()
        except Exception as e:
            print(e)
            # Since objects.create() already saved it, we must delete it if validation fails
            x.delete()
            return Response(
                {
                    "ResultDesc": "Reserve Airspace Not Created",
                    "ReserveAirspaceError": str(e),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {"ResultDesc": "Reserve Airspace Created successfully"},
            status=status.HTTP_201_CREATED,
        )


class ReserveAirspaceListAPIView(ListAPIView):
    queryset = ReserveAirspace.objects.all()
    serializer_class = ReserveAirspaceListSerializer


class ReserveAirspaceDetailAPIView(RetrieveAPIView):
    queryset = ReserveAirspace.objects.all()
    serializer_class = ReserveAirspaceDetailSerializer
    lookup_field = "pk"
