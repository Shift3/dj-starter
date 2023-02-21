# Generated by Django 4.0.3 on 2022-03-18 21:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
        ("farms", "0002_alter_agent_options_agent_created_agent_modified_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="agent",
            options={},
        ),
        migrations.AddField(
            model_name="agent",
            name="address",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="core.address",
            ),
        ),
        migrations.AddField(
            model_name="historicalagent",
            name="address",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="core.address",
            ),
        ),
        migrations.AddIndex(
            model_name="agent",
            index=models.Index(fields=["name"], name="agents_agen_name_26b7c8_idx"),
        ),
        migrations.AddIndex(
            model_name="agent",
            index=models.Index(fields=["email"], name="agents_agen_email_c3a8fb_idx"),
        ),
    ]
