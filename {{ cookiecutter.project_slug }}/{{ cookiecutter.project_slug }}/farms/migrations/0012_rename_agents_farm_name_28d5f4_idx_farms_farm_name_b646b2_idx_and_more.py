# Generated by Django 4.1.2 on 2023-01-31 20:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("farms", "0011_rename_agent_farm_and_more"),
    ]

    operations = [
        migrations.RenameIndex(
            model_name="farm",
            new_name="farms_farm_name_b646b2_idx",
            old_name="agents_farm_name_28d5f4_idx",
        ),
        migrations.RenameIndex(
            model_name="farm",
            new_name="farms_farm_email_46efd1_idx",
            old_name="agents_farm_email_4f6512_idx",
        ),
        migrations.RenameIndex(
            model_name="farm",
            new_name="farms_farm_phone_n_402305_idx",
            old_name="agents_farm_phone_n_bae812_idx",
        ),
    ]