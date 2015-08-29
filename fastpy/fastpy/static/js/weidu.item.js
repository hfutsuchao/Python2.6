
$(function() {
        filldata(result);
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

function filldata(result) {
    if(result && result.index) {
        var html = renderSearchTable(result.index);
        $('#item_detail').html(html);
    }
    else if(result && result.error_str) {
        alert(result.error_str);
    }
}

function renderSearchTable(index) {
    var buffer = new Array();
    buffer.push('<table id="tb_detail" align="center" border="0" cellspacing="0" cellpadding="0" width="800px">');
    buffer.push('<tr><td style="font-size: large; color: #0000FF; background-color:#F6F6F6">'+index._title+'</td></tr>');
    buffer.push('<tr><td>'+index._content+'</td></tr>');
    buffer.push('<tr><td>');
    if (index._av != '') { 
        buffer.push('<embed autostart="false" src="'+index._av+'" width="150" height="15" controller="true" align="middle" bgcolor="black" target="myself" type="video/quicktime" pluginspage="http://www.apple.com/quicktime/download/index.html"></embed>');
    }
    buffer.push('</td></tr>');
    buffer.push('<tr><td>');
    for(var i = 0;i < index._photo_list.length;++i) {
    buffer.push('<img style="max-width:800px" src="'+index._photo_list[i]+'"/></br>');
    }
    buffer.push('</td></tr>');
    buffer.push('</table>');
    return buffer.join('');
}
