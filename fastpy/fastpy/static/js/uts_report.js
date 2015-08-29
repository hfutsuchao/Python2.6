function callAPI(qData,action,callback,sync){
	qData.action = action;
	$('button').button('disable');
	var deferred = $.ajax({url:"//"+server.domain+server.port+server.api_path
		,data:qData
		,async:!sync
		,success:function(text){
			try{
				if($.isPlainObject(text)){
					var result = text;
				}else{
					eval('var result = '+text);
				}
				if(callback)callback(result);
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
			alert(xhr.responseText);
		}
	});
	return deferred;
}
function viewChart(sender){
	var t_index = $(sender).parents('table').data('tindex');
	var selectedKeys = $(sender).parents('table').find('tbody td.row_key.ui-selected').map(function(index,item){
		return $(item).data('key');
	});
	selectedKeys = $.makeArray(selectedKeys);
	window.open('/chart?'+['id='+REPORT_ID,'i='+t_index,'k='+encodeURIComponent(selectedKeys.join('\t'))].join('&'));
}
function exportData(sender){
	var t_index = $(sender).parents('table').data('tindex');
	var selectedKeys = $(sender).parents('table').find('tbody td.row_key.ui-selected').map(function(index,item){
		return $(item).data('key');
	});
	selectedKeys = $.makeArray(selectedKeys);
	window.open('/api?action=exportReportData&'+['id='+REPORT_ID,'i='+t_index,'k='+encodeURIComponent(selectedKeys.join('\t'))].join('&'));
}
$(function() {
		$('button').button();
		$( "#datepicker" ).datepicker({
			dateFormat:'yy-mm-dd',
			showOtherMonths: true,
			numberOfMonths: 2,
			showButtonPanel: true,
			maxDate:"-1d",
			onSelect: function(dateText, inst) {
				location.href = server.report_path+'?id='+REPORT_ID+'&date='+dateText;
			}
		});
		$('.tablesorter').tablesorter();
		$('.tablesorter').selectable({filter:'td.row_key',cancel:'td:not(.row_key)'});
	});