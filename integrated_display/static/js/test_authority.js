/**
 * Created by Administrator on 2017/5/10.
 */
/**
 * Created by Administrator on 2017/5/9.
 */

$(document).ready(function () {
     var authority=$("#authority").val();
       alert("权限:"+authority);
     if (authority!="全平台")
     {
            alert(11);
            $("#allplatform").attr("href","#");
            $("#allplatform").parent().removeClass("active");
             $("#channel_list").addClass("active");
         $("a[name='channel']").each(function ()
         {
             var txt = $(this).html();
             if (authority != txt)
             {
                  $("#this").attr("href","#");
             }
         });
            //$("#allplatform").hide();

     }
     else
         {
             // alert(authority);
         }

             $("#allplatform").click(function () {
                var authority=$("#authority").val();
               if (authority!="全平台")

               {
                    alert("没有权限");
               }
        })

           $("#show").click(function () {
                var authority=$("#authority").val();
               if (authority!="全平台")
               {
                  if($("#show").html()!=authority)
                  {
                      alert("没有权限");
                  }
               }
        })
      $("#tv").click(function () {
                var authority=$("#authority").val();
               if (authority!="全平台")
               {
                  if($("#tv").html()!=authority)
                  {
                      alert("没有权限");
                  }
               }
        })
      $("#movie").click(function () {
                var authority=$("#authority").val();
               if (authority!="全平台")
               {
                  if($("#show").html()!=authority)
                  {
                      alert("没有权限");
                  }
               }
        })
      $("#cartoon").click(function () {
                var authority=$("#authority").val();
               if (authority!="全平台")
               {
                  if($("#show").html()!=authority)
                  {
                      alert("没有权限");
                  }
               }
        })
});