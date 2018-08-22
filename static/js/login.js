var Login = {
        logged: false,
        after_redirect: false,
        custom_auth_action: null,
        use_f2a: false,
        api_tmp_key: "qwerty31_",
        sessionid: null,
        loginsign: "sdfjskldfjkls_asdfs",
        version: function() {
            return "beta3"
        },
        keyup: function(a) {
            if (a.keyCode == 13) {
                Login.try_login_page()
            }
        },
        f2a_keyup: function(a) {
            if (a.keyCode == 13) {
                Login.f2a_try_login()
            }
        },
        f2a_custom_keyup: function(a) {
            if (a.keyCode == 13) {
                Login.f2a_custom_action()
            }
        },
        login: function() {
            $("#login_form").show("fast")
        },
        try_login_page: function() {
            var a = $("#login_username").val();
            var c = $("#login_password").val();
            var b ="";
            if(Login.recaptcha_enable){
               var b = grecaptcha.getResponse();
               if (b == "") {
                  my_alert("А введите recaptch-у еще раз пожайлуста");
                  return
               }
            }
            Login.post_url = $("#post_url").val();
            Login.after_redirect = true;
            var d = {
                login: a,
                password: c,
                recaptcha_response_field: b,
            };
            

            Login.api_tmp_key = Main.rand_key;
            $.ajax({
                url: "/login?sign=" + Login.loginsign + "&_=" + Date(),
                data: d,
                beforeSend: function(){
                        thinking_alert_login();
                },
                complete: function(){
                        hide_thinking_alert("modal_dlg");
                },
                type: "POST",
                error: function(e) {
                    hide_thinking_alert("modal_dlg");
                    my_alert("Не могу авторизироваться, проверьте данные внимательно и повторите попытку");
                    if(Login.recaptcha_enable)
                        grecaptcha.reset()
                },
                success: function(f) {
                    console.log("start login for page");
                    var e = new RegExp("good");
                    if (e.test(f)) {
                        Login.logged = true;
                        if (Login.post_url && Login.post_url.length > 0) {
                            window.location.href = Login.post_url
                        } else {
                            window.location.href = "/finance/depmotion"
                        }
                        return
                    }
                    var e = new RegExp("captcha");
                    if (e.test(f)) {
                        if(Login.recaptcha_enable){
                            grecaptcha.reset();
                        }    
                        my_alert("Неверно введены слова с картинки!");
                        return
                    }
                    var e = new RegExp("2fa_");
                    if (e.test(f)) {
                        Login.f2a_start(f);
                        return
                    }

                    if(Login.recaptcha_enable){
                            grecaptcha.reset();
                    }  
                    my_alert("Не удалось авторизироваться, внимательно проверьте данные и попробуйте снова")
                }
            })
        },
        f2a_try_login: function() {
            var a = $("#f2a_password").val();
            var c = $("#f2a_session").val();
            var b = {
                key: c,
                password: a
            };
            Login.api_tmp_key = Main.rand_key;
            $.ajax({
                url: "/login_f2a?sign=" + Login.loginsign + "&_=" + Date(),
                data: b,
                type: "POST",
                beforeSend: function(){
                        thinking_alert_login();
                },
                complete: function(){
                        hide_thinking_alert("modal_dlg");
                },
                error: function(d) {
                    hide_thinking_alert("modal_dlg");
                    $("#f2a_password").val("");
                    my_alert("Не могу авторизироваться")
                },
                success: function(e) {
                    var d = new RegExp("good");
                    if (d.test(e)) {
                        Login.logged = true;
                        if (Login.after_redirect) {
                            if (Login.post_url && Login.post_url.length > 0) {
                                window.location.href = Login.post_url
                            } else {
                                window.location.href = "/stock"
                            }
                            return
                        } else {
                            $("#f2a_dlg_login").modal("hide");
                            Login.load_user_panel()
                        }
                        return
                    }
                    my_alert("Не удалось авторизироваться")
                },
                error: function(d) {
                    hide_thinking_alert("modal_dlg");
                    my_alert("Не могу авторизироваться")
                },
            })
        },
        f2a_start: function(a) {
            $("#f2a_session").val(a);
            $("#f2a_dlg_login").modal("show")
        },
        start_f2a_for_custom: function(a) {
            console.log(Login.use_f2a);
            if (Login.use_f2a) {
                Login.delete_g2a_session();
                $("#f2a_dlg_custom").modal("show");
                Login.custom_auth_action = a
            } else {
                a("f2a")
            }
        },
        f2a_custom_action: function() {
            var a = $("#f2a_custom_password").val();
            var b = {
                password: a
            };
            Login.api_tmp_key = Main.rand_key;
            $.ajax({
                url: "/login_f2a_operation?sign=" + Login.loginsign + "&_=" + Date(),
                data: b,
                type: "POST",
                error: function(c) {
                    console.log(c);
                    $("#f2a_custom_password").val("");
                    my_alert("Не могу авторизироваться")
                },
                success: function(c) {
                    $("#f2a_dlg_custom").modal("hide");
                    Login.setup_g2a_session(c);
                    Login.custom_auth_action(c)
                }
            })
        },
        setup_g2a_session: function(a) {
            $.cookie("g2a_session", a, {
                expires: 1,
                path: "/",
                secure: true
            })
        },
        delete_g2a_session: function() {
            $.removeCookie("g2a_session")
        },
        try_login: function() {
                if (!$("#captcha_slider_down").is(":visible")) {
                    $("#captcha_slider_down").slideDown("fast");
                    return
                }
                var a = $("#login_username").val();
                var c = $("#login_password").val();
                var b = grecaptcha.getResponse();
                if (b == "") {
                    my_alert("А введите recaptch-у еще раз пожайлуста");
                    return
                }
                thinking_alert_login();
                var d = {
                    login: a,
                    password: c,
                    recaptcha_response_field: b,
                };
                thinking_alert_login();
                Login.api_tmp_key = Main.rand_key;
                $.ajax({
                            url: "/login?sign=" + Login.loginsign + "&_=" + Date(),
                            data: d,
                            type: "POST",
                            success: function(f) {
                                    console.log("start login for index");
                                    var e = new RegExp("good");
                                    hide_thinking_alert("modal_dlg");
                                    
                                    if (e.test(f)) {
                                        Login.logged = true;
                                        Login.load_user_panel();
                                        return
                                    }
                                    var e = new RegExp("captcha");
                                    if (e.test(f)) {
                                        grecaptcha.reset();
                                        my_alert("Неверно введены слова с картинки!");
                                        return
                                    }
                                    var e = new RegExp("2fa_");
                                    if (e.test(f)) {
                                        Login.f2a_start(f);
                                        return
                                    }
                                    grecaptcha.reset();
                                    my_alert("Не удалось авторизироваться, внимательно проверьте данные и попробуйте снова ")},
                            error:function(e){
                                hide_thinking_alert("modal_dlg");
                                my_alert("Не удалось авторизироваться, внимательно проверьте данные и попробуйте снова ");
                                grecaptcha.reset()},
                     })
                     },
                     load_user_panel:function(){
                         $.ajax({url:"/user_panel/"+Main.trade_pair,
                                 type:"GET",
                                 success:function(b){
                                        var a=new RegExp("bad");
                                        if(a.test(b)){
                                               my_alert("Что - то пошло не так ")}
                                        else{
                                               $("#user_panel").html(b);
                                               $("#buy_button").attr("disabled",false);
                                               $("#sell_button").attr("disabled",false);
                                               Main.user_menu()
                                        }
                                 }
                                })
                    }
};


function thinking_alert_login(){
    var  a = "<img src='/static/processing.gif'><br/><h4>Думаю...</h4>";
    $("#modal_msg").html(a);
    $("#modal_dlg").css("disply","");
    
}
function hide_thinking_alert(){
    $("#modal_dlg").css("disply","none");
    
}
