"use strict";
var wayforpay = 0;

var finance = {
    crypto_currency: {
        "XRP":1,
        "XEM":1,
        TLR: 1,
        ETC: 1,
        BCH: 1,
        ETH: 1,
        KRB: 1,
        SIB: 1,
        NVC: 1,
        ZEC: 1,
        XMR: 1,
        BTC: 1,
        LTC: 1,
        HIRO: 1,
        DASH: 1,
        VTC:  1,
        PPC:  1,
        DOGE: 1,
        CLR:  1,
        RMS:  1,
        ITI:  1,
        USDT: 1,
        FNO: 1,
        BTG:1,
        EOS:1,
        ZCL:1,
        BNB:1

    },
    bank_comission: 1.01,
    order_id: "",
    min_deal: 0.00001,
    timer: null,
    liqpay_flag: false,
    p24_flag: false,
    show_conclusion: function(order_id) {
        thinking_alert();
        $.ajax({
            url: "/finance/get_conv/" + order_id,
            type: 'GET',
            error: function(Data) {
                my_alert("не удалось получить выписку, если ошибка повторяется часто напишите нам support@btc-trade.com.ua");
            },
            success: function(Data) {
                $("#modal_msg").html((Data));
            }
        });
    },
    generate_wallets: function(currency){
        var a = $.ajax({
            url: "/finance/crypto_currency/" + currency,
            type: "GET",
            cache: false,
            error: function(d) {
                my_alert("что-то пошло не так обратитесь к нам пожайлуста bogdan.chayka@btc-trade.com.ua")
            },
            success: function(g) {
                console.log(g)
                my_alert(g);
            }
        });
    },
    ui_check_status: function() {
        $.ajax({
            dataType: "json",
            url: "/api/order/status/" + finance.order_id,
            type: "GET",
            cache: false,
            error: function(a) {
                console.log(a);
                my_alert("Не могу создать ордер  ")
            },
            success: function(b) {
                var a = b.status;
                if (a == "processed") {
                    $("#work_msg").html("<p>Средства удачно зачислены</p>");
                    window.location.href = "/finance/balance";
                    clearTimeout(finance.timer);
                    return
                }
                if (a == "created") {
                    $("#work_msg").html('Cтатус платежа <font color="greed" id="depo_status"> в обработке </font>');
                    return
                }
                if (a == "processing") {
                    $("#work_msg").html('Cтатус платежа <font color="greed" id="depo_status"> в обработке </font>');
                    return
                }
                if (a == "wait_secure") {
                    $("#work_msg").html("<p>Ваша оплата была отправленна платежной системой на ручную обработку</p> <p>После проверки, ваши средства будут немедленно зачисленны</p>");
                    clearTimeout(finance.timer);
                    return
                }
                if (a == "order_cancel") {
                    clearTimeout(finance.timer);
                    $("#work_msg").html("Ваша оплата была забракована платежной системой");
                    return
                }
                $("#work_msg").html("Что-то пошло не так, обратитесь в службу поддержки");
                clearTimeout(finance.timer);
                return
            }
        })
    },
    make_deposit: function(a) {
        $("#withdraw_form").modal("hide");
        finance.fill_providers_depo(a);
    },
    fill_providers_depo: function(a) {
        if (a == "USDT") {
            $("#currency_depo_invoice").val(a);
            $("#deposit_form_invoice").modal("show")
            return
        }
        if (a == "UAH") {
            $("#help_finance_block_fiat").html("Внимание! При первом пополнении гривневого счета с новой карты  может быть устанавлен холд на вывод 36 часов.");
            $("#currency_depo").val(a);
            $("#deposit_form").modal("show")
            return
        }

        if (finance.crypto_currency[a]) {
            $("#currency_depo_crypto").val(a);
            $("#res_provider").html("");
            $("#ext_info_show").hide();

            $.ajax({
                url: "/finance/crypto_currency/" + a,
                type: "GET",
                dataType: "json",
                cache: false,
                error: function(b) {
                    $("#res_provider").html("permission denied");
                    my_alert("Проблемы в работе с кошельком обратитесь в support@btc-trade.com.ua");
                    return false
                },
                success: function(Data) {
                    var Res = "";
                    if (Data["account"]) {
                        $("#crypto_account").val(Data["account"]);

                    }
                    if (Data["ext_info"]) {
                            $("#ext_info_show").show();
                            if(a=="XEM"){
                                    $("#crypto_ext_info_label").html("Message <strong>(обязательно)</strong>:");
                            }
                            else if(a=="XRP"){
                                $("#crypto_ext_info_label").html("Destination Tag <strong>(обязательно)</strong>:");
                            }
                            else{
                                $("#crypto_ext_info_label").html("Payment ID:");

                            }
                            $("#crypto_ext_info").val(Data["ext_info"]);

                    }
                    $("#help_finance_block_crypto").html(Data["help"]);
                    $("#deposit_form_crypto").modal("show")

                }
            })
        }


    },
    change_depo: function(d) {
        var a = $("#currency_depo").val();
        var b = $("#amnt_depo").val();
        if (d == "way4pay") {
            return finance.way4pay_start()
        }
        if (d == "liqpay_transfer") {
            return finance.liqpay_transfer( b, a)
        }
        if (d == "p24_transfer") {
            return finance.p24_start()
        }
    },
    way4pay_start: function() {
        if (wayforpay == 0) {
            wayforpay = new Wayforpay()
        }
        var c = $("#currency_depo").val();
        var e = $("#amnt_depo").val()*1;
//         var d = $("#name_depo").val();
//         var f = $("#lastname_depo").val();
        var b = $("#phone_depo").val();
        if (/*d.length < 2 || f.length < 2 ||*/ b.length < 2) {
            $("#provider_depo").val("");
            my_alert("Пожайлуста заполните авторизационные данные ФИО,телефон");
            return false
        }
        if (c != "UAH") {
            $("#provider_depo").val("");
            my_alert("Неправильная валюта");
            return false
        }
        if (e > 50000) {
            $("#provider_depo").val("");
            my_alert("Ограничение максимальной  суммы пополнения при оплате картой 50 000 ГРН");
            return false;
        }
        if (e < 499.99) {
            $("#provider_depo").val("");
            my_alert("Ограничение минимальной суммы пополнения через WayForPay, больше 500 ГРН");
            return false
        }
        $("#deposit_form").modal("hide");

        var a = $.ajax({
            url: "/finance/way4pay/start",
            type: "POST",
            data: {
                amount: e,
//                lastname: f,
//                name: d,
                phone: b
            },
            dataType: "json",
            cache: false,
            error: function(g) {
                $("#res_provider").html("permission denied");
                $("#provider_depo").val("");
                return false
            },
            success: function(g) {
                if (g.order_id) {
                    wayforpay.run({
                        merchantAccount: g.public_key,
                        merchantDomainName: g.host,
                        authorizationType: "SimpleSignature",
                        merchantSignature: g.sign,
                        orderReference: g.order_id,
                        orderDate: g.date,
                        paymentSystems: "card;lpTerminal",
                        amount: g.amnt,
                        currency: "UAH",
                        productName: g.product_name,
                        productPrice: g.price,
                        productCount: g.count,
                        clientFirstName: g.name,
                        clientLastName: g.last_name,
                        clientEmail: g.email,
                        clientPhone: g.phone,
                        serviceUrl: g.url,
                        returnUrl: g.returnUrl
                    }, function(h) {
                        cosole.log(h);
                        my_alert("Ваша оплата прошла успешно, в течении 15 минут деньги будут у вас на балансе")
                    }, function(h) {
                        cosole.log(h);
                        my_alert("Ваша оплата отклонена")
                    }, function(h) {
                        my_alert("Ваша оплата выпала на ручную обработку");
                        cosole.log(h)
                    })
                }
            }
        })
    },
    p24_start: function() {
        if (wayforpay == 0) {
            wayforpay = new Wayforpay()
        }
        var c = $("#currency_depo").val();
        var e = $("#amnt_depo").val()*1;
//         var d = $("#name_depo").val();
//         var f = $("#lastname_depo").val();
        var b = $("#phone_depo").val();
        if (/*d.length < 2 || f.length < 2 ||*/ b.length < 2) {
            $("#provider_depo").val("");
            my_alert("Пожайлуста заполните авторизационные  - телефон");
            return false
        }
        if (c != "UAH") {
            $("#provider_depo").val("");
            my_alert("Неправильная валюта");
            return false
        }
        if (e < 499.99) {
            $("#provider_depo").val("");
            my_alert("Ограничение минимальной суммы пополнения через Privat24 = 500 ГРН");
            return false
        }
        if (e > 149999) {
            $("#provider_depo").val("");
            my_alert("Ограничение максимальной суммы пополнения через Privat24 =  145500 ГРН");
            return false
        }
        $("#deposit_form").modal("hide");
        var c = $("#currency_depo").val();
        var e = $("#amnt_depo").val();
        if (wayforpay == 0) {
            wayforpay = new Wayforpay()
        }
        var a = $.ajax({
            url: "/finance/p24/start/" + e,
            type: "POST",
            dataType: "json",
            cache: false,
            data: {
                amount: e,
                //lastname: f,
                //name: d,
                phone: b
            },
            error: function(g) {
                $("#res_provider").html("permission denied");
                $("#provider_depo").val("");
                return false
            },
            success: function(g) {
                if (g.order_id) {
                    wayforpay.run({
                        merchantAccount: g.public_key,
                        merchantDomainName: g.host,
                        authorizationType: "SimpleSignature",
                        merchantSignature: g.sign,
                        orderReference: g.order_id,
                        orderDate: g.date,
                        amount: g.amnt,
                        currency: "UAH",
                        productName: g.product_name,
                        productPrice: g.price,
                        productCount: g.count,
                        clientFirstName: g.name,
                        clientLastName: g.last_name,
                        clientEmail: g.email,
                        clientPhone: g.phone,
                        serviceUrl: g.url,
                        returnUrl: g.returnUrl,
                        paymentSystems: "privat24"
                    }, function(h) {
                        cosole.log(h);
                        my_alert("Ваша оплата прошла успешно, в течении 15 минут деньги будут у вас на балансе")
                    }, function(h) {
                        cosole.log(h);
                        my_alert("Ваша оплата отклонена")
                    }, function(h) {
                        my_alert("Ваша оплата выпала на ручную обработку");
                        cosole.log(h)
                    })
                }
            }
        })
    },
    checkout_start: function() {
        var b = $("#currency_depo_invoice").val();
        var c = $("#amnt_depo_invoice").val();
        if (b != "USDT") {
            $("provider_depo").val("");
            my_alert("Неправильная валюта");
            return false
        }
        if (c < 10) {
            $("provider_depo").val("");
            my_alert("Ограничение минимальной суммы пополнения для этого типа операции 10 ");
            return false
        }
        var name = $("#name_depo_invoice").val() + " " + $("#lastname_depo_invoice").val();
        var phone = $("#phone_depo_invoice").val();
        var data_params = {"amnt":c, "currency":b, "name": name, "phone": phone};
        $.ajax({
            url: "/finance/checkout/start",
            type: "POST",
            data: data_params,
            error: function(d) {
                my_alert("Возникла непредвиденная ошибка, обратитесь пожайулуста support@btc-trade.com.ua");
                $("provider_depo").val("");
                return false
            },
            success: function(d) {
                window.location.href = d.invoice_page
            }
        });

        return false;
    },
    p24_transfer: function(d, b, c) {
        if (c != "UAH") {
            d.value = "";
            my_alert("Неправильная валюта");
            return false
        }
        if (b < 100) {
            d.value = "";
            my_alert("Ограничение минимальной суммы пополнения через Приват24, больше 100 ГРН");
            return false
        }
        var a = $.ajax({
            url: "/finance/p24/deposit/" + b,
            type: "GET",
            cache: false,
            error: function(e) {
                $("#res_provider").html("permission denied");
                d.value = ""
            },
            success: function(f) {
                var e = '<p class="help-block">Комиссия за пополнение составляет 3% с карты ПриватБанка</p>';
                $("#res_provider").html(e + f);
                $("#pay_p24_form").bind("submit", function() {
                    return finance.p24_flag
                });
                $("#p24_submit_button").bind("click", finance.p24_start)
            }
        })
    },
    liqpay_transfer: function(d, b, c) {
        if (c != "UAH") {
            d.value = "";
            my_alert("Неправильная валюта");
            return false
        }
        if (b < 100) {
            d.value = "";
            my_alert("Ограничение минимальной суммы пополнения через liqpay, больше 100 ГРН");
            return false
        }
        var a = $.ajax({
            url: "/finance/liqpay/deposit/" + b,
            type: "GET",
            cache: false,
            error: function(e) {
                $("#res_provider").html("permission denied");
                d.value = ""
            },
            success: function(f) {
                var e = '<p class="help-block">Комиссия за пополнение составляет 2.75% с карт Visa, MasterCard</p>';
                e += '<p class="help-block">2.75% наличными в терминалах ПриватБанка</p>';
                $("#res_provider").html(e + f);
                $("#pay_liqpay_form").bind("submit", function() {
                    return finance.liqpay_flag
                });
                $("#liqpay_submit_button").bind("click", finance.liqpay_start)
            }
        })
    },
    confirm_operation: function() {
        var b = $("#key_type").val();
        var a = $("#key").val();
        var d = $("#id_pin").val();
        var c = {
            key_type: b,
            pin: d
        };
        thinking_alert();
        $.ajax({
            url: "/finance/common_secure_confirm?key=" + a,
            type: "POST",
            data: c,
            error: function(e) {
                my_alert("Авторизация не прошла")
            },
            success: function(e) {
                main_hide_thinking_alert();
                $("#home").html((e))
            }
        })
    },
    confirm_g2a_operation: function(c) {
        var b = $("#key_type").val();
        var a = $("#key").val();
        var d = {
            key_type: b,
            g2a_session: c
        };
        $.ajax({
            url: "/finance/common_secure_confirm?key=" + a,
            type: "POST",
            data: d,
            error: function(e) {
                my_alert("Авторизация не прошла")
            },
            success: function(e) {
                $("#home").html((e))
            }
        })
    },
    bank_transfer: function(d, b, c) {
        if (c != "UAH") {
            d.value = "";
            my_alert("Неправильная валюта");
            return
        }
        if (b < 100) {
            d.value = "";
            my_alert("Ограничение минимальной суммы пополнения через банковские переводы, больше 100 ГРН");
            return
        }
        var a = $.ajax({
            url: "/finance/bank_transfer/UAH/" + b,
            type: "GET",
            cache: false,
            error: function(e) {
                $("#res_provider").html("permission denied");
                d.value = ""
            },
            success: function(e) {
                $("#res_provider").html(e)
            }
        })
    },
    withdraw: function(a) {
        $("#deposit_form").modal("hide");
        $("#res_provider_withdraw").html("");
        $("#currency_withdraw").val(a);
        $("#withdraw_form").modal("show");
        finance.withdraw_providers(a)
    },
    withdraw_providers: function(b) {
        $("#provider_withdraw").html("");
        if (b == "UAH") {
            $("#provider_withdraw").show();
            $("#label_provider_withdraw").show();
            $("#provider_withdraw").append($('<option value="">Выбрать</option>'));
            $("#provider_withdraw").append($('<option value="card_transfer">На платежную карту (Visa, MasterCard)</option>'))
        }
        if (finance.crypto_currency[b]) {
            $("#provider_withdraw").hide();
            $("#label_provider_withdraw").hide();
            var a = $.ajax({
                url: "/finance/crypto_transfer_withdraw/" + b,
                type: "GET",
                cache: false,
                error: function(c) {
                    $("#res_provider_withdraw").html(c)
                },
                success: function(d) {
                    // console.log(d);
                    $("#res_provider_withdraw").html(d);
                    $("#id_amnt_get").prop("disabled", true);
                    var c = $("#id_comission_withdraw").val();
                    $("#id_amnt").on("keyup", function(f) {
                        var e = $(this).val();
                        var g = e - c;
                        // console.log(g);
                        if (g < 0) {
                            $("#id_amnt_get").val("0")
                        } else {
                            $("#id_amnt_get").val(g)
                        }
                    });
                    $("#id_amnt").wrap("<div class='input-group'></div>");
                    $("#id_amnt").after("<div class='input-group-append'><button class='btn btn-success' type='button' id='all'>Вывести всё</button></div>");
                    $("#all").on("click", function (){
                        
                        $("#id_amnt").val( Main.format_float8($("#balance_" + b).data("balance")) );
                        $("#id_amnt_get").val($("#id_amnt").val() - c);
                    });
                    $("#ajax_form").submit(function(e) {
                        thinking_alert();
                        return  true;
                    });
                }
            });


        }
    },
    change_withdraw: function(b) {
        var c = b.value;
        if (c == "") {
            return
        }
        var a = $("#currency_withdraw").val();
        if (c == "bank_transfer") {
            return finance.bank_transfer_withdraw(b, a)
        }
        if (c == "liqpay_transfer") {
            return finance.liqpay_transfer_withdraw(b, a)
        }
        if (c == "card_transfer") {
            return finance.p2p_transfer_withdraw(b, a)
        }
    },
    p2p_transfer_withdraw: function(d, c) {
        if (c != "UAH") {
            d.value = "";
            my_alert("Неправильная валюта");
            return
        }
        var b = 500;
        var a = $.ajax({
            url: "/finance/p2p_transfer_withdraw/" + c + "/" + b,
            type: "GET",
            cache: false,
            error: function(e) {
                $("#res_provider_withdraw").html(e);
                d.value = ""
            },
            success: function(e) {
                $("#res_provider_withdraw").html(e);
                $('label[for="id_CardNumber"]').hide();
                $('label[for="id_CardName"]').hide();

                $("#ajax_form_submit").on("click", function() {
                    if (!checkMoon($("#id_CardNumber").val())) {
                      var label = $("#id_CardNumber").prop("labels")[0];
                      $(label).text("Введите валидный номер карты!").css('color', 'red');
                      $(label).text("Введите валидный номер карты!").css('display', '');
                      event.preventDefault();
                    }
                });
                $("#id_amnt_get").prop('disabled', true);
                $("#id_amnt").on("keyup", function(ev) {
                    var amnt = $(this).val();
                    var res_amnt = amnt / finance.bank_comission;
                    if (res_amnt < 0) {
                        $("#id_amnt_get").val("0");
                    } else {
                        $("#id_amnt_get").val(Main.format_float2(res_amnt));
                    }
                });
                $("#id_amnt").wrap("<div class='input-group'></div>");
                $("#id_amnt").after("<div class='input-group-append'><button class='btn btn-success' type='button' id='all'>Вывести всё</button></div>");
                $("#all").on("click", function (){
                    
                    var all = Main.format_float2( $("#balance_" + c).data("balance") );
                    $("#id_amnt").val( all );
                    var with_comission = all/1.01
                    $("#id_amnt_get").val(Main.format_float2(with_comission));
                    
                });
                $("#id_CardNumber").on("keyup", function(){
                    if (this.value.length >= 6) {
                        var bin = this.value.slice(0,6);
                        finance.withdrawPercent(bin);
                        var amnt = $("#id_amnt").val();
                        var res_amnt = amnt / finance.bank_comission;
                        $("#id_amnt_get").val(Main.format_float2(res_amnt));
                    }
                });
            }
        })
    },
    bank_transfer_withdraw: function(d, c) {
        if (c != "UAH") {
            d.value = "";
            my_alert("Неправильная валюта");
            return
        }
        var b = 10;
        var a = $.ajax({
            url: "/finance/bank_transfer_withdraw/" + c + "/" + b,
            type: "GET",
            cache: false,
            error: function(e) {
                $("#res_provider_withdraw").html(e);
                d.value = ""
            },
            success: function(e) {
                $("#res_provider_withdraw").html(e)
            }
        })
    },
    liqpay_transfer_withdraw: function(d, c) {
        if (c != "UAH") {
            d.value = "";
            my_alert("Неправильная валюта");
            return
        }
        var b = 10;
        var a = $.ajax({
            url: "/finance/liqpay_transfer_withdraw/" + c + "/" + b,
            type: "GET",
            cache: false,
            error: function(e) {
                $("#res_provider_withdraw").html(e);
                d.value = ""
            },
            success: function(e) {
                $("#res_provider_withdraw").html(e)
            }
        })
    },
    withdrawPercent: function(bin) {
        $.ajax({
            url: "https://ecommerce.liqpay.ua/ecommerce/fullbininfo2?bin="+bin,
            type: "GET",
            error: function(resp){
                console.log("Error request!");
            },
            success: function(resp){
                var b = JSON.parse(resp);
                finance.bank_comission = (b.bank == "privat") ? 1.01 : 1.013;
            }
        });
    }
};
var Main = {
    trade_pair: "",
    currency_base: "",
    currency_on: "",
    state: "",
    rand_key: "",
    state_calls: {},
    usd_uah_rate: null,
    timer_deals: null,
    chart: null,
    server_timeoffset:0, // 7200000 + 60 * 60 * 1000,
    first: true,
    calendar_loaded: false,
    timer_sell_list: null,
    timer_buy_list: null,
    sell_list_objects: null,
    buy_list_objects: null,
    sell_list_sum: null,
    balance: null,
    comission: 0.0005,
    percentOfMarket: 0.25,
    start_stock: function() {
        Main.start_market_prices();
        if (Main.currency_base == "UAH") {
            $("#buy_result_usd_eq").show();
            $("#sell_result_usd_eq").show();
            $("#sell_price_usd_eq").show();
            $("#buy_price_usd_eq").show()
        }
        Main.draw_highcharts()
    },
    format_time: function(b) {
        var c = new Date(b * 1000 + Main.server_timeoffset);
        var a = dateFormat(c, "HH:MM:ss");
        return a
    },
    format_date_time: function(b) {
        var c = new Date(b * 1000 - Main.server_timeoffset);
        var a = dateFormat(c, "dd.mm.yyyy, HH:MM:ss");
        return a
    },
    format_date: function(b) {
        
        var c = new Date(b * 1000 - Main.server_timeoffset);
        var a = dateFormat(c, "dd.mm.yyyy");
        return a
    },
    start_time: function() {
        if (Main.first) {
            $("#simple_form").submit(function(a) {
                thinking_alert()
            });
            Main.first = false
        }
        Main.server_time(function() {
            setTimeout(Main.start_time, 7000)
        })
    },
    val_eq_to_usd: function(c, b) {
        if (Main.currency_base == "UAH") {
            var a = Main.format_float4(c / Main.usd_uah_rate);
            $("#" + b).html(a);
            $("#" + b).parent().show();
        }
        /*else {
            $("#" + b).parent().hide();
        }*/
    },
    eq_to_usd: function(c, b) {
        if (Main.currency_base == "UAH") {
            var a = Main.format_float4(c.value / Main.usd_uah_rate);
            $("#" + b).html(a);
            $("#" + b).parent().show();
        }/*else {
            $("#" + b).parent().hide();
        }*/
    },
    server_time: function(a) {
        $.ajax({
            dataType: "json",
            url: "/time",
            type: "GET",
            cache: false,
            error: function(b) {
                console.log(b);
                Main.update_stock();
                setTimeout(a, 27000)
            },
            success: function(b) {
                Login.use_f2a = b.use_f2a;
                Login.sessionid = b.sessionid;
                Login.logged = b.logged;
                if (Main.state != b.state) {
                    Main.state = b.state;
                    if (Main.start_stock) {
                        Main.update_stock()
                    }
                }
                Main.usd_uah_rate = b.usd_uah_rate;
                $("#server_time").html(Main.format_date_time(b.time - 60 * 60 * 3));
                $("#client_comis").html(b.deal_comission);
                if (a) {
                    a()
                }
            }
        })
    },
    makeid: function() {
        var c = "";
        var a = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
        for (var b = 0; b < 64; b++) {
            c += a.charAt(Math.floor(Math.random() * a.length))
        }
        return c
    },
    own_deals: function(b) {
        var a = "";
        var date1 = "";
        if (!Main.calendar_loaded) {
            $("#date_deals_comp").removeClass("hidden");
            $("#date_deals").datepicker({
                format: "dd-mm-yyyy"
            }).on("changeDate", function(e) {
                $("#date_deals").datepicker("hide");
                Main.own_deals();
            });
            console.log("load date picker");
            $("#date_deals1").datepicker({
                format: "dd-mm-yyyy"
            }).on("changeDate", function(e) {
                $("#date_deals1").datepicker("hide");
                Main.own_deals();
            });
            $("#date_deals").datepicker("hide");
            $("#date_deals1").datepicker("hide");
            a = "";
            date1 = "";
            Main.calendar_loaded = true;
        } else {
            a = $("#date_deals").val();
            date1 = $("#date_deals1").val();
        }

       thinking_alert();
       $.ajax({
            dataType: "json",
            url: "/api/my_deals/" + Main.trade_pair + "?ts=" + a + "&ts1=" + date1,
            type: "GET",
            cache: false,
            error: function(c) {
                main_hide_thinking_alert();
                if (b) {
                    Main.own_deals(1)
                }
            },
            success: function(f) {
                var e = f.length;
                main_hide_thinking_alert();
                $("#trade_deals").html("");
                var g = 0;
                var e1 =0;
                var e2 =0;
                var c = 0;
                var j = 0;
                for (var d = 0; d < e; d++) {
                    var h = "<tr>";
                    h += "<td>" + Main.format_date_time(f[d]["unixtime"]) + "</td>";
                    h += "<td><a href='/profile/" + f[d]["user"] + "'>" + f[d]["user"] + "</a></td>";
                    if (f[d]["type"] == "buy") {
                        h += "<td style='color:green'>" + f[d]["type"] + "</td>";
                        c += f[d]["amnt_trade"] * 1
                    } else {
                        h += "<td style='color:red'>" + f[d]["type"] + "</td>";
                        j += f[d]["amnt_trade"] * 1
                    }
                    h += "<td>" + f[d]["price"] + "&nbsp;<strong>" + Main.currency_base + "</strong></td>";
                    h += "<td>" + f[d]["amnt_base"] + "</td>";
                    h += "<td>" + f[d]["amnt_trade"] + "</td></tr>";
                    $("#trade_deals").append(h)
                }
                for (var d = 0; d < e; d++) {
                    if(f[d]["type"] == "sell"){
                       e1 += (f[d]["price"] * 1 * (f[d]["amnt_trade"]/j)  );
                    }else{
                       e2 += (f[d]["price"] * 1 * (f[d]["amnt_trade"]/c) );

                    }
                    g += f[d]["price"] * 1 * ( f[d]["amnt_trade"]/( j+c ) );
                }
                $("#avarage_rate").html(Main.format_float4(g));
                $("#avarage_rate_sell").html(Main.format_float4(e1));
                $("#avarage_rate_buy").html(Main.format_float4(e2));
                $("#sum_buy").html(Main.format_float4(c));
                $("#sum_sell").html(Main.format_float4(j));
                if (b) {
                    Main.own_deals(1)
                }
            }
        })
    },
    market_prices: function(a) {
        $.ajax({
            dataType: "json",
            url: "/api/market_prices",
            type: "GET",
            cache: false,
            error: function(b) {
                console.log(b);
                if (a) {
                    a()
                }
            },
            success: function(d) {
                var c = d.prices.length;
                var f = d.prices;
                for (var b = 0; b < c; b++) {
                    var e = f[b];
                    $("#" + e.type).html(e.price)
                }
                if (a) {
                    a()
                }
            }
        })
    },
    user_menu: function(b, a) {
        console.log("load balancei");
        if (!Login.logged) {
            return
        }
        $.ajax({
            dataType: "json",
            url: "/api/balance",
            type: "GET",
            cache: false,
            error: function(c) {
                console.log(c);
                if (a) {
                    a()
                }
            },
            success: function(e) {
                var d = e.accounts.length;
                var g = e.accounts;
                Main.balance = {};
                for (var c = 0; c < d; c++) {
                    var f = g[c];
                    $("#balance_" + f.currency).html(Main.format_float8(f.balance))
                    Main.balance[f.currency] = f.balance;
                }
                Login.use_f2a = e.use_f2a;
                $("#notify_count").html("(" + e.notify_count + ")");
                $("#msg_count").html("(" + e.msg_count + ")");
                if (b) {
                    return b()
                }
            }
        })
    },
    create_msg: function(a) {
        $("#msgs").hide();
        $("#msg_form").modal("show");
        $("#whom").val(a)
    },
    send_msg: function() {
        var a = {
            whom: $("#whom").val(),
            msg: $("#msg").val()
        };
        $.ajax({
            url: "/msgs/create",
            type: "POST",
            data: a,
            cache: false,
            error: function(b) {
                my_alert(b)
            },
            success: function(b) {
                if (b.status) {
                    window.location.href = "/msgs/out"
                } else {
                    my_alert(b.description)
                }
            }
        })
    },
    cancel_msg: function() {
        $("#msgs").show("fast");
        $("#msg_form").modal("hide");
        $("#whom").val("")
    },
    notify_remove: function(a) {
        $.ajax({
            dataType: "json",
            url: "/msgs/hide/" + a,
            type: "GET",
            cache: false,
            error: function(b) {
                console.log(b)
            },
            success: function(b) {
                if (b.status) {
                    $("#notify_" + a).hide()
                } else {
                    my_alert("something wrong try later")
                }
            }
        })
    },
    user_menu_timeout500: function() {
        if (Login.logged) {
            setTimeout(function() {
                Main.user_menu(false, Main.user_menu_timeout500)
            }, 1500)
        }
    },
    sell_list_timeout500: function() {
        setTimeout(function() {
            Main.sell_list(false, Main.sell_list_timeout500)
        }, 1500)
    },
    buy_list_timeout500: function() {
        setTimeout(function() {
            Main.buy_list(false, Main.buy_list_timeout500)
        }, 1500)
    },
    my_orders_timeout500: function() {
        if (Login.logged) {
            setTimeout(function() {
                Main.my_orders(false, Main.my_orders_timeout500)
            }, 1500)
        }
    },
    deals_list_timeout1000: function() {
        setTimeout(function() {
            Main.deals_list(false, Main.deals_list_timeout1000)
        }, 1000)
    },
    update_stock: function() {
        if (Main.trade_pair) {
            setTimeout(function() {
                Main.deals_list(false, Main.deals_list_timeout1000)
            }, 1000);
            setTimeout(function() {
                Main.user_menu(false, Main.user_menu_timeout500)
            }, 100);
            setTimeout(function() {
                Main.my_orders(false, Main.my_orders_timeout500)
            }, 1000);
            setTimeout(function() {
                Main.sell_list(false, Main.sell_list_timeout500)
            }, 500);
            setTimeout(function() {
                Main.buy_list(false, Main.buy_list_timeout500)
            }, 700)
        }
    },
    start_market_prices: function() {
        console.log("market");
        Main.market_prices(function() {
            setTimeout(Main.start_market_prices, 30000)
        })
    },
    start_user_menu: function() {
        console.log("balance");
        Main.user_menu(function() {
            setTimeout(Main.start_user_menu, 1000)
        })
    },
    start_my_orders: function() {
        Main.my_orders(function() {
            console.log("call my orders");
            setTimeout(Main.start_my_orders, 5000)
        })
    },
    start_sell_list: function() {
        Main.sell_list(function() {
            console.log("sell list ");
            setTimeout(Main.start_sell_list, 6000)
        })
    },
    start_buy_list: function() {
        Main.buy_list(function() {
            console.log("buy list ");
            setTimeout(Main.start_buy_list, 6000)
        })
    },
    start_deals_timer: function() {
        Main.deals_list(function() {
            console.log("deal list ");
            setTimeout(Main.start_deals_timer, 4500)
        })
    },
    sell_list: function(b, a) {
        $.ajax({
            dataType: "json",
            url: "/api/trades/sell/" + Main.trade_pair,
            type: "GET",
            cache: false,
            error: function(c) {
                console.log(c);
                if (a) {
                    a()
                }
            },
            success: function(g) {
                var f = g.list.length;
                $("#sell_orders_list").html("");
                var e = g.list;
                Main.sell_list_objects = e;
                Main.sell_list_sum = g.orders_sum;
                $("#sell_orders_sum").html(g.orders_sum);
                var k = Main.format_float6(g.min_price);
                $("#buy_min_price").html(k);
                var c = $("#buy_price").val();
                if (!c) {
                    $("#buy_price").val(k);
                    Main.val_eq_to_usd(k, "buy_price_usd_eq")
                }
                for (var d = 0; d < f; d++) {
                    var j = Main.format_float4(e[d]["price"] / Main.usd_uah_rate);
                    var title = Main.format_float6(e[d]["price"]) + "" + Main.currency_base + "(" + j + "$)";
                    var h = "<tr class='cursor' onclick='Main.order2this_buy(this," + e[d]["price"] + "," + e[d]["currency_trade"] + " )'>";
                    h += "<td title=" + title + ">" + Main.format_float6(e[d]["price"]) + "&nbsp;<strong>" + Main.currency_base + "</strong>&nbsp;<small>(" + j + "&#36;</small>)</td>";
                    h += "<td >" + Main.format_float6(e[d]["currency_trade"]) + "</td>";
                    h += "<td>" + Main.format_float6(e[d]["currency_base"]) + "</td></tr>";
                    $("#sell_orders_list").append(h)
                }
                if (b) {
                    b()
                }
            }
        })
    },
    order2this_sell: function(f, price, b) {
        price = price * 1 - 0.00000001;
        var e = "#sell_count";
        var a = "#sell_price";
        $(a).val(price);
        if (Login.logged) {
            var d = $("#balance_" + Main.currency_on).html();
            if (d > b) {
                $(e).val(b)
                $("#sell_market_count").val(b);

            } else {
                $(e).val(d)
                $("#sell_market_count").val(d);

            }
        } else {
            $("#sell_market_count").val(b);
            $(e).val(b)
        }
        Main.calc_order_market("sell_market");        
        Main.calc_order("sell")
    },
    order2this_buy: function(f, price, b) {
        price = price * 1 + 0.00000001;
        var e = "#buy_count";
        var a = "#buy_price";
        $(a).val(price);
        if (Login.logged) {
            var d = $("#balance_" + Main.currency_base).html();
            if (d / price > b) {
                $(e).val(b)
                $("#buy_market_count").val(b*price);     

            } else {
                $(e).val(Main.format_float8(d / price))
                $("#buy_market_count").val(d);     

            }
        } else {
            $(e).val(b)
            $("#buy_market_count").val(b*price);     

        }
        Main.calc_order_market("buy_market");
        Main.calc_order("buy")
    },
    buy_list: function(b, a) {
        $.ajax({
            dataType: "json",
            url: "/api/trades/buy/" + Main.trade_pair,
            type: "GET",
            cache: false,
            error: function(c) {
                console.log(c);
                if (a) {
                    a()
                }
            },
            success: function(f) {
                var e = f.list.length;
                $("#buy_orders_list").html("");
                var d = f.list;
                Main.buy_list_objects = d;
                $("#buy_orders_sum").html(f.orders_sum);
                var k = Main.format_float6(f.max_price);
                $("#sell_max_price").html(k);
                var j = $("#sell_price").val();
                if (!j) {
                    $("#sell_price").val(k);
                    Main.val_eq_to_usd(k, "sell_price_usd_eq")
                }
                for (var c = 0; c < e; c++) {
                    var h = Main.format_float4(d[c]["price"] / Main.usd_uah_rate);
                    var title = Main.format_float6(d[c]["price"]) + "" + Main.currency_base + "(" + h + "$)";
                    var g = "<tr class='cursor' onclick='Main.order2this_sell(this," + d[c]["price"] + "," + d[c]["currency_trade"] + " )'>";
                    g += "<td title=" + title + ">" + Main.format_float6(d[c]["price"]) + "&nbsp;<strong>" + Main.currency_base + "</strong>&nbsp;<small>(" + h + "&#36;</small>)</td>";
                    g += "<td>" + Main.format_float6(d[c]["currency_trade"]) + "</td>";
                    g += "<td>" + Main.format_float6(d[c]["currency_base"]) + "</td></tr>";
                    $("#buy_orders_list").append(g)
                }
                if (b) {
                    b()
                }
            }
        })
    },
    
    my_orders: function(c, b) {
        if (!Login.logged) {
            if (c) {
                return c()
            }
        }


        var a = $.ajax({
            url: "/api/my_orders/" + Main.trade_pair,
            type: "GET",
            dataType: "json",
            cache: false,
            error: function(d) {
                console.log(d);
                if (b) {
                    b()
                }
            },
            success: function(g) {
                if (g.auth) {
                    var f = g.your_open_orders.length;
                    $("#your_open_orders").html("");
                    var e = g.your_open_orders;
                    if(Main.currency_base && Main.balance){
                        $("#your_balance_currency1").html(Main.balance[Main.currency_base]);
                        $("#your_balance_currency").html(Main.balance[Main.currency_on]);
                    }
                    for (var d = 0; d < f; d++) {
                        var h = '<tr id="my_order_' + e[d]["id"] + '"><td>' + e[d]["id"] + "</td>";
                        h += "<td>" + Main.format_date_time(e[d]["unixtime"]) + "</td>";
                        if (e[d]["type"] == "sell"){
                            h += "<td style=\"color:red\">" + e[d]["type"] + "</td>";
                        }else{
                            h += "<td style=\"color:green\">" + e[d]["type"] + "</td>";
                            
                        }
                        
                        h += "<td>" + Main.format_float6(e[d]["price"]) + "&nbsp;<strong>" + Main.currency_base + "</strong></td>";
                        h += "<td>" + Main.format_float6(e[d]["amnt_base"]) + "</td>";
                        h += "<td>" + Main.format_float6(e[d]["amnt_trade"]) + "</td>";
                        h += "<td> <span onclick=\"Main.remove('" + e[d]["id"] + '\')" class="btn btn-primary btn-xs">Cancel</span></td></tr>';
                        $("#your_open_orders").append(h)
                    }
                }
                if (c) {
                    c()
                }
            }
        })
    },
    remove: function(b) {
        var a = "#my_order_" + b;
        $(a).hide();
        $.ajax({
            dataType: "json",
            url: "/api/remove/order/" + b,
            type: "GET",
            cache: false,
            error: function(c) {
                my_alert("Не могу удалить ордер  ");
                $(a).show()
            },
            success: function(c) {
                if (c.status) {
                    $(a).hide()
                } else {
                    my_alert(c.description)
                }
            }
        })
    },
    deals_list: function(b, a) {
        $.ajax({
            dataType: "json",
            url: "/api/deals/" + Main.trade_pair,
            type: "GET",
            cache: false,
            error: function(c) {
                console.log(c);
                if (a) {
                    a()
                }
            },
            success: function(e) {
                var d = e.length;
                $("#trade_deals").html("");
                for (var c = 0; c < d; c++) {
                    var f = "<tr>";
                    if("unixtime" in e[c]){
                        f += "<td>" + Main.format_date_time(e[c]["unixtime"]) + "</td>";
                    }else{                    
                        f += "<td>" + e[c]["pub_date"] + "</td>";
                    }
                    f += "<td><a href='/profile/" + e[c]["user"] + "'>" + e[c]["user"] + "</a></td>";
                    if (e[c]["type"] == "buy") {
                        f += "<td style='color:green'>" + e[c]["type"] + "</td>"
                    } else {
                        f += "<td style='color:red'>" + e[c]["type"] + "</td>"
                    }
                    f += "<td>" + Main.format_float4(e[c]["price"]) + "&nbsp;<strong>" + Main.currency_base + "</strong></td>";
                    f += "<td>" + Main.format_float4(e[c]["amnt_base"]) + "</td>";
                    f += "<td>" + Main.format_float4(e[c]["amnt_trade"]) + "</td></tr>";
                    $("#trade_deals").append(f)
                }
                if (b) {
                    b()
                }
            }
        })
    },
    deal_order_status: function(D) {
        $.ajax({
            url: "/api/order/status/" + D,
            type: 'GET',
            dataType: 'json',
            error: function(data) {
                console.log(data);
            },
            success: function(data) {
                if (data["status"] == "core_error") {
                    my_alert("Похоже у вас недостаточно средств для этой сделки");
                }
                if (data["status"] == "processed") {
                    my_alert("Ваш заявка полностью исполнена, проверьте наличие средств на вашем балансе");
                }
                if (data["status"] == "processing") {
                    if (data["sum2"] == data["sum2"]) {
                        my_alert("Ваша заявка создана  и добавлена в стакан торгов");
                    } else {
                        my_alert("Ваша заявка исполнена не полностью...остаток " + Data["sum2"] + " " + Data["currency1"] + "добавлен в стакан торгов");
                    }
                }
            }
        });
    },
    make_order: function(c, d) {
        var b = $("#buy_price").val();
        var a = $("#buy_count").val();
        var e = {
            count: a,
            price: b,
            currency1: d,
            currency: c
        };
        $.ajax({
            url: "/api/buy/" + Main.trade_pair,
            type: "POST",
            data: e,
            dataType: "json",
            success: function(f) {
                if (f.status == true) {
                    thinking_alert();
                    setTimeout(Main.deal_order_status, 800, f["order_id"]);
                    Main.clear_buy_form();
                    return
                }
                if (f.status == "process_order_error") {
                    my_alert(f.description);
                    return
                }
                if (f.status == "incifition_funds") {
                    my_alert(f.description);
                    return
                }
                if (f.status == "processed") {
                    my_alert(f.description);
                    Main.clear_buy_form();
                    return
                }
                if (f.status == "part_processed") {
                    my_alert(f.description);
                    Main.clear_buy_form();
                    return
                }
                my_alert("Не могу создать ордер, проверьте пожайлуста данный и попробуйте снова")
            }
        })
    },
    clear_sell_form :function(){
        $("#sell_count").val("0");
        $("#sell_help").html("Нажмите посчитать, чтобы рассчитать сумму в соответствии с ордерами.");
        $("#sell_market_count").val("0");
        $("#sell_market_help").html("Нажмите посчитать, чтобы рассчитать сумму в соответствии с ордерами.");
        
    },
    clear_buy_form :function(){
        $("#buy_count").val("0");
        $("#buy_help").html("Нажмите посчитать, чтобы рассчитать сумму в соответствии с ордерами.");
        $("#buy_market_count").val("0");
        $("#buy_market_help").html("Нажмите посчитать, чтобы рассчитать сумму в соответствии с ордерами.");
    },
    make_order_sell: function(c, d) {
        var b = $("#sell_price").val();
        var a = $("#sell_count").val();
        var e = {
            count: a,
            price: b,
            currency1: d,
            currency: c
        };
        $.ajax({
            url: "/api/sell/" + Main.trade_pair,
            type: "POST",
            data: e,
            dataType: "json",
            success: function(f) {
                if (f.status == true) {
                    thinking_alert();
                    setTimeout(Main.deal_order_status, 800, f["order_id"]);
                    Main.clear_sell_form();
                    return
                }
                if (f.status == "incifition_funds") {
                    my_alert(f.description);
                    Main.clear_sell_form();
                    return
                }
                if (f.status == "processed") {
                    my_alert(f.description);
                    Main.clear_sell_form();
                     return
                }
                if (f.status == "part_processed") {
                    my_alert(f.description);
                    Main.clear_sell_form();
                    return
                }
                my_alert("Не могу создать ордер, проверьте пожайлуста данный и попробуйте снова")
            }
        })
    },
    make_order_market: function(cur1, cur2){
        Main.calc_order_market("buy_market");
        var orderCount = $("#buy_market_help").val();
        var orderPrice = $("#buy_market_result").val();
        var data = {
            count: orderCount,
            price: orderPrice,
            currency1: cur2,
            currency: cur1
        };
        if($("#buy_market_warning").text() == ""){
            $.ajax({
                url: "/api/buy/" + Main.trade_pair+"?market=1",
                type: "POST",
                data: data,
                dataType: "json",
                success: function(f) {
                    if (f.status == true) {
                        thinking_alert();
                        setTimeout(Main.deal_order_status, 800, f["order_id"]);
                        Main.clear_buy_form();
                        return
                    }
                    if (f.status == "process_order_error") {
                        my_alert(f.description);
                        return
                    }
                    if (f.status == "incifition_funds") {
                        my_alert(f.description);
                        return
                    }
                    if (f.status == "processed") {
                        my_alert(f.description);
                        Main.clear_buy_form();
                        return
                    }
                    if (f.status == "part_processed") {
                        my_alert(f.description);
                        Main.clear_buy_form();
                        return
                    }
                    my_alert("Не могу создать ордер, проверьте пожайлуста данный и попробуйте снова");
                }
            });
        }else {
            var modalWnd = $("#exampleModal_buy");
            $("#modal_buy_sum").text(orderPrice);
            $("#modal_buy_result").text(orderCount - $("#buy_market_comission").text());
            $("#modal_buy_disperse").text($("#buy_market_result").text());
            $("#modal_buy_comission").text($("#buy_market_comission").text());
            $("#modal_buy_percent").text(Main.percentOfMarket*100 + "%");
            modalWnd.modal('show');
            $("#proceed_buy").on('click', function(){
                console.log("continue");
                $.ajax({
                    url: "/api/buy/" + Main.trade_pair +"?market=1",
                    type: "POST",
                    data: data,
                    dataType: "json",
                    success: function(f) {
                        if (f.status == true) {
                            thinking_alert();
                            setTimeout(Main.deal_order_status, 800, f["order_id"]);
                            $("#buy_market_count").val("0");
                            $("#buy_market_help").html("Нажмите посчитать, чтобы рассчитать сумму в соответствии с ордерами.");
                            return
                        }
                        if (f.status == "process_order_error") {
                            my_alert(f.description);
                            return
                        }
                        if (f.status == "incifition_funds") {
                            my_alert(f.description);
                            return
                        }
                        if (f.status == "processed") {
                            my_alert(f.description);
                            $("#buy_market_count").val("0");
                            $("#buy_market_help").html("Нажмите посчитать, чтобы рассчитать сумму в соответствии с ордерами.");
                            return
                        }
                        if (f.status == "part_processed") {
                            my_alert(f.description);
                            $("#buy_market_count").val("0");
                            $("#buy_market_help").html("Нажмите посчитать, чтобы рассчитать сумму в соответствии с ордерами.");
                            return
                        }
                        my_alert("Не могу создать ордер, проверьте пожайлуста данный и попробуйте снова");
                    }
                });
                modalWnd.modal('hide');
            });
        }
    },
    make_order_sell_market: function(cur1, cur2){
        Main.calc_order_market("sell_market");
        var orderCount = $("#sell_market_count").val();
        var orderPrice = $("#sell_market_result").val();
        var data = {
            count: orderCount,
            price: orderPrice,
            currency1: cur2,
            currency: cur1
        };
        if($("#sell_market_warning").text() == ""){
                $.ajax({
                url: "/api/sell/" + Main.trade_pair+"?market=1",
                type: "POST",
                data: data,
                dataType: "json",
                success: function(f) {
                    if (f.status == true) {
                        thinking_alert();
                        setTimeout(Main.deal_order_status, 800, f["order_id"]);
                        Main.clear_sell_form()
                        return
                    }
                    if (f.status == "process_order_error") {
                        my_alert(f.description);
                        return
                    }
                    if (f.status == "incifition_funds") {
                        my_alert(f.description);
                        return
                    }
                    if (f.status == "processed") {
                        my_alert(f.description);
                        Main.clear_sell_form();
                        return
                    }
                    if (f.status == "part_processed") {
                        my_alert(f.description);
                        Main.clear_sell_form();
                        return
                    }
                    my_alert("Не могу создать ордер, проверьте пожайлуста данный и попробуйте снова");
                }
            });
        }else {
            var modalWnd = $("#exampleModal_sell");
            $("#modal_sell_sum").text(orderCount);
            $("#modal_sell_result").text($("#sell_market_help").val() - $("#sell_market_comission").text());
            $("#modal_sell_disperse").text($("#sell_market_result").text());
            $("#modal_sell_comission").text($("#sell_market_comission").text());
            $("#modal_sell_percent").text(Main.percentOfMarket*100 + "%");
            modalWnd.modal('show');
            $("#proceed_sell").on('click', function(){
                console.log("continue");
                $.ajax({
                    url: "/api/sell/" + Main.trade_pair + "?market=1",
                    type: "POST",
                    data: data,
                    dataType: "json",
                    success: function(f) {
                        if (f.status == true) {
                            thinking_alert();
                            setTimeout(Main.deal_order_status, 800, f["order_id"]);
                            $("#sell_market_count").val("0");
                            $("#sell_market_help").html("Нажмите посчитать, чтобы рассчитать сумму в соответствии с ордерами.");
                            return
                        }
                        if (f.status == "process_order_error") {
                            my_alert(f.description);
                            return
                        }
                        if (f.status == "incifition_funds") {
                            my_alert(f.description);
                            return
                        }
                        if (f.status == "processed") {
                            my_alert(f.description);
                            $("#sell_market_count").val("0");
                            $("#sell_market_help").html("Нажмите посчитать, чтобы рассчитать сумму в соответствии с ордерами.");
                            return
                        }
                        if (f.status == "part_processed") {
                            my_alert(f.description);
                            $("#sell_market_count").val("0");
                            $("#sell_market_help").html("Нажмите посчитать, чтобы рассчитать сумму в соответствии с ордерами.");
                            return
                        }
                        my_alert("Не могу создать ордер, проверьте пожайлуста данный и попробуйте снова");
                    }
                });
                modalWnd.modal('hide');
            });
        }
    },
    calc_order: function(d) {
        var g = "#" + d + "_count";
        var c = "#" + d + "_price";
        var f = "#" + d + "_result";
        var a = "#" + d + "_comission";
        var b = $(g).val();
        var e = $(c).val();
        console.log("d:     " + d + "\nb:   " + b + "\ne:   " + e);
        if (b < Main.min_deal) {
            if (d == "buy") {
                $("#buy_help").html("К сожалению сумма сделки меньше минимальной возможной");
            } else {
                $("#sell_help").html("К сожалению сумма сделки меньше минимальной возможной");
            }
            return
        }
        var h = e * b;
        $(f).html(Main.format_float8(h));
        Main.val_eq_to_usd(h, d + "_result_usd_eq");
        if (d == "buy") {
            var i = b * Main.comission;
            $(a).html(Main.format_float8(i));
            $("#buy_help").html("Вы получаете  " + Main.format_float8(b - i) + " " + Main.currency_on)
        } else {
            var i = h * Main.comission;
            $(a).html(Main.format_float8(i));
            $("#sell_help").html("Вы получаете  " + Main.format_float8(h - i) + " " + Main.currency_base)
        }
    },
    calc_order_market: function(action) {
        if(action == "sell_market"){
            return Main.calc_order_market_sell();
        }else{
            return Main.calc_order_market_buy();
        }
    },
    calc_order_market_sell: function()
    {
        var sumId = "#sell_market_count";
        var comissionId = "#sell_market_comission";
        var resultId = "#sell_market_result";
        var sumValue = parseFloat($(sumId).val());
        var buy_list = Main.buy_list_objects;

        if (!sumValue||sumValue<0) {
            $(sumId).val("");
            $("#sell_market_help").html("Введите корректное значение в поле суммы");
            return
        }
        $(sumId).val( sumValue) ;

        var minDealValue = Main.min_deal;

        $("#sell_market_help").empty();

        if (sumValue < minDealValue) {
            $("#sell_market_help").html("К сожалению сумма сделки меньше минимальной возможной для продажи по рынку");
            return
        }

        var counterSum = 0;
        var avarage_rate = 0;
        var getValueSum = 0;
        var comissionValue = 0;
        var last_rate = 0;
        var currency2ValueSpent = 0;
        var currency1ValueBuy = 0;
        var start_rate = 0;
                       
        if(buy_list.length){
             start_rate =  buy_list[0].price*1;
        }else
        {
            $("#sell_market_help").html("К сожалению пока рынка нет");
            return false;
        }                

        for (var i = 0; i < buy_list.length; i++) {
            currency2ValueSpent = +buy_list[i].currency_trade;
            currency1ValueBuy = +buy_list[i].currency_base;
            last_rate = buy_list[i].price;
            if (counterSum + currency2ValueSpent > sumValue) {
                var currency2ValueSpentTemp = (sumValue - counterSum) //tail sum
                getValueSum += (currency2ValueSpentTemp/currency2ValueSpent) * currency1ValueBuy;
                comissionValue = getValueSum * Main.comission;
                avarage_rate += last_rate * (currency2ValueSpentTemp / sumValue);
                break;
            }else {
                counterSum += currency2ValueSpent;
                getValueSum += currency1ValueBuy;
                avarage_rate += last_rate * (currency2ValueSpent / sumValue);
            }
            comissionValue = getValueSum * Main.comission;

        }

        Main.val_eq_to_usd(avarage_rate, "sell_market_result_usd_eq");
        $(resultId).html(avarage_rate);
        $(resultId).val(last_rate*1 - 0.00000001);//float correction :(
        $("#sell_market_help").html("Вы получаете  &asymp;&nbsp;" + Main.format_float8(getValueSum - comissionValue) + " " + Main.currency_base);
        $("#sell_market_help").val(Main.format_float8(getValueSum));
        $("#sell_count").val(sumValue);//copy value to another from
        $("#sell_price").val(avarage_rate);
        $(comissionId).html(Main.format_float12(comissionValue));
        if (sumValue > Main.sell_list_sum) {
            $("#sell_market_warning").html("Вы закроете все ордера на рынке, <strong>цена  не выгодна</strong>, и будет создан ордер на остаток суммы по последней цене!");
        }else if((1-last_rate/start_rate)>Main.percentOfMarket) {
            $("#sell_market_warning").html("Эта сделка включает заявки, которые меньше верхней цены рынка на  <strong>" + Main.percentOfMarket*100 + "%</strong> !");
        }else {
            $("#sell_market_warning").empty();
        }

    },
    calc_order_market_buy:function(){
        var sumId = "#buy_market_count";
        var comissionId = "#buy_market_comission";
        var resultId = "#buy_market_result";
        var sumValue = parseFloat($(sumId).val());
        var sell_list = Main.sell_list_objects;

        if (!sumValue||sumValue<0) {
            $("#buy_market_help").html("Введите корректное значение в поле суммы");
            $(sumId).val("");

            return
        }
        $(sumId).val(Main.format_float12(sumValue));

        var minDealValue = $("#buy_min_price").text()*Main.min_deal;

        $("#buy_market_help").empty();

        if (sumValue < minDealValue) {
            $("#buy_market_help").html("К сожалению сумма сделки меньше минимальной возможной для покупки по рынку");
            return
        }

        var counterSum = 0;
        var avarage_rate = 0;
        var getValueSum = 0;
        var comissionValue = 0;
        var currency2ValueSpent = 0;
        var currency1ValueBuy = 0;
        var last_rate = 0;
        var start_rate = 0;
        if(sell_list.length){
            start_rate = sell_list[0].price*1;
        }else
        {
            $("#buy_market_help").html("К сожалению пока рынка нет");
            return false
        }                 

        for (var i = 0; i < sell_list.length; i++) {
            currency2ValueSpent = +sell_list[i].currency_base;
            currency1ValueBuy = +sell_list[i].currency_trade;
            last_rate = sell_list[i].price;
            if (counterSum + currency2ValueSpent > sumValue) {
                var currency2ValueSpentTemp = (sumValue - counterSum) //tail sum
                getValueSum += (currency2ValueSpentTemp/currency2ValueSpent) * currency1ValueBuy;
                comissionValue = getValueSum * Main.comission;
                avarage_rate += last_rate * (currency2ValueSpentTemp / sumValue);
                break;
            }else {
                counterSum += currency2ValueSpent;
                getValueSum += currency1ValueBuy;
                avarage_rate += last_rate * (currency2ValueSpent / sumValue);
            }
            comissionValue = getValueSum * Main.comission;

        }

        Main.val_eq_to_usd(avarage_rate, "buy_market_result_usd_eq");
        $(resultId).html(avarage_rate);
        $(resultId).val(last_rate*1 + 0.00000001);//float correction;
        $("#buy_market_help").html("Вы получаете  &asymp;&nbsp;" + Main.format_float8(getValueSum - comissionValue) + " " + Main.currency_on);
        $("#buy_market_help").val(Main.format_float8(getValueSum));
        $("#buy_count").val(getValueSum);//copy value to another from
        $("#buy_price").val(avarage_rate);

        $(comissionId).html(Main.format_float12(comissionValue));
        if (i == sell_list.length) {
            $("#buy_market_warning").html("Вы закроете все ордера на рынке, <strong>цена  не выгодна</strong>, и будет создан ордер на остаток суммы по последней цене!");
        }else if((1-start_rate/last_rate)>Main.percentOfMarket) {
            $("#buy_market_warning").html("Эта сделка включает заявки, которые меньше верхней цены рынка на  <strong>" + Main.percentOfMarket*100 + "%</strong> !");
        }else {
            $("#buy_market_warning").empty();
        }



    },
    calc_over: function(b) {
        var c = b.innerHTML;
        var a = $("#buy_price").val();
        $("#buy_market_count").val(Main.format_float8(c));
        $("#buy_count").val(Main.format_float8(c / a));
    },
    calc_straight: function(a) {
        var b = a.innerHTML;
        $("#sell_count").val(b);
        $("#sell_market_count").val(b);
    },
    format_float6: function(b) {
        if (b < 0.001) {
            return Main.format_float8(b)
        }
        var a = b * 1000000;
        return Math.floor(a) / 1000000
    },
    format_float2: function(b) {
        if (b < 0.01) {
            return 0
        }
        var a = b * 100;
        return Math.floor(a) / 100
    },
    format_float4: function(b) {
        if (b < 0.01) {
            return Main.format_float6(b)
        }
        var a = b * 1000;
        return Math.floor(a) / 1000
    },
    format_float8: function(b) {
        if (b < 0.00001) {
            return Main.format_float12(b)
        }
        var a = b * 100000000;
        return Math.floor(a) / 100000000
    },
    format_float12: function(b) {
        return b;
        var a = b * 10000000000;
        return Math.floor(a) / 10000000000 + ""
    },
    drawVisualization: function() {
        var b = screen.width;
        var c = {
            1280: 800,
            1600: 945,
            1360: 800,
            1920: 1038
        };
        var a = c[b];
        if (!a) {
            a = 800
        }
        $.ajax({
            url: "/api/japan_stat/" + Main.trade_pair,
            type: "GET",
            dataType: "json",
            success: function(e) {
                console.log(e.trades);
                var g = google.visualization.arrayToDataTable(e.trades, true);
                $("#online_users").html(e.online);
                $("#volume_base").html(e.volume_base);
                $("#volume_trade").html(e.volume_trade);
                var d = {
                    legend: "none",
                    width: a,
                    height: 250,
                    fontSize: 10,
                    chartArea: {
                        width: a - 200,
                        height: 150
                    },
                    colors: ["#515151", "#515151"],
                    candlestick: {
                        fallingColor: {
                            fill: "#0ab92b",
                            stroke: "green",
                            strokeWidth: 1
                        },
                        risingColor: {
                            fill: "#f01717",
                            stroke: "#d91e1e",
                            strokeWidth: 1
                        },
                        hollowIsRising: true
                    },
                    hAxis: {
                        maxValue: 100
                    },
                    series: {
                        0: {
                            type: "candlesticks"
                        },
                        1: {
                            type: "bars",
                            targetAxisIndex: 1,
                            color: "#ebebeb"
                        }
                    },
                };
                var f = new google.visualization.CandlestickChart(document.getElementById("chart_trade"));
                f.draw(g, d)
            }
        })
    },
    draw_highcharts: function() {
        var b = screen.width;
        var c = {};
        var a = c[b];
        console.log("screen with" + b);
        a = $("#chart_trade").parent().width();
        $("#chart_trade").css({
            "width": "100%"
        });
        $.ajax({
            url: "/api/japan_stat/high/" + Main.trade_pair + "?_" + Date(),
            type: "GET",
            dataType: "json",
            success: highchart_candle,
            error: function(d) {
                console.log(d);
                setTimeout(Main.draw_highcharts, 4000)
            }
        })
    },
    highcharts_thema_enable: function() {
        if (Main.highcharts_enabled) {
            return true
        }
        Highcharts.createElement("link", {
            href: "https://fonts.googleapis.com/css?family=Signika:400,700",
            rel: "stylesheet",
            type: "text/css"
        }, null, document.getElementsByTagName("head")[0]);
        Highcharts.wrap(Highcharts.Chart.prototype, "getContainer", function(a) {
            a.call(this);
            this.container.style.background = "url(https://btc-trade.com.ua/img/sand.png)"
        });
        Highcharts.theme = {
            colors: ["gray", "#8085e9", "#8d4654", "#7798BF", "#aaeeee", "#ff0066", "#eeaaee", "#55BF3B", "#DF5353", "#7798BF", "#aaeeee"],
            chart: {
                backgroundColor: null,
                style: {
                    fontFamily: "Signika, serif"
                }
            },
            title: {
                style: {
                    color: "black",
                    fontSize: "16px",
                    fontWeight: "bold"
                }
            },
            subtitle: {
                style: {
                    color: "black"
                }
            },
            tooltip: {
                borderWidth: 0
            },
            legend: {
                itemStyle: {
                    fontWeight: "bold",
                    fontSize: "13px"
                }
            },
            xAxis: {
                labels: {
                    style: {
                        color: "#6e6e70"
                    }
                }
            },
            yAxis: {
                labels: {
                    style: {
                        color: "#6e6e70"
                    }
                }
            },
            plotOptions: {
                series: {
                    shadow: true
                },
                candlestick: {
                    lineColor: "#404048",
                    color: "#f01717",
                    upColor: "#43ac6a"
                },
                map: {
                    shadow: false
                }
            },
            navigator: {
                xAxis: {
                    gridLineColor: "#D0D0D8"
                }
            },
            rangeSelector: {
                buttonTheme: {
                    fill: "white",
                    stroke: "#C0C0C8",
                    "stroke-width": 1,
                    states: {
                        select: {
                            fill: "#D0D0D8"
                        }
                    }
                }
            },
            scrollbar: {
                trackBorderColor: "#C0C0C8"
            },
            background2: "#E0E0E8"
        };
        Highcharts.setOptions(Highcharts.theme);
        Highcharts.setOptions({
            global: {
                useUTC: false
            },
            lang: {
                loading: "Загружаем",
                months: ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июдь", "Авгут", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"],
                weekdays: ["Воскресенье", "Понедельник", "Вторник", "Среда", "Четверг", "Пятьница", "Суббота"],
                shortMonths: ["Янв", "Фев", "Мар", "Апр", "Май", "Июн", "Июль", "Авг", "Сент", "Окт", "Ноя", "Дек"],
                exportButtonTitle: "Экспортировать",
                printButtonTitle: "Печать",
                rangeSelectorFrom: "С",
                rangeSelectorTo: "По",
                rangeSelectorZoom: "Период",
                downloadPNG: "Скачать в  PNG",
                downloadJPEG: "Скачать в  JPEG",
                downloadPDF: "Скачать PDF",
                downloadSVG: "Скачать SVG"
            }
        });
        Main.highcharts_enabled = true
    },
    confirm_operation_privatkey: function() {
        var b = $("#key_type").val();
        var a = $("#key").val();
        var d = $("#id_pin").val();
        var c = {
            key: a,
            key_type: b,
            pin: d
        };
        $.ajax({
            url: "/profile/private_key",
            type: "POST",
            data: c,
            error: function(e) {
                my_alert("Авторизация не прошла")
            },
            success: function(e) {
                $("#home").html((e))
            }
        })
    },
    confirm_g2a_privatkey: function(c) {
        var b = $("#key_type").val();
        var a = $("#key").val();
        var d = {
            key: a,
            key_type: b,
            g2a_session: c
        };
        $.ajax({
            url: "/profile/private_key",
            type: "POST",
            data: d,
            error: function(e) {
                my_alert("Авторизация не прошла")
            },
            success: function(e) {
                $("#home").html((e))
            }
        })
    }
};
var Stock = {
    current_index: null,
    btce_serias_ask: null,
    btce_serias_bid: null,
    btce_serias_vol: null,
    sel_button: null,
    foreign_stock_name: null,
    foreign_stock: function(a, c, b) {
        if (a == "btc_e" && c == "btc_uah") {
            $("#chart_trade").highcharts().destroy();
            $("#stocks_trades .current_stock").
            removeClass("btn-success").removeClass("current_stock").addClass("btn-default");
            $(b).addClass("btn-success").addClass("current_stock");
            Stock.draw_btce_stock("btc_usd");
            return
        }
        if (a == "btc_e" && c == "ltc_uah") {
            $("#chart_trade").highcharts().destroy();
            $("#stocks_trades .current_stock").removeClass("btn-success").removeClass("current_stock").addClass("btn-default");
            $(b).addClass("btn-success").addClass("current_stock");
            Stock.draw_btce_stock("ltc_usd");
            return
        }
        if (a == "btc_e" && c == "nvc_uah") {
            $("#chart_trade").highcharts().destroy();
            $("#stocks_trades .current_stock").removeClass("btn-success").removeClass("current_stock").addClass("btn-default");
            $(b).addClass("btn-success").addClass("current_stock");
            Stock.draw_btce_stock("nvc_usd");
            return
        }
        my_alert("Еще немного и будет сделано, терпение")
    },
    own: function(a) {
        $("#chart_trade").highcharts().destroy();
        $("#stocks_trades .current_stock").removeClass("btn-success").removeClass("current_stock").addClass("btn-default");
        $(a).removeClass("btn-default").addClass("btn-success").addClass("current_stock");
        Main.draw_highcharts()
    },
    draw_btce_stock: function(a) {
        Stock.foreign_stock_name = a;
        $.ajax({
            url: "/foreign/stock/btce/" + a + "/minute/0",
            type: "GET",
            dataType: "json",
            success: draw_btce_stock
        })
    },
    update_btce_stock: function() {
        console.log(Stock.foreign_stock_name);
        $.ajax({
            url: "/foreign/stock/btce/" + Stock.foreign_stock_name + "/minute/" + Stock.current_index,
            type: "GET",
            dataType: "json",
            success: function(b) {
                Stock.current_index = b.last;
                console.log(Stock.current_index);
                var c = b.data_ask;
                for (var a = 0; a < c.length; a++) {
                    Stock.btce_serias_ask.addPoint([c[a][0], c[a][1]], true, true)
                }
                c = b.data_bid;
                for (var a = 0; a < c.length; a++) {
                    Stock.btce_serias_bid.addPoint([c[a][0], c[a][1]], true, true)
                }
                c = b.data_vol;
                for (var a = 0; a < c.length; a++) {
                    Stock.btce_serias_vol.addPoint([c[a][0], c[a][1]], true, true)
                }
            }
        })
    }
};

function draw_btce_stock(a) {
    Stock.current_index = a.last;
    $("#chart_trade").highcharts("StockChart", {
        chart: {
            events: {
                load: function() {
                    Stock.btce_serias_ask = this.series[0];
                    Stock.btce_serias_bid = this.series[1];
                    Stock.btce_serias_vol = this.series[2];
                    setInterval(Stock.update_btce_stock, 5000)
                }
            }
        },
        rangeSelector: {
            buttons: [{
                count: 1,
                type: "day",
                text: "1d"
            }, {
                count: 5,
                type: "day",
                text: "5d"
            }, {
                type: "all",
                text: "All"
            }],
            inputEnabled: false,
            selected: 0
        },
        title: {
            text: "Торги BTC-e  Биткоин к USD"
        },
        exporting: {
            enabled: false
        },
        yAxis: [{
            labels: {
                align: "right",
                x: -3
            },
            title: {
                text: "Продажа"
            },
            height: "60%",
            plotOptions: {
                series: {
                    compare: "percent"
                }
            },
            tooltip: {
                pointFormat: '<span style="color:{series.color}">{series.name}</span>: <b>{point.y}</b> ({point.change}%)<br/>',
                valueDecimals: 2
            },
            lineWidth: 2
        }, {
            labels: {
                align: "right",
                x: -3
            },
            title: {
                text: "Покупка"
            },
            plotOptions: {
                series: {
                    compare: "percent"
                }
            },
            tooltip: {
                pointFormat: '<span style="color:{series.color}">{series.name}</span>: <b>{point.y}</b> ({point.change}%)<br/>',
                valueDecimals: 2
            },
            height: "60%",
            lineWidth: 2
        }, {
            labels: {
                align: "right",
                x: -3
            },
            title: {
                text: "Volume"
            },
            top: "65%",
            height: "35%",
            offset: 0,
            lineWidth: 2
        }, ],
        series: [{
            name: "Продажа",
            data: a.data_ask
        }, {
            name: "Покупка",
            data: a.data_bid
        }, {
            type: "column",
            name: "Объем",
            yAxis: 2,
            data: a.data_vol
        }]
    })
}

function highchart_candle(c) {
    Main.highcharts_thema_enable();
    $("#online_users").html(c.online);
    $("#volume_base").html(c.volume_base);
    $("#volume_trade").html(c.volume_trade);
    var f = c.trades;
    Highcharts.setOptions(Highcharts.theme);
    var d = [],
        e = [],
        g = f.length;
    for (var b = 0; b < g; b++) {
        d.push([f[b][0], f[b][1], f[b][2], f[b][3], f[b][4]]);
        e.push([f[b][0], f[b][5]])
    }
    var a = [
        ["week", [1]],
        ["month", [1, 2, 3, 4, 6]]
    ];
    $("#chart_trade").highcharts("StockChart", {
        rangeSelector: {
            buttons: [{
                type: "day",
                count: 1,
                text: "1d"
            }, {
                type: "week",
                count: 1,
                text: "1w"
            }, {
                type: "month",
                count: 1,
                text: "1m"
            }, {
                type: "month",
                count: 3,
                text: "3m"
            }, {
                type: "month",
                count: 6,
                text: "6m"
            }, {
                type: "year",
                count: 1,
                text: "1y"
            }],
            inputEnabled: $("#chart_trade").width() > 480,
            selected: 4
        },
        title: {
            text: "Торги"
        },
        yAxis: [{
            labels: {
                align: "right",
                x: -3
            },
            title: {
                text: "Котировки"
            },
            height: "60%",
            lineWidth: 2
        }, {
            labels: {
                align: "right",
                x: -3
            },
            title: {
                text: "Объем"
            },
            top: "65%",
            height: "35%",
            offset: 0,
            lineWidth: 2
        }],
        series: [{
            type: "candlestick",
            name: "Торги",
            data: d,
            dataGrouping: {
                enable: false
            }
        }, {
            type: "column",
            name: "Объем",
            data: e,
            yAxis: 1,
            dataGrouping: {
                enable: false
            }
        }]
    })
}
function getUrlParameter(name) {
    name = name.replace(/[\[]/, '\\[').replace(/[\]]/, '\\]');
    var regex = new RegExp('[\\?&]' + name + '=([^&#]*)');
    var results = regex.exec(location.search);
    return results === null ? '' : decodeURIComponent(results[1].replace(/\+/g, ' '));
};

var thinking_syncing = 0;

function thinking_alert() {
    my_alert("<img src='/static/processing.gif'><br/><h4>Думаю...</h4>");

}
function main_hide_thinking_alert(){
    var $modal = $("#modal_dlg");
    if(thinking_syncing == 1){
        $modal.modal('hide');
    }else{
        thinking_syncing = 2;
    }

}

 $(document).ready(function(){

    var modal = $("#modal_dlg");
    modal.on('shown.bs.modal', function (e) {
        if(thinking_syncing==0){
            thinking_syncing=1;
        }
        if(thinking_syncing==2){
            // ok close it quickly
            modal.modal('hide');
        }
    });
    modal.on('hide.bs.modal', function (e) {
        thinking_syncing=3;
    });
    modal.on('hidden.bs.modal', function (e) {
        thinking_syncing=0;
    });


    });


function hide_modal(a) {
    $("#" + a).modal("hide");
}

function my_alert(a) {
    $("#modal_msg").html(a);
    $("#modal_dlg").modal("show");
};

function checkMoon(card_number) {
  var arr = [];
  for(var i = 0; i < card_number.length; i++) {
    if(i % 2 === 0) {
      var m = parseInt(card_number[i]) * 2;
      if(m > 9) {
        arr.push(m - 9);
      } else {
        arr.push(m);
      }
    } else {
        var n = parseInt(card_number[i]);
        arr.push(n)
      }
  }

  var summ = (arr.length == 16)
      ? arr.reduce(function(a, b) { return a + b; })
      : 1;
  return Boolean(!(summ % 10));
}
