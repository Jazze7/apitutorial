# Generated by Django 4.1.3 on 2022-11-30 04:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0006_place_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='main_comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='parent_comment', to='places.comment'),
        ),
    ]