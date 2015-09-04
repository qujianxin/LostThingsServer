/**
 * Created by qujianxin on 15-4-20.
 */


$(document).ready(function () {
    $(".mybutton").on("touchstart", (function () {
        $(this).css({background: "white", color: "#565656"});
    })).on("touchend", (function () {
        $(this).css({background: "#565656", color: "white"});
    })).on("touchmove", (function () {
        $(this).css({background: "#565656", color: "white"});
    }));
    $(".five_table td").on("touchstart", (function () {
        $(this).css({background: "lightgray"});
    })).on("touchend", (function () {
        $(this).css({background: "white"});
    })).on("touchmove", (function () {
        $(this).css({background: "white"});
    }));
});


function show_confirm() {
    var r = confirm("客官，网页小妹才疏学浅，客户端君才能实现此功能，快来下载吧～");
    if (r == true) {
        document.location.href = "../static/release/update/YiDiudiu.apk"
    }
}


function show_confirm1() {
    document.location.href = "../static/release/update/YiDiudiu.apk"
}


function list_else() {
    if (document.getElementById("loading_else").style.display == "none")  //展开
    {
        document.getElementById("loading_else").style.display = "inline";
    }
    document.getElementById("pid").innerHTML = "已加载全部";
}


function list_else1() {
    var r = confirm("客官，暂无更多评论了呦～想要了解更多信息，快来下载客户端吧～");
    if (r == true) {
        //document.location.href = "../static/release/update/YiDiudiu.apk"
    }
}