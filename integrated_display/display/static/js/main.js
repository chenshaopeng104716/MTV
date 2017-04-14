/******************日期控件的选择日期事件************************/
document.querySelector("[type='date']").onchange= function(){
    var now=new Date();
    var nowDay=now.toLocaleDateString();
    var selectDay=document.querySelector("#startTime").value;
    compareDate(selectDay,nowDay);
}

function compareDate(selectDay, nowDay) {
    var arys1= new Array();
    var arys2= new Array();
    var form=document.querySelector(".form-inline");
    var btn=document.querySelector("[type='submit']");
    if(selectDay != null) {
        arys1=selectDay.split('-');
        var sdate=new Date(arys1[0],parseInt(arys1[1]-1),arys1[2]);
        arys2=nowDay.split('/');
        var edate=new Date(arys2[0],parseInt(arys2[1]-1),arys2[2]-1);
        if(sdate > edate) {
            while(btn!=form.lastChild){
                form.removeChild(form.lastChild);
            }
            var label=document.createElement("label");
            label.innerHTML="请选择合理日期";
            label.className='text-danger';
            form.appendChild(label);
        }
        else
            while(btn!=form.lastChild){
                form.removeChild(form.lastChild);
            }
    }
}
/*******************鼠标移入事件*********************/
    //为每个.mini-widget添加一个自定义data-tip属性；
$('.mini-widget').hover(
    function(){
        var tip=$(this).attr("data-tip");
        $div=$(`<div class="tip"></div><span class='tip-span'></span>`);
        $(this).prepend($div);
        $(".tip").html(tip);
        if($('.tip').outerHeight()>40)
            $(".tip").animate({"top":-65,"opacity":1},300);
        else
            $(".tip").animate({"top":-45,"opacity":1},300);
        $(".tip-span").animate({"top":-15,"opacity":1},300);
    },
    function(){
        $(".tip").remove();
        $(".tip-span").remove();
    })

;


/******************更换字体图标************************/
var list=document.querySelectorAll(".fa-arrow");
for(var i=0;i<list.length;i++){
    var num=parseFloat(list[i].nextElementSibling.innerHTML);
    if(num>0){
        list[i].className="fa fa-arrow-up";
    }else{
        list[i].className="fa fa-arrow-down";
    }
}

//ScrollUp
      $(function () {
        $.scrollUp({
          scrollName: 'scrollUp', // Element ID
          topDistance: '300', // Distance from top before showing element (px)
          topSpeed: 300, // Speed back to top (ms)
          animation: 'fade', // Fade, slide, none
          animationInSpeed: 400, // Animation in speed (ms)
          animationOutSpeed: 400, // Animation out speed (ms)
          scrollText: 'Top', // Text for element
          activeOverlay: false // Set CSS color to display scrollUp active point, e.g '#00FFFF'
        });
      });