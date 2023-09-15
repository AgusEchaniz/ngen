from datetime import datetime, timedelta

import jwt
from auditlog.models import LogEntry
from colorfield.serializers import ColorField
from comment.models import Comment
from constance import config
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.utils.text import slugify
from django.utils.translation import gettext
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from ngen import models
from ngen.models import User
from ngen.utils import get_settings


class NgenModelSerializer(serializers.HyperlinkedModelSerializer):
    history = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='logentry-detail'
    )


class GenericRelationField(serializers.RelatedField):
    def to_internal_value(self, data):
        pass

    def to_representation(self, related_list):
        return self.generic_detail_links(related_list)

    def generic_detail_link(self, related, request=None):
        return self.generic_detail_link(related, request)

    def generic_detail_links(self, related_list, request=None):
        return [self.generic_detail_link(related, request) for related in related_list]

    def generic_detail_link(self, related, request=None):
        view_name = related.__class__.__name__.lower() + '-detail'
        serializer = serializers.HyperlinkedIdentityField(view_name=view_name)
        return serializer.get_url(obj=related, view_name=view_name,
                                  request=self.context.get('request', request),
                                  format=None)


class EvidenceSerializerMixin(NgenModelSerializer):

    def update(self, instance, validated_data):
        files = self.context.get('request').FILES
        if files:
            validated_data['files'] = files.getlist('evidence')
        event = super().update(instance, validated_data)
        return event

    def create(self, validated_data):
        files = self.context.get('request').FILES
        if files:
            validated_data['files'] = files.getlist('evidence')
        event = super().create(validated_data)
        return event


class MergeSerializerMixin:
    def get_extra_kwargs(self):
        extra_kwargs = super().get_extra_kwargs()
        action = self.context['view'].action
        if action in ['update', 'partial_update', 'retrieve'] and self.instance and not self.instance.mergeable:
            if self.instance.blocked:
                allowed_fields = self.allowed_fields()
            elif self.instance.merged:
                allowed_fields = []
            for field in self.instance._meta.fields:
                if field.name not in allowed_fields:
                    kwargs = extra_kwargs.get(field.name, {})
                    kwargs['read_only'] = True
                    if field.is_relation:
                        kwargs['queryset'] = None
                    extra_kwargs[field.name] = kwargs

        return extra_kwargs

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if self.instance and self.instance.merged:
            raise ValidationError(
                gettext('Merged instances can\'t be modified'))
        if self.instance and self.instance.blocked:
            allowed_fields = self.allowed_fields()
            for attr in list(attrs):
                if attr not in allowed_fields:
                    if config.ALLOWED_FIELDS_EXCEPTION:
                        raise ValidationError(
                            {attr: gettext('%s of blocked instances can\'t be modified') % attr})
                    attrs.pop(attr)
        return attrs

    @staticmethod
    def allowed_fields():
        raise NotImplementedError


class SlugOrHyperlinkedRelatedField(serializers.HyperlinkedRelatedField):
    """
    A custom field to allow creation of related objects using either a slug or
    hyperlink.
    """

    def __init__(self, **kwargs):
        self.slug_field = kwargs.pop('slug_field', 'slug')
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        """
        Override the `to_internal_value` method to allow slugs.
        """
        try:
            # Try to get the related object using a hyperlink
            return super().to_internal_value(data)
        except serializers.ValidationError:
            # If that fails, try to get the related object using a slug
            slug = slugify(data).replace('-', '_')
            try:
                queryset = self.get_queryset()
                return queryset.get(**{self.slug_field: slug})
            except queryset.model.DoesNotExist:
                raise serializers.ValidationError(
                    f"{slug} is not a valid slug for {queryset.model.__name__}."
                )


class EvidenceSerializer(NgenModelSerializer):
    related = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Evidence
        exclude = ['content_type', 'object_id']

    def get_related(self, obj):
        return GenericRelationField(read_only=True).generic_detail_link(obj.content_object, self.context.get('request'))


class TaxonomySerializer(NgenModelSerializer):
    reports = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='report-detail'
    )
    playbooks = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='playbook-detail'
    )

    class Meta:
        model = models.Taxonomy
        fields = '__all__'
        read_only_fields = ['slug']


class ReportSerializer(NgenModelSerializer):
    problem = CharField(style={'base_template': 'textarea.html', 'rows': 10})
    derived_problem = CharField(
        style={'base_template': 'textarea.html', 'rows': 10}, allow_null=True)
    verification = CharField(
        style={'base_template': 'textarea.html', 'rows': 10}, allow_null=True)
    recommendations = CharField(
        style={'base_template': 'textarea.html', 'rows': 10}, allow_null=True)
    more_information = CharField(
        style={'base_template': 'textarea.html', 'rows': 10}, allow_null=True)

    class Meta:
        model = models.Report
        fields = '__all__'


class FeedSerializer(NgenModelSerializer):
    class Meta:
        model = models.Feed
        fields = '__all__'
        read_only_fields = ['slug']


class StateSerializer(NgenModelSerializer):
    class Meta:
        model = models.State
        fields = '__all__'
        read_only_fields = ['slug']


class EdgeSerializer(NgenModelSerializer):
    class Meta:
        model = models.Edge
        fields = '__all__'


class TlpSerializer(NgenModelSerializer):
    color = ColorField()

    class Meta:
        model = models.Tlp
        fields = '__all__'
        read_only_fields = ['slug']


class PrioritySerializer(NgenModelSerializer):
    color = ColorField()

    class Meta:
        model = models.Priority
        fields = '__all__'
        read_only_fields = ['slug']


class CaseTemplateSerializer(NgenModelSerializer):
    class Meta:
        model = models.CaseTemplate
        fields = '__all__'


class NetworkSerializer(NgenModelSerializer):
    children = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='network-detail'
    )
    parent = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='network-detail'
    )

    class Meta:
        model = models.Network
        fields = '__all__'


class NetworkEntitySerializer(NgenModelSerializer):
    networks = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='network-detail'
    )

    class Meta:
        model = models.NetworkEntity
        fields = '__all__'
        read_only_fields = ['slug']


class ContactSerializer(NgenModelSerializer):
    class Meta:
        model = models.Contact
        fields = '__all__'


class UserSerializer(NgenModelSerializer):
    user_permissions = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='permission-detail',
        read_only=True
    )

    class Meta:
        model = models.User
        fields = '__all__'

    def to_representation(self, obj):
        rep = super(UserSerializer, self).to_representation(obj)
        if 'password' in rep:
            if rep.get('password'):
                rep['password'] = '********'
            else:
                rep['password'] = None
        return rep

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance


class GroupSerializer(NgenModelSerializer):
    permissions = serializers.HyperlinkedRelatedField(
        queryset=Permission.objects.prefetch_related('content_type').all(),
        many=True,
        view_name='permission-detail'
    )

    class Meta:
        model = Group
        fields = '__all__'


class PermissionSerializer(NgenModelSerializer):
    content_type = serializers.HyperlinkedRelatedField(
        queryset=ContentType.objects.all().prefetch_related('permission_set'),
        view_name='contenttype-detail'
    )

    class Meta:
        model = Permission
        fields = '__all__'


class ContentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentType
        fields = '__all__'


class PlaybookSerializer(NgenModelSerializer):
    tasks = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='task-detail'
    )

    class Meta:
        model = models.Playbook
        fields = '__all__'


class TaskSerializer(NgenModelSerializer):
    class Meta:
        model = models.Task
        fields = '__all__'


class TodoTaskSerializer(NgenModelSerializer):
    class Meta:
        model = models.TodoTask
        fields = '__all__'
        read_only_fields = ['completed_date', 'task', 'event']


class ArtifactEnrichmentSerializer(NgenModelSerializer):
    class Meta:
        model = models.ArtifactEnrichment
        fields = '__all__'


class ArtifactSerializer(NgenModelSerializer):
    related = serializers.SerializerMethodField(read_only=True)
    enrichments = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='artifactenrichment-detail'
    )

    class Meta:
        model = models.Artifact
        fields = '__all__'

    def get_related(self, obj):
        return GenericRelationField(read_only=True).generic_detail_links(obj.related, self.context.get('request'))


class ArtifactRelationSerializer(NgenModelSerializer):
    related = serializers.SerializerMethodField(read_only=True)
    content_type = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.ArtifactRelation
        fields = '__all__'

    def get_related(self, obj):
        return GenericRelationField(read_only=True).generic_detail_link(obj.related, self.context.get('request'))

    def get_content_type(self, obj):
        return str(obj.content_type)


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        min_length=4, max_length=128, write_only=True)
    username = serializers.CharField(max_length=255, required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ["id", "username", "password", "email", "is_active"]

    def create(self, validated_data):

        try:
            User.objects.get(email=validated_data["email"])
        except ObjectDoesNotExist:
            return User.objects.create_user(**validated_data)

        raise ValidationError({"success": False, "msg": "Email already taken"})


def _generate_jwt_token(user):
    token = jwt.encode(
        {"id": user.pk, "exp": datetime.utcnow() + timedelta(days=7)},
        settings.SECRET_KEY,
    )

    return token


class AnnouncementSerializer(EvidenceSerializerMixin, NgenModelSerializer):
    body = CharField(style={'base_template': 'textarea.html', 'rows': 10})
    evidence = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='evidence-detail'
    )

    class Meta:
        model = models.Announcement
        fields = '__all__'


class CommentSerializer(NgenModelSerializer):
    class Meta:
        model = models.Comment
        exclude = ['content_type', 'object_id']


class EventSerializer(MergeSerializerMixin, EvidenceSerializerMixin, NgenModelSerializer):
    feed = SlugOrHyperlinkedRelatedField(
        slug_field='slug',
        queryset=models.Feed.objects.all(),
        view_name='feed-detail'
    )
    tlp = SlugOrHyperlinkedRelatedField(
        slug_field='slug',
        queryset=models.Tlp.objects.all(),
        view_name='tlp-detail'
    )
    priority = SlugOrHyperlinkedRelatedField(
        slug_field='slug',
        queryset=models.Priority.objects.all(),
        view_name='priority-detail'
    )
    taxonomy = SlugOrHyperlinkedRelatedField(
        slug_field='slug',
        queryset=models.Taxonomy.objects.all(),
        view_name='taxonomy-detail'
    )
    evidence = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='evidence-detail'
    )
    children = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='event-detail'
    )
    todos = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='todo-detail'
    )
    artifacts = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='artifact-detail'
    )
    reporter = serializers.HyperlinkedRelatedField(
        default=serializers.CreateOnlyDefault(
            serializers.CurrentUserDefault()),
        queryset=models.User.objects.all(),
        view_name='user-detail'
    )
    comments = serializers.SerializerMethodField()

    class Meta:
        model = models.Event
        fields = '__all__'

    def get_comments(self, obj):
        comments_qs = Comment.objects.filter_parents_by_object(obj)
        return GenericRelationField(read_only=True).generic_detail_links(comments_qs, self.context.get('request'))

    @staticmethod
    def allowed_fields():
        return config.ALLOWED_FIELDS_EVENT.split(',')

    @staticmethod
    def not_allowed_fields():
        return ['taxonomy', 'feed', 'network']

    def get_extra_kwargs(self):
        extra_kwargs = super().get_extra_kwargs()
        action = self.context['view'].action
        if action in ['update', 'partial_update', 'retrieve']:
            if self.instance and self.instance.is_parent():
                for field in self.instance._meta.fields:
                    if field.name in self.not_allowed_fields():
                        kwargs = extra_kwargs.get(field.name, {})
                        kwargs['read_only'] = True
                        extra_kwargs[field.name] = kwargs

        return extra_kwargs

    def validate(self, attrs):
        attrs = super().validate(attrs)

        if self.instance:
            if self.instance.merged or self.instance.is_parent():
                for attr in list(attrs):
                    if attr in self.not_allowed_fields():
                        if config.ALLOWED_FIELDS_EXCEPTION:
                            raise ValidationError(
                                {attr: gettext('%s of merged events can\'t be modified') % self.not_allowed_fields()})
                        attrs.pop(attr)
        return attrs


class CaseSerializer(MergeSerializerMixin, EvidenceSerializerMixin, NgenModelSerializer):
    events = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='event-detail'
    )
    children = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='case-detail'
    )
    evidence = serializers.SerializerMethodField(read_only=True)
    comments = serializers.SerializerMethodField()
    user_creator = serializers.HyperlinkedRelatedField(
        default=serializers.CreateOnlyDefault(
            serializers.CurrentUserDefault()),
        queryset=models.User.objects.all(),
        view_name='user-detail'
    )
    template_creator = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='casetemplate-detail'
    )

    class Meta:
        model = models.Case
        fields = '__all__'
        read_only_fields = ['attend_date', 'solve_date',
                            'report_message_id', 'raw', 'created_by', 'notification_count']

    def get_evidence(self, obj):
        return GenericRelationField(read_only=True).generic_detail_links(obj.evidence_all, self.context.get('request'))

    def validate_state(self, attrs):
        if self.instance is not None and self.instance.state != attrs and not self.instance.state.is_parent_of(attrs):
            raise ValidationError(
                {'state': gettext(
                    'It\'s not possible to change the state "%s" to "%s". The new possible states are %s') % (
                    self.instance.state, attrs, list(self.instance.state.children.all()))})
        return attrs

    def get_extra_kwargs(self):
        extra_kwargs = super().get_extra_kwargs()
        if self.instance:
            kwargs = extra_kwargs.get('state', {})
            action = self.context['view'].action
            if not kwargs.get('read_only', False):
                if action in ['update', 'partial_update']:
                    queryset = (self.instance.state.children.all() | models.State.objects.filter(
                        pk=self.instance.state.pk)).distinct()
                    kwargs['queryset'] = queryset
                else:
                    kwargs['queryset'] = models.State.get_initial().children.all()
                extra_kwargs['state'] = kwargs
        return extra_kwargs

    @staticmethod
    def allowed_fields():
        return config.ALLOWED_FIELDS_CASE.split(',')

    def get_comments(self, obj):
        comments_qs = Comment.objects.filter_parents_by_object(obj)
        return GenericRelationField(read_only=True).generic_detail_links(comments_qs, self.context.get('request'))


class AuditSerializer(NgenModelSerializer):
    related = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = LogEntry
        fields = '__all__'

    def get_related(self, obj):
        try:
            new_obj = obj.content_type.get_object_for_this_type(
                pk=obj.object_id)
            return GenericRelationField(read_only=True).generic_detail_link(new_obj, self.context.get('request'))
        except ObjectDoesNotExist:
            return None


class ConstanceValueField(serializers.Field):
    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        return data


class ConstanceSerializer(serializers.Serializer):
    key = serializers.CharField()
    default = serializers.SerializerMethodField()
    help_text = serializers.SerializerMethodField()
    value_type = serializers.SerializerMethodField()
    value = ConstanceValueField()
    settings = None

    def get_settings(self):
        if not self.settings:
            self.settings = get_settings()
        return self.settings

    def get_default(self, obj):
        value = next((item for item in self.get_settings()
                     if item["key"] == obj['key']), None)
        return value['default'] if value else None

    def get_help_text(self, obj):
        value = next((item for item in self.get_settings()
                     if item["key"] == obj['key']), None)
        return value['help_text'] if value else None

    def get_value_type(self, obj):
        value = next((item for item in self.get_settings()
                     if item["key"] == obj['key']), None)
        return value['value_type'] if value else None

    def is_valid(self, raise_exception=False):
        super().is_valid()
        if not 'value' in self.validated_data:
            raise ValidationError('No value provided')
        return True

    def create(self, validated_data):
        key = validated_data.get('key')
        value = validated_data.get('value')

        try:
            setattr(config, key, '' if value is None else value)
        except AttributeError:
            raise serializers.ValidationError('Invalid key')
        except ValidationError:
            raise serializers.ValidationError('Invalid value')
        return validated_data

    def update(self, instance, validated_data):
        return self.create(validated_data)


class StringIdentifierSerializer(serializers.Serializer):
    input_string = serializers.CharField(required=True)

    class Meta:
        model = models.StringIdentifier
        fields = '__all__'
        read_only_fields = ['input_type',
                            'address_string', 'address_type', 'all_types']

    def get_all_types(self, obj):
        return models.StringType._member_names_

    def create(self, validated_data):
        return models.StringIdentifier(**validated_data).__dict__

    def list(self):
        return {'all_types': models.StringType._member_names_,
                'all_network_types': models.StringIdentifier.all_network_types(),
                'all_artifact_types': models.StringIdentifier.all_artifact_types()}
