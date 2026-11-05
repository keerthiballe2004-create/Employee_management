import django.db.models.deletion
from django.db import migrations, models


def update_status_values(apps, schema_editor):
    OffboardingCase = apps.get_model('offboarding', 'OffboardingCase')

    status_mapping = {
        'NOT_STARTED': 'REQUESTED',
        'IN_PROGRESS': 'IN_PROGRESS',
        'COMPLETED': 'COMPLETED',
        'ON_HOLD': 'ON_HOLD',
    }

    for old_status, new_status in status_mapping.items():
        OffboardingCase.objects.filter(
            status=old_status
        ).update(status=new_status)


def reverse_status_values(apps, schema_editor):
    OffboardingCase = apps.get_model('offboarding', 'OffboardingCase')

    status_mapping = {
        'REQUESTED': 'NOT_STARTED',
        'IN_PROGRESS': 'IN_PROGRESS',
        'COMPLETED': 'COMPLETED',
        'ON_HOLD': 'ON_HOLD',
    }

    for old_status, new_status in status_mapping.items():
        OffboardingCase.objects.filter(
            status=old_status
        ).update(status=new_status)


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0001_initial'),
        ('offboarding', '0001_initial'),
    ]

    operations = [

        migrations.RenameModel(
            old_name='OnboardingCase',
            new_name='OffboardingCase',
        ),

        migrations.RenameField(
            model_name='offboardingcase',
            old_name='onboarding_id',
            new_name='offboarding_id',
        ),

        migrations.RenameField(
            model_name='offboardingcase',
            old_name='start_date',
            new_name='exit_date',
        ),

        migrations.AddField(
            model_name='offboardingcase',
            name='reason',
            field=models.TextField(default=''),
            preserve_default=False,
        ),

        migrations.RunPython(
            update_status_values,
            reverse_status_values,
        ),

        migrations.AlterField(
            model_name='offboardingcase',
            name='status',
            field=models.CharField(
                max_length=20,
                choices=[
                    ('REQUESTED', 'Requested'),
                    ('APPROVAL_PENDING', 'Approval Pending'),
                    ('IN_PROGRESS', 'In Progress'),
                    ('COMPLETED', 'Completed'),
                    ('ON_HOLD', 'On Hold'),
                ],
                default='REQUESTED',
            ),
        ),

        migrations.AlterField(
            model_name='offboardingcase',
            name='employee',
            field=models.ForeignKey(
                to='employees.employee',
                on_delete=django.db.models.deletion.PROTECT,
                related_name='offboarding_cases',
            ),
        ),
    ]