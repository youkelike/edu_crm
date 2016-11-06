/**
 * Created by 81566 on 2016/11/6.
 */

$(function(){
    $('#btn-filter').on('click',function(){
        if($('.panel-body').hasClass('hide')){
            $('.panel-body').removeClass('hide')
        }else{
            $('.panel-body').addClass('hide')
        }
    })

})
