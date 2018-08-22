var profile = {
  user_setting: function(a, c) {
    var b = "";
    if (c.checked) {
      b = "yes";
      $.ajax({
        url: "/profile/settings/" + a + "/" + b,
        type: "GET",
        dataType: "json",
        error: function(d) {
          c.checked = true;
          Login.delete_g2a_session()
        },
        success: function(d) {
          if (!d.status) {
            my_alert("Что-то пошло не так, сообщите на support@btc-trade.com.ua  ");
            c.checked = false
          } else {
            c.checked = true;
            my_alert("Настройки сохранены")
          }
        }
      })
    } else {
      b = "no";
      $.ajax({
        url: "/profile/settings/" + a + "/" + b,
        type: "GET",
        dataType: "json",
        error: function(d) {
          c.checked = true;
          Login.delete_g2a_session()
        },
        success: function(d) {
          if (!d.status) {
            my_alert("Что-то пошло не так, сообщите на support@btc-trade.com.ua  ");
            c.checked = true
          } else {
            c.checked = false;
            my_alert("Настройки сохранены")
          }
        }
      })
    }
  },
  user_g2a: function(a, c) {
    var b = "";
    if (!c.checked) {
      c.checked = true;
      var d = function(e) {
        $.ajax({
          url: "/profile/settings/g2a/no",
          type: "GET",
          dataType: "json",
          error: function(f) {
            c.checked = true;
            Login.delete_g2a_session()
          },
          success: function(f) {
            if (!f.status) {
              my_alert(f.ru_description);
              c.checked = true
            } else {
              c.checked = false;
              my_alert("Двухфакторная авторизация выключена")
            }
          }
        })
      };
      return Login.start_f2a_for_custom(d)
    }
    $("#g2a_pwd").val("");
    $.ajax({
      url: "/profile/setup_g2a",
      type: "GET",
      dataType: "json",
      error: function(e) {
        my_alert("Что-то пошло не так, сообщите на support@btc-trade.com.ua  ");
        c.checked = false
      },
      success: function(e) {
        $("#g2a_private_key32").val(e.g2a_private_key32);
        $("#g2a_private_key").val(e.g2a_private_key);
        $("#g2a_qr").attr("src", e.g2a_qr);
        $("#f2a_dlg").modal("show");
        c.checked = false
      }
    })
  },
  check_g2a: function() {
    var b = document.getElementById("g2a_setting");
    var a = $("#g2a_pwd").val();
    $.ajax({
      url: "/profile/setup_g2a_verify/" + a,
      type: "GET",
      dataType: "json",
      error: function(c) {
        my_alert("Пароль не подходит!!!")
      },
      success: function(c) {
        $("#f2a_dlg").modal("hide");
        my_alert("Двухфакторная авторизация удачно установлена, теперь  \n                                          при следующей авторизации мы спросим у вас пароль из приложения. \n                                          Что бы отключить двухфакторную авторизацию достаточно снять флажок \n                                          в настройках вашего профиля.\n                                          ");
        b.checked = true
      }
    })
  },
  email_change: function() {
    var a = $("#email2change").val();
    thinking_alert();
    $.ajax({
      url: "/finance/email_change_make_request",
      type: "POST",
      data: {
        email: a
      },
      dataType: "json",
      error: function(b) {
        my_alert("Что-то пошло не так, сообщите на support@btc-trade.com.ua  ")
      },
      success: function(b) {
        if (b.status) {
          window.location.href = "/finance/common_secure_page/email_change_request/" + b.key
        } else {
          my_alert("Не получилось создать запрос на изменение электронной  почты, обратитесь пожайлуста в support@btc-trade.com.ua")
        }
      }
    })
  },
  reset_passwd: function() {
    $.ajax({
      url: "/profile/reset",
      type: "GET",
      dataType: "json",
      error: function(a) {
        my_alert("Что-то пошло не так, сообщите на support@btc-trade.com.ua  ")
      },
      success: function(a) {
        if (a.status) {
          my_alert("Новый пароль выслан на ваш электронный адрес")
        } else {
          my_alert("Не получилось обновить пароль, попробуйте позже")
        }
      }
    })
  }
};
