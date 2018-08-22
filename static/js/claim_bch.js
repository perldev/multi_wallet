
var finance_claim={
    claim_bch_deposit :function(Currency){
         $.ajax({
                                    url : "/finance/claim_bch",
                                    type : 'GET',
                                    cache: false,
                                    error: function (data) {
                                          my_alert("По всей видимости мы вам уже вернули BCH");
                                    },
                                    success : function(Data){
                                              var balance = Data["balance"];
                                              $("#bch_balance_claim").html(balance);
                                              $("#bch_claim").modal("show");      

                                        }
                                    });



   },
   approve: function(){

                              $('#bch_claim').modal('hide');
                              thinking_alert(); 					
                              $.ajax({
                                    url : "/finance/approve_claim_bch",
                                    type : 'GET',
                                    cache: false,
                                    error: function (data) {
                                          hide_modal("modal_dlg");
                                          my_alert("По всей видимости мы вам уже вернули BCH");
                                    },
                                    success : function(Data){
                                            hide_modal("modal_dlg");
                                            my_alert("Ваш баланс начислен");
                                            window.location.reload();
                                        }
                                    });
   }
   

}


