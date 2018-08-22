var Chat = {
  host_ws: "wss://btc-trade.com.ua/chat",
  id: "",
  container: "",
  session: "",
  is_delete: false,
  timer: null,
  ws: null,
  username: null,
  is_availible: true,
  mutex_busy: false,
  last_post: null,
  turnoff: function() {
    clearTimeout(Chat.timer);
    Chat.ws.close();
    Chat.is_availible = false
  },
  attach2chat: function(container) {
    Chat.container = container;
    if (!document.getElementById(container)) {
      console.log("container is not existed")
      return
    }
    Chat.ws = new WebSocket(Chat.host_ws);
    Chat.is_availible = true;
    Chat.ws.onopen = function() {
      console.log("Connected");
      Chat.timer = setInterval(Chat.ping, 3000)
    };
    Chat.ws.onmessage = function(evt) {
      var received_msg = evt.data;
      var myObject = eval("(" + received_msg + ")");
      console.log("Received: " + received_msg);
      if (myObject.status) {
        var size = myObject.new_messages.length;
        var messages = myObject.new_messages;
        var NewElements = "";
        for (var i = 0; i < size; i++) {
          var username = messages[i]["username"];
          var message = messages[i]["message"];
          var time = Main.format_time(messages[i]["time"]);
          var NewElement = "<tr style='background-color: #f9f9f9;' class='cursor' onclick=\"answer('" + username + "')\">";
          NewElement += "<td><strong>" + username + "</strong>:&nbsp;</td><td class='pull-right text-right'>" + time + "</td></tr><tr><td colspan='2'>";
          NewElement += message + "</td></tr>";
          NewElements += NewElement
        }
        $("#" + Chat.container).prepend(NewElements)
      }
    };
    Chat.ws.onclose = function() {
      Chat.is_availible = false;
      clearTimeout(Chat.timer);
      Chat.attach2chat(Chat.container)
    }
  },
  ping: function() {
    Chat.ws.send(JSON.stringify({
      ping: true
    }))
  },
  put_message: function(f) {
    if (!Chat.is_availible) {
      my_alert("Мы потеряли связь  с сервером Чата");
      return false
    }
    if (!Login.logged) {
      my_alert("Вы должны пройти процедуру авторизации, что бы писать в чат")
    }
    var h = Login.sessionid;
    if (Chat.last_post) {
      var e = new Date();
      e = e.getTime() - Chat.last_post.getTime();
      console.log("ofter " + e);
      if (e < 15000) {
        my_alert("Погодь не так часто, подумай что хочешь сказать");
        return
      }
    }
    Chat.last_post = new Date();
    var g = f;
    console.log("send " + g);
    Chat.ws.send(JSON.stringify({
      new_message: g,
      session: h
    }));
    return true
  }
};

function scroll_chat() {
  var f = $("#chat_wrapper").scrollTop();
  console.log("start scroll " + f);
  var h = f + $("#chat_wrapper").innerHeight();
  console.log("current scroll " + h);
  var e = $("#chat_wrapper")[0].scrollHeight;
  console.log(" scroll height " + e);
  var g = $("#chat_wrapper")[0];
  g.scrollTop = e
}

function send_message() {
  var b = $("#msg").val();
  if (b == "") {
    return
  }
  if (Chat.put_message(b)) {
    $("#msg").val("")
  }
}

function answer(d) {
  var c = $("#msg").val();
  if (c.indexOf(d) < 0) {
    c = d + "," + c;
  } else {
    return
  }
  $("#msg").focus();
  $("#msg").val(c)
}

function createCookie(j, i, h) {
  if (h) {
    var f = new Date();
    f.setTime(f.getTime() + (h * 24 * 60 * 60 * 1000));
    var g = "; expires=" + f.toGMTString()
  } else {
    var g = ""
  }
  document.cookie = escape(j) + "=" + escape(i) + g + "; path=/"
}

function readCookie(c) {
  var i = escape(c) + "=";
  var g = document.cookie.split(";");
  for (var j = 0; j < g.length; j++) {
    var h = g[j];
    while (h.charAt(0) == " ") {
      h = h.substring(1, h.length)
    }
    if (h.indexOf(i) == 0) {
      return unescape(h.substring(i.length, h.length))
    }
  }
  return null
}

function eraseCookie(b) {
  createCookie(b, "", -1)
};
