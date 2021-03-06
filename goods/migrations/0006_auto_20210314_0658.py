# Generated by Django 3.1.6 on 2021-03-14 01:28

from django.db import migrations, models
import goods.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_auto_20210313_0814'),
        ('goods', '0005_auto_20210313_2054'),
    ]

    operations = [
        migrations.RenameField(
            model_name='amount',
            old_name='raw_material',
            new_name='raw_mate',
        ),
        migrations.AlterField(
            model_name='amount',
            name='required_amount',
            field=models.FloatField(default=1, validators=[goods.models.validate_positive]),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='amount',
            unique_together={('goods', 'raw_mate')},
        ),
    ]
