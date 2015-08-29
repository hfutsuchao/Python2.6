
$(function() {
	reloadPublishData();
	$('button').button();
	$('#publish_time').datepicker({dateFormat:'yy-mm-dd'});
});

function getContainer(container){
	return $(container).hasClass('query_instance')?$(container):$(container).parents('.query_instance')
}

function callAPI(qData,action,callback,sync){
	qData.action = action;
	$('button').button('disable');
	$.ajax({url:"//"+server.domain+server.port+server.api_path
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
var publish_data = [];

function reloadPublishData(sender,pager_command){
	var skip = 0;
	if(sender && pager_command){
		var currentPageIndex = $('#publish').data('page_index') || 0;
		switch(pager_command){
			case 'first':currentPageIndex=0;break;
			case 'prev':currentPageIndex -= 1;if(currentPageIndex<0){currentPageIndex=0}break;
			case 'next':currentPageIndex += 1;break;
			case 'refresh':
			default:break;
		}
		$('#publish').data('page_index',currentPageIndex);
		skip = currentPageIndex * 50;
	}
	callAPI({'type':'user','skip':skip},'getPublish',function(result){
		if(result && result.results){
			task_data = result.results;
			var html = renderPublishTable(result.results);
			$('#publish').html(html);
			$('#publish table').tablesorter({headers: { 0: { sorter: false}}});
		}
	    hideall('.edit');
		initDatePicker();
	});
}
function renderPublishTable(publish_data){
	var currentPageIndex = $('#publish').data('page_index') || 0;
	var buffer = ['<div class="publish_pager"><button onclick="reloadPublishData(this,\'refresh\')">刷新</button>',
	'<button onclick="reloadPublishData(this,\'first\')">首页</button>',
	'<button onclick="reloadPublishData(this,\'prev\')">上一页</button>',
	'<button onclick="reloadPublishData(this,\'next\')">下一页</button>',
	' 当前第 '+(currentPageIndex+1) + ' 页',
	'<button onclick="confirm(\'确定要删除吗?\')?removePublishs(this):false;return false;">删除选中</button>',
	'</div>',
	"<table cellspacing='1' class='tablesorter'><thead><tr><th><input type='checkbox' onclick='checkAllPublish(this)' /></th><th>发布信息</th><th>发布时间</th><th>操作</th></tr></thead><tbody>"]
	for(var i=0,c=publish_data.length;i<c;i++){
		var rowData = publish_data[i];
		buffer.push("<tr>");
		buffer.push("<td><input type='checkbox' value="+rowData._id+" /></td>");
		buffer.push("<td>");
		buffer.push("<div class='view' id='v_content_"+rowData._id+"'>"+_s(rowData.content).replace(/\n/g,'<br/>')+"</div>");
		buffer.push("<textarea class='edit' id='e_content_"+rowData._id+"' cols='50' rows='5'>"+_s(rowData.content)+"</textarea>");
		buffer.push("</td>");
		buffer.push("<td>");
		buffer.push("<div class='view' id='v_time_"+rowData._id+"'>"+_s(rowData.publish_time)+"</div>");
		buffer.push("<input class='edit' id='e_time_"+rowData._id+"' type='text' value='"+_s(rowData.publish_time)+"'/>");
		buffer.push("</td>");
        buffer.push("<td>");
		buffer.push(' <a class="view" id="v_href_'+rowData._id+'" href="#" onclick="editPublish(\''+rowData._id+'\');">编辑</a> ');
		buffer.push(' <a class="edit" id="e_update_'+rowData._id+'" href="#" onclick="updatePublish(\''+rowData._id+'\');">提交</a> ');
		buffer.push(' <a class="edit" id="e_href_'+rowData._id+'" href="#" onclick="cancelEditPublish(\''+rowData._id+'\');">取消</a> ');
		buffer.push('<br/> <a href="#" onclick="confirm(\'确定要删除吗?\')?removePublish(\''+rowData._id+'\'):false;return false;">删除</a> ');
		buffer.push("</td>");
		buffer.push("</tr>");
	}
	buffer.push('</tbody></table>');
	return buffer.join('');
}
function initDatePicker(){
	$("input[id^='e_time_']").each(function(){
		$(this).datepicker({dateFormat:'yy-mm-dd'});
	});
}
function hideall(p){
	$(p).each(function(){
		$(this).hide();
	});
}
function showall(p){
	$(p).each(function(){
		$(this).show();
	});
}
function editPublish(id){
	showall('.view');
	hideall('.edit');
	$('#v_content_'+id).hide();
	$('#v_time_'+id).hide();
	$('#v_href_'+id).hide();
	$('#e_content_'+id).show();
	$('#e_time_'+id).show();
	$('#e_href_'+id).show();
	$('#e_update_'+id).show();
}
function cancelEditPublish(id){
	$('#e_content_'+id).hide();
	$('#e_time_'+id).hide();
	$('#e_href_'+id).hide();
	$('#e_update_'+id).hide();
	$('#v_content_'+id).show();
	$('#v_time_'+id).show();
	$('#v_href_'+id).show();
}
function updatePublish(p){
	var id = p;
	var content = $('#e_content_'+id).val();
	var time = $('#e_time_'+id).val();
	callAPI({_id:id,_content:content,_time:time},'updatePublish',function(result){
		reloadPublishData();
	});
}
function addpublish(){
	var content = $('#publish_content').val();
	var time = $('#publish_time').val();
	callAPI({_content:content,_time:time},'addPublish',function(result){
		reloadPublishData();
	});
}
function removePublish(id){
	callAPI({_id:id},'removePublish',function(result){
		reloadPublishData();
	});
}
function removePublishs(sender){
	var container = getContainer(sender);
	$('tbody input[type=checkbox]:checked',container).each(function(){
		removePublish(this.value);
	});
}
function checkAllPublish(sender){
	var container = getContainer(sender);
	$('tbody input[type=checkbox]',container).prop('checked',$(sender).prop('checked'));
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
