# Generated by Django 4.2.1 on 2023-06-18 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0004_alter_bilan_actif_immobilisé_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='actif',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AddField(
            model_name='bilan',
            name='actif',
            field=models.FloatField(default=0),
        ),
    ]
