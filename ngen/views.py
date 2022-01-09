import django_filters
from rest_framework import permissions, filters
from rest_framework import viewsets

from ngen.models import Case, Network, Taxonomy, IncidentFeed, IncidentState, StateBehavior, \
    User, NetworkEntity, IncidentTlp, Priority, IncidentDecision, \
    Event, Report, IncidentStateChange, StateEdge, Contact
from ngen.serializers import IncidentSerializer, NetworkSerializer, TaxonomySerializer, IncidentFeedSerializer, \
    IncidentStateSerializer, StateBehaviorSerializer, UserSerializer, \
    NetworkEntitySerializer, IncidentTlpSerializer, PrioritySerializer, \
    IncidentDecisionSerializer, \
    IncidentDetectedSerializer, ReportSerializer, IncidentStateChangeSerializer, StateEdgeSerializer, \
    ContactSerializer


class IncidentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Case.objects.all()
    serializer_class = IncidentSerializer
    permission_classes = [permissions.IsAuthenticated]


class TaxonomyViewSet(viewsets.ModelViewSet):
    queryset = Taxonomy.objects.all()
    serializer_class = TaxonomySerializer
    permission_classes = [permissions.IsAuthenticated]


class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]


class IncidentFeedViewSet(viewsets.ModelViewSet):
    queryset = IncidentFeed.objects.all()
    serializer_class = IncidentFeedSerializer
    permission_classes = [permissions.IsAuthenticated]


class IncidentStateViewSet(viewsets.ModelViewSet):
    queryset = IncidentState.objects.all()
    serializer_class = IncidentStateSerializer
    permission_classes = [permissions.IsAuthenticated]


class IncidentStateChangeViewSet(viewsets.ModelViewSet):
    queryset = IncidentStateChange.objects.all()
    serializer_class = IncidentStateChangeSerializer
    permission_classes = [permissions.IsAuthenticated]


class StateEdgeViewSet(viewsets.ModelViewSet):
    queryset = StateEdge.objects.all()
    serializer_class = StateEdgeSerializer
    permission_classes = [permissions.IsAuthenticated]


class StateBehaviorViewSet(viewsets.ModelViewSet):
    queryset = StateBehavior.objects.all()
    serializer_class = StateBehaviorSerializer
    permission_classes = [permissions.IsAuthenticated]


class IncidentTlpViewSet(viewsets.ModelViewSet):
    queryset = IncidentTlp.objects.all()
    serializer_class = IncidentTlpSerializer
    permission_classes = [permissions.IsAuthenticated]


class PriorityViewSet(viewsets.ModelViewSet):
    queryset = Priority.objects.all()
    serializer_class = PrioritySerializer
    permission_classes = [permissions.IsAuthenticated]


class IncidentDecisionViewSet(viewsets.ModelViewSet):
    queryset = IncidentDecision.objects.all()
    serializer_class = IncidentDecisionSerializer
    permission_classes = [permissions.IsAuthenticated]


class IncidentDetectedViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = IncidentDetectedSerializer
    permission_classes = [permissions.IsAuthenticated]


class NetworkViewSet(viewsets.ModelViewSet):
    queryset = Network.objects.all()
    serializer_class = NetworkSerializer
    filter_backends = [filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend]
    search_fields = ['cidr', 'type', 'domain']
    filterset_fields = ['type']
    permission_classes = [permissions.IsAuthenticated]


class NetworkEntityViewSet(viewsets.ModelViewSet):
    queryset = NetworkEntity.objects.all()
    serializer_class = NetworkEntitySerializer
    permission_classes = [permissions.IsAuthenticated]


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
