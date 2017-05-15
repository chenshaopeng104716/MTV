/**
 * Created by Administrator on 2017/5/9.
 */

$(document).ready(function () {
     var authority=$("#authority").val();
       //alert("权限:"+authority);
     if (authority!="全平台")
     {
           /// alert(11);
            $("#allplatform").attr("href","#");
            $("#allplatform").parent().removeClass("active");
             $("#channel_list").addClass("active");
         $("a[name='channel']").each(function ()
         {
             var txt = $(this).html();
             if (authority != txt)
             {
                  $(this).attr("href","#");
             }
         });
            //$("#allplatform").hide();

     }
     else
         {
             // alert(authority);
         }
            //参数设置，若用默认值可以省略以下面代
    toastr.options = {
        "closeButton": false, //是否显示关闭按钮
        "debug": false, //是否使用debug模式
        "positionClass": "toast-top-full-width",//弹出窗的位置
        "showDuration": "300",//显示的动画时间
        "hideDuration": "500",//消失的动画时间
        "timeOut": "500", //展现时间
        "extendedTimeOut": "1000",//加长展示时间
        "showEasing": "swing",//显示时的动画缓冲方式
        "hideEasing": "linear",//消失时的动画缓冲方式
        "showMethod": "fadeIn",//显示时的动画方式
        "hideMethod": "fadeOut" //消失时的动画方式
        };



             $("#allplatform").click(function () {
                var authority=$("#authority").val();
               if (authority!="全平台")

               {
                    toastr.options.positionClass = 'toast-center-center';
                      toastr.warning('没有权限');
               }
        })

            $("#show").click(function () {
                var authority=$("#authority").val();
               if (authority!="全平台")
               {
                  if($("#show").html()!=authority)
                  {
                      toastr.options.positionClass = 'toast-center-center';
                      toastr.warning('没有权限');
                  }
               }
        })
      $("#tv").click(function () {
                var authority=$("#authority").val();
               if (authority!="全平台")
               {
                  if($("#tv").html()!=authority)
                  {
                     toastr.options.positionClass = 'toast-center-center';
                      toastr.warning('没有权限');
                  }
               }
        })
      $("#movie").click(function () {
                var authority=$("#authority").val();
               if (authority!="全平台")
               {
                  if($("#movie").html()!=authority)
                  {
                      toastr.options.positionClass = 'toast-center-center';
                      toastr.warning('没有权限');
                  }
               }
        })
      $("#cartoon").click(function () {
                var authority=$("#authority").val();
               if (authority!="全平台")
               {
                  if($("#cartoon").html()!=authority)
                  {
                      toastr.options.positionClass = 'toast-center-center';
                      toastr.warning('没有权限');

                  }
               }
        })
});



// $(document).ready(function () {
//
//      var authority=$("#authority").val();
//        //alert("权限:"+authority);
//      if (authority!="全平台")
//      {
//             $("#allplatform").addClass("notclick");
//             $("#allplatform").parent().removeClass("active");
//              $("#channel_list").addClass("active");
//          $("a[name='channel']").each(function ()
//          {
//              var txt = $(this).html();
//              // $(this).removeClass("notclick");
//              if (authority != txt)
//              {
//                   //  alert(txt);
//                  // $("#this").parent().hide();
//                  //  $("#this").attr("visible", false);
//                  $(this).addClass("notclick");
//              }
//          });
//             //$("#allplatform").hide();
//
//      }
//      else
//          {
//              // alert(authority);
//          }
//
//              $("#allplatform").click(function () {
//                 var authority=$("#authority").val();
//                if (authority!="全平台")
//
//                {
//                     alert("没有权限");
//                }
//         })
// });