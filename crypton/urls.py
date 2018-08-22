from django.conf.urls import patterns, include, url


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from crypton import settings
#from django.contrib.staticfiles import views


urlpatterns = patterns('',
    # Examples:
    url(r'^stop', 'main.api.stop', name='stop'),
    url(r'^reload', 'main.api.reload', name='reload'),
    url(r'^suspend', 'main.api.suspend', name='suspend'),
    url(r'^start', 'main.api.start', name='start'),
    url(r'^logout$', 'main.views.try_logout', name='try_logout'),
    url(r'^$', 'main.views.login_page', name='login_page'),
    url(r'^login_page$', 'main.views.login_page', name='login_page'),
    url(r'^login$', 'main.views.try_login', name='try_login'),
    
    url(r'^finance/crypto_currency/([\w\.]+)',
         'main.finance.crypto_currency_get_account',
         name='crypto_currency_get_account'),
    url(r'^finance/depmotion/([\w]+)', 'main.finance.depmotion', name='depmotion'),
    url(r'^finance/depmotion', 'main.finance.depmotion_home', name='depmotion_home'),
    url(r'^finance',
         'main.finance.home',
         name='home'),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT,} ),
    url(r'^admin/', include(admin.site.urls)),

)

    

