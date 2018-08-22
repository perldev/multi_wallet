# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Accounts',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('balance', models.DecimalField(default=0, verbose_name='\u0411\u0430\u043b\u0430\u043d\u0441', max_digits=20, decimal_places=10)),
                ('pub_date', models.DateTimeField(default=datetime.datetime.now, verbose_name='\u0414\u0430\u0442\u0430 \u043f\u0443\u0431\u043b\u0438\u043a\u0430\u0446\u0438\u0438')),
                ('reference', models.CharField(max_length=255, unique=True, null=True, verbose_name=' \u0412\u043d\u0435\u0448\u043d\u0438\u0439 \u043a\u043b\u044e\u0447 \u0438\u0434\u0435\u043d\u0442\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u0438 \u0438\u043b\u0438 \u043a\u043e\u0448\u0435\u043b\u0435\u043a \u043a\u0440\u0438\u043f\u0442\u043e\u0432\u0430\u043b\u044e\u0442\u044b ', blank=True)),
                ('last_trans_id', models.IntegerField(null=True, verbose_name=b'last_trans')),
            ],
            options={
                'ordering': ('id',),
                'verbose_name': '\u0421\u0447\u0435\u0442',
                'verbose_name_plural': '\u0421\u0447\u0435\u0442\u0430',
            },
        ),
        migrations.CreateModel(
            name='CommandsLogs',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='\u043d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u043f\u0435\u0440\u0435\u043c\u0435\u043d\u043d\u043e\u0439')),
                ('name2', models.CharField(max_length=255, verbose_name='\u043d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u043f\u0435\u0440\u0435\u043c\u0435\u043d\u043d\u043e\u0439')),
                ('start_date', models.DateTimeField(default=datetime.datetime.now, verbose_name='\u0414\u0430\u0442\u0430 \u043f\u0443\u0431\u043b\u0438\u043a\u0430\u0446\u0438\u0438')),
                ('end_start_date', models.DateTimeField(verbose_name='\u0414\u0430\u0442\u0430 \u043e\u043a\u043e\u043d\u0447\u0430\u043d\u0438\u044f', blank=True)),
                ('log', models.CharField(max_length=255, verbose_name='\u0417\u043d\u0430\u0447\u0435\u043d\u0438\u0435')),
            ],
            options={
                'verbose_name': '\u043b\u043e\u0433\u0438 \u043a\u043e\u043c\u043c\u0430\u043d\u0434',
                'verbose_name_plural': '\u043b\u043e\u0433\u0438 \u043a\u043e\u043c\u043c\u0430\u043d\u0434',
            },
        ),
        migrations.CreateModel(
            name='CryptoRawTrans',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('crypto_txid', models.CharField(max_length=255, null=True, blank=True)),
                ('tx_archive', models.TextField(null=True, blank=True)),
                ('block_height', models.IntegerField(default=0)),
                ('pub_date', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
        migrations.CreateModel(
            name='CryptoTransfers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('account', models.CharField(max_length=255, verbose_name='\u0421\u0447\u0435\u0442')),
                ('description', models.CharField(max_length=255, verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435', blank=True)),
                ('payment_id', models.CharField(max_length=255, verbose_name='Payment Id', blank=True)),
                ('amnt', models.DecimalField(verbose_name='\u0421\u0443\u043c\u043c\u0430', max_digits=18, decimal_places=10)),
                ('confirms', models.IntegerField(default=0, verbose_name=' \u041f\u043e\u0434\u0442\u0432\u0435\u0440\u0436\u0434\u0435\u043d\u0438\u044f')),
                ('pub_date', models.DateTimeField(default=datetime.datetime.now, verbose_name='\u0414\u0430\u0442\u0430')),
                ('status', models.CharField(default=b'created', max_length=40, choices=[(b'manually', '\u0440\u0443\u0447\u043d\u0430\u044f'), (b'deposit', '\u0434\u0435\u043f\u043e\u0437\u0438\u0442'), (b'withdraw', '\u0432\u044b\u0432\u043e\u0434'), (b'bonus', '\u043f\u0430\u0440\u0442\u043d\u0435\u0440\u0441\u043a\u043e\u0435 \u0432\u043e\u0437\u043d\u0430\u0433\u0440\u0430\u0436\u0434\u0435\u043d\u0438\u0435'), (b'payin', '\u043f\u043e\u043f\u043e\u043b\u043d\u0435\u043d\u0438\u0435'), (b'comission', '\u043a\u043e\u043c\u043c\u0438\u0441\u0441\u0438\u043e\u043d\u043d\u044b\u0435'), (b'created', '\u0441\u043e\u0437\u0434\u0430\u043d'), (b'incifition_funds', '\u043d\u0435\u0434\u043e\u0441\u0442\u0430\u0442\u043e\u0447\u043d\u043e \u0441\u0440\u0435\u0434\u0441\u0442\u0432'), (b'currency_core', '\u0432\u0430\u043b\u044e\u0442\u044b \u0441\u0447\u0435\u0442\u043e\u0432 \u043d\u0435 \u0441\u043e\u0432\u043f\u0430\u0434\u0430\u044e\u0442'), (b'processing', '\u0432 \u0440\u0430\u0431\u043e\u0442\u0435'), (b'processing2', '\u0432 \u0440\u0430\u0431\u043e\u0442\u0435 2'), (b'canceled', '\u043e\u0442\u043c\u0435\u043d\u0435\u043d'), (b'wait_secure', '\u0440\u0443\u0447\u043d\u0430\u044f \u043e\u0431\u0440\u0430\u0431\u043e\u0442\u043a\u0430'), (b'order_cancel', '\u043e\u0442\u043c\u0435\u043d\u0430 \u0437\u0430\u044f\u0432\u043a\u0438'), (b'deal', '\u0441\u0434\u0435\u043b\u043a\u0430'), (b'auto', '\u0430\u0432\u0442\u043e\u043c\u0430\u0442'), (b'automanually', '\u043c\u0430\u043d\u0443\u0430\u043b\u044c\u043d\u044b\u0439 \u0430\u0432\u0442\u043e\u043c\u0430\u0442'), (b'deal_return', '\u0432\u043e\u0437\u0432\u0440\u0430\u0442 \u043c\u0430\u043b\u0435\u043d\u044c\u043a\u043e\u0433\u043e \u043e\u0441\u0442\u0430\u0442\u043a\u0430'), (b'processed', '\u0438\u0441\u043f\u043e\u043b\u043d\u0435\u043d'), (b'core_error', '\u043e\u0448\u0438\u0431\u043a\u0430 \u044f\u0434\u0440\u0430')])),
                ('comission', models.DecimalField(verbose_name='\u043a\u043e\u043c\u0438\u0441\u0441\u0438\u044f', editable=False, max_digits=18, decimal_places=10)),
                ('confirm_key', models.CharField(max_length=255, null=True, editable=False, blank=True)),
                ('crypto_txid', models.CharField(max_length=255, null=True, blank=True)),
                ('tx_archive', models.TextField(null=True, blank=True)),
                ('sign', models.CharField(max_length=255, verbose_name='\u043f\u043e\u0434\u043f\u0438\u0441\u044c \u043a\u043b\u0438\u0435\u043d\u0442\u0430')),
                ('debit_credit', models.CharField(default=b'in', max_length=40, choices=[(b'in', 'debit'), (b'out', 'credit')])),
            ],
            options={
                'verbose_name': '\u041f\u0435\u0440\u0435\u0432\u043e\u0434 \u043a\u0440\u0438\u043f\u0442\u043e\u0432\u0430\u043b\u044e\u0442\u044b',
                'verbose_name_plural': '\u041f\u0435\u0440\u0435\u0432\u043e\u0434\u044b \u043a\u0440\u0438\u043f\u0442\u043e\u0432\u0430\u043b\u044e\u0442\u044b',
            },
        ),
        migrations.CreateModel(
            name='CryptoTransfers2',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('account', models.CharField(max_length=255, verbose_name='\u0421\u0447\u0435\u0442')),
                ('description', models.CharField(max_length=255, verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435', blank=True)),
                ('payment_id', models.CharField(max_length=255, verbose_name='Payment Id', blank=True)),
                ('amnt', models.DecimalField(verbose_name='\u0421\u0443\u043c\u043c\u0430', max_digits=18, decimal_places=10)),
                ('confirms', models.IntegerField(default=0, verbose_name=' \u041f\u043e\u0434\u0442\u0432\u0435\u0440\u0436\u0434\u0435\u043d\u0438\u044f')),
                ('pub_date', models.DateTimeField(default=datetime.datetime.now, verbose_name='\u0414\u0430\u0442\u0430')),
                ('status', models.CharField(default=b'created', max_length=40, choices=[(b'manually', '\u0440\u0443\u0447\u043d\u0430\u044f'), (b'deposit', '\u0434\u0435\u043f\u043e\u0437\u0438\u0442'), (b'withdraw', '\u0432\u044b\u0432\u043e\u0434'), (b'bonus', '\u043f\u0430\u0440\u0442\u043d\u0435\u0440\u0441\u043a\u043e\u0435 \u0432\u043e\u0437\u043d\u0430\u0433\u0440\u0430\u0436\u0434\u0435\u043d\u0438\u0435'), (b'payin', '\u043f\u043e\u043f\u043e\u043b\u043d\u0435\u043d\u0438\u0435'), (b'comission', '\u043a\u043e\u043c\u043c\u0438\u0441\u0441\u0438\u043e\u043d\u043d\u044b\u0435'), (b'created', '\u0441\u043e\u0437\u0434\u0430\u043d'), (b'incifition_funds', '\u043d\u0435\u0434\u043e\u0441\u0442\u0430\u0442\u043e\u0447\u043d\u043e \u0441\u0440\u0435\u0434\u0441\u0442\u0432'), (b'currency_core', '\u0432\u0430\u043b\u044e\u0442\u044b \u0441\u0447\u0435\u0442\u043e\u0432 \u043d\u0435 \u0441\u043e\u0432\u043f\u0430\u0434\u0430\u044e\u0442'), (b'processing', '\u0432 \u0440\u0430\u0431\u043e\u0442\u0435'), (b'processing2', '\u0432 \u0440\u0430\u0431\u043e\u0442\u0435 2'), (b'canceled', '\u043e\u0442\u043c\u0435\u043d\u0435\u043d'), (b'wait_secure', '\u0440\u0443\u0447\u043d\u0430\u044f \u043e\u0431\u0440\u0430\u0431\u043e\u0442\u043a\u0430'), (b'order_cancel', '\u043e\u0442\u043c\u0435\u043d\u0430 \u0437\u0430\u044f\u0432\u043a\u0438'), (b'deal', '\u0441\u0434\u0435\u043b\u043a\u0430'), (b'auto', '\u0430\u0432\u0442\u043e\u043c\u0430\u0442'), (b'automanually', '\u043c\u0430\u043d\u0443\u0430\u043b\u044c\u043d\u044b\u0439 \u0430\u0432\u0442\u043e\u043c\u0430\u0442'), (b'deal_return', '\u0432\u043e\u0437\u0432\u0440\u0430\u0442 \u043c\u0430\u043b\u0435\u043d\u044c\u043a\u043e\u0433\u043e \u043e\u0441\u0442\u0430\u0442\u043a\u0430'), (b'processed', '\u0438\u0441\u043f\u043e\u043b\u043d\u0435\u043d'), (b'core_error', '\u043e\u0448\u0438\u0431\u043a\u0430 \u044f\u0434\u0440\u0430')])),
                ('comission', models.DecimalField(verbose_name='\u043a\u043e\u043c\u0438\u0441\u0441\u0438\u044f', editable=False, max_digits=18, decimal_places=10)),
                ('confirm_key', models.CharField(max_length=255, null=True, editable=False, blank=True)),
                ('crypto_txid', models.CharField(max_length=255, null=True, blank=True)),
                ('debit_credit', models.CharField(default=b'in', max_length=40, choices=[(b'in', 'debit'), (b'out', 'credit')])),
                ('tx_archive', models.TextField(null=True, blank=True)),
                ('tx_checking', models.CharField(default=b'', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('long_title', models.CharField(max_length=255, verbose_name='\u0414\u043b\u0438\u043d\u043e\u0435 \u043d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('text', models.TextField(verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435')),
                ('img', models.ImageField(upload_to=b'clogo', verbose_name='\u041b\u043e\u0433\u043e\u0442\u0438\u043f')),
                ('ordering', models.IntegerField(default=1, verbose_name='\u0421\u043e\u0440\u0442\u0438\u0440\u043e\u0432\u043a\u0430')),
                ('pub_date', models.DateTimeField(default=datetime.datetime.now, verbose_name='\u0414\u0430\u0442\u0430 \u043f\u0443\u0431\u043b\u0438\u043a\u0430\u0446\u0438\u0438')),
            ],
            options={
                'ordering': ('id',),
                'verbose_name': '\u0412\u0430\u043b\u044e\u0442\u0430',
                'verbose_name_plural': '\u0412\u0430\u043b\u044e\u0442\u044b',
            },
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sum1_history', models.DecimalField(verbose_name='\u0418\u0437\u043d\u0430\u0447\u0430\u043b\u044c\u043d\u0430\u044f \u0441\u0443\u043c\u043c\u0430 \u043f\u0440\u043e\u0434\u0430\u0436\u0438', max_digits=20, decimal_places=10)),
                ('price', models.DecimalField(verbose_name='\u0426\u0435\u043d\u0430', max_digits=24, decimal_places=16, blank=True)),
                ('sum1', models.DecimalField(verbose_name='\u0441\u0443\u043c\u043c\u0430 \u043f\u0440\u043e\u0434\u0430\u0436\u0438', max_digits=20, decimal_places=10)),
                ('sum2_history', models.DecimalField(verbose_name='\u0418\u0437\u043d\u0430\u0447\u0430\u043b\u044c\u043d\u0430\u044f \u0441\u0443\u043c\u043c\u0430 \u043f\u043e\u043a\u0443\u043f\u043a\u0438', max_digits=20, decimal_places=10)),
                ('sum2', models.DecimalField(verbose_name='\u0441\u0443\u043c\u043c\u0430 \u043f\u043e\u043a\u0443\u043f\u043a\u0438', max_digits=20, decimal_places=10)),
                ('status', models.CharField(default=b'created', max_length=40, verbose_name='\u0421\u0442\u0430\u0442\u0443\u0441', choices=[(b'manually', '\u0440\u0443\u0447\u043d\u0430\u044f'), (b'deposit', '\u0434\u0435\u043f\u043e\u0437\u0438\u0442'), (b'withdraw', '\u0432\u044b\u0432\u043e\u0434'), (b'bonus', '\u043f\u0430\u0440\u0442\u043d\u0435\u0440\u0441\u043a\u043e\u0435 \u0432\u043e\u0437\u043d\u0430\u0433\u0440\u0430\u0436\u0434\u0435\u043d\u0438\u0435'), (b'payin', '\u043f\u043e\u043f\u043e\u043b\u043d\u0435\u043d\u0438\u0435'), (b'comission', '\u043a\u043e\u043c\u043c\u0438\u0441\u0441\u0438\u043e\u043d\u043d\u044b\u0435'), (b'created', '\u0441\u043e\u0437\u0434\u0430\u043d'), (b'incifition_funds', '\u043d\u0435\u0434\u043e\u0441\u0442\u0430\u0442\u043e\u0447\u043d\u043e \u0441\u0440\u0435\u0434\u0441\u0442\u0432'), (b'currency_core', '\u0432\u0430\u043b\u044e\u0442\u044b \u0441\u0447\u0435\u0442\u043e\u0432 \u043d\u0435 \u0441\u043e\u0432\u043f\u0430\u0434\u0430\u044e\u0442'), (b'processing', '\u0432 \u0440\u0430\u0431\u043e\u0442\u0435'), (b'processing2', '\u0432 \u0440\u0430\u0431\u043e\u0442\u0435 2'), (b'canceled', '\u043e\u0442\u043c\u0435\u043d\u0435\u043d'), (b'wait_secure', '\u0440\u0443\u0447\u043d\u0430\u044f \u043e\u0431\u0440\u0430\u0431\u043e\u0442\u043a\u0430'), (b'order_cancel', '\u043e\u0442\u043c\u0435\u043d\u0430 \u0437\u0430\u044f\u0432\u043a\u0438'), (b'deal', '\u0441\u0434\u0435\u043b\u043a\u0430'), (b'auto', '\u0430\u0432\u0442\u043e\u043c\u0430\u0442'), (b'automanually', '\u043c\u0430\u043d\u0443\u0430\u043b\u044c\u043d\u044b\u0439 \u0430\u0432\u0442\u043e\u043c\u0430\u0442'), (b'deal_return', '\u0432\u043e\u0437\u0432\u0440\u0430\u0442 \u043c\u0430\u043b\u0435\u043d\u044c\u043a\u043e\u0433\u043e \u043e\u0441\u0442\u0430\u0442\u043a\u0430'), (b'processed', '\u0438\u0441\u043f\u043e\u043b\u043d\u0435\u043d'), (b'core_error', '\u043e\u0448\u0438\u0431\u043a\u0430 \u044f\u0434\u0440\u0430')])),
                ('pub_date', models.DateTimeField(default=datetime.datetime.now, verbose_name='\u0414\u0430\u0442\u0430 \u043f\u0443\u0431\u043b\u0438\u043a\u0430\u0446\u0438\u0438')),
                ('comission', models.DecimalField(default=b'0.0005', verbose_name='\u041a\u043e\u043c\u0438\u0441\u0441\u0438\u044f', max_digits=20, decimal_places=10, blank=True)),
                ('sign', models.CharField(default=b'0.0005', max_length=255, verbose_name='Custom sign')),
                ('public_key', models.CharField(default=b'0.0005', max_length=255, verbose_name='public key')),
                ('currency1', models.ForeignKey(related_name='from_currency', verbose_name='\u0412\u0430\u043b\u044e\u0442\u0430 A', to='main.Currency')),
                ('currency2', models.ForeignKey(related_name='to_currency', verbose_name='\u0412\u0430\u043b\u044e\u0442\u0430 \u0411', to='main.Currency')),
            ],
            options={
                'ordering': ('-id',),
                'verbose_name': '\u0421\u0434\u0435\u043b\u043a\u0430',
                'verbose_name_plural': '\u0421\u0434\u0435\u043b\u043a\u0438',
            },
        ),
        migrations.CreateModel(
            name='OrdersMem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.IntegerField()),
                ('trade_pair', models.IntegerField(verbose_name='\u0412\u0430\u043b\u044e\u0442\u043d\u0430\u044f \u043f\u0430\u0440\u0430')),
                ('currency1', models.IntegerField(verbose_name='\u0412\u0430\u043b\u044e\u0442\u0430')),
                ('sum1_history', models.DecimalField(verbose_name='\u0418\u0437\u043d\u0430\u0447\u0430\u043b\u044c\u043d\u0430\u044f \u0441\u0443\u043c\u043c\u0430 \u043f\u0440\u043e\u0434\u0430\u0436\u0438', max_digits=20, decimal_places=10)),
                ('price', models.DecimalField(verbose_name='\u0426\u0435\u043d\u0430', max_digits=24, decimal_places=16, blank=True)),
                ('sum1', models.DecimalField(verbose_name='\u0441\u0443\u043c\u043c\u0430 \u043f\u0440\u043e\u0434\u0430\u0436\u0438', max_digits=20, decimal_places=10)),
                ('status', models.CharField(default=b'created', max_length=40, verbose_name='\u0421\u0442\u0430\u0442\u0443\u0441', choices=[(b'manually', '\u0440\u0443\u0447\u043d\u0430\u044f'), (b'deposit', '\u0434\u0435\u043f\u043e\u0437\u0438\u0442'), (b'withdraw', '\u0432\u044b\u0432\u043e\u0434'), (b'bonus', '\u043f\u0430\u0440\u0442\u043d\u0435\u0440\u0441\u043a\u043e\u0435 \u0432\u043e\u0437\u043d\u0430\u0433\u0440\u0430\u0436\u0434\u0435\u043d\u0438\u0435'), (b'payin', '\u043f\u043e\u043f\u043e\u043b\u043d\u0435\u043d\u0438\u0435'), (b'comission', '\u043a\u043e\u043c\u043c\u0438\u0441\u0441\u0438\u043e\u043d\u043d\u044b\u0435'), (b'created', '\u0441\u043e\u0437\u0434\u0430\u043d'), (b'incifition_funds', '\u043d\u0435\u0434\u043e\u0441\u0442\u0430\u0442\u043e\u0447\u043d\u043e \u0441\u0440\u0435\u0434\u0441\u0442\u0432'), (b'currency_core', '\u0432\u0430\u043b\u044e\u0442\u044b \u0441\u0447\u0435\u0442\u043e\u0432 \u043d\u0435 \u0441\u043e\u0432\u043f\u0430\u0434\u0430\u044e\u0442'), (b'processing', '\u0432 \u0440\u0430\u0431\u043e\u0442\u0435'), (b'processing2', '\u0432 \u0440\u0430\u0431\u043e\u0442\u0435 2'), (b'canceled', '\u043e\u0442\u043c\u0435\u043d\u0435\u043d'), (b'wait_secure', '\u0440\u0443\u0447\u043d\u0430\u044f \u043e\u0431\u0440\u0430\u0431\u043e\u0442\u043a\u0430'), (b'order_cancel', '\u043e\u0442\u043c\u0435\u043d\u0430 \u0437\u0430\u044f\u0432\u043a\u0438'), (b'deal', '\u0441\u0434\u0435\u043b\u043a\u0430'), (b'auto', '\u0430\u0432\u0442\u043e\u043c\u0430\u0442'), (b'automanually', '\u043c\u0430\u043d\u0443\u0430\u043b\u044c\u043d\u044b\u0439 \u0430\u0432\u0442\u043e\u043c\u0430\u0442'), (b'deal_return', '\u0432\u043e\u0437\u0432\u0440\u0430\u0442 \u043c\u0430\u043b\u0435\u043d\u044c\u043a\u043e\u0433\u043e \u043e\u0441\u0442\u0430\u0442\u043a\u0430'), (b'processed', '\u0438\u0441\u043f\u043e\u043b\u043d\u0435\u043d'), (b'core_error', '\u043e\u0448\u0438\u0431\u043a\u0430 \u044f\u0434\u0440\u0430')])),
                ('pub_date', models.DateTimeField(default=datetime.datetime.now, verbose_name='\u0414\u0430\u0442\u0430 \u043f\u0443\u0431\u043b\u0438\u043a\u0430\u0446\u0438\u0438', blank=True)),
                ('comission', models.DecimalField(default=b'0.0005', verbose_name='\u041a\u043e\u043c\u0438\u0441\u0441\u0438\u044f', max_digits=20, decimal_places=10, blank=True)),
                ('sign', models.CharField(max_length=255, verbose_name='Custom sign')),
                ('last_trans_id', models.IntegerField(null=True, verbose_name='last id', blank=True)),
                ('currency2', models.IntegerField(verbose_name='\u0412\u0430\u043b\u044e\u0442\u0430 \u0411', blank=True)),
                ('type_deal', models.CharField(default=b'transfer', max_length=40, verbose_name='\u0422\u0438\u043f', choices=[(b'sell', 'sell'), (b'buy', 'buy'), (b'transfer', 'transfer')])),
            ],
            options={
                'ordering': ('-id',),
                'verbose_name': '\u0417\u0430\u044f\u0432\u043a\u0430',
                'verbose_name_plural': '\u0417\u0430\u044f\u0432\u043a\u0438',
            },
        ),
        migrations.CreateModel(
            name='PoolAccounts',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(default=b'created', max_length=40, choices=[(b'manually', '\u0440\u0443\u0447\u043d\u0430\u044f'), (b'deposit', '\u0434\u0435\u043f\u043e\u0437\u0438\u0442'), (b'withdraw', '\u0432\u044b\u0432\u043e\u0434'), (b'bonus', '\u043f\u0430\u0440\u0442\u043d\u0435\u0440\u0441\u043a\u043e\u0435 \u0432\u043e\u0437\u043d\u0430\u0433\u0440\u0430\u0436\u0434\u0435\u043d\u0438\u0435'), (b'payin', '\u043f\u043e\u043f\u043e\u043b\u043d\u0435\u043d\u0438\u0435'), (b'comission', '\u043a\u043e\u043c\u043c\u0438\u0441\u0441\u0438\u043e\u043d\u043d\u044b\u0435'), (b'created', '\u0441\u043e\u0437\u0434\u0430\u043d'), (b'incifition_funds', '\u043d\u0435\u0434\u043e\u0441\u0442\u0430\u0442\u043e\u0447\u043d\u043e \u0441\u0440\u0435\u0434\u0441\u0442\u0432'), (b'currency_core', '\u0432\u0430\u043b\u044e\u0442\u044b \u0441\u0447\u0435\u0442\u043e\u0432 \u043d\u0435 \u0441\u043e\u0432\u043f\u0430\u0434\u0430\u044e\u0442'), (b'processing', '\u0432 \u0440\u0430\u0431\u043e\u0442\u0435'), (b'processing2', '\u0432 \u0440\u0430\u0431\u043e\u0442\u0435 2'), (b'canceled', '\u043e\u0442\u043c\u0435\u043d\u0435\u043d'), (b'wait_secure', '\u0440\u0443\u0447\u043d\u0430\u044f \u043e\u0431\u0440\u0430\u0431\u043e\u0442\u043a\u0430'), (b'order_cancel', '\u043e\u0442\u043c\u0435\u043d\u0430 \u0437\u0430\u044f\u0432\u043a\u0438'), (b'deal', '\u0441\u0434\u0435\u043b\u043a\u0430'), (b'auto', '\u0430\u0432\u0442\u043e\u043c\u0430\u0442'), (b'automanually', '\u043c\u0430\u043d\u0443\u0430\u043b\u044c\u043d\u044b\u0439 \u0430\u0432\u0442\u043e\u043c\u0430\u0442'), (b'deal_return', '\u0432\u043e\u0437\u0432\u0440\u0430\u0442 \u043c\u0430\u043b\u0435\u043d\u044c\u043a\u043e\u0433\u043e \u043e\u0441\u0442\u0430\u0442\u043a\u0430'), (b'processed', '\u0438\u0441\u043f\u043e\u043b\u043d\u0435\u043d'), (b'core_error', '\u043e\u0448\u0438\u0431\u043a\u0430 \u044f\u0434\u0440\u0430')])),
                ('pub_date', models.DateTimeField(default=datetime.datetime.now, verbose_name='\u0414\u0430\u0442\u0430 \u043f\u0443\u0431\u043b\u0438\u043a\u0430\u0446\u0438\u0438')),
                ('address', models.CharField(unique=True, max_length=255, verbose_name=' \u0412\u043d\u0435\u0448\u043d\u0438\u0439 \u043a\u043b\u044e\u0447 \u0438\u0434\u0435\u043d\u0442\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u0438 \u0438\u043b\u0438 \u043a\u043e\u0448\u0435\u043b\u0435\u043a \u043a\u0440\u0438\u043f\u0442\u043e\u0432\u0430\u043b\u044e\u0442\u044b ')),
                ('ext_info', models.CharField(unique=True, max_length=255, verbose_name='\u0414\u043e\u043f\u043e\u043b\u043d\u0438\u0442\u0435\u043b\u044c\u043d\u0430\u044f \u0438\u043d\u0444\u043e\u0440\u043c\u0430\u0446\u0438\u044f')),
                ('currency', models.ForeignKey(verbose_name='\u0412\u0430\u043b\u044e\u0442\u0430', to='main.Currency')),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('id',),
                'verbose_name': '\u041f\u0443\u043b\u0421\u0447\u0435\u0442\u043e\u0432',
                'verbose_name_plural': '\u041f\u0443\u043b\u0421\u0447\u0435\u0442\u0430',
            },
        ),
        migrations.CreateModel(
            name='TradePairs',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('url_title', models.CharField(max_length=255, verbose_name='Url \u0438\u0434\u0435\u043d\u0442\u0438\u0444\u0438\u043a\u0430\u0442\u043e\u0440')),
                ('ordering', models.IntegerField(default=1, verbose_name='\u0421\u043e\u0440\u0442\u0438\u0440\u043e\u0432\u043a\u0430')),
                ('status', models.CharField(default=b'created', max_length=40, verbose_name='\u0421\u0442\u0430\u0442\u0443\u0441', choices=[(b'manually', '\u0440\u0443\u0447\u043d\u0430\u044f'), (b'deposit', '\u0434\u0435\u043f\u043e\u0437\u0438\u0442'), (b'withdraw', '\u0432\u044b\u0432\u043e\u0434'), (b'bonus', '\u043f\u0430\u0440\u0442\u043d\u0435\u0440\u0441\u043a\u043e\u0435 \u0432\u043e\u0437\u043d\u0430\u0433\u0440\u0430\u0436\u0434\u0435\u043d\u0438\u0435'), (b'payin', '\u043f\u043e\u043f\u043e\u043b\u043d\u0435\u043d\u0438\u0435'), (b'comission', '\u043a\u043e\u043c\u043c\u0438\u0441\u0441\u0438\u043e\u043d\u043d\u044b\u0435'), (b'created', '\u0441\u043e\u0437\u0434\u0430\u043d'), (b'incifition_funds', '\u043d\u0435\u0434\u043e\u0441\u0442\u0430\u0442\u043e\u0447\u043d\u043e \u0441\u0440\u0435\u0434\u0441\u0442\u0432'), (b'currency_core', '\u0432\u0430\u043b\u044e\u0442\u044b \u0441\u0447\u0435\u0442\u043e\u0432 \u043d\u0435 \u0441\u043e\u0432\u043f\u0430\u0434\u0430\u044e\u0442'), (b'processing', '\u0432 \u0440\u0430\u0431\u043e\u0442\u0435'), (b'processing2', '\u0432 \u0440\u0430\u0431\u043e\u0442\u0435 2'), (b'canceled', '\u043e\u0442\u043c\u0435\u043d\u0435\u043d'), (b'wait_secure', '\u0440\u0443\u0447\u043d\u0430\u044f \u043e\u0431\u0440\u0430\u0431\u043e\u0442\u043a\u0430'), (b'order_cancel', '\u043e\u0442\u043c\u0435\u043d\u0430 \u0437\u0430\u044f\u0432\u043a\u0438'), (b'deal', '\u0441\u0434\u0435\u043b\u043a\u0430'), (b'auto', '\u0430\u0432\u0442\u043e\u043c\u0430\u0442'), (b'automanually', '\u043c\u0430\u043d\u0443\u0430\u043b\u044c\u043d\u044b\u0439 \u0430\u0432\u0442\u043e\u043c\u0430\u0442'), (b'deal_return', '\u0432\u043e\u0437\u0432\u0440\u0430\u0442 \u043c\u0430\u043b\u0435\u043d\u044c\u043a\u043e\u0433\u043e \u043e\u0441\u0442\u0430\u0442\u043a\u0430'), (b'processed', '\u0438\u0441\u043f\u043e\u043b\u043d\u0435\u043d'), (b'core_error', '\u043e\u0448\u0438\u0431\u043a\u0430 \u044f\u0434\u0440\u0430')])),
                ('pub_date', models.DateTimeField(default=datetime.datetime.now, verbose_name='\u0414\u0430\u0442\u0430')),
                ('min_trade_base', models.DecimalField(null=True, verbose_name='\u043c\u0438\u043d\u0438\u043c\u0430\u043b\u044c\u043d\u044b\u0439 \u0440\u0430\u0437\u043c\u0435\u0440 \u0441\u0434\u0435\u043b\u043a\u0438 \u0432\u0430\u043b\u044e\u0442\u044b \u0442\u043e\u0440\u0433\u0430/\u043a\u043e\u043c\u0438\u0441\u0441\u0438\u044f \u043f\u0440\u0438 \u0432\u044b\u0432\u043e\u0434\u0435', max_digits=12, decimal_places=10)),
                ('currency_from', models.ForeignKey(related_name='trade_currency_from', verbose_name='\u0412\u0430\u043b\u044e\u0442\u0430 \u0431\u0430\u0437\u043e\u0432\u0430\u044f', to='main.Currency')),
                ('currency_on', models.ForeignKey(related_name='trade_currency_on', verbose_name='\u0412\u0430\u043b\u044e\u0442\u0430 \u0442\u043e\u0440\u0433\u0430', to='main.Currency')),
                ('transit_from', models.ForeignKey(related_name='transit_account_from', verbose_name='\u0442\u0440\u0430\u043d\u0437\u0438\u0442\u043d\u044b\u0439 \u0441\u0447\u0435\u0442 \u0431\u0430\u0437\u043e\u0432\u043e\u0439 \u0432\u0430\u043b\u044e\u0442\u044b', to='main.Accounts')),
                ('transit_on', models.ForeignKey(related_name='transit_account_on', verbose_name='\u0442\u0440\u0430\u043d\u0437\u0438\u0442\u043d\u044b\u0439 \u0441\u0447\u0435\u0442 \u0432\u0430\u043b\u044e\u0442\u044b \u0442\u043e\u0440\u0433\u0430', to='main.Accounts')),
            ],
            options={
                'ordering': ('id',),
                'verbose_name': '\u0412\u0430\u043b\u044e\u0442\u043d\u0430\u044f \u043f\u0430\u0440\u0430',
                'verbose_name_plural': '\u0412\u0430\u043b\u044e\u0442\u043d\u044b\u0435 \u043f\u0430\u0440\u044b',
            },
        ),
        migrations.CreateModel(
            name='Trans',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('out_order_id', models.CharField(max_length=255, null=True, verbose_name=b'\xd0\x92\xd0\xbd\xd0\xb5\xd1\x88\xd0\xbd\xd0\xb8\xd0\xb9 order', blank=True)),
                ('balance1', models.DecimalField(verbose_name='\u0411\u0430\u043b\u0430\u043d\u0441 \u043e\u0442\u043f\u0440\u0430\u0432\u0438\u0442\u0435\u043b\u044f', editable=False, max_digits=20, decimal_places=10)),
                ('balance2', models.DecimalField(verbose_name='\u0411\u0430\u043b\u0430\u043d\u0441 \u043f\u043e\u043b\u0443\u0447\u0430\u0442\u0435\u043b\u044f', editable=False, max_digits=20, decimal_places=10)),
                ('res_balance1', models.DecimalField(verbose_name='\u0411\u0430\u043b\u0430\u043d\u0441 \u043e\u0442\u043f\u0440\u0430\u0432\u0438\u0442\u0435\u043b\u044f', editable=False, max_digits=20, decimal_places=10)),
                ('res_balance2', models.DecimalField(verbose_name='\u0411\u0430\u043b\u0430\u043d\u0441 \u043f\u043e\u043b\u0443\u0447\u0430\u0442\u0435\u043b\u044f', editable=False, max_digits=20, decimal_places=10)),
                ('amnt', models.DecimalField(verbose_name='\u0421\u0443\u043c\u043c\u0430', max_digits=20, decimal_places=10)),
                ('status', models.CharField(default=b'created', max_length=40, verbose_name='\u0421\u0442\u0430\u0442\u0443\u0441', choices=[(b'manually', '\u0440\u0443\u0447\u043d\u0430\u044f'), (b'deposit', '\u0434\u0435\u043f\u043e\u0437\u0438\u0442'), (b'withdraw', '\u0432\u044b\u0432\u043e\u0434'), (b'bonus', '\u043f\u0430\u0440\u0442\u043d\u0435\u0440\u0441\u043a\u043e\u0435 \u0432\u043e\u0437\u043d\u0430\u0433\u0440\u0430\u0436\u0434\u0435\u043d\u0438\u0435'), (b'payin', '\u043f\u043e\u043f\u043e\u043b\u043d\u0435\u043d\u0438\u0435'), (b'comission', '\u043a\u043e\u043c\u043c\u0438\u0441\u0441\u0438\u043e\u043d\u043d\u044b\u0435'), (b'created', '\u0441\u043e\u0437\u0434\u0430\u043d'), (b'incifition_funds', '\u043d\u0435\u0434\u043e\u0441\u0442\u0430\u0442\u043e\u0447\u043d\u043e \u0441\u0440\u0435\u0434\u0441\u0442\u0432'), (b'currency_core', '\u0432\u0430\u043b\u044e\u0442\u044b \u0441\u0447\u0435\u0442\u043e\u0432 \u043d\u0435 \u0441\u043e\u0432\u043f\u0430\u0434\u0430\u044e\u0442'), (b'processing', '\u0432 \u0440\u0430\u0431\u043e\u0442\u0435'), (b'processing2', '\u0432 \u0440\u0430\u0431\u043e\u0442\u0435 2'), (b'canceled', '\u043e\u0442\u043c\u0435\u043d\u0435\u043d'), (b'wait_secure', '\u0440\u0443\u0447\u043d\u0430\u044f \u043e\u0431\u0440\u0430\u0431\u043e\u0442\u043a\u0430'), (b'order_cancel', '\u043e\u0442\u043c\u0435\u043d\u0430 \u0437\u0430\u044f\u0432\u043a\u0438'), (b'deal', '\u0441\u0434\u0435\u043b\u043a\u0430'), (b'auto', '\u0430\u0432\u0442\u043e\u043c\u0430\u0442'), (b'automanually', '\u043c\u0430\u043d\u0443\u0430\u043b\u044c\u043d\u044b\u0439 \u0430\u0432\u0442\u043e\u043c\u0430\u0442'), (b'deal_return', '\u0432\u043e\u0437\u0432\u0440\u0430\u0442 \u043c\u0430\u043b\u0435\u043d\u044c\u043a\u043e\u0433\u043e \u043e\u0441\u0442\u0430\u0442\u043a\u0430'), (b'processed', '\u0438\u0441\u043f\u043e\u043b\u043d\u0435\u043d'), (b'core_error', '\u043e\u0448\u0438\u0431\u043a\u0430 \u044f\u0434\u0440\u0430')])),
                ('pub_date', models.DateTimeField(default=datetime.datetime.now, verbose_name='\u0414\u0430\u0442\u0430', editable=False)),
                ('currency', models.ForeignKey(verbose_name='\u0412\u0430\u043b\u044e\u0442\u0430', to='main.Currency')),
                ('order', models.ForeignKey(verbose_name='\u041e\u0440\u0434\u0435\u0440', blank=True, to='main.Orders', null=True)),
                ('user1', models.ForeignKey(related_name='from_account', verbose_name=b'\xd0\xa1\xd1\x87\xd0\xb5\xd1\x82 \xd0\xbe\xd1\x82\xd0\xbf\xd1\x80\xd0\xb0\xd0\xb2\xd0\xb8\xd1\x82\xd0\xb5\xd0\xbb\xd1\x8f', to='main.Accounts')),
                ('user2', models.ForeignKey(related_name='to_account', verbose_name=b'\xd0\xa1\xd1\x87\xd0\xb5\xd1\x82 \xd0\xbf\xd0\xbe\xd0\xbb\xd1\x83\xd1\x87\xd0\xb0\xd1\x82\xd0\xb5\xd0\xbb\xd1\x8f', to='main.Accounts')),
            ],
            options={
                'ordering': ('-id',),
                'verbose_name': '\u0422\u0440\u0430\u043d\u0437\u0430\u043a\u0446\u0438\u044f',
                'verbose_name_plural': '\u0422\u0440\u0430\u043d\u0437\u0430\u043a\u0446\u0438\u0438',
            },
        ),
        migrations.CreateModel(
            name='TransMem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('balance1', models.DecimalField(verbose_name='\u0411\u0430\u043b\u0430\u043d\u0441 \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044f', editable=False, max_digits=20, decimal_places=10)),
                ('res_balance1', models.DecimalField(verbose_name='\u0411\u0430\u043b\u0430\u043d\u0441 \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044f', editable=False, max_digits=20, decimal_places=10)),
                ('amnt', models.DecimalField(verbose_name='\u0421\u0443\u043c\u043c\u0430', max_digits=20, decimal_places=10)),
                ('comission', models.DecimalField(default=0, verbose_name='\u0421\u0443\u043c\u043c\u0430', max_digits=20, decimal_places=10)),
                ('status', models.CharField(default=b'created', max_length=40, verbose_name='\u0421\u0442\u0430\u0442\u0443\u0441', choices=[(b'manually', '\u0440\u0443\u0447\u043d\u0430\u044f'), (b'deposit', '\u0434\u0435\u043f\u043e\u0437\u0438\u0442'), (b'withdraw', '\u0432\u044b\u0432\u043e\u0434'), (b'bonus', '\u043f\u0430\u0440\u0442\u043d\u0435\u0440\u0441\u043a\u043e\u0435 \u0432\u043e\u0437\u043d\u0430\u0433\u0440\u0430\u0436\u0434\u0435\u043d\u0438\u0435'), (b'payin', '\u043f\u043e\u043f\u043e\u043b\u043d\u0435\u043d\u0438\u0435'), (b'comission', '\u043a\u043e\u043c\u043c\u0438\u0441\u0441\u0438\u043e\u043d\u043d\u044b\u0435'), (b'created', '\u0441\u043e\u0437\u0434\u0430\u043d'), (b'incifition_funds', '\u043d\u0435\u0434\u043e\u0441\u0442\u0430\u0442\u043e\u0447\u043d\u043e \u0441\u0440\u0435\u0434\u0441\u0442\u0432'), (b'currency_core', '\u0432\u0430\u043b\u044e\u0442\u044b \u0441\u0447\u0435\u0442\u043e\u0432 \u043d\u0435 \u0441\u043e\u0432\u043f\u0430\u0434\u0430\u044e\u0442'), (b'processing', '\u0432 \u0440\u0430\u0431\u043e\u0442\u0435'), (b'processing2', '\u0432 \u0440\u0430\u0431\u043e\u0442\u0435 2'), (b'canceled', '\u043e\u0442\u043c\u0435\u043d\u0435\u043d'), (b'wait_secure', '\u0440\u0443\u0447\u043d\u0430\u044f \u043e\u0431\u0440\u0430\u0431\u043e\u0442\u043a\u0430'), (b'order_cancel', '\u043e\u0442\u043c\u0435\u043d\u0430 \u0437\u0430\u044f\u0432\u043a\u0438'), (b'deal', '\u0441\u0434\u0435\u043b\u043a\u0430'), (b'auto', '\u0430\u0432\u0442\u043e\u043c\u0430\u0442'), (b'automanually', '\u043c\u0430\u043d\u0443\u0430\u043b\u044c\u043d\u044b\u0439 \u0430\u0432\u0442\u043e\u043c\u0430\u0442'), (b'deal_return', '\u0432\u043e\u0437\u0432\u0440\u0430\u0442 \u043c\u0430\u043b\u0435\u043d\u044c\u043a\u043e\u0433\u043e \u043e\u0441\u0442\u0430\u0442\u043a\u0430'), (b'processed', '\u0438\u0441\u043f\u043e\u043b\u043d\u0435\u043d'), (b'core_error', '\u043e\u0448\u0438\u0431\u043a\u0430 \u044f\u0434\u0440\u0430')])),
                ('order_id', models.IntegerField(verbose_name='\u041e\u0440\u0434\u0435\u0440')),
                ('pub_date', models.DateTimeField(default=datetime.datetime.now, verbose_name='\u0414\u0430\u0442\u0430', editable=False, blank=True)),
                ('currency', models.ForeignKey(verbose_name='\u0412\u0430\u043b\u044e\u0442\u0430', to='main.Currency')),
                ('user1', models.ForeignKey(related_name='from_mem', verbose_name=b'\xd0\xa1\xd1\x87\xd0\xb5\xd1\x82 \xd0\xbf\xd0\xbe\xd0\xbb\xd1\x8c\xd0\xb7\xd0\xbe\xd0\xb2\xd0\xb0\xd1\x82\xd0\xb5\xd0\xbb\xd1\x8f', to='main.Accounts')),
            ],
            options={
                'ordering': ('-id',),
                'verbose_name': '\u0422\u0440\u0430\u043d\u0437\u0430\u043a\u0446\u0438\u044f \u0432 \u043f\u0430\u043c\u044f\u0442\u0438',
                'verbose_name_plural': '\u0422\u0440\u0430\u043d\u0437\u0430\u043a\u0446\u0438\u0438 \u0432 \u043f\u0430\u043c\u044f\u0442\u0438',
            },
        ),
        migrations.CreateModel(
            name='VolatileConsts',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Name', models.CharField(max_length=255, verbose_name='\u043d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u043f\u0435\u0440\u0435\u043c\u0435\u043d\u043d\u043e\u0439')),
                ('Value', models.CharField(max_length=255, verbose_name='\u0417\u043d\u0430\u0447\u0435\u043d\u0438\u0435')),
            ],
            options={
                'verbose_name': '\u0412\u0440\u0435\u043c\u0435\u043d\u043d\u0430\u044f \u043f\u0435\u0440\u0435\u043c\u0435\u043d\u043d\u0430\u044f',
                'verbose_name_plural': '\u0412\u0440\u0435\u043c\u0435\u043d\u043d\u044b\u0435 \u043f\u0435\u0440\u0435\u043c\u0435\u043d\u043d\u044b\u0435',
            },
        ),
        migrations.AddField(
            model_name='orders',
            name='trade_pair',
            field=models.ForeignKey(verbose_name='\u0412\u0430\u043b\u044e\u0442\u043d\u0430\u044f \u043f\u0430\u0440\u0430', to='main.TradePairs'),
        ),
        migrations.AddField(
            model_name='orders',
            name='transit_1',
            field=models.ForeignKey(related_name='transit_account_1', verbose_name='\u0442\u0440\u0430\u043d\u0437\u0438\u0442\u043d\u044b\u0439 \u0441\u0447\u0435\u0442 \u043f\u043e\u043a\u0443\u043f\u043a\u0438', to='main.Accounts'),
        ),
        migrations.AddField(
            model_name='orders',
            name='transit_2',
            field=models.ForeignKey(related_name='transit_account_2', verbose_name='\u0442\u0440\u0430\u043d\u0437\u0438\u0442\u043d\u044b\u0439 \u0441\u0447\u0435\u0442 \u043f\u0440\u043e\u0434\u0430\u0436\u0438', to='main.Accounts'),
        ),
        migrations.AddField(
            model_name='orders',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='cryptotransfers2',
            name='comis_tid',
            field=models.ForeignKey(related_name='trans_comis_trans2', verbose_name='\u0422\u0440\u0430\u043d\u0437\u0430\u043a\u0446\u0438\u044f \u043a\u043e\u043c\u0438\u0441\u0441\u0438\u0438', to='main.Trans'),
        ),
        migrations.AddField(
            model_name='cryptotransfers2',
            name='currency',
            field=models.ForeignKey(related_name='currency_2', verbose_name='\u0412\u0430\u043b\u044e\u0442\u0430', to='main.Currency'),
        ),
        migrations.AddField(
            model_name='cryptotransfers2',
            name='order',
            field=models.ForeignKey(blank=True, editable=False, to='main.Orders', null=True, verbose_name='\u041e\u0440\u0434\u0435\u0440'),
        ),
        migrations.AddField(
            model_name='cryptotransfers2',
            name='user',
            field=models.ForeignKey(related_name='user_crypto_requested2', verbose_name='\u041a\u043b\u0438\u0435\u043d\u0442', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='cryptotransfers2',
            name='user_accomplished',
            field=models.ForeignKey(related_name='operator_crypto_processed2', verbose_name='\u041e\u043f\u0435\u0440\u0430\u0442\u043e\u0440 \u043f\u0440\u043e\u0432\u043e\u0434\u043a\u0438', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='cryptotransfers',
            name='comis_tid',
            field=models.ForeignKey(related_name='trans_comis_trans', verbose_name='\u0422\u0440\u0430\u043d\u0437\u0430\u043a\u0446\u0438\u044f \u043a\u043e\u043c\u0438\u0441\u0441\u0438\u0438', to='main.Trans'),
        ),
        migrations.AddField(
            model_name='cryptotransfers',
            name='currency',
            field=models.ForeignKey(verbose_name='\u0412\u0430\u043b\u044e\u0442\u0430', to='main.Currency'),
        ),
        migrations.AddField(
            model_name='cryptotransfers',
            name='order',
            field=models.ForeignKey(blank=True, editable=False, to='main.Orders', null=True, verbose_name='\u041e\u0440\u0434\u0435\u0440'),
        ),
        migrations.AddField(
            model_name='cryptotransfers',
            name='user',
            field=models.ForeignKey(related_name='user_crypto_requested', verbose_name='\u041a\u043b\u0438\u0435\u043d\u0442', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='cryptotransfers',
            name='user_accomplished',
            field=models.ForeignKey(related_name='operator_crypto_processed', verbose_name='\u041e\u043f\u0435\u0440\u0430\u0442\u043e\u0440 \u043f\u0440\u043e\u0432\u043e\u0434\u043a\u0438', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='accounts',
            name='currency',
            field=models.ForeignKey(verbose_name='\u0412\u0430\u043b\u044e\u0442\u0430', to='main.Currency'),
        ),
        migrations.AddField(
            model_name='accounts',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
