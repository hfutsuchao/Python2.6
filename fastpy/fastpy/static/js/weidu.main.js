
$(function() {
});


function startsearch() {
    var num_perpage = 10;
    var query_content = $('#search_input').val(); 
    query_content = encodeURIComponent(query_content);
    if (query_content == '' || query_content == undefined) {
        alert('搜索内容为空哦 亲');
    }
    else {
        window.location.href='/search/weidu_list?query_key='+query_content+'&skip=0&shownum='+num_perpage;
    }
    
}
