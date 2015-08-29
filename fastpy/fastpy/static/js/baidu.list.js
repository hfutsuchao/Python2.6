
$(function() {
});

function start_search() {
        var query_content = $('#kw').val();
        query_content = encodeURIComponent(query_content);
        if (query_content == '' || query_content == undefined) {
                alert('搜索内容为空哦 亲');
        }
        else {
                parent.location.href='/search/results?wd='+query_content;
        }
}

function start_search2() {
        var query_content = $('#kw2').val();
        query_content = encodeURIComponent(query_content);
        if (query_content == '' || query_content == undefined) {
                alert('搜索内容为空哦 亲');
        }
        else {
                parent.location.href='/search/results?wd='+query_content;
        }
}
