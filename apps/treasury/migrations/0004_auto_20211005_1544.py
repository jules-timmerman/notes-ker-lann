# Generated by Django 2.2.24 on 2021-10-05 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('treasury', '0003_auto_20210321_1034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sogecredit',
            name='transactions',
            field=models.ManyToManyField(blank=True, related_name='_sogecredit_transactions_+', to='note.MembershipTransaction', verbose_name='membership transactions'),
        ),
    ]
