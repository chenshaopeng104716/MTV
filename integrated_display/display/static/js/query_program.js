$(document).ready(function ()
{
       $.ajaxSetup({
                   data: {csrfmiddlewaretoken: '{{ csrf_token }}' },
              });
var selectedItem = -1;
var setSelectedItem = function(item){
    //更新索引变量
    selectedItem = item ;
    //按上下键是循环显示的，小于0就置成最大的值，大于最大值就置成
    var length=0;
    var  inputname = $('#search-text').val();
    var length1=$(document).find("li[name='program_list']").length-1;
    if (length1 >=0)
        length=length1;
    else
         length=$(document).find("li[name='program_list_ago']").length-1;
    if(selectedItem < 0)
    {
      selectedItem = length;
    }
    else if(selectedItem > length)
    {
      selectedItem = 0;
    }
}


$("#search-text").keyup(function(event) {
    var inputname = $('#search-text').val();
    var length=$(document).find("li[name='program_list']").length-1;
    //上
    if (event.keyCode == 38)
    {
        if (selectedItem == -1) {
            if (inputname != "" && length >=0) {
                selectedItem = $(document).find("li[name='program_list']").length - 1;
            }
             else
                 selectedItem=$(document).find("li[name='program_list_ago']").length-1;
        }
        else
        {
             setSelectedItem(selectedItem-1);

        }
         if(inputname!=""&&length>=0)
         {
             $('#search-text').val($(document).find("li[name='program_list']").eq(selectedItem).text());
             $(document).find("li[name='program_list']").removeClass('highlight_program').eq(selectedItem).addClass('highlight_program');
         }
             else
         {
             $('#search-text').val($(document).find("li[name='program_list_ago']").eq(selectedItem).text());
             $(document).find("li[name='program_list_ago']").removeClass('highlight_program').eq(selectedItem).addClass('highlight_program');
         }
    }

         //下
        else if(event.keyCode==40)
         {
              if (selectedItem == -1)
            {
                     selectedItem=0;
            }
            else
            {
                 setSelectedItem(selectedItem+1);
            }
                if(inputname!=""&&length>=0)
             {
                 $('#search-text').val($(document).find("li[name='program_list']").eq(selectedItem).text());
                 $(document).find("li[name='program_list']").removeClass('highlight_program').eq(selectedItem).addClass('highlight_program');
             }
                 else
             {
                 $('#search-text').val($(document).find("li[name='program_list_ago']").eq(selectedItem).text());
                 $(document).find("li[name='program_list_ago']").removeClass('highlight_program').eq(selectedItem).addClass('highlight_program');
             }
         }

         else
             {
                 selectedItem = -1;
             if (inputname) {
                 $(document).find("li[name='program_list_ago']").hide();
                 $.ajax({
                     'url': '/display/Fsearch/', //服务器的地址
                     'data': {'search-text': inputname}, //参数
                     'dataType': 'json', //返回数据类型
                     'type': 'POST', //请求类型
                     'success': function (data) {
                         if (data.length > 0) {

                             var html_result = "";
                             $.each(data, function (i, term) {
                                 html_result += '<li name="program_list">' + '<a href="/display/program?id=' + term[0] + '">' + term[1] + '</a>' + '</li>';
                             })

                         }
                          $(document).find("li[name='program_list']").remove();
                             $('#search_result_location').after(html_result);
                     }
                 });
             }
             else {
                 $(document).find("li[name='program_list']").remove();
                 $(document).find("li[name='program_list_ago']").show();
             }
         }
    });

    $("#search-text").keypress(function(event)
    {
          //enter
         var inputname=$('#search-text').val();
         if(event.keyCode==13)
         {
             if(inputname)
             {
                 $.ajax({
              'url':'/display/getprogramid/', //服务器的地址
              'data':{'search-text':inputname}, //参数
              'dataType':'json', //返回数据类型
              'type':'POST', //请求类型
              'success':function(data)
               {
                    if(data.length>0)
                  {
                         $.each(data,function(i,term) {
                             window.location.href='/display/program/?id='+term[0];
                         })
                  }
                  else
                    {
                        //不存在节目,进行处理
                        toastr.options.positionClass = 'toast-center-center';
                        toastr.info('输入的节目不存在,请重新输入');
                        //alert("输入的节目不存在,请重新输入");
                        $('#search-text').focus();
                    }
               }
                   });

             }
             //表示为空
             else
             {
                 // html_result="";
                 // html_result+="<label>不能为空</label>";
                 // $('#search-text').after(html_result);
                 toastr.options.positionClass = 'toast-center-center';
                 toastr.warning('查询不能为空');
                 $('#search-text').focus();
                 // alert("查询不能为空");
             }
         }

    });
    $(".disabled").click(function(event)
    {
        event.preventDefault();
    });
})