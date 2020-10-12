# Generated by Django 3.1 on 2020-10-09 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Men',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('price', models.FloatField(default=0)),
                ('category', models.CharField(choices=[('C', 'coat'), ('S', 'shoes'), ('T', 'tower'), ('O', 'orange')], max_length=1)),
                ('img', models.ImageField(upload_to='images')),
                ('quantity', models.IntegerField(default=1)),
            ],
        ),
    ]
