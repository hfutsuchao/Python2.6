$(function(){
	$( "#tabs").tabs({cookie:{expires: 30}}).bind('tabsselect',function(e,ui){
		$('.code',ui.panel).each(function(){
			var cm = $(this).data('CodeMirror');
			if(cm){
				setTimeout(cm.refresh,1);
			}
		})
	});
	reloadTaskData();
	$('button').button();
	$( ".download_task_from, .download_task_to").datepicker({
		defaultDate: "-1d",
		dateFormat:'yy-mm-dd',
		minDate:new Date(2012,3,1),
		maxDate:"-1d",
		onSelect: function( selectedDate ) {
			var option = this.className.indexOf("download_task_from")>=0 ? "minDate" : "maxDate",
				instance = $( this ).data( "datepicker" ),
				date = $.datepicker.parseDate(
					instance.settings.dateFormat ||
					$.datepicker._defaults.dateFormat,
					selectedDate, instance.settings );
			$( ".download_task_from, .download_task_to").not( this ).datepicker( "option", option, date );
		}
	});
	$('.code').each(function(){
		var cm = CodeMirror.fromTextArea(this, {
	        mode: {name: "python",
	               version: 2,
	               singleLineStringErrors: false},
	        lineNumbers: true,
	        tabMode: "shift",
	        matchBrackets: true,
	        indentUnit : 4,
	        indentWithTabs: true
	      });
		$(this).data('CodeMirror',cm);
	});
});
function getContainer(container){
	container = $(container).hasClass('tab_container')?$(container):$(container).parents('.tab_container');
	return container;
}
function getData(container){
	container = getContainer(container);
	var cm = $('textarea[name=parse]',container).data('CodeMirror');
	if(cm){
		$('textarea[name=parse]',container).val(cm.getValue());
	}
	cm = $('textarea[name=normalizer]',container).data('CodeMirror');
	if(cm){
		$('textarea[name=normalizer]',container).val(cm.getValue());
	}
	var table = $('.field_mapping',container);
	var existMapping = getFieldMappingData(table);
	var data = {
		'_id':$('input[name=_id]',container).val(),
		'name':$('input[name=name]',container).val(),
		'desc':$('input[name=desc]',container).val(),
		'size':$('input[name=size]',container).val(),
		'duplicate_mode':$('select[name=duplicate_mode]',container).val(),
		'is_ucd':$('input[name=is_ucd]',container).attr('checked')?"checked":"",
		'download':$('textarea[name=download]',container).val(),
		'allow_missing':$('input[name=allow_missing]',container).attr('checked')?"checked":"",
		'normalizer':$('textarea[name=normalizer]',container).val(),
		'test':$('textarea[name=test]',container).val(),
		'parse':$('textarea[name=parse]',container).val(),
		'field_mapping':$.toJSON(existMapping.mappings)
	};
	if(!data._id){
		delete data._id;
	}
	return data;
}
function col_save(sender){
	var data = getData(sender);
	callAPI(data,'saveImportColData',function(result){
		location.reload();
	});
}
function col_del(sender){
	confirm('确定要删除吗?这将会删除所有已导入的数据!') && 
		callAPI(getData(sender),'delImportColData',function(result){
			location.reload();
		});
}
function col_test(sender){
	var data = getData(sender);
	var container = getContainer(sender);
	callAPI(data,'testImportColData',function(result){
		$('.test_result',container).html(result.status<0?'<div>代码有一些错误</div>':'').inspect($.isArray(result.results)?result.results:result,'测试结果');
		if(result.status===0){
			$('.edit_btns',container).show();
			renderFieldMappingTable(result.field_mapping,container);
		}else{
			$('.edit_btns',container).hide();
		}
	});
}

function renderFieldMappingTable(field_mapping,container){
	var tBody = $('.field_mapping tbody',container);
	tBody.html('');
	for (var i = 0; i < field_mapping.length; i++) {
		var item = field_mapping[i];
		tBody.append('<tr data-mini-key="'+item[0]+'" data-name="'+item[1]+'"><td>'+item[0]+'</td><td>'+item[1]+'</td><td><input type="text" class="field_desc" value="'+item[2]+'" /></td><td><input type="checkbox" class="ensure_index"'+(item[3]?'checked="checked"':'')+'/></td></tr>');
	};
}

var miniKeys = '0ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'.split('');

function getValByStr(str){
	var arrStr = str.split('');
	var val = 0;
	for (var i = arrStr.length - 1; i >= 0; i--) {
		val += getValBySingleChar(arrStr[i]) * Math.pow(miniKeys.length,arrStr.length-1-i)
	};
	return val;
}
function getStrByVal(val){
	var result = [];
	var base = miniKeys.length;
	result.unshift(miniKeys[val%base]);
	var left = Math.floor(val/base);
	while(left>0){
		result.unshift(miniKeys[left%base]);
		left = Math.floor(left/base);
	}
	return result.join('');
}
function getValBySingleChar(chr){
	var c = chr.charCodeAt(0);
	if(c==48){//'0'
		return 0;
	}else if(c>=65 && c<=90){ //A to Z
		return c-64;
	}else if(c>=97 && c<=122){ //a to z
		return c-70;
	}else{
		return 0;
	}
}
function getFieldMappingData(table){
	var result = {
		mappings : [],
		_max_keycode : 0
	};
	$(table).find('tbody>tr').each(function(index){
		var miniKey = $(this).attr('data-mini-key');
		var name = $(this).attr('data-name');
		var desc = $('.field_desc',this).val();
		var ensureIndex = $('.ensure_index',this).prop('checked');
		result.mappings.push([miniKey,name,desc,ensureIndex]);
		if(index==0){
			result._max_keycode = getValByStr(miniKey);
		}else{
			result._max_keycode = Math.max(getValByStr(miniKey),result._max_keycode)
		}
	});
	return result;
}
function addImportTask(sender){
	var container = getContainer(sender);
	var data = {
		'_id':$('select[name=data_source]',container).val(),
		'start':$('.download_task_from',container).val(),
		'end':$('.download_task_to',container).val()
	};
	callAPI(data,'addImportTaskOnce',function(result){
		reloadTaskData();
	});
}
function callAPI(qData,action,callback,sync){
	$('button').button('disable');
	qData.action = action;
	$.ajax({url:"//"+server.domain+server.port+server.api_path
		,data:qData
		,async:!sync
		,success:function(text){
			$('button').button('enable');
			try{
				if($.isPlainObject(text)){
					var result = text;
				}else{
					eval('var result = '+text);
				}
				callback(result);
			}catch(e){
				$('button').button('enable');
				alert(e);
				throw e;
			}
		}
		,type:location.hostname==server.domain?'POST':'GET'
		,dataType:location.hostname==server.domain?'json':'jsonp'
		,error:function(xhr,err){
			$('button').button('enable');
			alert(xhr.responseText);
		}
		});
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
var task_data = [];
function showJSONDetails(sender){
	var a = $(sender).parent();
    var obj = a.data('details');
    a.html('').inspect(obj);
}
function reloadTaskData(sender,pager_command){
	var skip = 0;
	if(sender && pager_command){
		var currentPageIndex = $('#task_list').data('page_index') || 0;
		switch(pager_command){
			case 'first':currentPageIndex=0;break;
			case 'prev':currentPageIndex -= 1;if(currentPageIndex<0){currentPageIndex=0}break;
			case 'next':currentPageIndex += 1;break;
			case 'refresh':
			default:break;
		}
		$('#task_list').data('page_index',currentPageIndex);
		skip = currentPageIndex * 50;
	}
	callAPI({'type':'import','skip':skip},'getTasks',function(result){
		if(result && result.results){
			task_data = result.results;
			var html = renderTaskTable(result.results);
			$('#task_list').html(html);
			$('#task_list table').tablesorter({headers: { 0: { sorter: false}}});
		}
	});
}
function renderTaskTable(task_data){
	var currentPageIndex = $('#task_list').data('page_index') || 0;
	var buffer = ['<div class="task_pager"><button onclick="reloadTaskData(this,\'refresh\')">刷新</button>',
	'<button onclick="reloadTaskData(this,\'first\')">首页</button>',
	'<button onclick="reloadTaskData(this,\'prev\')">上一页</button>',
	'<button onclick="reloadTaskData(this,\'next\')">下一页</button>',
	' 当前第 '+(currentPageIndex+1) + ' 页',
	'<button onclick="confirm(\'确定要删除吗?\')?removeTasks(this):false;return false;">删除选中</button>',
	'<button onclick="confirm(\'确定要重置吗?\')?resetTasks(this):false;return false;">重置选中</button>',
	'</div>',
	"<table cellspacing='1' class='tablesorter'><thead><tr><th><input type='checkbox' onclick='checkAllTasks(this)' /></th><th>名称</th><th>类型</th><th>周期</th><th>扩展信息</th><th>排队时间</th><th>当前状态</th><th>开始</th><th>结束</th><th>错误</th><th>操作</th></tr></thead><tbody>"]
	for(var i=0,c=task_data.length;i<c;i++){
		var rowData = task_data[i];
		buffer.push("<tr>");
		buffer.push("<td><input type='checkbox' value="+rowData._id+" /></td>");
		buffer.push("<td>"+_s(rowData.name)+"</td>");
		buffer.push("<td>"+_s(rowData.type)+"</td>");
		buffer.push("<td>"+_s(rowData.repeat)+"</td>");
		buffer.push("<td"+(rowData.extend_info?' data-details=\''+_s(rowData.extend_info)+'\'><a href="#" onclick="showJSONDetails(this);return false;">查看</a>':'>')+"</td>");
		// buffer.push("<td>"+_s(rowData.send_mail)+"</td>");
		// buffer.push("<td>"+_s(rowData.mail.join())+"</td>");
		buffer.push("<td>"+_s(rowData.queue_time)+"</td>");
		buffer.push("<td");
		if(rowData.status=='error'){
			buffer.push(' style="background:#faa"');
		}else if(rowData.status=='doing'){
			buffer.push(' style="background:#bfb"');
		}
		buffer.push(">"+_s(rowData.status)+"</td>");
		buffer.push("<td>"+_s(rowData.start_time)+"</td>");
		buffer.push("<td>"+_s(rowData.finish_time)+"</td>");
		buffer.push("<td"+(rowData.error_msg?' data-details=\''+_s(rowData.error_msg)+'\'><a href="#" onclick="showJSONDetails(this);return false;">查看</a>':'>')+"</td>");
		buffer.push("<td>");
		buffer.push(' <a href="#" onclick="confirm(\'确定要重置吗?\')?resetTask(\''+rowData._id+'\'):false;return false;">重置</a> ');
		if(rowData.status!='doing'){
			buffer.push(' <a href="#" onclick="confirm(\'确定要删除吗?\')?removeTask(\''+rowData._id+'\'):false;return false;">删除</a> ');
		}
		buffer.push("</td>");
		buffer.push("</tr>");
	}
	buffer.push('</tbody></table>');
	return buffer.join('');
}
function resetTask(id){
	callAPI({_id:id},'resetTask',function(result){
		reloadTaskData();
	});
}
function removeTask(id){
	callAPI({_id:id},'removeTask',function(result){
		reloadTaskData();
	});
}
function resetTasks(sender){
	var container = getContainer(sender);
	$('tbody input[type=checkbox]:checked',container).each(function(){
		resetTask(this.value);
	});
}
function removeTasks(sender){
	var container = getContainer(sender);
	$('tbody input[type=checkbox]:checked',container).each(function(){
		removeTask(this.value);
	});
}
function checkAllTasks(sender){
	var container = getContainer(sender);
	$('tbody input[type=checkbox]',container).prop('checked',$(sender).prop('checked'));
}