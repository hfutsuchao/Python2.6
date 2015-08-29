$(function() {
        var query_content = encodeURIComponent(query_key);
        document.getElementById("hide_frame").contentWindow.location.href='http://www.baidu.com/s?wd='+query_content+'&pn='+pn;
        document.getElementById("show_frame").contentWindow.location.href='/search/baidu_list?wd='+query_content+'&pn='+pn;
});

