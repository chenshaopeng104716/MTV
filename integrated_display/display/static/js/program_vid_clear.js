/**
 * Created by Administrator on 2017/5/11.
 */
/*
* 清空内容
* */
function program_vid_clear() {
    // if (obj.id == 'program_vid_full_day_clear')
    //  {
       document.getElementById("program_vid_show").style.display="inline";
       document.getElementById("program_vid_clear").style.display="none";
         var myChart1 = echarts.init(document.getElementById('program_vid_full_day'));
   //  }
    //else if(obj.id == 'program_vid_short_day_clear')
   // {
        var myChart2 = echarts.init(document.getElementById('program_vid_short_day'));

   // }
      myChart1.clear();
      myChart2.clear();
       document.getElementById('program_vid_full_day_show').style.display="none";
       document.getElementById('program_vid_short_day_show').style.display="none";
}
