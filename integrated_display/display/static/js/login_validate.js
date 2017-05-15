/**
 * Created by Administrator on 2017/5/8.
 */
$(document).ready(function () {
    $("#username").focus();
    // $('#bt_login').attr('disabled',true);

    $('#bt_login').click(function()
    {
        if($('#username').val()=="")
         {
             toastr.options.positionClass = 'toast-center-center_1';
             toastr.info('用户名不能为空');
              $("#username").focus();
              return false;
         }
         else if($('#password').val()=="" )
        {
            toastr.options.positionClass = 'toast-center-center_2';
            toastr.info('密码不能为空');
            $("#password").focus();
            return false;
        }
        else
            {
                return true;
            }

    })


    $("#username").keypress(function ()
    {
      //  alert($("#error_message").html());
        $("#error_message").html("");

    })
    $("#password").keypress(function ()
    {
         $("#error_message").html("");
    })
    // $("#username").blur(function(){
    //
    //     if($('#username').val()=="")
    //     {
    //         //alert("用户名不能为空");
    //         // var ErrorMsg="用户名不能为空";
    //          toastr.options.positionClass = 'toast-center-center_1';
    //          toastr.info('用户名不能为空');
    //           $("#username").focus();
    //         // $('#username').append("<div style='color: red;'>"+ErrorMsg+"</div>");
    //     }
    //     if($('#password').val()=="" || $('#username').val()=="")
    //        {
    //              $('#bt_login').attr('disabled',true);
    //        }
    //        else
    //          {
    //              $('#bt_login').attr('disabled',false);
    //          }
    // })
    //
    //   $("#password").blur(function(){
    //
    //     if($('#password').val()=="")
    //     {
    //          toastr.options.positionClass = 'toast-center-center_2';
    //         toastr.info('密码不能为空');
    //         $("#password").focus();
    //     }
    //
    //       if(($('#password').val()=="") || ($('#username').val()==""))
    //    {
    //          $('#bt_login').attr('disabled',true);
    //    }
    //    else
    //      {
    //          $('#bt_login').attr('disabled',false);
    //      }
    // })

});
