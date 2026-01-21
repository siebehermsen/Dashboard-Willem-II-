from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_remove_wellnessentry_rpe_alter_wellnessentry_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='popgesprek',
            name='datum',
            field=models.DateField(auto_now_add=True),
        ),
    ]
