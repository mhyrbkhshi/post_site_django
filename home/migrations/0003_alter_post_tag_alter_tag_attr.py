# Generated by Django 4.1.4 on 2022-12-26 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='tag',
            field=models.ManyToManyField(blank=True, null=True, to='home.tag'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='attr',
            field=models.CharField(default='bi-tag', help_text='Bootstrap icon class for example(bi-person)', max_length=30, verbose_name='Icon class name'),
        ),
    ]
