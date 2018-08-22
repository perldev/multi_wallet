from main.models import Accounts, AccountsAdmin
from main.models import Trans, TransAdmin
from main.models import Orders, OrdersAdmin
from main.models import CryptoTransfers, CryptoTransfersAdmin
from main.models import VolatileConsts

from django.contrib import admin



from main.models import CurrencyAdmin, Currency



admin.site.disable_action('delete_selected')




admin.site.register(Currency, CurrencyAdmin)


admin.site.register(VolatileConsts)




admin.site.register(CryptoTransfers, CryptoTransfersAdmin)


admin.site.register(Accounts, AccountsAdmin)

admin.site.register(Trans, TransAdmin)

admin.site.register(Orders, OrdersAdmin)

