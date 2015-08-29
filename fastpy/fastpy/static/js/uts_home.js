
var tab_counter = 4;
window.onunload = function(){
	lastQuery = getQueryData($('#search'));
	localStorage['last_query'] = $.toJSON(lastQuery);
	localStorage['last_export_query'] = $.toJSON(getExportIdData());
	var open_tabs = []
	$('.ui-tabs-panel').each(function(){open_tabs.push(this.id)})
	localStorage['open_tabs'] = open_tabs.join(',');
}
window.onhashchange = function(){
	var tabIdFromHash = location.hash.replace('$','');
	if(tabIdFromHash){
		if($(tabIdFromHash).length>0){
			$tabs.tabs( "select", tabIdFromHash );
		}else{
			loadQueryTab(tabIdFromHash.replace('#',''));
		}
	}
}
!!shortcut && (function(){
	shortcut.add("Ctrl+S",function(){
		saveQuery(getCurrentContainer());
	});
	shortcut.add("Ctrl+Q",function(){
		getSingleLog(getCurrentContainer());
	});
	shortcut.add("Ctrl+Shift+S",function(){
		saveQueryAs(getCurrentContainer());
	});
	shortcut.add("Ctrl+D",function(){
		deleteQuery(getCurrentContainer());
	});
	shortcut.add("Alt+W",function(){
		closeQuery(getCurrentContainer());
	});
})();
$(function() {
	$tabs = $( "#tabs").tabs({
		tabTemplate: "<li><a href='#{href}'>#{label}</a> <span class='ui-icon ui-icon-close' title='Alt+W'>关闭</span></li>"
		,panelTemplate:'<div class="query_instance">' + $('#search').html()+"</div>"
		,cookie:{expires: 30}
		,select: function(event, ui) {
			var target_hash = ui.tab.href.substring(ui.tab.href.indexOf('#')+1);
			location.hash = '#$'+target_hash;
		}
	});
	$( "#tabs span.ui-icon-close" ).live( "click", function() {
		var index = $( "li", $tabs ).index( $( this ).parent() );
		$tabs.tabs( "remove", index );
	});
	
	initQueryList();
	
	//恢复工作数据
	if(localStorage['last_query']){
		setQueryData($('#search'),$.evalJSON(localStorage['last_query']));
	}
	if(localStorage['last_export_query']){
		setExportIdData($.evalJSON(localStorage['last_export_query']));
	}
	if(server.user_db && field_tips_data[server.user_db]){
		initQueryBuilder($('#analystic'),field_tips_data[server.user_db].fields);
		initQueryBuilder($('#export'),field_tips_data[server.user_db].fields);
	}
	var tabIdFromHash = location.hash.replace('$','');
	if(tabIdFromHash){
		if($(tabIdFromHash).length>0){
			$tabs.tabs( "select", tabIdFromHash );
		}else{
			loadQueryTab(tabIdFromHash.replace('#',''));
		}
	}else{
		if(localStorage['open_tabs']){
			var open_tabs = localStorage['open_tabs'].split(',');
			for(var i=0,c=open_tabs.length;i<c;i++){
				if($('#'+open_tabs[i]).length==0){
					loadQueryTab(open_tabs[i]);
				}
			}
		}
	}
	reloadTaskData();
	//分析界面按钮事件
	$("#look_by_id_group").button().click(function(){
		getUserAnalysisInfo(function(result){
			$('#lookup_by_id_result').html(result);
			$('#lookup_by_id_result table').tablesorter();
			$('#save_to_html_btn').click(function(){
				$( "#saveToHTMLDialog" ).dialog({
					width:500,
					modal: true,
					buttons: {
						"保存": function() {
							if(!$('#save_result_filename').val()){
								return false;
							}else{
								$('#save_result_form')[0].submit();
							}
							$( this ).dialog( "close" );
						},
						"取消": function() {
							$( this ).dialog( "close" );
						}
					},
					open: function() {
						$('#save_result_filename').val($('#user_by_query_id').val()+'-用户信息').focus();
						$('#save_to_html_btn').hide();
						$('#save_result_html').val($('#lookup_by_id_result').html())
						$('#save_to_html_btn').show();
					},
					close: function() {
						$('#save_query_form')[0].reset();
					}
				});
			});
		})
	});
	$('button').button();
	$('#export_uid_btn').click(function(){
		$( "#exportUidToFileDialog" ).dialog({
			width:500,
			modal: true,
			buttons: {
				"保存": function() {
					if(!$('#export_filename').val()){
						return false;
					}else{
						callAPI(getExportIdData(),'export_uid',function(result){
							$('#export_file_download_link').attr('href',result.results).html('点此下载或右键另存为');
						});
					}
				},
				"取消": function() {
					$( this ).dialog( "close" );
				}
			},
			open: function() {
				$('#export_file_download_link').html('');
			}
		});
	});
	initDatepicker('#search');
});
function getContainer(container){
	return $(container).hasClass('query_instance')?$(container):$(container).parents('.query_instance')
}
function getCurrentContainer(){
	return $('#'+location.hash.replace('$','').replace('#',''));
}
function initQueryList(){
	var defaultAutoOptions = { minLength:0
		, source:function(request, response){
			callAPI({ 
				"term":request.term
				}
				,"getSavedQueries"
				, function (r) {
					var content = r.results;
					var realContent = [];
					for (var i = 0; i < content.length; i++) {
						var item= content[i];
						var display_title = item.title;
						if(item.creator){display_title+='['+item.creator+']'}
						else if(item.last_modifier){display_title+='['+item.last_modifier+']'}
						realContent.push({_id:item._id,label:display_title,value:item.title,title:item.title});
					};
					response(realContent);
			});
		}
	};
	$('.saved_query_list').autocomplete(defaultAutoOptions).each(function(){
		var listControl = $(this);
		if(!listControl.next('.group_expr_dropdown').hasClass('ui-corner-right')){
				listControl.next('.group_expr_dropdown').button({
	                    icons: {
	                        primary: "ui-icon-triangle-1-s"
	                    },
	                    text: false
	                }).removeClass("ui-corner-all")
	                .addClass("ui-corner-right ui-button-icon")
	                .click(function() {
	                    if (listControl.autocomplete("widget").is(":visible")) {
	                        listControl.autocomplete("close");
	                        return;
	                    }
	                    if(listControl.attr("menuMode")=='1'){
	                    	listControl.autocomplete("search");
	                    }else{
		                    listControl.autocomplete("search","");
		                }
	                    listControl.focus();
	                });
			}
		}).on("autocompleteselect",function(event, ui){
			$(this).data('selectedItem',ui.item);
		});
	$( "#combobox" ).autocomplete(defaultAutoOptions).attr("menuMode",'1').on("autocompleteselect",function(event,ui){
			var tabId = "#" + ui.item._id;
			if($(tabId).length>0){
				$tabs.tabs( "select", tabId );
			}else{
				loadQueryTab(ui.item._id);
			}
			return false;
	});
	$( "#user_by_query_id" ).autocomplete(defaultAutoOptions).on("autocompleteselect",function(e,option){
			$('#user_by_query')[0].checked=true;
			getTasksByQueryId(this,true);
	});
	onDataSourceChanged($('#search'));
	onDataSourceChanged($('#analystic .analysis_dimension'));
}
function show_field_tips(container){
	container = getContainer(container);
	var db = $('.exec_code_source',container).val();
	var title = $('.exec_code_source',container)[0].options[$('.exec_code_source',container)[0].selectedIndex].text;
	renderFieldTips(container,field_tips_data[db].fields);
	$('.field_tips_table',container).dialog({
		modal: true,
		title:title,
		width:500,
		buttons: {
			Ok: function() {
				$( this ).dialog( "close" );
			}
		}
	});
}
function onDataSourceChanged(sender){
	var container = getContainer(sender);
	var db = $('.exec_code_source',container).val();
	if(db=='saved_query_result'){
		$('.saved_query_as_db,.saved_query_as_db_show',container).show();
		$('.flex-date',container).hide();
		$('.fix-date',container).hide();
	}else if(db=='lsp_query_result'){
		$('.saved_query_as_db,.saved_query_as_db_show',container).show();
		$('.simple-group,.advance-query',container).hide();
		if($('.use_flex_date',container).val()=='1'){
			$('.flex-date',container).show();
			$('.fix-date',container).hide();
		}else{
			$('.flex-date',container).hide();
			$('.fix-date',container).show();
		}
	}else{
		$('.saved_query_as_db,.saved_query_as_db_show',container).hide();
		if($('.use_advance',container).val()=='1'){
			$('.advance-query',container).show();
			$('.simple-group',container).hide();
		}else{
			$('.advance-query',container).hide();
			$('.simple-group',container).show();
		}
		if($('.use_flex_date',container).val()=='1'){
			$('.flex-date',container).show();
			$('.fix-date',container).hide();
		}else{
			$('.flex-date',container).hide();
			$('.fix-date',container).show();
		}
		//toggleTimeRange(container,$('.use_flex_date',container).val()=='1');
	}
	if(field_tips_data && field_tips_data[db]){
		renderFieldList(container,field_tips_data[db].fields);
		initQueryBuilder(container,field_tips_data[db].fields);
	}
}
function initQueryBuilder(container,data){
	var mappedData = [];
	if(data&&data.length){
		for(var i=0,c=data.length;i<c;i++){
			var item = {label:data[i][1],value:data[i][0]};
			mappedData.push(item);
		}
	}
	$('.query_expr',container).hide();
	$('.query_builder',container).html('').uts_query_builder({completion_source:mappedData,value_field:$('.query_expr',container)});
}
function clearQueryExpr(container){
	container = getContainer(container);
	$('.query_builder',container).uts_query_builder('clear_query');
}
function fillField(container,target,value){
	container = getContainer(container);
	$(target,container).val(value);
}
function renderFieldList(container,data){
	if(data){
		var mappedData = [];
		for(var i=0,c=data.length;i<c;i++){
			var item = {label:data[i][1],value:data[i][0]};
			mappedData.push(item);
		}
		var listControls = $('.fields_list',container);
		var singleSelectionListOptions = { minLength:0, source: mappedData};
		var multiSelectionListOptions = { minLength:0, 
			source: function( request, response ) {
				// delegate back to autocomplete, but extract the last term
				response( $.ui.autocomplete.filter(
					mappedData, request.term.split( /\s*\|\s*/ ).pop() ) );
			},
			focus: function() {
				// prevent value inserted on focus
				return false;
			},
			select: function( event, ui ) {
				var terms = this.value.split( /\s*\|\s*/ );
				// remove the current input
				terms.pop();
				// add the selected item
				terms.push( ui.item.value );
				// add placeholder to get the comma-and-space at the end
				terms.push( "" );
				this.value = terms.join( "|" );
				return false;
			}
		};
		listControls.each(function(){
			var listControl = $(this);
			listControl.autocomplete(listControl.attr('data-mode')=='single'?singleSelectionListOptions:multiSelectionListOptions);
			if(!listControl.next('.group_expr_dropdown').hasClass('ui-corner-right')){
				listControl.next('.group_expr_dropdown').button({
	                    icons: {
	                        primary: "ui-icon-triangle-1-s"
	                    },
	                    text: false
	                }).removeClass("ui-corner-all")
	                .addClass("ui-corner-right ui-button-icon")
	                .click(function() {
	                    if (listControl.autocomplete("widget").is(":visible")) {
	                        listControl.autocomplete("close");
	                        return;
	                    }
	                    listControl.autocomplete("search", "");
	                    listControl.focus();
	                });
			}
		});
		
	}
}
function toggleAdvance(container,setVisible){
	container = getContainer(container);
	if(setVisible===true){
		$('.advance-query',container).show();
		$('.simple-group',container).hide();
		$('.use_advance',container).val('1');
	}else if(setVisible===false){
		$('.advance-query',container).hide();
		$('.simple-group',container).show();
		$('.use_advance',container).val('0');
	}else{
		$('.advance-query',container).toggle();
		$('.simple-group',container).toggle();
		if($('.use_advance',container).val()=='1'){
			$('.use_advance',container).val('0');
		}else{
			$('.use_advance',container).val('1');
		}
	}
}
function toggleFilterMode(container,setVisible){
	container = getContainer(container);
	if(setVisible===true){
		$('.query_expr',container).show();
		$('.query_builder',container).hide();
		$('.filter_advance',container).val('1');
	}else if(setVisible===false){
		$('.query_expr',container).hide();
		$('.query_builder',container).show();
		$('.filter_advance',container).val('0');
	}else{
		$('.query_builder',container).toggle();
		$('.query_expr',container).toggle();
		if($('.filter_advance',container).val()=='1'){
			$('.filter_advance',container).val('0');
		}else{
			$('.filter_advance',container).val('1');
		}
	}
}
function toggleTimeRange(container,setVisible){
	container = getContainer(container);
	var zeroDate = $('.exec_code_day_0',container).val();
	if(setVisible===true || typeof(setVisible)=='undefined' && $('.use_flex_date',container).val()!='1'){
		$('.flex-date',container).show();
		$('.fix-date',container).hide();
		$('.exec_code_from_d',container).val(getDateDiff(zeroDate,$('.exec_code_from',container).val()));
		$('.exec_code_to_d',container).val(getDateDiff(zeroDate,$('.exec_code_to',container).val()));
		$('.use_flex_date',container).val('1');
	}else if(setVisible===false|| typeof(setVisible)=='undefined' && $('.use_flex_date',container).val()=='1'){
		$('.flex-date',container).hide();
		$('.fix-date',container).show();
		$('.exec_code_from',container).val(getOffsetDate(safeParseInt($('.exec_code_from_d',container).val()),zeroDate));
		$('.exec_code_to',container).val(getOffsetDate(safeParseInt($('.exec_code_to_d',container).val()),zeroDate));
		$('.use_flex_date',container).val('0');
	}else{
		$('.flex-date',container).toggle();
		$('.fix-date',container).toggle();
	}
}
/////////////
//date func.
////////////
function safeParseInt(source){
	var result=parseInt(source);
	if(isNaN(result)){
		result = 0;
	}
	return result;
}
function getOffsetDate(dayOffset,startDate){
	if(typeof dayOffset == 'undefined'){
		dayOffset = -1;
	}
	startDate = startDate || new Date();
	return formatDate(new Date(parseDate(startDate).getTime()+(dayOffset*24*60*60*1000)));
}
function getDateDiff(start,end){
	var startDate = parseDate(start);
	var endDate = parseDate(end);
	return Math.floor((endDate-startDate)/(24*3600*1000));
}
function formatDate(source){
	var day="00"+ source.getDate();
	day = day.substring(day.length-2,day.length);
	var month="00"+ (source.getMonth() + 1);
	month = month.substring(month.length-2,month.length);
	var year=source.getFullYear();
	return year + "-" + month + "-" + day;
}
function parseDate(source) {
    var reg = new RegExp("^\\d+(\\-|\\/)\\d+(\\-|\\/)\\d+\x24");
    if (source && 'string' == typeof source) {
        if (reg.test(source) || isNaN(Date.parse(source))) {
            var d = source.split(/ |T/),
                d1 = d.length > 1 
                        ? d[1].split(/[^\d]/) 
                        : [0, 0, 0],
                d0 = d[0].split(/[^\d]/);
            return new Date(d0[0] - 0, 
                            d0[1] - 1, 
                            d0[2] - 0, 
                            d1[0] - 0, 
                            d1[1] - 0, 
                            d1[2] - 0);
        } else {
            return new Date(source);
        }
    }
    
    return new Date(parseDate(formatDate(new Date())).getTime()+(-1*24*60*60*1000));
}
/////////////
//date func end.
////////////
function renderFieldTips(container,data){
	if(data){
		var buffer = ["<table cellspacing='1' class='field_tips_table'><thead><tr><th>字段</th><th>说明</th></tr></thead><tbody>"]
		for(var i=0,c=data.length;i<c;i++){
			buffer.push("<tr><td>"+data[i][0]+"</td><td>"+data[i][1]+"</td></tr>")
		}
		buffer.push('</tbody></table>');
		$('.field_tips',container).html(buffer.join(''));
	}
}
function loadQueryTab(tabId){
		// if(data&&data.db){
		// 	_createQueryTab(data);
		// }else{
			callAPI({'_id':tabId},'getSavedQuery',function(res){
				_createQueryTab(res.results);
				// if(selectedIndex){
				// 	$("#combobox").data('q_'+selectedIndex,res.results);
				// }
			});
		// }
		tab_counter++;
}
function _createQueryTab(data){
	var tabId = "#"+data._id;
	$tabs.tabs( "add", tabId, data.title );
	$tabs.tabs( "select", tabId );
	$('.hidden',$(tabId)).show();
	$('button',$(tabId)).button();
	initDatepicker(tabId);
	//resetQueryList($(tabId));
	setQueryData($(tabId),data);
	// if(data.exec_result){
	// 	renderQueryResult(data.exec_result,$(tabId));
	// }
	getTasksByQueryId($(tabId));
}
function initDatepicker(id){
	$( ".exec_code_from, .exec_code_to",$(id) ).datepicker({
		defaultDate: "-1d",
		dateFormat:'yy-mm-dd',
		minDate:new Date(2012,3,1),
		maxDate:"-1d",
		onSelect: function( selectedDate ) {
			var option = this.className.indexOf("exec_code_from")>=0 ? "minDate" : "maxDate",
				instance = $( this ).data( "datepicker" ),
				date = $.datepicker.parseDate(
					instance.settings.dateFormat ||
					$.datepicker._defaults.dateFormat,
					selectedDate, instance.settings );
			$( ".exec_code_from, .exec_code_to",$(id) ).not( this ).datepicker( "option", option, date );
		}
	});
	$('.exec_code_day_0',$(id)).datepicker({
		defaultDate: "-1d",
		dateFormat:'yy-mm-dd',
		maxDate:"-1d",
		minDate:new Date(2012,3,1),
	});
}
function closeQuery(container){
	container = getContainer(container);
	var index = $( "li", $tabs ).index( $( '.ui-tabs-selected' ) );
	if(index>4)$tabs.tabs( "remove", index );
}
function deleteQuery(container){
	container = getContainer(container);
	if(confirm('确定要删除该查询吗?')){
		var _id = $('._id',container).val();
		if(_id){
			callAPI({'_id':_id},'deleteQuery',function(result){
				initQueryList();
				$tabs.tabs( "remove", '#'+_id );
			})
		}
	}
}
function saveQueryAs(container){
	container = getContainer(container);
	$( "#saveDialog" ).dialog({
			width:500,
			modal: true,
			title:'另存为',
			buttons: {
				"保存": function() {
					var qData = getQueryData(container);
					qData['_id']='';
					qData.title=encodeURIComponent($('#query_title').val());
					qData.description=encodeURIComponent($('#query_description').val());
					if(webkitNotifications){
						webkitNotifications.requestPermission();
					}
					callAPI(qData,'saveQuery',function(result){
						initQueryList();
						$('.exec_hint',container).html('保存成功');
						setTimeout(function(){$('.exec_hint',container).html('');},3000);
						window.lastUpdateTime[result.results] = new Date().getTime();
						location.hash = '#$'+result.results;
						$( "#saveDialog" ).dialog( "close" );
					});
				},
				"取消": function() {
					$( this ).dialog( "close" );
				}
			},
			open: function() {
				$('#query_title').val($('.query_title',container).val()).focus();
				$('#query_description').val($('.query_description',container).val());
			},
			close: function() {
				$('#save_query_form')[0].reset();
			}
		});
}
function saveQuery(sender){
	var container = getContainer(sender);
	if($('._id',container).val()){
		var qData = getQueryData(container);
		if(webkitNotifications){
			webkitNotifications.requestPermission();
		}
		callAPI(qData,'saveQuery',function(result){
			initQueryList();
			$('.exec_hint',container).html('保存成功');
			setTimeout(function(){$('.exec_hint',container).html('');},3000);
			window.lastUpdateTime[$('._id',container).val()] = new Date().getTime();
			getTasksByQueryId(sender);
		});
	}else{
		$( "#saveDialog" ).dialog({
			width:500,
			modal: true,
			buttons: {
				"保存": function() {
					var qData = getQueryData(container);
					qData.title=encodeURIComponent($('#query_title').val());
					qData.description=encodeURIComponent($('#query_description').val());
					callAPI(qData,'saveQuery',function(result){
						initQueryList();
						$('.exec_hint',container).html('保存成功');
						setTimeout(function(){$('.exec_hint',container).html('');},3000);
						location.hash = '#$'+result.results;
						$( "#saveDialog" ).dialog( "close" );
					});
				},
				"取消": function() {
					$( this ).dialog( "close" );
				}
			},
			open: function() {
				$('#query_title').val($('.exec_code_source',container)[0].options[$('.exec_code_source',container)[0].selectedIndex].text+'-').focus();
			},
			close: function() {
				$('#save_query_form')[0].reset();
			}
		});
	}
}
function deleteQueryCache(sender){
	var container = getContainer(sender);
	var qData = getQueryData(container);
	callAPI(qData,'deleteQueryCache',function(result){
		initQueryList();
		$('.exec_hint',container).html('操作成功');
		setTimeout(function(){$('.exec_hint',container).html('');},3000);
	});
}
function getExportIdData(){
	var qData = {};
	qData.export_collection = $('#export_source').val();
	qData.export_query_expr = $('#export_query_expr').val();
	qData.export_skip_num = $('#export_skip_num').val();
	qData.export_limit_num = $('#export_limit_num').val();
	qData.export_line_template = $('#export_line_template').val();
	qData.export_filename = $('#export_filename').val();
	return qData;
}
function setExportIdData(qData){
	$('#export_query_expr').val(qData.export_query_expr);
	$('#export_skip_num').val(qData.export_skip_num);
	$('#export_limit_num').val(qData.export_limit_num);
	$('#export_line_template').val(qData.export_line_template);
	$('#export_filename').val(qData.export_filename);
}
function getQueryData(container){
	var data = {
			'db':$('.exec_code_source',container).val(),
			'title':$('.query_title',container).val(),
			'description':$('.query_description',container).val(),
			'start':$('.exec_code_from',container).val(),
			'end':$('.exec_code_to',container).val(),
			'query_expr':$('.query_expr',container).val(),
			'exec_code_map':$('.exec_code_map',container).val(),
			'exec_code_reduce':$('.exec_code_reduce',container).val(),
			'exec_code_finalize':$('.exec_code_finalize',container).val(),
			'use_advance':$('.use_advance',container).val(),
			'use_flex_date':$('.use_flex_date',container).val(),
			'filter_advance':$('.filter_advance',container).val(),
			'group_expr':$('.group_expr',container).val(),
			'group_expr_val':$('.group_expr_val',container).val(),
			'show_only_counts':''//$('.show_only_counts',container).attr('checked'),
		};
	if($('._id',container).length>0){
		data['_id'] = $('._id',container).val();
	}
	if(data['db']=='saved_query_result'||data['db']=='lsp_query_result'){
		//var selectedIndex = $('.saved_query_as_db',container)[0].selectedIndex;
		//var queryData = $('#combobox').data('q_'+selectedIndex);
		data['qid'] = $('.saved_query_as_db',container).val();
	}
	if(data['use_flex_date']=='1'){
		data['start'] = $('.exec_code_from_d',container).val();
		data['end'] = $('.exec_code_to_d',container).val();
		data['zeroDate'] = $('.exec_code_day_0',container).val();
	}
	if(data['use_advance']=='1'){
		data['group_expr'] = '';
		data['group_expr_val']='';
	}else{
		data['exec_code_map'] = data['exec_code_reduce'] = data['exec_code_finalize']='';
	}
	return data;
}
function setQueryData(container,data){
	$('._id',container).val(data['_id']);
	$('.query_title',container).val(data['title']);
	$('.query_description',container).val(data['description']);
	$('.exec_code_source',container).val(data['db']);
	$('.use_advance',container).val(data['use_advance']);
	$('.filter_advance',container).val(data['filter_advance']);
	$('.use_flex_date',container).val(data['use_flex_date']);
	$('.query_expr',container).val(data['query_expr']);
	$('.exec_code_map',container).val(data['exec_code_map']);
	$('.saved_query_as_db',container).val(data['qid']);
	if(data['use_advance']=='1'){
		toggleAdvance($('.exec_code_map',container),true);
	}
	if(data['filter_advance']=='1'){
		toggleFilterMode($('.query_expr',container),true);
	}
	if(data['use_flex_date']=='1'){
		$('.exec_code_from_d',container).val(data['start']);
		$('.exec_code_to_d',container).val(data['end']);
		toggleTimeRange($('.use_flex_date',container),false);
		toggleTimeRange($('.use_flex_date',container),true);
	}else{
		$('.exec_code_from',container).val(data['start']);
		$('.exec_code_to',container).val(data['end']);
	}
	$('.exec_code_reduce',container).val(data['exec_code_reduce']);
	$('.exec_code_finalize',container).val(data['exec_code_finalize']);
	$('.group_expr',container).val(data['group_expr']);
	$('.group_expr_val',container).val(data['group_expr_val']);
	$('.exec_result',container).val($.toJSON(data['exec_result']));
	if(!!data['exec_result']){
		if(!localStorage.is_developer)$('.query_condition',container).hide();
	}
	
	$('.show_only_counts',container).attr('checked',data['show_only_counts']?true:false);
	onDataSourceChanged($('.exec_code_source',container));
}
function renderQueryResult(result,container){
	$('.exec_hint',container).html('');
	if(result&&result.results!=undefined){
		var res = result.results;
		var qid = $('._id',container).val();
		if(window.lastUpdateTime[qid] && (new Date().getTime() - window.lastUpdateTime[qid] > 10000)){
			uts_notify('查询结果已就绪','名称:'+$('.query_title',container).val()+'\n处理条目数:'+ result.input + "\n结果数: "+ result.output,function(){
				location.hash = '#$'+qid;
			});
		}
		window.lastUpdateTime[$('._id',container).val()] = null;
		if($.isArray(res)){
			var description="";
			if(result.input){
				description += "<span class='input-count'>处理条目数: "+ result.input +"; </span>";
			}
			description += "<span class='output-count'>结果数: "+ result.output +";</span>";
			// if(res[0] && getPropertyCount(res[0])==2){
			// 	description += "<button class='save_to_excel_btn'>全部导出到Excel...</button><br/>";
			// }
			if(result.timeMillis){
				description += "<span class='time-millis'>查询耗时: "+result.timeMillis+" 毫秒; </span>";
			}
			if(res.length<result.output){
				description += "<span class='count-limit'>网页中仅显示前500条;</span>";
				$('.exec_result',container).val('');
			}else{
				//保存查询结果(如果是全部返回的话)
				// var strResult = $.toJSON(result);
				// $('.exec_result',container).val(strResult);
			}
			//description += "<span class='time-exec'>("+result.exec_timestamp+") </span>"
			if(res[0] && getPropertyCount(res[0])==2){
				$('.exec_code_result',container).html(description+renderTable(res));
				res.length && $(".exec_code_result_table",container).tablesorter({sortList:[[0,0]]});
			}else{
				$('.exec_code_result',container).html(description).inspect(res,'结果详情');
			}
		}else if($.isNumeric(res)){
			$('.exec_code_result',container).html("<span class='output-count'>共找到记录: "+res+" 条</span>");
		}else{
			$('.exec_code_result',container).html('').inspect(res,'结果详情');
		}
	}
}
function getPropertyCount(o){  
	var n, count = 0;  
	for(n in o){  
		if(o.hasOwnProperty(n)){  
			count++;  
		}  
	}  
	return count;  
}  
function callAPI(qData,action,callback,sync){
	qData.action = action;
	//$('button').button('disable');
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
				//$('button').button('enable');
			}catch(e){
				if(!!console)console.log(e);
				//$('button').button('enable');
				throw e;
			}
		}
		,type:location.hostname==server.domain?'POST':'GET'
		,dataType:location.hostname==server.domain?'json':'jsonp'
		,error:function(xhr,err){
			//$('button').button('enable');
			if(!!console)console.log(err);
			if('console' in window){
				console.info(xhr.responseText);
			}
		}
		});
}
function renderTable(data){
	if(data.length==0){
		return '无数据';
	}
	var sumArray = {};
	var buffer = ["<table class='exec_code_result_table tablesorter' cellspacing='1'><thead><tr>"];
	
	if($.isPlainObject(data[0]._id)){
		for(var key in data[0]._id){
			buffer.push('<th>'+_s(key)+'</th>')
		}
	}else{
		buffer.push('<th>名称</th>');
	}
	if($.isPlainObject(data[0].value)){
		for(var key in data[0].value){
			buffer.push('<th>'+_s(key)+'</th>')
			sumArray[key]=$.isNumeric(data[0].value[key])?0:'-';
		}
	}else{
		buffer.push('<th>值</th>');
		sumArray["value"] =$.isNumeric(data[0].value)?0:'-';
	}
	buffer.push('</tr></thead><tbody>');
	for(var i=0,c=data.length;i<c;i++){
		buffer.push('<tr>');
		if($.isPlainObject(data[0]._id)){
			for(var key in data[0]._id){
				buffer.push('<td>'+_s(data[i]._id[key])+'</th>')
			}
		}else{
			buffer.push('<td>'+_s(data[i]._id)+'</td>');
		}
		
		if($.isPlainObject(data[0].value)){
			for(var key in data[0].value){
				buffer.push('<td align="right">'+_s(data[i].value[key])+'</td>');
				sumArray[key] += $.isNumeric(sumArray[key])?data[i].value[key]:'';
			}
		}else{
			buffer.push("<td align='right'>"+_s(data[i].value)+"</td>");
			sumArray["value"] += $.isNumeric(sumArray["value"])?data[i].value:'';
		}
		buffer.push('</tr>');
	}
	buffer.push("</tr><thead><tr>");
	if($.isPlainObject(data[0]._id)){
			for(var key in data[0]._id){
				buffer.push('<td></td>')
			}
		}else{
			buffer.push('<td>合计:</td>');
		}
	if($.isPlainObject(data[0].value)){
		for(var key in data[0].value){
			buffer.push('<td align="right">'+_s(sumArray[key])+'</td>');
		}
	}else{
		buffer.push('<td align="right">'+_s(sumArray["value"])+'</td>');
	}
	buffer.push("</tr></thead>");
	buffer.push('</tbody></table>');
	return buffer.join('');
}
function getUserAnalysisInfo(callback){
	var cachedKey = $('#user_detail_pane .task_history_selector').val();
	var group_exprs = {};
	$('.analysis_condition').each(function(){
		if($('.group_expr',this).val().length>0){
			group_exprs[$(this).attr('data-db')]=$('.group_expr',this).val();
		}
	});
	$.post("//" + server.domain + server.port + server.api_path,{
			action:'getUsersSummary'
			,'user_id':$('#field_text_id').val()
			,'query_user_type':$('#user_by_input')[0].checked?'by_input':($('#user_by_file')[0].checked?'by_file':'by_query')
			,'user_by_query_id':cachedKey?cachedKey:''
			,'user_by_file_name':$('#user_by_file_name').val()
			,'group_exprs':$.toJSON(group_exprs)
			,'dimention_db':$('.analysis_dimension .exec_code_source').val()
			,'dimension_field':$('.analysis_dimension .group_expr').val()
			,'excel_filename':$('#excel_filename').val()
		},function(result){
			callback(result);
	},'html');
}

function bindReportConfigData(data){
	if(data){
		$('#current_report_id').val(data.attr.id);
		data.source && $('#report_source').val(data.source).change();
		$('#report_href').val(data.href);
		$('#report_description').val(data.description);
		$('#report_subscriber').val(data.subscriber);
		$('#report_filter').val(data.filter);
		$('#report_black').val(data.blacklist);
		$('#reports_to_range').empty();
		if(data.tables){
			$.each(data.tables,function(index,table){
				addQueryElement(table);
			})
		}
	}
}
function saveReportConfig(){
	var data = getReportConfigData();
	data.tables = $.toJSON(data.tables);
	callAPI(data
		,"updateReport"
		,function (r) {
			if(!r.status) {
				alert('saving error, please retry later.')
			}else{
				//$('#report_config').hide();
				//$('#category_tree').jstree('refresh');
				$('#report_frame')[0].contentWindow.location.reload();
			}
		});
}
function getReportConfigData(onlySelected){
	var data = {};
	data.id = $('#current_report_id').val();
	data.source = $('#report_source').val();
	data.href = $('#report_href').val();
	data.description = $('#report_description').val();
	data.subscriber = $('#report_subscriber').val();
	data.filter = $('#report_filter').val();
	data.blacklist = $('#report_black').val();
	data.tables = [];
	if(data.source=='uts'){
		$('#reports_to_range>li'+(!!onlySelected?'.ui-selected':'')).each(function() {
			var table = getTableInfoFromUI(this);
			data.tables.push(table);
		});
	}
	return data;
}

function getTableInfoFromUI(target){
	var table= {};
	table.qid=$(target).attr('rel');
	table.type=$(target).attr('data-type');
	table.name=$('.table_title',target).text();
	if(table.type=='group'){
		table.mergeType = $(target).attr('data-mergetype');
		table.formula = $(target).attr('data-formula');
		table.queries = {};
		$('li',target).each(function(){
			table.queries[$(this).attr('data-varname')] = {
				'qid':$(this).attr('rel')
				,'type':$(this).attr('data-type')
				,'name':$('.query_item_title',this).text()
			};
		});
	}
	return table;
}
function startReportEdit(obj){
	callAPI({id:obj.attr("id").replace("node_","")},"getReport",function(r){
		bindReportConfigData(r);
		$('#report_config').show();
	})
}
function onReportSourceChanged(target){
	var src=$(target).val();
	$('#config_report_uts,#config_report_custom').hide();
	$('#config_report_'+src).show();
}
function onQueryMergeTypeChange(target){
	var mergeType = $(target).val();
	if(mergeType=='formula'){
		$('#query_merge_datials').show();
	}else{
		$('#query_merge_datials').hide();
	}
}
function addQueryToReport(){
	var query_data = $('#report_saved_query').data('selectedItem');
	query_data.type='set';
	addQueryElement(query_data);
}
function addQueryCountToReport(){
	var query_data = $('#report_saved_query').data('selectedItem');
	query_data.type='output_count';
	addQueryElement(query_data);
}
function addQueryInputCountToReport(){
	var query_data = $('#report_saved_query').data('selectedItem');
	query_data.type='input_count';
	addQueryElement(query_data);
}
function getGroupedQueryUI(data){
	var buffer = ['<ol class="query_group">'];
	$.each(getSortedObjectArray(data),function(index,item){
		var q=item.value;
		var var_name = item.key;
		buffer.push('<li rel="'+q.qid+'" data-type="'+q.type+'" data-varname="'+var_name+'">');
		buffer.push('<span class="query_item_title" onclick="inlineEdit(this);">');
		buffer.push(q.name);
		buffer.push('</span>');
		buffer.push('<a href="#$'+q.qid+'" class="handle" style="cursor:pointer"><span class="ui-icon ui-icon-newwin" style="display:inline-block"> </span></a>');
		buffer.push('</li>');
	});
	buffer.push('</ol>');
	return buffer.join('');
}
function getSortedObjectArray(obj){
	return $.map(obj,function(item,k){return {'key':k,'value':item}}).sort(function(a,b){return a.key>b.key});
}
function addQueryElement(query_data){
	var title = '';
	if(!query_data.name){
		switch(query_data.type){
			case "input_count":title=query_data.title+"(处理条数)";break;
			case "output_count":title=query_data.title+"(结果数)";break;
			case "set":title=query_data.title;break;
			case "group":
				break;
		}
		query_data.qid = query_data._id;//统一字段名
	}else{
		title = query_data.name;
	}
	var newItem = null;
	if(query_data.type=="group"){
		newItem = $('<li rel="" data-mergetype="'+query_data.mergeType+'" data-formula="'+query_data.formula+'" data-type="'+query_data.type+'" class="ui-state-default ui-corner-all query_group_c"><span class="ui-icon ui-icon-carat-2-n-s handle"> </span><span class="table_title" onmousedown="arguments[0].stopPropagation()" ondblclick="inlineEdit(this);">'+title+'</span><span class="ui-icon ui-icon-close handle" onclick="removeQueryFromReport(this)"> </span><span class="ui-icon ui-icon-arrow-4-diag handle" title="取消合并" onclick="unpackQueryGroup(this)"> </span><span class="ui-icon ui-icon-gear handle" onclick="editQueryGroup(this)"> </span>'+getGroupedQueryUI(query_data.queries)+'<span class="merge-type-desc">合并方式: '+(query_data.mergeType=='formula'?query_data.formula:(query_data.mergeType=='key'?'按行名合并':'简单合并'))+'</span></li>');
	}else{
		newItem = $('<li rel="'+query_data.qid+'" data-type="'+query_data.type+'" class="ui-state-default ui-corner-all"><span class="ui-icon ui-icon-carat-2-n-s handle"> </span><span class="table_title" ondblclick="inlineEdit(this);" onmousedown="arguments[0].stopPropagation()">'+title+'</span><a href="#$'+query_data.qid+'" class="handle" style="cursor:pointer"><span class="ui-icon ui-icon-newwin" style="display:inline-block"> </span></a>'+'<span class="ui-icon ui-icon-close handle" onclick="removeQueryFromReport(this)"> </span></li>');
	}
	$('#reports_to_range').append(newItem);
	$('#reports_to_range').sortable({handle:'.handle'});
	$('#reports_to_range').selectable({
		selected:function(event,ui){
			updateReportButtonState();
		}
		,unselected:function(event,ui){
			updateReportButtonState();
		}
		,filter:">li[data-type!=group]"
	});
	updateReportButtonState();
	return newItem;
}
function inlineEdit(sender){
	if(!$(sender).attr('data-inline-editing')){
		var txt = $(sender).text();
		var oldWidth = Math.max($(sender).width()+40,100);
		$(sender).attr('data-inline-editing','true').empty().append($('<input type="text" onblur="endInlineEdit(this);" />').width(oldWidth).val(txt))
	}
}
function endInlineEdit(sender){
	$(sender).parent().text($(sender).val()).attr('data-inline-editing',null);
}
function updateReportButtonState(){
	$('#reports_to_range').find('.ui-selected').length>1?$('#merge_selected_query').button('enable'):$('#merge_selected_query').button('disable');
	$('#reports_to_range').find('li').length>1?$('#auto_merge_selected_query').button('enable'):$('#auto_merge_selected_query').button('disable');
}
function removeQueryFromReport(elem){
	$(elem).parent().remove();
	updateReportButtonState();
}
function unpackQueryGroup(sender){
	sender = $(sender).closest('li');
	var groupTable = getTableInfoFromUI(sender);
	$.each(groupTable.queries,function(index,q){
		var newItem = addQueryElement(q);
		newItem.insertBefore(sender);
		newItem.addClass('ui-selected');
	});
	sender.remove();
}
function editQueryGroup(sender){
	$( "#mergeQueryDialog" ).dialog({
			width:700,
			modal: true,
			buttons: {
				"确定": function() {
					if(validateGroupInfo()){
						//点击确定对话框时:
						packQueryGroup($(sender).closest('li'));
						$( this ).dialog( "close" );
					}
				},
				"取消": function() {
					$( this ).dialog( "close" );
				}
			},
			open: function() {
				//提取当前分组信息,显示对话框时,将分组信息填充到对话框,
				var groupTable = getTableInfoFromUI($(sender).closest('li'));
				$('#query_merge_type').val(groupTable.mergeType).change();
				$('#merge_formula').val(groupTable.formula);
				$('#query_merge_name').val(groupTable.name);
				$('#mergeValList').html(getGroupedQueryUI(groupTable.queries));
			},
			close: function(){
				
			}
		});
}
function packQueryGroup(target){
	//提取选中条目信息,加上分组信息,删除选中条目,添加新建组.
	var groupData = {
		qid:'',
		name:$('#query_merge_name').val(),
		mergeType:$('#query_merge_type').val(),
		formula:$('#merge_formula').val(),
		type:"group",
		queries:{}
	};
	if(!target){
		var selectedConfigData = getReportConfigData(true);
		$.each(selectedConfigData.tables,function(index,table){
			groupData.queries[String.fromCharCode(65+index)] = table;
		});
		addQueryElement(groupData);
		$('#reports_to_range>li.ui-selected:first').replaceWith($('#reports_to_range>li:last'));
		$('#reports_to_range>li.ui-selected').remove();		
	}else{
		var selectedConfigData = getTableInfoFromUI(target);
		groupData.queries = selectedConfigData.queries;
		addQueryElement(groupData);
		$(target).replaceWith($('#reports_to_range>li:last'));
	}
}
function validateGroupInfo(){
	//校验公式是否正确
	return true;
}
function mergeSelection () {
	$( "#mergeQueryDialog" ).dialog({
			width:700,
			modal: true,
			buttons: {
				"确定": function() {
					if(validateGroupInfo()){
						packQueryGroup();
						$( this ).dialog( "close" );
					}
				},
				"取消": function() {
					$( this ).dialog( "close" );
				}
			},
			open: function() {
				var selectedConfigData = getReportConfigData(true);
				$('#mergeValList').html(getGroupedQueryUI(selectedConfigData.tables));
				$('#query_merge_name').val($.map(selectedConfigData.tables,function(item,index){return item.name}).join('+'));
			},
			close: function(){
				
			}
		});
}
//jstree doc:http://www.jstree.com/demo , http://www.jstree.com/documentation/core
$(function () {
var apiUrl = "//"+server.domain+server.port+server.api_path;
$("#category_tree")
	.jstree({ 
		"plugins" : [ 
			"themes","json_data","ui","crrm","cookies","dnd","types","hotkeys","contextmenu" 
		],
		"cookies" : {
			"cookie_options":{expires: 30}
		},
		"json_data" : { 
			"ajax" : {
				"url" : apiUrl
				,type:location.hostname==server.domain?'POST':'GET'
				,dataType:location.hostname==server.domain?'json':'jsonp'
				// the `data` function is executed in the instance's scope
				// the parameter is the node being loaded 
				// (may be -1, 0, or undefined when loading the root nodes)
				,"data" : function (n) { 
					// the result is fed to the AJAX request `data` option
					return { 
						"action" : "getReports", 
						"id" : n.attr ? n.attr("id").replace("node_","") : '504726f90c707a5386d9f1c9'
					}; 
				}
				,success:function(r){
					if($.isArray(r)){
						$.each(r,function(index,d){
							d.data.attr = d.data.attr||{};
							if(!d.data.attr.href){
								d.data.attr.href = "//"+server.domain+server.port+server.report_path+"?id="+d.attr.id;
							}
							d.data.attr.target="report_frame";
							d.attr.id = "node_" + d.attr.id;
						})
					}
				}
			}
		},
		"ui" :{
			"select_limit":1
		},
		"contextmenu":{
			"items":{
				"edit" : {
					"separator_before"	: true,
					"separator_after"	: false,
					"label"				: "编辑报表详情",
					"action"			: function (obj) { this.select_node(obj,true);startReportEdit(obj); }
				}
				,"open" : {
					"separator_before"	: false,
					"separator_after"	: false,
					"label"				: "在新窗口中打开",
					"action"			: function (obj) { window.open($('>a',obj)[0].href) }			
				}
				,"create":{label:'新建'}
				,"rename":{label:'重命名'}
				,"remove":{label:'删除',action:function(obj){ 
					if(confirm('确定要删除该报表吗?(其子报表将保留)')){
						if(this.is_selected(obj)) { this.remove(); } else { this.remove(obj); }
					}
				}}
				,"ccp":{label:'更多...',submenu:{
					"copy":{label:'复制'}
					,"paste":{label:'粘贴'}
					,"cut":{label:'剪切'}
				}}
			}
		},
		// Using types - most of the time this is an overkill
		// read the docs carefully to decide whether you need types
		"types" : {
			// I set both options to -2, as I do not need depth and children count checking
			// Those two checks may slow jstree a lot, so use only when needed
			"max_depth" : -2,
			"max_children" : -2,
			// I want only `drive` nodes to be root nodes 
			// This will prevent moving or creating any other type as a root node
			"valid_children" : [ "root" ],
			"types" : {
				"root" : {
					// can have files and folders inside, but NOT other `drive` nodes
					"valid_children" : [ "default" ],
					// those prevent the functions with the same name to be used on `drive` nodes
					// internally the `before` event is used
					"start_drag" : false,
					"move_node" : false,
					"delete_node" : false,
					"remove" : false
				}
			}
		},
	})
	.bind("create.jstree", function (e, data) {
		callAPI({ 
				"ref" : data.rslt.parent.attr("id").replace("node_",""), 
				"position" : data.rslt.position,
				"title" : data.rslt.name,
				"type" : data.rslt.obj.attr("rel")
			}
			,"addReport"
			, function (r) {
				if(r.status) {
					$(data.rslt.obj).attr("id", "node_" + r.id);
					$('a',data.rslt.obj).attr('target','report_frame');
					$('a',data.rslt.obj).attr('href',"//"+server.domain+server.port+server.report_path+"?id="+r.id);
				}
				else {
					$.jstree.rollback(data.rlbk);
				}
		});
	})
	.bind("remove.jstree", function (e, data) {
		data.rslt.obj.each(function () {
			callAPI({ 
					"id" : this.id.replace("node_","")
				}
				,"removeReport"
				,function (r) {
					// if(!r.status) {
					// 	data.inst.refresh();
					// }
				},true);
		});
	})
	.bind("rename.jstree", function (e, data) {
		callAPI({ 
				"id" : data.rslt.obj.attr("id").replace("node_",""),
				"title" : data.rslt.new_name
			}
			,"updateReport"
			,function (r) {
				if(!r.status) {
					$.jstree.rollback(data.rlbk);
				}
			});
	})
	.bind("select_node.jstree", function (event, data) {
			$('#report_frame').attr('src',data.rslt.obj.find('a').eq(0).attr('href'));
			if($('#report_config').css('display')!='none'){
				startReportEdit(data.rslt.obj);
			}
            updateReportButtonState();
        })
	.bind("move_node.jstree", function (e, data) {
		data.rslt.o.each(function (i) {
			var copyId= $(this).attr("id").replace("node_","");
			callAPI({ 
					"id" : copyId, 
					"ref" : data.rslt.cr === -1 ? 1 : data.rslt.np.attr("id").replace("node_",""), 
					"position" : data.rslt.cp + i,
					"title" : data.rslt.name,
					"copy" : data.rslt.cy ? 1 : 0
				}
				,"updateReport"
				,function (r) {
					if(!r.status) {
						$.jstree.rollback(data.rlbk);
					}
					else {
						$(data.rslt.oc).attr("id", "node_" + r.id);
						$(data.rslt.oc).children("a:eq(0)").attr('href',$(data.rslt.oc).children("a:eq(0)").attr('href').replace(copyId,r.id));
						if(data.rslt.cy && $(data.rslt.oc).children("UL").length) {
							data.inst.refresh(data.inst._get_parent(data.rslt.oc));
						}
					}
				},true);
		});
	});

});


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
		var currentPageIndex = $('#tasks').data('page_index') || 0;
		switch(pager_command){
			case 'first':currentPageIndex=0;break;
			case 'prev':currentPageIndex -= 1;if(currentPageIndex<0){currentPageIndex=0}break;
			case 'next':currentPageIndex += 1;break;
			case 'refresh':
			default:break;
		}
		$('#tasks').data('page_index',currentPageIndex);
		skip = currentPageIndex * 50;
	}
	callAPI({'type':'user','skip':skip},'getTasks',function(result){
		if(result && result.results){
			task_data = result.results;
			var html = renderTaskTable(result.results);
			$('#tasks').html(html);
			$('#tasks table').tablesorter({headers: { 0: { sorter: false}}});
		}
	});
}
function renderTaskTable(task_data){
	var currentPageIndex = $('#tasks').data('page_index') || 0;
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
		if(rowData.type=='query'||rowData.type=='report'){
			buffer.push("<td><a href='#$"+_s(rowData.ref_id)+"'>"+_s(rowData.name)+' '+_s(rowData.extend_info.owner)+"</a></td>");
		}else{
			buffer.push("<td>"+_s(rowData.name)+"</td>");
		}
		buffer.push("<td>"+_s(rowData.type)+"</td>");
		buffer.push("<td>"+_s(rowData.repeat)+"</td>");
		buffer.push("<td"+(rowData.extend_info?(' data-details=\''+_s(rowData.extend_info)+'\'><a href="#" onclick="showJSONDetails(this);return false;">查看</a>'):'>')+"</td>");
		//buffer.push("<td>"+_s(rowData.script)+"</td>");
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
		buffer.push("<td"+(rowData.error_msg?(' data-details=\''+_s(rowData.error_msg)+'\'><a href="#" onclick="showJSONDetails(this);return false;">查看</a>'):'>')+"</td>");
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
window.lastUpdateTime = {};
function getTasksByQueryId(sender,queryOnly){
	var container = getContainer(sender);
	var qData = {};
	if(!queryOnly){
		qData = getQueryData(container);
	}else{
		qData = $('#user_by_query_id').data('selectedItem')
	}
	callAPI({'_id':qData._id},'getTasksByQueryId',function(result){
		if(result && result.results){
			var buffer = [];
			if(result.results.length>0){
				buffer.push('<select class="task_history_selector"');
				if(!queryOnly){
					buffer.push(' onchange="onTaskResultSelectionChange(this)">');
				}else{
					buffer.push('>');
				}
				for (var i = 0; i < result.results.length; i++) {
					var task = result.results[i];
						if(!queryOnly && i==0&& (task.status!='done' && task.status!='error')){
							setTimeout(function(){getTasksByQueryId(sender);},3000);
						}
					if(!queryOnly || task.status=='done'){
						buffer.push('<option value="'+task._id+'">['+task.queue_time+']'+task.name+' ['+task.status+']');
						if(_s(task.extend_info.log_date)){
							buffer.push('['+_s(task.extend_info.log_date)+']');
						}
						if(_s(task.extend_info.owner)){
							buffer.push('['+_s(task.extend_info.owner)+']');
						}
						buffer.push('</option>');
					}
				};
				buffer.push('</select>');
			}else{
				buffer.push('');
			}
			if(!queryOnly){
				buffer.push(' <button onclick="getTasksByQueryId(this)">刷新结果</button>');
				buffer.push(' <button onclick="exportQueryResult(this)">导出CSV</button>');
			}
			$('.task_history',container).html(buffer.join(''));
			onTaskResultSelectionChange($('.task_history_selector',container));
		}
	});
}
function onTaskResultSelectionChange(sender){
	var container = getContainer(sender);
	callAPI({'_id':$(sender).val()},'getTaskExecResult',function(result){
		if(result && result.results){
			renderQueryResult(result,container);
		}
	});
}
function exportQueryResult(sender){
	var container = getContainer(sender);
	callAPI({'_id':$('.task_history_selector',container).val(),'dataType':'excel'},'getTaskExecResult',function(result){
		if(result){
			location.href = result.results;
		}
	});
}
var uts_notify = function(title,msg,onclick){
	if(!window.webkitNotifications){
		return;
	}
    var _fun = function(){
        var notify = webkitNotifications.createNotification(
                "//"+server.domain+server.port+"/images/statics.png",
                "UTS: "+title,
                msg
            );
        notify.onclick = function(event){
            if(!!onclick){
            	onclick();
            }
            notify.close();
        };
        notify.show();
    };
    try{
	    // 检查权限，0：已授权，1：已拒绝
	    if(webkitNotifications.checkPermission() > 0) {
	        // 请求授权
	        webkitNotifications.requestPermission(function(){
	            _fun();
	        });
	    }else{
	        _fun();
	    }
	}catch(e){
		
	}
};