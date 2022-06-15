$(function(){
    var IMP=window.IMP;
    IMP.init('imp11166264');
    $('.order-form').on('submit', function(e) {
        var amount = parseFloat($('.order-form input[name="amount"]').val().replace(',',''));
        var type=$('.order-form input[name="type"]:checkout').val();
        var order_id = AjaxCreateOrder(e);
        if(order_id==false){
            alert('주문 생성 실패\n다시 시도해주세요.');
            return false;
        }

        var merchant_id = AjaxStoreTransaction(e, order_id, amount, type);

        if(merchant_id!=='') {
            IMP.request_pay({
                merchant_uid:merchant_id,
                name:'E-Shop product',
                buyer_name:$('input[name="first_name"]').val()+" "+$('input[name="last_name"]').val(),
                buyer_email:$('input[name="email"]'),
                amount:amount
            }, function(rsp) {
                if(rsp.success){
                    var msg = '결제가 완료되었습니다.';
                    msg += '고유 ID : '+rsp.imp_uid;
                    // 결제 완료 후 보여줄 메시지
                    ImpTransaction(e, order_id, rsp.merchant_uid, rsp.imp_uid, rsp.paid_amount);
                } else {
                    var msg = '결제에 실패하였습니다.';
                    msg += '에러내용 : ' + rsp.error_msg;
                    console.log(msg);
                }
            });
        }
        return false;
    });
});