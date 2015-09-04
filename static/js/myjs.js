/**
 * Created by qujianxin on 15-4-14.
 */

$(document).ready(function() {
    $(".mybutton").on("touchstart",(function(){
        $(this).className = "hover,focus";
    }));
});



function show_confirm()
{
    var r=confirm("客官，好想被下载哦╭(╯3╰)╮");
    if (r==true)
    {
        document.location.href="../static/release/test/release_app.apk"
    }
    //else
    //{
    //    alert("You pressed Cancel!");
    //}
}
