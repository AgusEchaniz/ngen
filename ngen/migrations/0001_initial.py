# Generated by Django 3.2.5 on 2021-09-01 18:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ContactCase',
            fields=[
                ('slug', models.CharField(max_length=45, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=45, null=True)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('level', models.IntegerField()),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('deletedat', models.DateTimeField(blank=True, db_column='deletedAt', null=True)),
            ],
            options={
                'db_table': 'contact_case',
            },
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('ip', models.CharField(blank=True, max_length=39, null=True)),
                ('domain', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('slug', models.CharField(blank=True, max_length=100, null=True)),
                ('active', models.IntegerField()),
                ('deletedat', models.DateTimeField(blank=True, db_column='deletedAt', null=True)),
            ],
            options={
                'db_table': 'host',
            },
        ),
        migrations.CreateModel(
            name='Incident',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('date', models.DateTimeField()),
                ('renotification_date', models.DateTimeField(blank=True, null=True)),
                ('slug', models.CharField(blank=True, max_length=100, null=True)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('evidence_file_path', models.CharField(blank=True, max_length=255, null=True)),
                ('report_message_id', models.CharField(blank=True, max_length=255, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('ltd_count', models.IntegerField()),
                ('response_dead_line', models.DateTimeField(blank=True, null=True)),
                ('solve_dead_line', models.DateTimeField(blank=True, null=True)),
                ('active', models.IntegerField()),
                ('deletedat', models.DateTimeField(blank=True, db_column='deletedAt', null=True)),
                ('raw', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'incident',
            },
        ),
        migrations.CreateModel(
            name='IncidentCommentThread',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('incident_id', models.IntegerField(blank=True, null=True, unique=True)),
                ('permalink', models.CharField(max_length=255)),
                ('is_commentable', models.IntegerField()),
                ('num_comments', models.IntegerField()),
                ('last_comment_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'incident_comment_thread',
            },
        ),
        migrations.CreateModel(
            name='IncidentImpact',
            fields=[
                ('slug', models.CharField(max_length=45, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(blank=True, max_length=512, null=True)),
                ('active', models.IntegerField()),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('deletedat', models.DateTimeField(blank=True, db_column='deletedAt', null=True)),
            ],
            options={
                'db_table': 'incident_impact',
            },
        ),
        migrations.CreateModel(
            name='IncidentState',
            fields=[
                ('slug', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('active', models.IntegerField()),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('description', models.CharField(blank=True, max_length=250, null=True)),
                ('deletedat', models.DateTimeField(blank=True, db_column='deletedAt', null=True)),
            ],
            options={
                'db_table': 'incident_state',
            },
        ),
        migrations.CreateModel(
            name='TaxonomyPredicate',
            fields=[
                ('slug', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=1024)),
                ('expanded', models.CharField(max_length=255)),
                ('version', models.IntegerField()),
                ('value', models.CharField(max_length=255, unique=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('active', models.IntegerField()),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('deletedat', models.DateTimeField(blank=True, db_column='deletedAt', null=True)),
            ],
            options={
                'db_table': 'taxonomy_predicate',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('firstname', models.CharField(max_length=50)),
                ('lastname', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=180)),
                ('username', models.CharField(max_length=180)),
                ('password', models.CharField(max_length=255)),
                ('salt', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField()),
                ('api_key', models.CharField(blank=True, max_length=255, null=True)),
                ('slug', models.CharField(blank=True, max_length=100, null=True)),
                ('enabled', models.IntegerField()),
                ('username_canonical', models.CharField(max_length=180, unique=True)),
                ('email_canonical', models.CharField(max_length=180, unique=True)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('confirmation_token', models.CharField(blank=True, max_length=180, null=True, unique=True)),
                ('password_requested_at', models.DateTimeField(blank=True, null=True)),
                ('roles', models.TextField()),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ngen.user')),
            ],
            options={
                'db_table': 'user',
            },
        ),
        migrations.CreateModel(
            name='TaxonomyValue',
            fields=[
                ('slug', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=1024)),
                ('expanded', models.CharField(max_length=255)),
                ('value', models.CharField(max_length=255, unique=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('version', models.IntegerField()),
                ('active', models.IntegerField()),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('deletedat', models.DateTimeField(blank=True, db_column='deletedAt', null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ngen.user')),
                ('taxonomypredicate', models.ForeignKey(blank=True, db_column='taxonomyPredicate', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ngen.taxonomypredicate')),
            ],
            options={
                'db_table': 'taxonomy_value',
            },
        ),
        migrations.AddField(
            model_name='taxonomypredicate',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ngen.user'),
        ),
        migrations.CreateModel(
            name='StateEdge',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('discr', models.CharField(max_length=255)),
                ('deletedat', models.DateTimeField(blank=True, db_column='deletedAt', null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ngen.user')),
                ('mail_admin', models.ForeignKey(blank=True, db_column='mail_admin', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='ngen.contactcase')),
                ('mail_assigned', models.ForeignKey(blank=True, db_column='mail_assigned', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='ngen.contactcase')),
                ('mail_reporter', models.ForeignKey(blank=True, db_column='mail_reporter', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='ngen.contactcase')),
                ('mail_team', models.ForeignKey(blank=True, db_column='mail_team', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='ngen.contactcase')),
                ('newstate', models.ForeignKey(blank=True, db_column='newState', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='ngen.incidentstate')),
                ('oldstate', models.ForeignKey(blank=True, db_column='oldState', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='ngen.incidentstate')),
            ],
            options={
                'db_table': 'state_edge',
            },
        ),
        migrations.CreateModel(
            name='StateBehavior',
            fields=[
                ('slug', models.CharField(max_length=45, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=45, null=True)),
                ('description', models.CharField(blank=True, max_length=250, null=True)),
                ('can_edit_fundamentals', models.IntegerField()),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('can_edit', models.IntegerField()),
                ('can_enrich', models.IntegerField()),
                ('can_add_history', models.IntegerField()),
                ('can_comunicate', models.IntegerField()),
                ('discr', models.CharField(max_length=255)),
                ('deletedat', models.DateTimeField(blank=True, db_column='deletedAt', null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ngen.user')),
            ],
            options={
                'db_table': 'state_behavior',
            },
        ),
        migrations.CreateModel(
            name='NetworkEntity',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('slug', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('active', models.IntegerField()),
                ('deletedat', models.DateTimeField(blank=True, db_column='deletedAt', null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ngen.user')),
            ],
            options={
                'db_table': 'network_entity',
            },
        ),
        migrations.CreateModel(
            name='NetworkAdmin',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('slug', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('active', models.IntegerField()),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('deletedat', models.DateTimeField(blank=True, db_column='deletedAt', null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ngen.user')),
            ],
            options={
                'db_table': 'network_admin',
            },
        ),
        migrations.CreateModel(
            name='Network',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('ip_mask', models.IntegerField(blank=True, null=True)),
                ('ip', models.CharField(blank=True, max_length=39, null=True)),
                ('active', models.IntegerField()),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('domain', models.CharField(blank=True, max_length=255, null=True)),
                ('type', models.CharField(blank=True, max_length=8, null=True)),
                ('country_code', models.CharField(blank=True, max_length=2, null=True)),
                ('ip_start_address', models.CharField(blank=True, max_length=255, null=True)),
                ('ip_end_address', models.CharField(blank=True, max_length=255, null=True)),
                ('asn', models.CharField(blank=True, max_length=255, null=True)),
                ('deletedat', models.DateTimeField(blank=True, db_column='deletedAt', null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ngen.user')),
                ('network_admin', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ngen.networkadmin')),
                ('network_entity', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ngen.networkentity')),
            ],
            options={
                'db_table': 'network',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('data', models.JSONField()),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('response', models.JSONField(blank=True, null=True)),
                ('pending', models.IntegerField()),
                ('discr', models.CharField(max_length=255)),
                ('deletedat', models.DateTimeField(blank=True, db_column='deletedAt', null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ngen.user')),
                ('incident', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ngen.incident')),
            ],
            options={
                'db_table': 'message',
            },
        ),
        migrations.CreateModel(
            name='IncidentUrgency',
            fields=[
                ('slug', models.CharField(max_length=45, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=45, null=True)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('active', models.IntegerField()),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('deletedat', models.DateTimeField(blank=True, db_column='deletedAt', null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ngen.user')),
            ],
            options={
                'db_table': 'incident_urgency',
            },
        ),
        migrations.CreateModel(
            name='IncidentType',
            fields=[
                ('slug', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('active', models.IntegerField()),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('description', models.CharField(blank=True, max_length=250, null=True)),
                ('is_classification', models.IntegerField(db_column='is_Classification')),
                ('deletedat', models.DateTimeField(blank=True, db_column='deletedAt', null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ngen.user')),
                ('taxonomyvalue', models.ForeignKey(blank=True, db_column='taxonomyValue', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ngen.taxonomyvalue')),
            ],
            options={
                'db_table': 'incident_type',
            },
        ),
        migrations.CreateModel(
            name='IncidentTlp',
            fields=[
                ('slug', models.CharField(max_length=45, primary_key=True, serialize=False)),
                ('rgb', models.CharField(blank=True, max_length=45, null=True)),
                ('when', models.CharField(blank=True, max_length=500, null=True)),
                ('encrypt', models.IntegerField(blank=True, null=True)),
                ('why', models.CharField(blank=True, max_length=500, null=True)),
                ('information', models.CharField(blank=True, max_length=10, null=True)),
                ('description', models.CharField(blank=True, max_length=150, null=True)),
                ('name', models.CharField(blank=True, max_length=45, null=True)),
                ('code', models.IntegerField(blank=True, null=True)),
                ('active', models.IntegerField()),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('deletedat', models.DateTimeField(blank=True, db_column='deletedAt', null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ngen.user')),
            ],
            options={
                'db_table': 'incident_tlp',
            },
        ),
        migrations.CreateModel(
            name='IncidentStateChange',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('incident_id', models.IntegerField(blank=True, null=True)),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('method', models.CharField(max_length=25)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('deletedat', models.DateTimeField(blank=True, db_column='deletedAt', null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='ngen.user')),
                ('responsable', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='ngen.user')),
                ('state_edge', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ngen.stateedge')),
            ],
            options={
                'db_table': 'incident_state_change',
            },
        ),
        migrations.AddField(
            model_name='incidentstate',
            name='behavior',
            field=models.ForeignKey(blank=True, db_column='behavior', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ngen.statebehavior'),
        ),
        migrations.AddField(
            model_name='incidentstate',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ngen.user'),
        ),
        migrations.CreateModel(
            name='IncidentReport',
            fields=[
                ('slug', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('lang', models.CharField(max_length=2)),
                ('problem', models.TextField()),
                ('derivated_problem', models.TextField(blank=True, null=True)),
                ('verification', models.TextField(blank=True, null=True)),
                ('recomendations', models.TextField(blank=True, null=True)),
                ('more_information', models.TextField(blank=True, null=True)),
                ('active', models.IntegerField()),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('deletedat', models.DateTimeField(blank=True, db_column='deletedAt', null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ngen.user')),
                ('type', models.ForeignKey(blank=True, db_column='type', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ngen.incidenttype')),
            ],
            options={
                'db_table': 'incident_report',
            },
        ),
        migrations.CreateModel(
            name='IncidentPriority',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.CharField(max_length=255, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('response_time', models.IntegerField()),
                ('solve_time', models.IntegerField()),
                ('code', models.IntegerField()),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('unresponse_time', models.IntegerField()),
                ('unsolve_time', models.IntegerField()),
                ('active', models.IntegerField()),
                ('deletedat', models.DateTimeField(blank=True, db_column='deletedAt', null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ngen.user')),
                ('impact', models.ForeignKey(blank=True, db_column='impact', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ngen.incidentimpact')),
                ('urgency', models.ForeignKey(blank=True, db_column='urgency', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ngen.incidenturgency')),
            ],
            options={
                'db_table': 'incident_priority',
            },
        ),
        migrations.AddField(
            model_name='incidentimpact',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ngen.user'),
        ),
        migrations.CreateModel(
            name='IncidentFeed',
            fields=[
                ('slug', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('active', models.IntegerField()),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('description', models.CharField(blank=True, max_length=250, null=True)),
                ('deletedat', models.DateTimeField(blank=True, db_column='deletedAt', null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ngen.user')),
            ],
            options={
                'db_table': 'incident_feed',
            },
        ),
        migrations.CreateModel(
            name='IncidentDetected',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('incident_id', models.IntegerField(blank=True, null=True)),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('evidence_file_path', models.CharField(blank=True, max_length=255, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('active', models.IntegerField()),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('deletedat', models.DateTimeField(blank=True, db_column='deletedAt', null=True)),
                ('assigned', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='ngen.user')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='ngen.user')),
                ('feed', models.ForeignKey(blank=True, db_column='feed', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ngen.incidentfeed')),
                ('priority', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ngen.incidentpriority')),
                ('reporter', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='ngen.user')),
                ('state', models.ForeignKey(blank=True, db_column='state', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ngen.incidentstate')),
                ('tlp_state', models.ForeignKey(blank=True, db_column='tlp_state', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ngen.incidenttlp')),
                ('type', models.ForeignKey(blank=True, db_column='type', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ngen.incidenttype')),
            ],
            options={
                'db_table': 'incident_detected',
            },
        ),
        migrations.CreateModel(
            name='IncidentDecision',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('auto_saved', models.IntegerField()),
                ('active', models.IntegerField()),
                ('deletedat', models.DateTimeField(blank=True, db_column='deletedAt', null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ngen.user')),
                ('feed', models.ForeignKey(blank=True, db_column='feed', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ngen.incidentfeed')),
                ('network', models.ForeignKey(blank=True, db_column='network', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ngen.network')),
                ('priority', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ngen.incidentpriority')),
                ('state', models.ForeignKey(blank=True, db_column='state', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='ngen.incidentstate')),
                ('tlp', models.ForeignKey(blank=True, db_column='tlp', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ngen.incidenttlp')),
                ('type', models.ForeignKey(blank=True, db_column='type', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ngen.incidenttype')),
                ('unresponded_state', models.ForeignKey(blank=True, db_column='unresponded_state', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='ngen.incidentstate')),
                ('unsolved_state', models.ForeignKey(blank=True, db_column='unsolved_state', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='ngen.incidentstate')),
            ],
            options={
                'db_table': 'incident_decision',
            },
        ),
        migrations.CreateModel(
            name='IncidentComment',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('body', models.TextField()),
                ('ancestors', models.CharField(max_length=1024)),
                ('depth', models.IntegerField()),
                ('created_at', models.DateTimeField()),
                ('state', models.IntegerField()),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ngen.user')),
                ('thread', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ngen.incidentcommentthread')),
            ],
            options={
                'db_table': 'incident_comment',
            },
        ),
        migrations.AddField(
            model_name='incident',
            name='assigned',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='ngen.user'),
        ),
        migrations.AddField(
            model_name='incident',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ngen.user'),
        ),
        migrations.AddField(
            model_name='incident',
            name='feed',
            field=models.ForeignKey(blank=True, db_column='feed', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ngen.incidentfeed'),
        ),
        migrations.AddField(
            model_name='incident',
            name='network',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ngen.network'),
        ),
        migrations.AddField(
            model_name='incident',
            name='origin',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ngen.host'),
        ),
        migrations.AddField(
            model_name='incident',
            name='priority',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ngen.incidentpriority'),
        ),
        migrations.AddField(
            model_name='incident',
            name='reporter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='ngen.user'),
        ),
        migrations.AddField(
            model_name='incident',
            name='state',
            field=models.ForeignKey(blank=True, db_column='state', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='ngen.incidentstate'),
        ),
        migrations.AddField(
            model_name='incident',
            name='tlp_state',
            field=models.ForeignKey(blank=True, db_column='tlp_state', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ngen.incidenttlp'),
        ),
        migrations.AddField(
            model_name='incident',
            name='type',
            field=models.ForeignKey(blank=True, db_column='type', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ngen.incidenttype'),
        ),
        migrations.AddField(
            model_name='incident',
            name='unresponded_state',
            field=models.ForeignKey(blank=True, db_column='unresponded_state', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='ngen.incidentstate'),
        ),
        migrations.AddField(
            model_name='incident',
            name='unsolved_state',
            field=models.ForeignKey(blank=True, db_column='unsolved_state', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='ngen.incidentstate'),
        ),
        migrations.AddField(
            model_name='host',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ngen.user'),
        ),
        migrations.AddField(
            model_name='host',
            name='network',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ngen.network'),
        ),
        migrations.CreateModel(
            name='ExtTranslations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('locale', models.CharField(max_length=8)),
                ('object_class', models.CharField(max_length=255)),
                ('field', models.CharField(max_length=32)),
                ('foreign_key', models.CharField(max_length=64)),
                ('content', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'ext_translations',
                'unique_together': {('locale', 'object_class', 'field', 'foreign_key')},
            },
        ),
        migrations.AddField(
            model_name='contactcase',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ngen.user'),
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('username', models.CharField(max_length=255)),
                ('encryption_key', models.CharField(blank=True, max_length=4000, null=True)),
                ('contact_type', models.CharField(max_length=255)),
                ('discr', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('deletedat', models.DateTimeField(blank=True, db_column='deletedAt', null=True)),
                ('contact_case', models.ForeignKey(blank=True, db_column='contact_case', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ngen.contactcase')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='ngen.user')),
                ('network_admin', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ngen.networkadmin')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='ngen.user')),
            ],
            options={
                'db_table': 'contact',
            },
        ),
    ]
