# Generated by Django 5.1.3 on 2025-02-08 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='organisationmember',
            name='is_organisation_admin',
            field=models.BooleanField(default=False, verbose_name='organisation admin?'),
        ),
        migrations.AddField(
            model_name='organisationmember',
            name='is_organisation_superadmin',
            field=models.BooleanField(default=False, verbose_name='organisation superadmin?'),
        ),
        migrations.AddField(
            model_name='teammember',
            name='is_team_admin',
            field=models.BooleanField(default=False, verbose_name='team admin?'),
        ),
        migrations.AddField(
            model_name='teammember',
            name='is_team_superadmin',
            field=models.BooleanField(default=False, verbose_name='team superadmin?'),
        ),
        migrations.AddField(
            model_name='workspacemember',
            name='is_workspace_admin',
            field=models.BooleanField(default=False, verbose_name='workspace admin?'),
        ),
        migrations.AddField(
            model_name='workspacemember',
            name='is_workspace_superadmin',
            field=models.BooleanField(default=False, verbose_name='workspace superadmin?'),
        ),
    ]
