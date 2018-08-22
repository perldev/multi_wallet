"use strict";var wayforpay=0;var finance={crypto_currency:{NVC:1,BTC:1,LTC:1,HIRO:1,DRK:1,VTC:1,PPC:1,DOGE:1,CLR:1,RMS:1},order_id:"",min_deal:0.00001,timer:null,liqpay_flag:false,p24_flag:false,ui_check_status:function(){$.ajax({dataType:"json",url:"/api/order/status/"+finance.order_id,type:"GET",cache:false,error:function(a){console.log(a);my_alert("Не могу создать ордер  ")},success:function(b){var a=b.status;if(a=="processed"){$("#work_msg").html("<p>Средства удачно зачислены</p>");window.location.href="/finance/balance";clearTimeout(finance.timer);return}if(a=="created"){$("#work_msg").html('Cтатус платежа <font color="greed" id="depo_status">                                                                                в обработке </font>');return}if(a=="processing"){$("#work_msg").html('Cтатус платежа <font color="greed" id="depo_status">                                                                                в обработке </font>');return}if(a=="wait_secure"){$("#work_msg").html("<p>Ваша оплата была отправленна платежной системой на ручную обработку</p>                                                                                <p>После проверки, ваши средства будут немедленно зачисленны</p>");clearTimeout(finance.timer);return}if(a=="order_cancel"){clearTimeout(finance.timer);$("#work_msg").html("Ваша оплата была забракована платежной системой");return}$("#work_msg").html("Что-то пошло не так, обратитесь в службу поддержки");clearTimeout(finance.timer);return}})},make_deposit:function(a){$("#withdraw_form").css({display:"none"});window.scrollTo(0,0);$("#currency_depo").val(a);finance.fill_providers_depo(a);$("#deposit_form").slideDown("slow")},fill_providers_depo:function(a){$("#provider_depo").html("");$("#res_provider").html("");if(a=="UAH"){$("#provider_depo").append($('<option value="">Выбрать</option>'));$("#provider_depo").append($('<option value="way4pay">Картой 2.2% Visa,MasterCard Украины </option>'));$("#provider_depo").append($('<option value="p24_transfer">Через Приват24( 2% ) </option>'));$("#label_depo").html("Cпособ пополения:");$("#label_amnt_depo").show();$("#amnt_depo").show();$("#provider_depo").show()}if(finance.crypto_currency[a]){$("#provider_depo").hide();$("#label_depo").html("Кошелек пополения:");$("#label_amnt_depo").hide();$("#amnt_depo").hide();$.ajax({url:"/finance/crypto_currency/"+a,type:"GET",dataType:"json",cache:false,error:function(b){$("#res_provider").html("permission denied");my_alert("Проблемы в работе с кошельком обратитесь в support@btc-trade.com.ua");$("#provider_depo").val("");return false},success:function(b){if(b.account){$("#res_provider").html('<div class="col-sm-6"><strong>'+b.account+"</strong></div>")}}})}},change_depo:function(c){var d=c.value;if(d==""){return}var a=$("#currency_depo").val();var b=$("#amnt_depo").val();if(d=="way4pay"){return finance.way4pay_start(c,b,a)}if(d=="liqpay_transfer"){return finance.liqpay_transfer(c,b,a)}if(d=="p24_transfer"){return finance.p24_transfer(c,b,a)}},way4pay_start:function(){if(wayforpay==0){wayforpay=new Wayforpay()}var c=$("#currency_depo").val();var e=$("#amnt_depo").val();var d=$("#name_depo").val();var f=$("#lastname_depo").val();var b=$("#phone_depo").val();if(d.length<2||f.length<2||b.length<2){$("#provider_depo").val("");my_alert("Пожайлуста заполните авторизационные данные ФИО,телефон");return false}if(c!="UAH"){$("#provider_depo").val("");my_alert("Неправильная валюта");return false}if(e<10){$("#provider_depo").val("");my_alert("Ограничение минимальной суммы пополнения через Way4Pay, больше 100 ГРН");return false}$("#deposit_form").css({display:"none"});var a=$.ajax({url:"/finance/way4pay/start",type:"POST",data:{amount:e,lastname:f,name:d,phone:b},dataType:"json",cache:false,error:function(g){$("#res_provider").html("permission denied");$("#provider_depo").val("");return false},success:function(g){if(g.order_id){wayforpay.run({merchantAccount:g.public_key,merchantDomainName:g.host,authorizationType:"SimpleSignature",merchantSignature:g.sign,orderReference:g.order_id,orderDate:g.date,amount:g.amnt,currency:"UAH",productName:g.product_name,productPrice:g.price,productCount:g.count,clientFirstName:g.name,clientLastName:g.last_name,clientEmail:g.email,clientPhone:g.phone,serviceUrl:g.url,returnUrl:g.returnUrl},function(h){cosole.log(h);my_alert("Ваша оплата прошла успешно, в течении 15 минут деньги будут у вас на балансе")},function(h){cosole.log(h);my_alert("Ваша оплата отклонена")},function(h){my_alert("Ваша оплата выпала на ручную обработку");cosole.log(h)})}}})},p24_start:function(){var b=$("#currency_depo").val();var c=$("#amnt_depo").val();if(b!="UAH"){$("#provider_depo").val("");my_alert("Неправильная валюта");return false}if(c<100){$("#provider_depo").val("");my_alert("Ограничение минимальной суммы пополнения через Приват24, больше 100 ГРН");return false}var a=$.ajax({url:"/finance/p24/start/"+c,type:"GET",dataType:"json",cache:false,error:function(d){$("#res_provider").html("permission denied");$("#provider_depo").val("");return false},success:function(d){if(d.order_id){$("#p24_public_key").val(d.public_key);$("#p24_order_id").val(d.order_id);$("#p24_ext_details").val(d.ext_details);$("#p24_amt").val(d.amount);$("#p24_ccy").val(d.currency);$("#p24_description").val(d.description);$("#p24_return_url").val(d.result_url);$("#p24_server_url").val(d.server_url);$("#p24_type").val(d.type);$("#p24_signature").val(d.signature);finance.p24_flag=true;$("#pay_p24_form").submit()}}})},liqpay_start:function(){var b=$("#currency_depo").val();var c=$("#amnt_depo").val();if(b!="UAH"){$("#provider_depo").val("");my_alert("Неправильная валюта");return false}if(c<100){$("#provider_depo").val("");my_alert("Ограничение минимальной суммы пополнения через liqpay, больше 100 ГРН");return false}var a=$.ajax({url:"/finance/liqpay/start/"+c,type:"GET",dataType:"json",cache:false,error:function(d){$("#res_provider").html("permission denied");$("#provider_depo").val("");return false},success:function(d){if(d.order_id){$("#liqpay_public_key").val(d.public_key);$("#liqpay_order_id").val(d.order_id);$("#liqpay_amount").val(d.amount);$("#liqpay_currency").val(d.currency);$("#liqpay_description").val(d.description);$("#liqpay_result_url").val(d.result_url);$("#liqpay_server_url").val(d.server_url);$("#liqpay_type").val(d.type);$("#liqpay_signature").val(d.signature);$("#liqpay_language").val(d.language);$("#liqpay_sandbox").val("1");finance.liqpay_flag=true;$("#pay_liqpay_form").submit()}}})},p24_transfer:function(d,b,c){if(c!="UAH"){d.value="";my_alert("Неправильная валюта");return false}if(b<100){d.value="";my_alert("Ограничение минимальной суммы пополнения через Приват24, больше 100 ГРН");return false}var a=$.ajax({url:"/finance/p24/deposit/"+b,type:"GET",cache:false,error:function(e){$("#res_provider").html("permission denied");d.value=""},success:function(f){var e='<p class="help-block">Комиссия за пополнение составляет 2% с карты ПриватБанка, 2% + 10 грн с карт других банков</p>';$("#res_provider").html(e+f);$("#pay_p24_form").bind("submit",function(){return finance.p24_flag});$("#p24_submit_button").bind("click",finance.p24_start)}})},liqpay_transfer:function(d,b,c){if(c!="UAH"){d.value="";my_alert("Неправильная валюта");return false}if(b<100){d.value="";my_alert("Ограничение минимальной суммы пополнения через liqpay, больше 100 ГРН");return false}var a=$.ajax({url:"/finance/liqpay/deposit/"+b,type:"GET",cache:false,error:function(e){$("#res_provider").html("permission denied");d.value=""},success:function(f){var e='<p class="help-block">Комиссия за пополнение составляет 2.75% с карт Visa, MasterCard</p>';e+='<p class="help-block">2.75% наличными в терминалах ПриватБанка</p>';$("#res_provider").html(e+f);$("#pay_liqpay_form").bind("submit",function(){return finance.liqpay_flag});$("#liqpay_submit_button").bind("click",finance.liqpay_start)}})},confirm_operation:function(){var b=$("#key_type").val();var a=$("#key").val();var d=$("#id_pin").val();var c={key_type:b,pin:d};thinking_alert();$.ajax({url:"/finance/common_secure_confirm?key="+a,type:"POST",data:c,error:function(e){my_alert("Авторизация не прошла")},success:function(e){hide_modal("modal_dlg");$("#home").html((e))}})},confirm_g2a_operation:function(c){var b=$("#key_type").val();var a=$("#key").val();var d={key_type:b,g2a_session:c};$.ajax({url:"/finance/common_secure_confirm?key="+a,type:"POST",data:d,error:function(e){my_alert("Авторизация не прошла")},success:function(e){$("#home").html((e))}})},bank_transfer:function(d,b,c){if(c!="UAH"){d.value="";my_alert("Неправильная валюта");return}if(b<100){d.value="";my_alert("Ограничение минимальной суммы пополнения через банковские переводы, больше 100 ГРН");return}var a=$.ajax({url:"/finance/bank_transfer/UAH/"+b,type:"GET",cache:false,error:function(e){$("#res_provider").html("permission denied");d.value=""},success:function(e){$("#res_provider").html(e)}})},withdraw:function(a){$("#deposit_form").css({display:"none"});window.scrollTo(0,0);$("#res_provider_withdraw").html("");$("#currency_withdraw").val(a);$("#withdraw_form").slideDown("slow");finance.withdraw_providers(a)},withdraw_providers:function(b){$("#provider_withdraw").html("");if(b=="UAH"){$("#provider_withdraw").show();$("#label_provider_withdraw").show();$("#provider_withdraw").append($('<option value="">Выбрать</option>'));$("#provider_withdraw").append($('<option value="card_transfer">На платежную карту (Visa,MasterCard)</option>'))}if(finance.crypto_currency[b]){$("#provider_withdraw").hide();$("#label_provider_withdraw").hide();var a=$.ajax({url:"/finance/crypto_transfer_withdraw/"+b,type:"GET",cache:false,error:function(c){$("#res_provider_withdraw").html(c)},success:function(c){$("#res_provider_withdraw").html(c);$("#ajax_form").submit(function(d){thinking_alert()})}})}},change_withdraw:function(b){var c=b.value;if(c==""){return}var a=$("#currency_withdraw").val();if(c=="bank_transfer"){return finance.bank_transfer_withdraw(b,a)}if(c=="liqpay_transfer"){return finance.liqpay_transfer_withdraw(b,a)}if(c=="card_transfer"){return finance.p2p_transfer_withdraw(b,a)}},p2p_transfer_withdraw:function(d,c){if(c!="UAH"){d.value="";my_alert("Неправильная валюта");return}var b=100;var a=$.ajax({url:"/finance/p2p_transfer_withdraw/"+c+"/"+b,type:"GET",cache:false,error:function(e){$("#res_provider_withdraw").html(e);d.value=""},success:function(e){$("#res_provider_withdraw").html(e);$("#ajax_form").submit(function(f){thinking_alert()})}})},bank_transfer_withdraw:function(d,c){if(c!="UAH"){d.value="";my_alert("Неправильная валюта");return}var b=10;var a=$.ajax({url:"/finance/bank_transfer_withdraw/"+c+"/"+b,type:"GET",cache:false,error:function(e){$("#res_provider_withdraw").html(e);d.value=""},success:function(e){$("#res_provider_withdraw").html(e)}})},liqpay_transfer_withdraw:function(d,c){if(c!="UAH"){d.value="";my_alert("Неправильная валюта");return}var b=10;var a=$.ajax({url:"/finance/liqpay_transfer_withdraw/"+c+"/"+b,type:"GET",cache:false,error:function(e){$("#res_provider_withdraw").html(e);d.value=""},success:function(e){$("#res_provider_withdraw").html(e)}})}};var Main={trade_pair:"",currency_base:"",currency_on:"",usd_uah_rate:null,timer_deals:null,chart:null,server_timeoffset:7200000+60*60*1000,first:true,calendar_loaded:false,timer_sell_list:null,timer_buy_list:null,comission:0.0005,start_stock:function(){Main.start_deals_timer();Main.start_my_orders();Main.start_sell_list();Main.start_buy_list();Main.start_user_menu();Main.start_market_prices();if(Main.currency_base=="UAH"){$("#buy_result_usd_eq").show();$("#sell_result_usd_eq").show();$("#sell_price_usd_eq").show();$("#buy_price_usd_eq").show()}Main.draw_highcharts()},format_time:function(b){var c=new Date(b*1000-Main.server_timeoffset);var a=dateFormat(c,"HH:MM:ss");return a},format_date_time:function(b){var c=new Date(b*1000-Main.server_timeoffset);var a=dateFormat(c,"dd.mm.yyyy, HH:MM:ss");return a},format_date:function(b){return b;var c=new Date(b*1000-Main.server_timeoffset);var a=dateFormat(c,"dd.mm.yyyy, HH:MM:ss");return a},start_time:function(){if(Main.first){$("#simple_form").submit(function(a){thinking_alert()});Main.first=false}Main.server_time(function(){setTimeout(Main.start_time,7000)})},val_eq_to_usd:function(c,b){if(Main.currency_base=="UAH"){var a=Main.format_float4(c/Main.usd_uah_rate);$("#"+b).html(a+"&nbsp;<strong>USD</strong>")}},eq_to_usd:function(c,b){if(Main.currency_base=="UAH"){var a=Main.format_float4(c.value/Main.usd_uah_rate);$("#"+b).html(a+"&nbsp;<strong>USD</strong>")}},server_time:function(a){$.ajax({dataType:"json",url:"/time",type:"GET",cache:false,error:function(b){console.log(b);a()},success:function(b){Login.use_f2a=b.use_f2a;Login.sessionid=b.sessionid;Login.logged=b.logged;Main.usd_uah_rate=b.usd_uah_rate;$("#server_time").html(Main.format_date_time(b.time));$("#client_comis").html(b.deal_comission);a()}})},own_deals:function(b){var a="";if(!Main.calendar_loaded){$("#date_deals_comp").removeClass("hidden");$("#date_deals").datepicker({format:"dd-mm-yyyy"}).on("changeDate",function(c){$("#date_deals").datepicker("hide");Main.own_deals()});$("#date_deals").datepicker("hide");a="";Main.calendar_loaded=true}else{a=$("#date_deals").val()}thinking_alert();$.ajax({dataType:"json",url:"/api/my_deals/"+Main.trade_pair+"?ts="+a,type:"GET",cache:false,error:function(c){hide_modal("modal_dlg");if(b){b(c)}},success:function(f){var e=f.length;hide_modal("modal_dlg");$("#trade_deals").html("");var g=0;var c=0;var j=0;for(var d=0;d<e;d++){var h="<tr>";h+="<td>"+Main.format_date(f[d]["pub_date"])+"</td>";h+="<td><a href='/profile/"+f[d]["user"]+"'>"+f[d]["user"]+"</a></td>";if(f[d]["type"]=="buy"){h+="<td style='color:green'>"+f[d]["type"]+"</td>";c+=f[d]["amnt_trade"]*1}else{h+="<td style='color:red'>"+f[d]["type"]+"</td>";j+=f[d]["amnt_trade"]*1}h+="<td>"+f[d]["price"]+"&nbsp;<strong>"+Main.currency_base+"</strong></td>";h+="<td>"+f[d]["amnt_base"]+"</td>";h+="<td>"+f[d]["amnt_trade"]+"</td></tr>";g+=f[d]["price"]*1;$("#trade_deals").append(h)}g/=e;$("#avarage_rate").html(Main.format_float4(g));$("#sum_buy").html(Main.format_float4(c));$("#sum_sell").html(Main.format_float4(j));if(b){b(f)}}})},market_prices:function(a){$.ajax({dataType:"json",url:"/api/market_prices",type:"GET",cache:false,error:function(b){console.log(b);a()},success:function(d){var c=d.prices.length;var f=d.prices;for(var b=0;b<c;b++){var e=f[b];$("#"+e.type).html(e.price)}a()}})},user_menu:function(a){if(!Login.logged){return a()}$.ajax({dataType:"json",url:"/api/balance",type:"GET",cache:false,error:function(b){console.log(b);a();return},success:function(d){var c=d.accounts.length;var f=d.accounts;for(var b=0;b<c;b++){var e=f[b];$("#balance_"+e.currency).html(Main.format_float6(e.balance))}Login.use_f2a=d.use_f2a;$("#notify_count").html("("+d.notify_count+")");$("#msg_count").html("("+d.msg_count+")");a()}})},create_msg:function(a){$("#msgs").hide();$("#msg_form").slideDown();$("#whom").val(a)},send_msg:function(){var a={whom:$("#whom").val(),msg:$("#msg").val()};$.ajax({url:"/msgs/create",type:"POST",data:a,cache:false,error:function(b){my_alert(b)},success:function(b){if(b.status){window.location.href="/msgs/out"}else{my_alert(b.description)}}})},cancel_msg:function(){$("#msgs").show("fast");$("#msg_form").hide("fast");$("#whom").val("")},notify_remove:function(a){$.ajax({dataType:"json",url:"/msgs/hide/"+a,type:"GET",cache:false,error:function(b){console.log(b)},success:function(b){if(b.status){$("#notify_"+a).hide()}else{my_alert("something wrong try later")}}})},start_market_prices:function(){console.log("market");Main.market_prices(function(){setTimeout(Main.start_market_prices,20000)})},start_user_menu:function(){console.log("balance");Main.user_menu(function(){setTimeout(Main.start_user_menu,10000)})},sell_list:function(a){$.ajax({dataType:"json",url:"/api/trades/sell/"+Main.trade_pair,type:"GET",cache:false,error:function(b){console.log(b)},success:function(f){var e=f.list.length;$("#sell_orders_list").html("");var d=f.list;$("#sell_orders_sum").html(f.orders_sum);var j=Main.format_float6(f.min_price);$("#buy_min_price").html(j);var b=$("#buy_price").val();if(!b){$("#buy_price").val(j);Main.val_eq_to_usd(j,"buy_price_usd_eq")}for(var c=0;c<e;c++){var h=Main.format_float4(d[c]["price"]/Main.usd_uah_rate);var g="<tr class='cursor' onclick='Main.order2this_buy(this,"+d[c]["price"]+","+d[c]["currency_trade"]+" )'>";g+="<td>"+Main.format_float6(d[c]["price"])+"&nbsp;<strong>"+Main.currency_base+"</strong>";g+="&nbsp;<small>("+h+"&#36;</small>)</td>";g+="<td >"+Main.format_float6(d[c]["currency_trade"])+"</td>";g+="<td>"+Main.format_float6(d[c]["currency_base"])+"</td></tr>";$("#sell_orders_list").append(g)}a()}})},order2this_sell:function(f,c,b){c=c*1-1e-8;var e="#sell_count";var a="#sell_price";$(a).val(c);if(Login.logged){var d=$("#balance_"+Main.currency_on).html();if(d>b){$(e).val(b)}else{$(e).val(d)}}else{$(e).val(b)}Main.calc_order("sell")},order2this_buy:function(f,c,b){c=c*1+1e-8;var e="#buy_count";var a="#buy_price";$(a).val(c);if(Login.logged){var d=$("#balance_"+Main.currency_base).html();if(d/c>b){$(e).val(b)}else{$(e).val(Main.format_float8(d/c))}}else{$(e).val(b)}Main.calc_order("buy")},buy_list:function(a){$.ajax({dataType:"json",url:"/api/trades/buy/"+Main.trade_pair,type:"GET",cache:false,error:function(b){console.log(b);a()},success:function(e){var d=e.list.length;$("#buy_orders_list").html("");var c=e.list;$("#buy_orders_sum").html(e.orders_sum);var j=Main.format_float6(e.max_price);$("#sell_max_price").html(j);var h=$("#sell_price").val();if(!h){$("#sell_price").val(j);Main.val_eq_to_usd(j,"sell_price_usd_eq")}for(var b=0;b<d;b++){var g=Main.format_float4(c[b]["price"]/Main.usd_uah_rate);var f="<tr class='cursor' onclick='Main.order2this_sell(this,"+c[b]["price"]+","+c[b]["currency_trade"]+" )'>";f+="<td>"+Main.format_float6(c[b]["price"])+"&nbsp;<strong>"+Main.currency_base+"</strong>&nbsp;<small>("+g+"&#36;</small>)</td>";f+="<td>"+Main.format_float6(c[b]["currency_trade"])+"</td>";f+="<td>"+Main.format_float6(c[b]["currency_base"])+"</td></tr>";$("#buy_orders_list").append(f)}a()}})},start_my_orders:function(){Main.my_orders(function(){console.log("call my orders");setTimeout(Main.start_my_orders,10000)})},start_sell_list:function(){Main.sell_list(function(){console.log("sell list ");setTimeout(Main.start_sell_list,12600)})},start_buy_list:function(){Main.buy_list(function(){console.log("buy list ");setTimeout(Main.start_buy_list,13400)})},my_orders:function(b){if(!Login.logged){return b()}var a=$.ajax({url:"/api/my_orders/"+Main.trade_pair,type:"GET",dataType:"json",cache:false,error:function(c){console.log(c);b()},success:function(f){if(f.auth){var e=f.your_open_orders.length;$("#your_open_orders").html("");var d=f.your_open_orders;$("#your_balance_currency1").html(f.balance_buy);$("#your_balance_currency").html(f.balance_sell);for(var c=0;c<e;c++){var g='<tr id="my_order_'+d[c]["id"]+'"><td>'+d[c]["id"]+"</td>";g+="<td>"+d[c]["pub_date"]+"</td>";g+="<td>"+d[c]["type"]+"</td>";g+="<td>"+Main.format_float6(d[c]["price"])+"&nbsp;<strong>"+Main.currency_base+"</strong></td>";g+="<td>"+Main.format_float6(d[c]["amnt_base"])+"</td>";g+="<td>"+Main.format_float6(d[c]["amnt_trade"])+"</td>";g+="<td> <span onclick=\"Main.remove('"+d[c]["id"]+'\')" class="btn btn-primary btn-xs">Cancel</span></td></tr>';$("#your_open_orders").append(g)}}b()}})},remove:function(b){var a="#my_order_"+b;$(a).hide();$.ajax({dataType:"json",url:"/api/remove/order/"+b,type:"GET",cache:false,error:function(c){my_alert("Не могу удалить ордер  ");$(a).show()},success:function(c){if(c.status){$(a).hide()}else{my_alert(c.description)}}})},deals_list:function(a){$.ajax({dataType:"json",url:"/api/deals/"+Main.trade_pair,type:"GET",cache:false,error:function(b){console.log(b);a()},success:function(d){var c=d.length;$("#trade_deals").html("");for(var b=0;b<c;b++){var e="<tr>";e+="<td>"+Main.format_date(d[b]["pub_date"])+"</td>";e+="<td><a href='/profile/"+d[b]["user"]+"'>"+d[b]["user"]+"</a></td>";if(d[b]["type"]=="buy"){e+="<td style='color:green'>"+d[b]["type"]+"</td>"}else{e+="<td style='color:red'>"+d[b]["type"]+"</td>"}e+="<td>"+Main.format_float4(d[b]["price"])+"&nbsp;<strong>"+Main.currency_base+"</strong></td>";e+="<td>"+Main.format_float4(d[b]["amnt_base"])+"</td>";e+="<td>"+Main.format_float4(d[b]["amnt_trade"])+"</td></tr>";$("#trade_deals").append(e)}a()}})},start_deals_timer:function(){Main.deals_list(function(){console.log("deal list ");setTimeout(Main.start_deals_timer,4500)})},make_order:function(c,d){var b=$("#buy_price").val();var a=$("#buy_count").val();var e={count:a,price:b,currency1:d,currency:c};$.ajax({url:"/api/buy/"+Main.trade_pair,type:"POST",data:e,dataType:"json",success:function(f){if(f.status==true){my_alert(f.description);$("#buy_count").val("0");$("#buy_help").html("Нажмите посчитать, чтобы рассчитать сумму в соответствии с ордерами.");return}if(f.status=="process_order_error"){my_alert(f.description);return}if(f.status=="incifition_funds"){my_alert(f.description);return}if(f.status=="processed"){my_alert(f.description);$("#buy_count").val("0");$("#buy_help").html("Нажмите посчитать, чтобы рассчитать сумму в соответствии с ордерами.");return}if(f.status=="part_processed"){my_alert(f.description);$("#buy_count").val("0");$("#buy_help").html("Нажмите посчитать, чтобы рассчитать сумму в соответствии с ордерами.");return}my_alert("Не могу создать ордер, проверьте пожайлуста данный и попробуйте снова")}})},make_order_sell:function(c,d){var b=$("#sell_price").val();var a=$("#sell_count").val();var e={count:a,price:b,currency1:d,currency:c};$.ajax({url:"/api/sell/"+Main.trade_pair,type:"POST",data:e,dataType:"json",success:function(f){if(f.status==true){my_alert(f.description);$("#sell_count").val("0");$("#sell_help").html("Нажмите посчитать, чтобы рассчитать сумму в соответствии с ордерами.");return}if(f.status=="incifition_funds"){my_alert(f.description);return}if(f.status=="processed"){my_alert(f.description);$("#sell_count").val("0");$("#sell_help").html("Нажмите посчитать, чтобы рассчитать сумму в соответствии с ордерами.");return}if(f.status=="part_processed"){my_alert(f.description);$("#sell_count").val("0");$("#sell_help").html("Нажмите посчитать, чтобы рассчитать сумму в соответствии с ордерами.");return}my_alert("Не могу создать ордер, проверьте пожайлуста данный и попробуйте снова")}})},calc_order:function(d){var g="#"+d+"_count";var c="#"+d+"_price";var f="#"+d+"_result";var a="#"+d+"_comission";var b=$(g).val();var e=$(c).val();if(b<Main.min_deal){if(d=="buy"){$("#buy_help").html("К сожелению сумма сделки меньше минимальной возможной")}else{$("#sell_help").html("К сожелению сумма сделки меньше минимальной возможной")}return}var h=e*b;$(f).html(Main.format_float8(h));Main.val_eq_to_usd(h,d+"_result_usd_eq");if(d=="buy"){var i=b*Main.comission;$(a).html(Main.format_float8(i));$("#buy_help").html("Вы получаете  "+Main.format_float8(b-i)+" "+Main.currency_on)}else{var i=h*Main.comission;$(a).html(Main.format_float8(i));$("#sell_help").html("Вы получаете  "+Main.format_float8(h-i)+" "+Main.currency_base)}},calc_straight:function(a){var b=a.innerHTML;$("#sell_count").val(b)},calc_over:function(b){var c=b.innerHTML;console.log("calculate "+c);var a=$("#buy_price").val();$("#buy_count").val(Main.format_float8(c/a))},format_float6:function(b){if(b<0.001){return Main.format_float8(b)}var a=b*1000000;return Math.floor(a)/1000000},format_float4:function(b){if(b<0.01){return Main.format_float6(b)}var a=b*1000;return Math.floor(a)/1000},format_float8:function(b){if(b<0.00001){return Main.format_float12(b)}var a=b*1000000;return Math.floor(a)/1000000},format_float12:function(b){return b;var a=b*10000000000;return Math.floor(a)/10000000000+""},drawVisualization:function(){var b=screen.width;var c={1280:800,1600:945,1360:800,1920:1038};var a=c[b];if(!a){a=800}$.ajax({url:"/api/japan_stat/"+Main.trade_pair,type:"GET",dataType:"json",success:function(e){console.log(e.trades);var g=google.visualization.arrayToDataTable(e.trades,true);$("#online_users").html(e.online);$("#volume_base").html(e.volume_base);$("#volume_trade").html(e.volume_trade);var d={legend:"none",width:a,height:250,fontSize:10,chartArea:{width:a-200,height:150},colors:["#515151","#515151"],candlestick:{fallingColor:{fill:"#0ab92b",stroke:"green",strokeWidth:1},risingColor:{fill:"#f01717",stroke:"#d91e1e",strokeWidth:1},hollowIsRising:true},hAxis:{maxValue:100},series:{0:{type:"candlesticks"},1:{type:"bars",targetAxisIndex:1,color:"#ebebeb"}},};var f=new google.visualization.CandlestickChart(document.getElementById("chart_trade"));f.draw(g,d)}})},draw_highcharts:function(){var b=screen.width;var c={};var a=c[b];console.log("screen with"+b);a=b*0.6391;$("#chart_trade").css({width:a});$.ajax({url:"/api/japan_stat/high/"+Main.trade_pair+"?_"+Date(),type:"GET",dataType:"json",success:highchart_candle})},highcharts_thema_enable:function(){if(Main.highcharts_enabled){return true}Highcharts.createElement("link",{href:"https://fonts.googleapis.com/css?family=Signika:400,700",rel:"stylesheet",type:"text/css"},null,document.getElementsByTagName("head")[0]);Highcharts.wrap(Highcharts.Chart.prototype,"getContainer",function(a){a.call(this);this.container.style.background="url(https://btc-trade.com.ua/img/sand.png)"});Highcharts.theme={colors:["gray","#8085e9","#8d4654","#7798BF","#aaeeee","#ff0066","#eeaaee","#55BF3B","#DF5353","#7798BF","#aaeeee"],chart:{backgroundColor:null,style:{fontFamily:"Signika, serif"}},title:{style:{color:"black",fontSize:"16px",fontWeight:"bold"}},subtitle:{style:{color:"black"}},tooltip:{borderWidth:0},legend:{itemStyle:{fontWeight:"bold",fontSize:"13px"}},xAxis:{labels:{style:{color:"#6e6e70"}}},yAxis:{labels:{style:{color:"#6e6e70"}}},plotOptions:{series:{shadow:true},candlestick:{lineColor:"#404048",color:"#f01717",upColor:"#43ac6a"},map:{shadow:false}},navigator:{xAxis:{gridLineColor:"#D0D0D8"}},rangeSelector:{buttonTheme:{fill:"white",stroke:"#C0C0C8","stroke-width":1,states:{select:{fill:"#D0D0D8"}}}},scrollbar:{trackBorderColor:"#C0C0C8"},background2:"#E0E0E8"};Highcharts.setOptions(Highcharts.theme);Highcharts.setOptions({global:{useUTC:false},lang:{loading:"Загружаем",months:["Январь","Февраль","Март","Апрель","Май","Июнь","Июдь","Авгут","Сентябрь","Октябрь","Ноябрь","Декабрь"],weekdays:["Воскресенье","Понедельник","Вторник","Среда","Четверг","Пятьница","Суббота"],shortMonths:["Янв","Фев","Мар","Апр","Май","Июн","Июль","Авг","Сент","Окт","Ноя","Дек"],exportButtonTitle:"Экспортировать",printButtonTitle:"Печать",rangeSelectorFrom:"С",rangeSelectorTo:"По",rangeSelectorZoom:"Период",downloadPNG:"Скачать в  PNG",downloadJPEG:"Скачать в  JPEG",downloadPDF:"Скачать PDF",downloadSVG:"Скачать SVG"}});Main.highcharts_enabled=true},confirm_operation_privatkey:function(){var b=$("#key_type").val();var a=$("#key").val();var d=$("#id_pin").val();var c={key:a,key_type:b,pin:d};$.ajax({url:"/profile/private_key",type:"POST",data:c,error:function(e){my_alert("Авторизация не прошла")},success:function(e){$("#home").html((e))}})},confirm_g2a_privatkey:function(c){var b=$("#key_type").val();var a=$("#key").val();var d={key:a,key_type:b,g2a_session:c};$.ajax({url:"/profile/private_key",type:"POST",data:d,error:function(e){my_alert("Авторизация не прошла")},success:function(e){$("#home").html((e))}})}};var Stock={current_index:null,btce_serias_ask:null,btce_serias_bid:null,btce_serias_vol:null,sel_button:null,foreign_stock_name:null,foreign_stock:function(a,c,b){if(a=="btc_e"&&c=="btc_uah"){$("#chart_trade").highcharts().destroy();$("#stocks_trades .current_stock").removeClass("btn-success").removeClass("current_stock").addClass("btn-default");$(b).addClass("btn-success").addClass("current_stock");Stock.draw_btce_stock("btc_usd");return}if(a=="btc_e"&&c=="ltc_uah"){$("#chart_trade").highcharts().destroy();$("#stocks_trades .current_stock").removeClass("btn-success").removeClass("current_stock").addClass("btn-default");$(b).addClass("btn-success").addClass("current_stock");Stock.draw_btce_stock("ltc_usd");return}if(a=="btc_e"&&c=="nvc_uah"){$("#chart_trade").highcharts().destroy();$("#stocks_trades .current_stock").removeClass("btn-success").removeClass("current_stock").addClass("btn-default");$(b).addClass("btn-success").addClass("current_stock");Stock.draw_btce_stock("nvc_usd");return}my_alert("Еще немного и будет сделано, терпение")},own:function(a){$("#chart_trade").highcharts().destroy();$("#stocks_trades .current_stock").removeClass("btn-success").removeClass("current_stock").addClass("btn-default");$(a).removeClass("btn-default").addClass("btn-success").addClass("current_stock");Main.draw_highcharts()},draw_btce_stock:function(a){Stock.foreign_stock_name=a;$.ajax({url:"/foreign/stock/btce/"+a+"/minute/0",type:"GET",dataType:"json",success:draw_btce_stock})},update_btce_stock:function(){console.log(Stock.foreign_stock_name);$.ajax({url:"/foreign/stock/btce/"+Stock.foreign_stock_name+"/minute/"+Stock.current_index,type:"GET",dataType:"json",success:function(b){Stock.current_index=b.last;console.log(Stock.current_index);var c=b.data_ask;for(var a=0;a<c.length;a++){Stock.btce_serias_ask.addPoint([c[a][0],c[a][1]],true,true)}c=b.data_bid;for(var a=0;a<c.length;a++){Stock.btce_serias_bid.addPoint([c[a][0],c[a][1]],true,true)}c=b.data_vol;for(var a=0;a<c.length;a++){Stock.btce_serias_vol.addPoint([c[a][0],c[a][1]],true,true)}}})}};function draw_btce_stock(a){Stock.current_index=a.last;$("#chart_trade").highcharts("StockChart",{chart:{events:{load:function(){Stock.btce_serias_ask=this.series[0];Stock.btce_serias_bid=this.series[1];Stock.btce_serias_vol=this.series[2];setInterval(Stock.update_btce_stock,5000)}}},rangeSelector:{buttons:[{count:1,type:"day",text:"1d"},{count:5,type:"day",text:"5d"},{type:"all",text:"All"}],inputEnabled:false,selected:0},title:{text:"Торги BTC-e  Биткоин к USD"},exporting:{enabled:false},yAxis:[{labels:{align:"right",x:-3},title:{text:"Продажа"},height:"60%",plotOptions:{series:{compare:"percent"}},tooltip:{pointFormat:'<span style="color:{series.color}">{series.name}</span>: <b>{point.y}</b> ({point.change}%)<br/>',valueDecimals:2},lineWidth:2},{labels:{align:"right",x:-3},title:{text:"Покупка"},plotOptions:{series:{compare:"percent"}},tooltip:{pointFormat:'<span style="color:{series.color}">{series.name}</span>: <b>{point.y}</b> ({point.change}%)<br/>',valueDecimals:2},height:"60%",lineWidth:2},{labels:{align:"right",x:-3},title:{text:"Volume"},top:"65%",height:"35%",offset:0,lineWidth:2},],series:[{name:"Продажа",data:a.data_ask},{name:"Покупка",data:a.data_bid},{type:"column",name:"Объем",yAxis:2,data:a.data_vol}]})}function highchart_candle(c){Main.highcharts_thema_enable();$("#online_users").html(c.online);$("#volume_base").html(c.volume_base);$("#volume_trade").html(c.volume_trade);var f=c.trades;Highcharts.setOptions(Highcharts.theme);var d=[],e=[],g=f.length;for(var b=0;b<g;b++){d.push([f[b][0],f[b][1],f[b][2],f[b][3],f[b][4]]);e.push([f[b][0],f[b][5]])}var a=[["week",[1]],["month",[1,2,3,4,6]]];$("#chart_trade").highcharts("StockChart",{rangeSelector:{buttons:[{type:"day",count:1,text:"1d"},{type:"week",count:1,text:"1w"},{type:"month",count:1,text:"1m"},{type:"month",count:3,text:"3m"},{type:"month",count:6,text:"6m"},{type:"year",count:1,text:"1y"}],inputEnabled:$("#chart_trade").width()>480,selected:4},title:{text:"Торги"},yAxis:[{labels:{align:"right",x:-3},title:{text:"Котировки"},height:"60%",lineWidth:2},{labels:{align:"right",x:-3},title:{text:"Объем"},top:"65%",height:"35%",offset:0,lineWidth:2}],series:[{type:"candlestick",name:"Торги",data:d,dataGrouping:{enable:false}},{type:"column",name:"Объем",data:e,yAxis:1,dataGrouping:{enable:false}}]})}function thinking_alert(){my_alert("<img src='/static/processing.gif'><br/><h4>Думаю...</h4>")}function hide_modal(a){$("#"+a).modal("hide")}function my_alert(a){$("#modal_msg").html(a);$("#modal_dlg").modal("show")};
