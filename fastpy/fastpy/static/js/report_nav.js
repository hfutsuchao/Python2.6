//jstree doc:http://www.jstree.com/demo , http://www.jstree.com/documentation/core
$(function () {
var rootNodeId = '504726f90c707a5386d9f1c9';
$("#category_tree")
	.jstree({ 
		"plugins" : [ 
			"themes","json_data","ui","cookies","types","hotkeys","contextmenu" 
		],
		"cookies" : {
			"cookie_options":{expires: 30}
		},
		"json_data" : { 
			"ajax" : {
				"url" : "//"+server.domain+server.port+server.api_path
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
				"open" : {
					"separator_before"	: false,
					"separator_after"	: false,
					"label"				: "在新窗口中打开",
					"action"			: function (obj) { window.open($('>a',obj)[0].href) }			
				}
				,"create":null
				,"rename":null
				,"remove":null
				,"ccp":null
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
			parent.frames['report_frame'].location.href = data.rslt.obj.find('a').eq(0).attr('href');
			setTimeout(function(){
				if($.cookie('jstree_select')){
					if(parent.history.pushState){
						parent.history.pushState(null,parent.document.title,$.cookie('jstree_select')+"|"+$.cookie('jstree_open'));
					}else{
						parent.location.hash = $.cookie('jstree_select');
					}
				}
			},1);
        })
	.bind("move_node.jstree", function (e, data) {
		data.rslt.o.each(function (i) {
			callAPI({ 
					"id" : $(this).attr("id").replace("node_",""), 
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
						if(data.rslt.cy && $(data.rslt.oc).children("UL").length) {
							data.inst.refresh(data.inst._get_parent(data.rslt.oc));
						}
					}
				},true);
		});
	});

});

function callAPI(qData,action,callback,sync){
	qData.action = action;
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
			}catch(e){
				alert(e);
				throw e;
			}
		}
		,type:location.hostname==server.domain?'POST':'GET'
		,dataType:location.hostname==server.domain?'json':'jsonp'
		,error:function(xhr,err){
			alert(xhr.responseText);
		}
		});
}
