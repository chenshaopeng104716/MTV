/**
 * Created by Administrator on 2017/5/12.
 */
function program_vid_show()
{
    document.getElementById('program_vid_full_day_show').style.display="inline";
    document.getElementById('program_vid_short_day_show').style.display="inline";
    document.getElementById("program_vid_show").style.display="none";
    document.getElementById("program_vid_clear").style.display="inline";
    program_vid_full_day();
    program_vid_short_day();
}
