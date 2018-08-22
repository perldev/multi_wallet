# -*- coding: utf-8 -*-
from django.core.mail import get_connection, EmailMultiAlternatives
from django.db import models
from django.contrib import admin
from crypton import settings
from django import forms
from django.db import connection
from django.core.cache import get_cache

from django.contrib.auth.models import User
from django.utils.html import strip_tags
from main.msgs import notify_email, pins_reset_email, notify_admin_withdraw_fail
from main.http_common import generate_key_from, start_show_pin, delete_show_pin, generate_key, generate_key_from2, \
    format_numbers10, format_numbers_strong
from django.db import connection
from sdk.image_utils import ImageText, draw_text, pin
from decimal import Decimal
from main.subscribing import subscribe_connection
from datetime import datetime
from django.utils import timezone
import requests
import traceback
import math
from Crypto.Cipher import AES
from django.db import transaction
import base64
from sdk.crypto import CryptoAccount
import main.http_common
from main.account import get_account
import main.account
from sdk.g2f import getcode
from django.core.urlresolvers import reverse
import uuid

from sdk.crypto_settings import Settings as CryptoSettings


TYPE = (
    ("sell", u"sell"),
    ("buy", u"buy"),
    ("transfer", u"transfer"),
)


# Create your models here.
DEBIT_CREDIT = (
    ("in", u"debit"),
    ("out", u"credit"),
)

BOOL = (
    ("true", u"true"),
    ("false", u"false"),
)

STATUS_ORDER = (
    ("manually", u"ручная"),
    ("deposit", u"депозит"),
    ("withdraw", u"вывод"),
    ("bonus", u"партнерское вознаграждение"),
    ("payin", u"пополнение"),
    ("comission", u"коммиссионные"),
    ("created", u"создан"),
    ("incifition_funds", u"недостаточно средств"),
    ("currency_core", u"валюты счетов не совпадают"),
    ("processing", u'в работе'),
    ("processing2", u'в работе 2'),
    ("canceled", u'отменен'),
    ("wait_secure", u'ручная обработка'),
    ("order_cancel", u"отмена заявки"),
    ("deal", u"сделка"),
    ("auto", u"автомат"),
    ("automanually", u"мануальный автомат"),
    ("deal_return", u"возврат маленького остатка"),
    ("processed", u'исполнен'),
    ("core_error", u'ошибка ядра'),
)


def checksum(Obj):
    return True





class TransError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


from django.core.management.base import BaseCommand, CommandError
class BaseCommand(BaseCommand):

    def handle(self, *args, **options):
        print "start logging command"
        command = self.__module__
        if hasattr(self, "strict_name"):
            command = command +"_"+ "_".join(args[:]) 

        #d = start_ping_command(command)
        self.handle2(*args, **options)
        #finish_ping_command(d)


def start_ping_command(command):
 d = CommandsLogs(name=command)
 d.save()
 return d


def finish_ping_command(command):
 command.end_start_date = datetime.now()
 command.save()
 return True



class CommandsLogs(models.Model):
    name = models.CharField(max_length=255, verbose_name=u"название переменной")
    name2 = models.CharField(max_length=255, verbose_name=u"название переменной")
    start_date = models.DateTimeField(default=datetime.now, verbose_name=u"Дата публикации")
    end_start_date = models.DateTimeField(blank=True, verbose_name=u"Дата окончания")
    log = models.CharField(max_length=255, verbose_name=u"Значение")

    class Meta:
        verbose_name = u'логи комманд'
        verbose_name_plural = u'логи комманд'

    ordering = ('id',)

    def __unicode__(o):
        return o.name + "=" + o.start_date




def mines_prec(dec_number1, dec_number2, Prec):
    return Decimal(Decimal(dec_number1)-Decimal(dec_number2))
    PrecMul = 10 ** Prec
    PreStr = list(str(int(dec_number1 * PrecMul) - int(dec_number2 * PrecMul)))
    #print PreStr
    MinesAdd = False
    if PreStr[0] == '-':
        PreStr = PreStr[1:]
        MinesAdd = True

    size = len(PreStr)
    #print size
    if size > Prec:
        Dot = size - Prec
        if MinesAdd:
            return Decimal("-" + "".join(PreStr[:Dot]) + "." + "".join(PreStr[Dot:]))
        return Decimal("".join(PreStr[:Dot]) + "." + "".join(PreStr[Dot:]))
    else:

        Mask = ['0'] * Prec
        #print Mask
        From = Prec - size
        #print From
        Mask[From:] = PreStr
        #print Mask
        if MinesAdd:
            return Decimal("-0." + "".join(Mask))
        return Decimal("0." + "".join(Mask))


def plus_prec(dec_number1, dec_number2, Prec):
    return Decimal(dec_number1)+Decimal(dec_number2)
    PrecMul = 10 ** Prec
    PreStr = list(str(int(dec_number1 * PrecMul) + int(dec_number2 * PrecMul)))
    MinesAdd = False
    if PreStr[0] == '-':
        PreStr = PreStr[1:]
        MinesAdd = True
    size = len(PreStr)

    if size > Prec:
        Dot = size - Prec
        if MinesAdd:
            return Decimal('-' + "".join(PreStr[:Dot]) + "." + "".join(PreStr[Dot:]))

        return Decimal("".join(PreStr[:Dot]) + "." + "".join(PreStr[Dot:]))
    else:
        Mask = ['0'] * Prec
        From = Prec - size
        Mask[From:] = PreStr
        if MinesAdd:
            return Decimal("-0." + "".join(Mask))
        return Decimal("0." + "".join(Mask))


def sato2Dec(Satochi):
    PreStr = list(str(int(Satochi)))
    size = len(PreStr)
    Prec = 8
    if size > Prec:
        Dot = size - Prec
        return Decimal("".join(PreStr[:Dot]) + "." + "".join(PreStr[Dot:]))
    else:
        Mask = ['0'] * Prec
        From = Prec - size
        Mask[From:] = PreStr
        return Decimal("0." + "".join(Mask))


def to_prec(dec_number, Prec):
    PrecMul = 10 ** Prec
    PreStr = list(str(int(dec_number * PrecMul)))
    MinesAdd = False
    if PreStr[0] == '-':
        PreStr = PreStr[1:]
        MinesAdd = True

    size = len(PreStr)

    if size > Prec:
        Dot = size - Prec
        if MinesAdd:
            return Decimal('-' + "".join(PreStr[:Dot]) + "." + "".join(PreStr[Dot:]))
        return Decimal("".join(PreStr[:Dot]) + "." + "".join(PreStr[Dot:]))
    else:
        Mask = ['0'] * Prec
        From = Prec - size
        Mask[From:] = PreStr
        if MinesAdd:
            return Decimal("-0." + "".join(Mask))

        return Decimal("0." + "".join(Mask))


class TransRepr(object):
    def __init__(self, trans, From, Amnt, Currency, To, Comis):
        self.trans_object = trans
        self.account = From
        self.amnt = Amnt
        self.currency = Currency
        self.order = To
        self.comis = Comis
        
    def __getitem__(self, i):
        if i == 0:
            return self.trans_object
        if i == 1:
            return self.account
        if i == 2:
            return self.amnt
        if i == 3:
            return self.currency
        if i == 4:
            return self.order
        if i == 5:
            return self.comis
        
    def __repr__(self):    
        return "%s %s %s %s" % (From, Amnt, Currency, To, Comis)    
        
        
####make a queue demon here there
### repeat functionality of add_trans
def add_trans2(From, Amnt, Currency, To, status="created", Strict=True, Comis = 0):
    if not isinstance(From, main.account.Account):
        raise TransError("requirment accounts from")

    if not isinstance(To, OrdersMem):
        raise TransError("requirment accounts To")
    Amnt = Decimal(Amnt)
    trans = TransMem(balance1=From.get_balance,
                     user1=From.acc(),
                     order_id=To.id,
                     currency_id=Currency,
                     amnt=Amnt,
                     res_balance1 = Decimal("0.0"),
                     status="core_error")
    trans.save()

    if From.currency <> Currency:
        trans.status = "currency_core"
        trans.save()
        raise TransError("currency_core %s and %s " % (From.currency, Currency))

    if To.currency <> Currency:
        trans.status = "currency_core"
        trans.save()
        raise TransError("currency_core %s and %s " % (To.currency, Currency))

    trans.save()
    NewBalance = 0
        
    if status == "deal" and Comis!=0:
        NewAmnt = Amnt - Amnt*Decimal(Comis)
        NewBalance = From.balance - NewAmnt
        trans.comission = Amnt - NewAmnt
    else:
        NewBalance = From.balance - Amnt
        
        
    if Strict:
        if NewBalance < 0:
            trans.status = "incifition_funds"
            trans.save()
            raise TransError("incifition_funds from %s" % NewBalance)

    ToNewBalance = Decimal(To.sum1) + Decimal(Amnt)
    
    if Strict:
        if ToNewBalance < 0:
            trans.status = "incifition_funds"
            trans.save()
            raise TransError("incifition_funds to %s" % NewBalance)

    #try:
    trans.res_balance1 = NewBalance
    with transaction.atomic():
        To.update(trans, ToNewBalance)
        # race condition
        From.save(trans)
        trans.status=status
    
    trans.save()
     
    #except:
    #    From.reload()
    #    trans.save()
    #    raise TransError("core_error")
    return TransRepr(trans, From, Amnt, Currency, To, Comis)
    

# DO NOT USE for highload operations
####make a queue demon here there only for back capability 
def add_trans(From, Amnt, Currency, To, order, status="created", Out_order_id=None, Strict=True):
    TransPrecession = settings.TRANS_PREC
    
    From = Accounts.objects.get(id=From.id)
    To = Accounts.objects.get(id=To.id)
    
    if Strict and order is None:
        raise TransError("requirment_params_order")

    if Out_order_id is None and order is not None:
        Out_order_id = str(order.id)

    trans = Trans(out_order_id=Out_order_id,
                  balance1=From.balance,
                  balance2=To.balance,
                  user1=From,
                  user2=To,
                  order=order,
                  currency=Currency,
                  amnt=Amnt,
                  status=status)
    trans.save()

    if From.currency <> Currency:
        trans.status = "currency_core"
        trans.save()
        raise TransError("currency_core")

    if To.currency <> Currency:
        trans.status = "currency_core"
        trans.save()
        raise TransError("currency_core")

    FromBalance = From.balance
    ToBalance = To.balance
    NewBalance = mines_prec(FromBalance, Amnt, TransPrecession)
    ToNewBalance = plus_prec(ToBalance, Amnt, TransPrecession)
    if Strict:
        if NewBalance < 0:
            trans.status = "incifition_funds"
            trans.save()
            raise TransError("incifition_funds")

    mem_order = order.mem_order()
    mem_order.sum1 = Decimal("0.0")
    FromAccount = get_account(user_id=From.user_id, currency_id=Currency.id)
    ToAccount = get_account(user_id=To.user_id, currency_id=Currency.id)
    try:
      Amnt = Decimal(Amnt)
      with transaction.atomic():
         add_trans2(FromAccount, Amnt, Currency.id, mem_order, status, Strict)
         add_trans2(ToAccount, -1*Amnt, Currency.id, mem_order, status, Strict)    
      trans.res_balance1 = NewBalance
      trans.res_balance2 = ToNewBalance
      trans.save()
      return trans
    except:
        mem_order.status = "core_error"
        mem_order.save()
        order.status ='core_error'
        order.save()
        trans.status = "core_error"
	trans.save()
        raise TransError("core_error")
    
   


class VolatileConsts(models.Model):
    Name = models.CharField(max_length=255, verbose_name=u"название переменной")
    Value = models.CharField(max_length=255, verbose_name=u"Значение")

    class Meta:
        verbose_name = u'Временная переменная'
        verbose_name_plural = u'Временные переменные'

    ordering = ('id',)

    def __unicode__(o):
        return o.Name + "=" + o.Value



class CurrencyAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        Comis = User.objects.get(id=settings.COMISSION_USER)
        Crypto = User.objects.get(id=settings.CRYPTO_USER)

        obj.save()
        if not change:
            for i in User.objects.all():
                d = Accounts(user=i, currency=obj, balance="0.000", last_trans_id=None)
                d.save()

        try:
            ComisAccount = Accounts.objects.get(user=Comis, currency=obj, last_trans_id=None)
        except Accounts.DoesNotExist:
            ComisAccount = Accounts(user=Comis, currency=obj, balance="0.000",  last_trans_id=None)
            ComisAccount.save()

        Crypto_Account = None
        try:
            Crypto_Account = Accounts.objects.get(user=Crypto, currency=obj,  last_trans_id=None)
        except Accounts.DoesNotExist:
            Crypto_Account = Accounts(user=Crypto, currency=obj, balance="0.000",  last_trans_id=None)
            Crypto_Account.save()

        try:
            Tr = TradePairs.objects.get(currency_from=obj,
                                        currency_on=obj,
                                        transit_on=Crypto_Account,
                                        transit_from=Crypto_Account)
        except TradePairs.DoesNotExist:
            trade_pair = TradePairs(
                currency_from=obj,
                currency_on=obj,
                transit_on=Crypto_Account,
                transit_from=Crypto_Account,
                title="CRYPTO_IN_OUT_%s" % (obj.title),
                url_title="crypto_in_out%s" % (obj.title),
                ordering=0
            )
            trade_pair.save()

        return True


class Currency(models.Model):
    title = models.CharField(max_length=255, verbose_name=u"Название")
    long_title = models.CharField(max_length=255, verbose_name=u"Длиное название")
    text = models.TextField(verbose_name=u"Описание")
    img = models.ImageField(upload_to='clogo', verbose_name=u'Логотип')
    ordering = models.IntegerField(verbose_name=u"Сортировка", default=1)
    pub_date = models.DateTimeField(default=datetime.now, verbose_name=u"Дата публикации")

    class Meta:
        verbose_name = u'Валюта'
        verbose_name_plural = u'Валюты'
        ordering = ('id',)

    def __unicode__(o):
        return o.title



class PoolAccounts(models.Model):
    status = models.CharField(max_length=40,
                              choices=STATUS_ORDER,
                              default='created')

    user = models.ForeignKey(User, blank=True, null=True)
    currency = models.ForeignKey("Currency", verbose_name=u"Валюта")
    pub_date = models.DateTimeField(default=datetime.now, verbose_name=u"Дата публикации")
    address = models.CharField(max_length=255,
                               unique=True,
                               verbose_name=u" Внешний ключ идентификации или кошелек криптовалюты ")

    ext_info = models.CharField(max_length=255,
                               unique=True,
                               verbose_name=u"Дополнительная информация")
    class Meta:
        verbose_name = u'ПулСчетов'
        verbose_name_plural = u'ПулСчета'
        ordering = ('id',)

    def __unicode__(o):
        return o.user.username + " " + str(o.address) + " " + str(o.currency)


class Accounts(models.Model):
    user = models.ForeignKey(User)
    currency = models.ForeignKey("Currency", verbose_name=u"Валюта")
    balance = models.DecimalField(verbose_name=u"Баланс", default=0, max_digits=20, decimal_places=10)
    pub_date = models.DateTimeField(default=datetime.now, verbose_name=u"Дата публикации")
    reference = models.CharField(max_length=255,
                                 null=True,
                                 unique=True,
                                 blank=True,
                                 verbose_name=u" Внешний ключ идентификации или кошелек криптовалюты ")
    last_trans_id = models.IntegerField(verbose_name = "last_trans", null=True)
    class Meta:
        verbose_name = u'Счет'
        verbose_name_plural = u'Счета'
        ordering = ('id',)

    def __unicode__(o):
        return o.user.username + " " + str(o.balance) + " " + str(o.currency)


class AccountsAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'currency', 'balance', 'reference', 'pub_date']
    actions = ["add", "delete", "edit"]
    list_filter = ('user', 'currency')

    #exclude = ['balance']
    search_fields = ['^user__username', 'user__email', ]
    #def get_form(self, request, obj=None, **kwargs):
    #    if obj is None:
    #            return super(AccountsAdmin, self).get_form(request, obj, **kwargs)               

    def __init__(self, *args, **kwargs):
        super(AccountsAdmin, self).__init__(*args, **kwargs)
        # self.list_display_links = (None, )


class TradePairs(models.Model):
    title = models.CharField(max_length=255, verbose_name=u"Название")
    url_title = models.CharField(max_length=255, verbose_name=u"Url идентификатор")
    ordering = models.IntegerField(verbose_name=u"Сортировка", default=1)
    transit_on = models.ForeignKey(Accounts,
                                   related_name="transit_account_on",
                                   verbose_name=u"транзитный счет валюты торга")
    transit_from = models.ForeignKey(Accounts, related_name="transit_account_from",
                                     verbose_name=u"транзитный счет базовой валюты")
    currency_on = models.ForeignKey("Currency", related_name="trade_currency_on",
                                    verbose_name=u"Валюта торга")
    currency_from = models.ForeignKey("Currency", related_name="trade_currency_from",
                                      verbose_name=u"Валюта базовая")
    status = models.CharField(max_length=40,
                              choices=STATUS_ORDER,
                              default='created', verbose_name=u"Статус")
    pub_date = models.DateTimeField(default=datetime.now, verbose_name=u"Дата")
    min_trade_base = models.DecimalField(verbose_name=u"минимальный размер сделки валюты торга/комиссия при выводе",
                                         max_digits=12, decimal_places=10, null=True)

    class Meta:
        verbose_name = u'Валютная пара'
        verbose_name_plural = u'Валютные пары'
        ordering = ('id',)

    def __unicode__(o):
        return o.title


def check_holds(order):
    Account = order.transit_2
    Now = timezone.localtime(timezone.now())
    try:
        trans = Trans.objects.get(user2=Account, status="payin")
    except Trans.DoesNotExist:
        hold = HoldsWithdraw(user=order.user, hours=36)
        hold.save()
    except:
        pass


class TransMemAdmin(admin.ModelAdmin):
    list_display = ['id',  'user1', 'order_id', 'balance1',  'currency', 'amnt',
                    'status', 'res_balance1',  'pub_date']
    list_filter = ('status', 'currency')


    def __init__(self, *args, **kwargs):
        super(TransMemAdmin, self).__init__(*args, **kwargs)
        self.list_display_links = (None, )


class TransMem(models.Model):

    balance1 = models.DecimalField(max_digits=20, editable=False, decimal_places=10, verbose_name=u"Баланс пользователя")
    res_balance1 = models.DecimalField(max_digits=20, editable=False, decimal_places=10,
                                       verbose_name=u"Баланс пользователя")
    user1 = models.ForeignKey(Accounts, related_name="from_mem",
                              verbose_name="Счет пользователя")
    currency = models.ForeignKey("Currency", verbose_name=u"Валюта")
    amnt = models.DecimalField(max_digits=20, decimal_places=10, verbose_name=u"Сумма")
    comission = models.DecimalField(max_digits=20, default=0, decimal_places=10, verbose_name=u"Сумма")

    status = models.CharField(max_length=40,
                              choices=STATUS_ORDER,
                              default='created', verbose_name=u"Статус")
    order_id = models.IntegerField(verbose_name=u"Ордер")
    pub_date = models.DateTimeField(default=datetime.now, blank=True, verbose_name=u"Дата", editable=False)


    class Meta:
        verbose_name = u'Транзакция в памяти'
        verbose_name_plural = u'Транзакции в памяти'
        ordering = ('-id',)

    def __unicode__(o):
        return o.order_id


class Trans(models.Model):
    out_order_id = models.CharField(max_length=255, verbose_name="Внешний order",
                                    null=True, blank=True)
    balance1 = models.DecimalField(max_digits=20, editable=False,
                                   decimal_places=10, verbose_name=u"Баланс отправителя")
    balance2 = models.DecimalField(max_digits=20, editable=False, 
                                   decimal_places=10, verbose_name=u"Баланс получателя")

    res_balance1 = models.DecimalField(max_digits=20, editable=False, decimal_places=10,
                                       verbose_name=u"Баланс отправителя")
    res_balance2 = models.DecimalField(max_digits=20, editable=False, decimal_places=10,
                                       verbose_name=u"Баланс получателя")
    user1 = models.ForeignKey(Accounts, related_name="from_account",
                              verbose_name="Счет отправителя")
    user2 = models.ForeignKey(Accounts, related_name="to_account",
                              verbose_name="Счет получателя")
    currency = models.ForeignKey("Currency", verbose_name=u"Валюта")
    amnt = models.DecimalField(max_digits=20, decimal_places=10, verbose_name=u"Сумма")
    status = models.CharField(max_length=40,
                              choices=STATUS_ORDER,
                              default='created', verbose_name=u"Статус")
    order = models.ForeignKey("Orders", verbose_name=u"Ордер", blank=True, null=True)

    pub_date = models.DateTimeField(default=datetime.now, verbose_name=u"Дата", editable=False)


    class Meta:
        verbose_name = u'Транзакция'
        verbose_name_plural = u'Транзакции'
        ordering = ('-id',)

    def __unicode__(o):
        return o.out_order_id


def cancel_trans(modeladmin, request, queryset):
    for obj in queryset:
        add_trans(obj.user2,
                  obj.amnt,
                  obj.currency,
                  obj.user1,
                  obj.order,
                  "canceled",
                  obj.id,
                  False)


cancel_trans.short_description = u"Cancel Trans"


class TransAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'user1', 'balance1', 'user2', 'balance2', 'currency', 'amnt', 'status',
                    'res_balance1', 'res_balance2', 'pub_date']
    list_filter = ('status', 'currency')

    actions = ["add", cancel_trans]

    def save_model(self, request, obj, form, change):
        return True


    def __init__(self, *args, **kwargs):
        super(TransAdmin, self).__init__(*args, **kwargs)
        self.list_display_links = (None, )


# this strips the html, so people will have the text as well.
# create the email, and attach the HTML version as well.





        
        
        
class OrdersMemAdmin(admin.ModelAdmin):
    list_display = ['user', 'trade_pair', 'price', 'currency1', 'sum1_history', 'sum1', 'currency2', 'status', 'pub_date']
    list_filter = ('user', 'currency1', 'currency2', 'status')


class OrdersMem(models.Model):
    user = models.IntegerField()
    trade_pair = models.IntegerField(verbose_name=u"Валютная пара")
    currency1 = models.IntegerField(verbose_name=u"Валюта", )
    sum1_history = models.DecimalField(verbose_name=u"Изначальная сумма продажи", max_digits=20, decimal_places=10)
    price = models.DecimalField(verbose_name=u"Цена", max_digits=24, decimal_places=16, blank=True)
    sum1 = models.DecimalField(verbose_name=u"сумма продажи", max_digits=20, decimal_places=10)
    status = models.CharField(max_length=40, choices=STATUS_ORDER, default='created', verbose_name=u"Статус")
    pub_date = models.DateTimeField(default=datetime.now, blank=True, verbose_name=u"Дата публикации")
    comission = models.DecimalField(max_digits=20, default='0.0005', blank=True, decimal_places=10,
                                    verbose_name=u"Комиссия")
    sign = models.CharField(max_length=255, verbose_name=u"Custom sign")
    last_trans_id = models.IntegerField(verbose_name=u"last id", blank=True, null=True)
    currency2 = models.IntegerField(blank=True, verbose_name=u"Валюта Б", )
    type_deal = models.CharField(max_length=40, choices=TYPE, default='transfer', verbose_name=u"Тип")

    
    @property
    def currency(self):
        return self.currency1
        
    def update(self, trans, new_amnt):
        # TODO rewrite to update statemant
        
        count = OrdersMem.objects.filter(last_trans_id=self.last_trans_id, 
                                         id=self.id).update(last_trans_id=trans.id, sum1=new_amnt)
        if count!=1:
            raise TransError("race condition at order %s" % self)
        
        self.last_trans_id = trans.id
        self.sum1 = new_amnt
        

    class Meta:
        verbose_name = u'Заявка'
        verbose_name_plural = u'Заявки'
        ordering = ('-id',)

    def make2processed(self):
        self.status = "processed"
        self.save()

    

    def salt_repr(self):
        return ",".join([str(getattr(self, field.name)) for field in self._meta.local_fields])

    def save_model(self, request, obj, form, change):
        checksum(self)
        super(OrdersMem, self).save(request, obj, form, change)


    def fields4sign(self):
        List = []
        for i in ('currency1', 'sum1_history', 'sum1',
                  'price', 'last_trans_id', 'user', 'comission'):
            Val = getattr(self, i)
            if i in ('sum1_history', 'sum1', 'sum2', 'comission'):
                List.append(format_numbers_strong(Val))
            else:
                List.append(str(Val))

        return ",".join(List)

    def stable_order(self, key):
        ### account buyer, sum to buy, item - order seller, Order - order buyer
        TradePair = TradePairs.objects.get(id = self.trade_pair)
        (sum2, sum2_history) = (None, None)
        if TradePair.currency_on.id == Currency1.id:
              transit1 = TradePair.transit_on
              transit2 = TradePair.transit_from
              sum2 = self.sum1*self.price
              sum2_history = self.sum1_history*self.price
        else :
              transit2 = TradePair.transit_on
              transit1 = TradePair.transit_from  
              sum2 = self.sum1/self.price
              sum2_history = self.sum1_history/self.price
        
        Mem = Orders(user_id=self.user,
                     trade_pair_id=self.trade_pair,
                     currency1_id=self.currency1,
                     sum1_history=self.sum1_history,
                     price=self.price,
                     sum1=self.sum1,
                     pub_date=self.pub_date,
                     currency2_id=self.currency2,
                     sum2_history=sum2_history,
                     sum2=sum2,
                     status=self.status,
                     transit_1_id=transit_1,
                     transit_2_id=transit_2,
                     comission=self.comission)

        Mem.sign_record(key)
        Mem.save()
        return Mem

    def __unicode__(self):
        return self.fields4sign()

    def verify(self, key):
        Fields = self.fields4sign()
        Sign = generate_key_from2(Fields, key + settings.SIGN_SALT)
        return Sign == self.sign

    def sign_record(self, key):
        Fields = self.fields4sign()
        self.sign = generate_key_from2(Fields, key + settings.SIGN_SALT)
        self.save()


class Orders(models.Model):
    user = models.ForeignKey(User)
    trade_pair = models.ForeignKey(TradePairs, verbose_name=u"Валютная пара")
    currency1 = models.ForeignKey("Currency", related_name='from_currency', verbose_name=u"Валюта A", )
    sum1_history = models.DecimalField(verbose_name=u"Изначальная сумма продажи", max_digits=20, decimal_places=10)
    price = models.DecimalField(verbose_name=u"Цена", max_digits=24, decimal_places=16, blank=True)
    sum1 = models.DecimalField(verbose_name=u"сумма продажи", max_digits=20, decimal_places=10)
    currency2 = models.ForeignKey("Currency", related_name='to_currency', verbose_name=u"Валюта Б", )
    sum2_history = models.DecimalField(verbose_name=u"Изначальная сумма покупки", max_digits=20, decimal_places=10)
    sum2 = models.DecimalField(verbose_name=u"сумма покупки", max_digits=20, decimal_places=10)
    status = models.CharField(max_length=40, choices=STATUS_ORDER, default='created', verbose_name=u"Статус")
    pub_date = models.DateTimeField(default=datetime.now, verbose_name=u"Дата публикации")
    transit_1 = models.ForeignKey(Accounts, related_name="transit_account_1", verbose_name=u"транзитный счет покупки")
    transit_2 = models.ForeignKey(Accounts, related_name="transit_account_2", verbose_name=u"транзитный счет продажи")
    comission = models.DecimalField(max_digits=20, default='0.0005', blank=True, decimal_places=10,
                                    verbose_name=u"Комиссия")
    sign = models.CharField(max_length=255, default='0.0005', verbose_name=u"Custom sign")
    public_key = models.CharField(max_length=255, default='0.0005', verbose_name=u"public key")

    # May be we can setup this
    def salt_repr(self):
        return ",".join([str(getattr(self, field.name)) for field in self._meta.local_fields])

    def fields4sign(self):
        List = []
        for i in ('currency1', 'currency2', 'sum1_history', 'sum2_history', 'sum1', 'sum2',
                  'transit_1', 'transit_2', 'user_id', 'trade_pair'):
            Val = getattr(self, i)
            if i in ('sum1_history', 'sum2_history', 'sum1', 'sum2'):
                List.append(format_numbers_strong(Val))
            else:
                List.append(str(Val))

        return ",".join(List)


    def verify(self, key):
        Fields = self.fields4sign()
        Sign = generate_key_from2(Fields, key + settings.SIGN_SALT)
        return Sign == self.sign

    def sign_record(self, key):
        Fields = self.fields4sign()
        self.sign = generate_key_from2(Fields, key + settings.SIGN_SALT)
        self.save()

    def save_model(self, *args, **kwargs):
        checksum(self)
        super(Orders, self).save(*args, **kwargs)

    
    #user = models.IntegerField(User)
    #trade_pair = models.IntegerField(verbose_name=u"Валютная пара")
    #currency1 = models.IntegerField(verbose_name=u"Валюта", )
    #sum1_history = models.DecimalField(verbose_name=u"Изначальная сумма продажи", max_digits=20, decimal_places=10)
    #price = models.DecimalField(verbose_name=u"Цена", max_digits=24, decimal_places=16, blank=True)
    #sum1 = models.DecimalField(verbose_name=u"сумма продажи", max_digits=20, decimal_places=10)
    #status = models.CharField(max_length=40, choices=STATUS_ORDER, default='created', verbose_name=u"Статус")
    #pub_date = models.DateTimeField(auto_now=True, verbose_name=u"Дата публикации")
    #comission = models.DecimalField(max_digits=20, default='0.0005', blank=True, decimal_places=10,
                                    #verbose_name=u"Комиссия")
    #sign = models.CharField(max_length=255, verbose_name=u"Custom sign")
    #last_trans_id = models.IntegerField(verbose_name=u"last id", blank=True, null=True)
    #currency2 = models.IntegerField(blank=True, verbose_name=u"Валюта Б", )

        

    def mem_order(self):
        Mem = OrdersMem(
                    user=self.user_id,
                    trade_pair=self.trade_pair.id,
                    currency1=self.currency1.id,
                    sum1_history=self.sum1_history,
                    price=self.price,
                    sum1=self.sum1,
                    currency2=self.currency2.id,
                    status=self.status,
                    comission=self.comission)
        Mem.save()
        return Mem


    class Meta:
        verbose_name = u'Сделка'
        verbose_name_plural = u'Сделки'
        ordering = ('-id',)

    def __unicode__(o):
        return str(o.id)




class OrdersAdmin(admin.ModelAdmin):
    list_display = ['user', 'trade_pair', 'price', 'currency1', 'sum1_history', 'sum1', 'currency2', 'sum2_history',
                    'sum2', 'status', 'pub_date']
    list_filter = ('user', 'currency1', 'currency2', 'status')


def dictfetchall(cursor, Query):
    "Returns all rows from a cursor as a dict"
    List = cursor.fetchall()
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in List
    ]


def process_in_crypto_low(List, user_system, CurrencyInstance):
        CurrencyTitle = CurrencyInstance.title
        for trans in List :
                try:
                  Txid = trans["txid"]
                except:
                  print "some error"
                  print trans
                  return None
                if trans["category"] == "receive":
                        Account  = None
                        Trans = None
                        New = False
                        Decimal = format_numbers_strong(trans["amount"])
                        if CurrencyTitle == "BCH" :
                            print "converting bch address"
                            print trans["address"]
                            trans["address"] = trans["address"]
                            print trans["address"]

                        try :
                               Account  = Accounts.objects.get(user_id=settings.SYSTEM_USER, currency_id=CurrencyInstance)
                               print "Txid is %s" % Txid

                               suffix = trans['address'][-5:]
                               FixCryptoTxid = Txid + "_" + suffix
                               print "check suffix first"    
                               count_sufix = CryptoTransfers.objects.filter(crypto_txid = FixCryptoTxid).count()
                               if count_sufix>0:
                                  print "but it's another adress %s add trans with suffix %s" % (trans['address'], FixCryptoTxid)
                                  continue
                               

                               Trans = CryptoTransfers.objects.get(crypto_txid = Txid, 
                                                                   account = trans["address"],
                                                                   currency = CurrencyInstance )

                                
                               
                               print "we have been there before"
                        except Accounts.DoesNotExist:
                               print "we do not find trans for this trans"
                        except  CryptoTransfers.DoesNotExist:
                                Trans =  CryptoTransfers(crypto_txid = Txid,
                                                         status="processing",
                                                         amnt = Decimal,
                                                         currency = CurrencyInstance ,
                                                         account = trans["address"],
                                                         user = Account.user,
                                                         confirms = 0
                                                        )
                                Trans.save()
                                print "in one trans to our accounts"
                                print "#%i receive %s to %s amount of %s" % (Trans.id ,Txid, trans["address"], trans['amount'] )
                        except :
                             traceback.print_exc()
                             print "some error"
                             print trans

                        if Trans is None :
                           continue
     
                        if (Trans.status == "processing" or Trans.status == "processing2" )\
                           and trans["confirmations"] > CryptoSettings[CurrencyTitle]["min_confirmation"]:
                                print "processing it %s" % (str(trans))
                                Trans.confirms = int(trans["confirmations"])
                                Trans.save()
                                crypton_in(Trans, user_system)
                                continue

                        if Trans.status == "processing" or Trans.status == "processing2":
                                Trans.confirms = int(trans["confirmations"])
                                Trans.save()
                                continue




#CRYPTO BANK TRANSFERS
def crypton_in(obj, user_accomplished):
    if False and not obj.verify(settings.CRYPTO_SALT):
        return

    TradePair = TradePairs.objects.get(currency_on=obj.currency,
                                       currency_from=obj.currency)

    AccountTo = Accounts.objects.get(user=obj.user,
                                     currency=obj.currency)
    ##create order for them
    order = Orders(user=obj.user,
                   currency1=obj.currency,
                   currency2=obj.currency,
                   sum1_history=obj.amnt,
                   sum2_history=obj.amnt,
                   price=obj.amnt,
                   sum1=obj.amnt,
                   sum2=obj.amnt,
                   transit_1=TradePair.transit_on,
                   transit_2=AccountTo,
                   trade_pair=TradePair,
                   status="processing"
    )
    order.save()
    obj.order = order
    try:
       print "start processing "
       resp = requests.get(settings.PROCESSING + "/add_payin/" + str(order.id))
       print resp
       print resp.text
    except:
       traceback.print_exc()
    #add_trans(TradePair.transit_on, obj.amnt, obj.currency,
    #          AccountTo, order, "payin", obj.crypto_txid, False)

    obj.status = "processed"
    obj.sign_record(settings.CRYPTO_SALT)
    obj.user_accomplished = user_accomplished
    obj.save()
    notify_email(obj.user, "deposit_notify", obj)



def process(modeladmin, request, queryset):
    for obj in queryset:

        if obj.user_accomplished is None and obj.status == "processing":
            obj.status = "processed"
            obj.user_accomplished = request.user
            obj.save()
            if obj.debit_credit == "in":
                crypton_in(obj, request.user)
            else:
                pass


def crypto_cancel(obj):
    TradePair = TradePairs.objects.get(currency_on=obj.currency,
                                       currency_from=obj.currency)
    AccountTo = Accounts.objects.get(user=obj.user,
                                     currency=obj.currency)
    ##create order for them
    add_trans(AccountTo, obj.amnt, obj.currency,
              TradePair.transit_on, obj.order, "canceled",
              obj.crypto_txid, False)
    obj.order.status = "canceled"
    obj.order.save()
    obj.status = "canceled"
    obj.save()


def crypto_cancel_out(obj, reason="by admin command", comis=True):
    try:  
        Trans.objects.get(order=obj.order, status="withdraw")
    except Trans.DoesNotExist:
        print "no trans"
        obj.order.status = "canceled"
        obj.order.save()
        obj.tx_archive = reason
        obj.status = "canceled"
        obj.save()
        return    
        
    TradePair = TradePairs.objects.get(currency_on=obj.currency,
                                       currency_from=obj.currency, title__contains="IN_OUT")
    AccountTo = Accounts.objects.get(user=obj.user,
                                     currency=obj.currency)
    ##create order for them
    amnt_back  = None
    if comis:
      amnt_back = obj.amnt + obj.comission
    else:
      amnt_back = obj.amnt

    add_trans(TradePair.transit_on, amnt_back, obj.currency,
              AccountTo, obj.order, "order_cancel",
              obj.crypto_txid, False)
    obj.order.status = "canceled"
    obj.order.save()
    obj.tx_archive = reason
    obj.status = "canceled"
    obj.save()




def crypto_cancel_action(modeladmin, request, queryset):
    for obj in queryset:
        if obj.status == "processed" and obj.debit_credit == "in":
            crypto_cancel(obj)

        if obj.status == "processing" and obj.debit_credit == "out":
            crypto_cancel_out(obj)


process.short_description = u"Process"
crypto_cancel_action.short_description = u"Cancel"


class CryptoTransfersAdmin(admin.ModelAdmin):
    list_display = ['confirms', 'account', 'description', "debit_credit", 'amnt', "comission", 'currency', 'user',
                    'status', "crypto_txid", "user_accomplished", "pub_date"]
    actions = ["add", process, crypto_cancel_action]
    list_filter = ('currency', 'user', 'user_accomplished', 'status')
    search_fields = ['account', 'description', '=amnt']
    exclude = ( "user_accomplished", "status")
    fields = ('account', 'description', "debit_credit", 'amnt', 'crypto_txid', 'currency')

    def __init__(self, *args, **kwargs):
        super(CryptoTransfersAdmin, self).__init__(*args, **kwargs)
        self.list_display_links = (None, )

    ### TODO add foreign check of transactions txid        
    def save_model(self, request, obj, form, change):
        ## try to find Account and user by reference
        ###we forbid any regulation after accomplishing transaction onnly manually 
        if obj.user_accomplished is not None:
            return False

        if obj.debit_credit == "out":
            return False

        if obj.crypto_txid is None or len(obj.crypto_txid) < 64:
            return False

        Account = None
        if obj.account is not None and obj.account != "":
            Account = Accounts.objects.get(reference=obj.account)
            obj.user = Account.user

        if obj.user is not None:
            ## if we have found  Account and user by reference
            AccountTo = None

            if Account is not None:
                AccountTo = Account
            else:
                AccountTo = Accounts.objects.get(user=obj.user,
                                                 currency=obj.currency)
            ## if not by reference, but by users
            obj.ref = Account.reference
            obj.currency = Account.currency

            TradePair = TradePairs.objects.get(currency_on=obj.currency, currency_from=obj.currency)

            ##create order for them
            order = Orders(user=obj.user,
                           currency1=obj.currency,
                           currency2=obj.currency,
                           sum1_history=obj.amnt,
                           sum2_history=obj.amnt,
                           price=obj.amnt,
                           sum1=obj.amnt,
                           sum2=obj.amnt,
                           transit_1=TradePair.transit_on,
                           transit_2=AccountTo,
                           trade_pair=TradePair,
                           status="created"
            )
            order.save()
            add_trans(TradePair.transit_on, obj.amnt, obj.currency, AccountTo, order, "payin", obj.ref, False)
            obj.order = order
            order.status = "processed"
            order.save()
            obj.user_accomplished = request.user
            obj.status = "processed"
            obj.save()

            return True

            ##if we have a transaction accomplishing
            
class CryptoRawTrans(models.Model):
    crypto_txid = models.CharField(max_length=255, blank=True, null=True)
    tx_archive = models.TextField(blank=True, null=True)
    block_height = models.IntegerField( default=0)
    pub_date = models.DateTimeField(default=datetime.now)
 
class CryptoTransfers2(models.Model):
    account = models.CharField(max_length=255, verbose_name=u"Счет")
    description = models.CharField(max_length=255, verbose_name=u"Описание", blank=True)
    payment_id = models.CharField(max_length=255, verbose_name=u"Payment Id", blank=True)
    currency = models.ForeignKey("Currency", verbose_name=u"Валюта", related_name="currency_2")
    amnt = models.DecimalField(max_digits=18, decimal_places=10, verbose_name=u"Сумма")
    user = models.ForeignKey(User, verbose_name=u"Клиент", related_name="user_crypto_requested2")
    comis_tid = models.ForeignKey(Trans, verbose_name=u"Транзакция комиссии", related_name="trans_comis_trans2")
    user_accomplished = models.ForeignKey(User, verbose_name=u"Оператор проводки",
                                          related_name="operator_crypto_processed2",
                                          blank=True, null=True)
    confirms = models.IntegerField(verbose_name=u" Подтверждения", default=0)
    pub_date = models.DateTimeField(default=datetime.now,
                                    verbose_name=u"Дата")
    status = models.CharField(max_length=40,
                              choices=STATUS_ORDER,
                              default='created')
    comission = models.DecimalField(max_digits=18,
                                    decimal_places=10,
                                    verbose_name=u"комиссия",
                                    editable=False)
    confirm_key = models.CharField(max_length=255, editable=False, blank=True, null=True)
    crypto_txid = models.CharField(max_length=255, blank=True, null=True)

    debit_credit = models.CharField(max_length=40,
                                    choices=DEBIT_CREDIT,
                                    default='in')

    tx_archive = models.TextField(blank=True, null=True)
    tx_checking = models.CharField(max_length=255, default='')

    order = models.ForeignKey(
        "Orders", verbose_name=u"Ордер",
        editable=False,
        null=True,
        blank=True)



class CryptoTransfers(models.Model):
    account = models.CharField(max_length=255, verbose_name=u"Счет")
    description = models.CharField(max_length=255, verbose_name=u"Описание", blank=True)
    payment_id = models.CharField(max_length=255, verbose_name=u"Payment Id", blank=True)
    currency = models.ForeignKey("Currency", verbose_name=u"Валюта")
    amnt = models.DecimalField(max_digits=18, decimal_places=10, verbose_name=u"Сумма")
    user = models.ForeignKey(User, verbose_name=u"Клиент", related_name="user_crypto_requested")
    comis_tid = models.ForeignKey(Trans, verbose_name=u"Транзакция комиссии", related_name="trans_comis_trans")
    user_accomplished = models.ForeignKey(User, verbose_name=u"Оператор проводки",
                                          related_name="operator_crypto_processed",
                                          blank=True, null=True)
    confirms = models.IntegerField(verbose_name=u" Подтверждения", default=0)
    pub_date = models.DateTimeField(default=datetime.now,
                                    verbose_name=u"Дата")
    status = models.CharField(max_length=40,
                              choices=STATUS_ORDER,
                              default='created')
    comission = models.DecimalField(max_digits=18,
                                    decimal_places=10,
                                    verbose_name=u"комиссия",
                                    editable=False)
    confirm_key = models.CharField(max_length=255, editable=False, blank=True, null=True)
    crypto_txid = models.CharField(max_length=255, blank=True, null=True)
    tx_archive = models.TextField(blank=True, null=True)

    order = models.ForeignKey(
        "Orders", verbose_name=u"Ордер",
        editable=False,
        null=True,
        blank=True)

    sign = models.CharField(verbose_name=u"подпись клиента", max_length=255, null=False)

    def salt_fields(self):
        return ('account', 'debit_credit', 'currency', 'amnt', 'status',
                'user_id', 'confirm_key', 'confirms', 'crypto_txid')

    def verify(self, key):
        Fields = self.salt_fields()
        StableData = ",".join([str(getattr(self, field)) for field in Fields])

      
        if self.order.public_key == "web":
          if generate_key_from2(StableData, key + settings.SIGN_SALT) == self.sign:
              return True
          else:
              return False

        else:
              apikey = None
              try:
                 apikey = ApiKeys.objects.get(public_key=self.order.public_key, channel="withdraw")  
              except ApiKeys.DoesNotExist:
                 return False

              f = main.http_common.convert2time(self.pub_date)
              key = getcode(apikey.private_key, f)
              if key == self.sign:
                 return True
              else:
                 return False

              
              

        return False

    def salt_repr(self):
        return ",".join([str(getattr(self, field.name)) for field in self._meta.local_fields])

    def save_model(self, request, obj, form, change):
        checksum(self)
        super(CryptoTransfers, self).save(request, obj, form, change)


    def sign_record(self, key):
        Fields = self.salt_fields()
        StableSalt = ",".join([str(getattr(self, field)) for field in Fields])
        self.sign = generate_key_from2(StableSalt, key + settings.SIGN_SALT)


    debit_credit = models.CharField(max_length=40,
                                    choices=DEBIT_CREDIT,
                                    default='in')

    class Meta:
        verbose_name = u'Перевод криптовалюты'
        verbose_name_plural = u'Переводы криптовалюты'

    ordering = ('id',)

    def __unicode__(o):
        return str(o.id) + " " + str(o.amnt) + " " + o.currency.title

def change_volitile_const(Name, Value):
    try:
        d = VolatileConsts.objects.get(Name=Name)
        d.Value = Value
        d.save()
    except:
         VolatileConsts(Name=Name, Value=Value).save()

    



def process_wallet_tx(Trans, OwnAccounts, OwnAccountsBCH):
                          CurrencyInstance = 2 # for BTC                
                          for output in Trans.outputs :
                            if OwnAccounts.has_key( output.address):
                               if is_out(Trans.inputs, OwnAccounts ):
                                   break
                               else:
                                    mistake_bch = "normal trans"
                                    if OwnAccountsBCH.has_key( output.address):
                                       mistake_bch = "mistake bch trans"
                                       print "seems it's mistake transaction to BCH chain"

                                    Decimal = sato2Dec(output.value)
                                    try :
                                            print "process %s" % Trans.hash
                                            TransObj = CryptoTransfers.objects.get(crypto_txid = Trans.hash)
                                            print "trans %s %s is existed to %s  amnt %s %i"  % (TransObj.account, TransObj.crypto_txid,
                                                                                                 TransObj.user_id, TransObj.amnt, TransObj.id)
                                            if TransObj.account != output.address:
                                                suffix = output.address[-5:]
                                                FixCryptoTxid = Trans.hash + "_" + suffix
                                                print "but it's another adress %s add trans with suffix %s" % (output.address, FixCryptoTxid)
                                                try:

                                                   TransObj = CryptoTransfers.objects.get(crypto_txid = FixCryptoTxid)
                                                   print "we have been there before"
                                                   continue
                                                except CryptoTransfers.DoesNotExist:

                                                        TransObj =  CryptoTransfers(crypto_txid = FixCryptoTxid,
                                                                    status="processing2",
                                                                    amnt = Decimal,
                                                                    currency_id = CurrencyInstance ,
                                                                    account = output.address,
                                                                    user_id = OwnAccounts[ output.address ],
                                                                    confirms = 0,
                                                                    description = mistake_bch
                                                                    )
                                                        TransObj.save()
                                                        continue
                                    except  CryptoTransfers.DoesNotExist:
                                            print "trans %s  to save  %s  amnt %s" % (Trans.hash, output.address, Decimal)


                                            TransObj =  CryptoTransfers(crypto_txid = Trans.hash,
                                                                    status="processing",
                                                                    amnt = Decimal,
                                                                    currency_id = CurrencyInstance ,
                                                                    account = output.address,
                                                                    user_id = OwnAccounts[ output.address ],
                                                                    confirms = 0,
                                                                    description = mistake_bch
                                                                    )
                                            TransObj.save()
                                            continue

 
