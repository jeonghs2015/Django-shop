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

// e : javascript event
// Order 내용을 생성해주는 함수
function AjaxCreateOrder(e) {
    // form이 submit 되는 현상을 막아줌
    e.preventDefault();
    var order_id = '';
    var request = $.ajax({
        method:'POST',
        url:order_create_url,
        async:false,         // 결제 과정이 꼬이지 않게 동기 과정으로 진행
        data:$('.order-form').serialize()
    });
    request.done(function(data){
        if(data.order_id) {
            order_id = data.order_id;
        }
    });
    request.fail(function(jqXHR, textStatus) {
        if(jqXHR.status == 404) {
            alert("페이지가 존재하지 않습니다.");
        }else if(jqXHR.status == 403) {
            alert("로그인해주세요");
        }else {
            alert("문제가 발생했습니다.\n다시 시도해주세요.");
        }
    });
    return order_id;
}