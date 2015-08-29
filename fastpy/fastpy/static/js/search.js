
$(function() {
	reloadSearchData();
});

function getContainer(container){
	return $(container).hasClass('query_instance')?$(container):$(container).parents('.query_instance')
}

function callAPI(qData,action,callback,sync){
	qData.action = action;
	$('button').button('disable');
	$.ajax({url:server.api_path
		,data:qData
		,async:!sync
		,success:function(text){
			try{
				if($.isPlainObject(text)){
					var result = text;
				}else{
					eval('var result = '+text);
				}
				callback(result);
				$('button').button('enable');
				}catch(e){
				alert(e);
				$('button').button('enable');
				throw e;
			}
		}
		,type:location.hostname==server.domain?'POST':'GET'
		,dataType:location.hostname==server.domain?'json':'jsonp'
		,error:function(xhr,err){
			$('button').button('enable');
			alert('呃,该系统有点贵恙...请联系管理员或稍后重试...');
			if('console' in window){
				console.info(xhr.responseText);
			}
		}
		});
}

function startsearch(){
    var query_content = $('#search_input').val();
    if (query_content == '' || query_content == undefined) {
		alert('搜索内容为空哦 亲');
    }
    var currentPageIndex = 0;
    $('#search_list').data('query_key',query_content);
	$('#search_list').data('page_index',currentPageIndex);
    reloadSearchData();
}

function reloadSearchData(sender,pager_command){
	var skip = 0;
    var num_perpage = 10;
	if(sender){
		var currentPageIndex = $('#search_list').data('page_index') || 0;
		switch(pager_command){
			case 'first':currentPageIndex=0;break;
			case 'prev':currentPageIndex -= 1;if(currentPageIndex<0){currentPageIndex=0}break;
			case 'next':currentPageIndex += 1;break;
			case 'refresh':break;
			default: currentPageIndex = pager_command;break;
		}
		$('#search_list').data('page_index',currentPageIndex);
		skip = currentPageIndex * num_perpage;
	}
    var query_key =  $('#search_list').data('query_key');
    if (query_key == '' || query_key == undefined) {
    }
    else {
        callAPI({'type':'user','skip':skip, 'query_key':query_key, 'shownum':num_perpage},'getSearchList',function(result){
            if(result && result.results){
                task_data = result.results;
                if (result.count > 0) {
                    pagecount = result.count;
                    var html = renderSearchTable(result.results, pagecount);
                    $('#search_list').html(html);
                }
                else {
                    var html = '抱歉，找到0条结果';
                    alert(task_data);
                }
            }
        });
    }
}

function filldata(result) {    
    if(result && result.results){
	task_data = result.results;
	if (result.count > 0) {
	    pagecount = result.count;
	    var html = renderSearchTable(result.results, pagecount);
	    $('#search_list').html(html);
	}
	else {
	    var html = '抱歉，找到0条结果';
	    $('#search_list').html(html);
	}
    }
}

function renderSearchTable(searchlist_data, pagecount){
	var currentPageIndex = $('#search_list').data('page_index') || 0;
	var pagebuffer = '<div id="page" style="text-align: center;" class="searchlist_pager">';
        if (currentPageIndex > 0) {
		pagebuffer += '&nbsp;<a href="#" onclick="reloadSearchData(this,\'first\')">首页</a>&nbsp;';
		pagebuffer += '&nbsp;<a href="#" onclick="reloadSearchData(this,\'prev\')">上一页</a>&nbsp;';
        }
	var si = currentPageIndex - 5;
	if (si < 0) {
		si = 0;
	}
	var ei = si + 10;
	if (ei > pagecount) {
		ei = pagecount;
	}
	for (var i = si; i < ei ; ++i) {
		if (i == currentPageIndex) {
			pagebuffer += '&nbsp;'+(i+1)+'&nbsp;';
		}
		else {
			pagebuffer += '&nbsp;<a href="#" onclick="reloadSearchData(this,'+i+')">'+(i+1)+'</a>&nbsp;';
		}
	}
	if (currentPageIndex +1 < pagecount) {
		pagebuffer += '&nbsp;<a href="#" onclick="reloadSearchData(this,\'next\')">下一页</a>&nbsp;';
	}
	pagebuffer += '共'+(pagecount) + ' 页';
	pagebuffer += '</div>';
    var buffer = new Array();
    buffer.push(pagebuffer);
    buffer.push("<table width='800' cellspacing='1' class='tablesorter'><thead><tr><th>搜索结果</th></tr></thead><tbody>");
	for(var i=0,c=searchlist_data.length;i<c;i++){
		var rowData = searchlist_data[i];
		buffer.push("<tr>");
        buffer.push("<td>");

		buffer.push("<table width='100%'>");
		buffer.push("<tr>");
		buffer.push("<td style='font-size: large; color: #0000FF; background-color:#F6F6F6' colspan='2' valign='top'>");
		buffer.push("<a href='#'>"+rowData._title+'</a>');
		buffer.push("</td>");
                buffer.push("</tr>");
                buffer.push("<tr>");
                if (rowData._photo != '#') {
		    buffer.push("<td width='20%'><a target='_blank' href='"+rowData._photo+"'><img src='"+rowData._thumb+"' height='120'/></a></td>");
                    buffer.push("<td width='80%' style='font-size: small;'>"+rowData._content+"</td>");
                }
                else {
                    buffer.push("<td colspan='2'><label style='font-size: small;'>"+rowData._content+"</label></td>");
                }
		buffer.push("</tr>");
		buffer.push("</table>");

		buffer.push("</td>");
		buffer.push("</tr>");
	}
	buffer.push('</tbody></table>');
    buffer.push(pagebuffer);
	return buffer.join('');
}

function _s(str){
	var result = '';
	if($.isPlainObject(str)){
		result = $.toJSON(str);
	}else{
		result = (str && str!='null')?str:'';
	}
	return (result+'').replace(/&/g,'&amp;')
                 .replace(/</g,'&lt;')
                 .replace(/>/g,'&gt;')
                 .replace(/"/g, "&quot;")
                 .replace(/'/g, "&#39;");
}
