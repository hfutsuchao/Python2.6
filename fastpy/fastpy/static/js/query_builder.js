$(function() {


/*
  Base class for uts objects
*/
$.widget("ui.uts_object", {
   _init: function() {
     // init code for mywidget
     var defaults = {
         
     };
     this.options  = $.extend({}, defaults, this.options);
     //alert('d:'+this.options.disabled);
     // can use this.options

   },
   //set_enabled(enabled) {}
   //value: function(a) { return a; },
   //length: function ( ) { return this.listeners.length;  },

   signal: function(signal_name, signal_source, signal_data ) {

   },

   destroy: function() {
       $.widget.prototype.apply(this, arguments); // default destroy
        // now do other stuff particular to this widget
   }
 });


 $.extend($.ui.uts_object, {
   getters: "value length"
   /*defaults: {
     //hidden: true
   }*/
 });
//end of uts_object

/*
* Query builder elemen
*/

uts_query_builder = $.extend({}, $.ui.uts_object.prototype,{
    _init: function(){ 
        var defaults = {
            autocomplete: true,
            completion_source: [],
            value_field: this.element //horizontal or vertical
        };
        this.options  = $.extend({}, defaults, this.options);

        $.ui.uts_object.prototype._init.call(this); // call the original function
        var this_obj = this;
        this.condition_count = 0;
        this.div = this.element;//$('#' + this.options['div_id']);
        $(this.div).addClass('uts_query_builder');

        $(this.div).append('<table></table>');

        this.table = $(this.div).children()[0];

        if(this.options.value_field && $(this.options.value_field).val()){
        	lastData = $.evalJSON($(this.options.value_field).val());
        	for(var k in lastData){
				var conditionData = {name:k};
        		var condiItem = lastData[k];
        		if(!$.isPlainObject(condiItem)){
                    if(typeof(condiItem)=='number'){
                        conditionData.condition = "$equals$num";
                    }else{
                        conditionData.condition = "$equals";
                    }
        			conditionData.value = condiItem;
	        		this.add_query(conditionData);
        		}else{
        			for(k2 in condiItem){
        				condition = k2;
        				value = condiItem[k2];//$.toJSON(condiItem[k2]);
                        if(typeof(value)=='number' || $.isArray(value) && typeof(value[0])=='number'){
                            condition = condition+'$num';
                        }
			            switch(condition) {
			                case '$exists':
			                	condition = value?'$exists':'$nexists';
			                	value = '';
			                    break;
                            case '$ne':
                            case '$ne$num':
			                case '$gt' :
			                case '$gte':
			                case '$lt' :
			                case '$lte':
			                case '$size':
			                case '$type':
			                case '$regex':
			                case '$in$query':
			                case '$nin$query':
			                case '$in$file':
			                case '$nin$file':
			                    break;
                            case '$in':
                            case '$in$num':
                            case '$nin$num':
			                case '$all':
			                	value=value.join('\n');
			                    break;
			            };
			            conditionData.condition = condition;
			            conditionData.value = value;
			            this.add_query(conditionData);
			        }
        		}
        	}
        }
        if(this.condition_count == 0){
        	this.add_query();
        }
    },

    add_query: function(conditionData) {
        var this_obj = this;
		conditionData = conditionData || {};
        var qb_field_condition = $('\
                            <select class="uts_query_builder_field_condition">\
                                <option value="_ignore">(未选择)</option>\
                                <option value="$equals">等于</option>\
                                <option value="$ne">不等于</option>\
                                <option value="$regex">正则表达式匹配</option>\
                                <option value="$in">等于其中任一</option>\
                                <option value="$nin">不等于其中任一</option>\
                                <option value="$all">包含全部</option>\
                                <option value="$in$query">来自查询结果</option>\
                                <option value="$nin$query">不来自查询结果</option>\
                                <option value="$in$file">来自文件</option>\
                                <option value="$nin$file">不来自文件</option>\
                                <option value="$equals$num">等于(数字类型)</option>\
                                <option value="$ne$num">不等于(数字类型)</option>\
                                <option value="$in$num">等于其中任一(数字类型)</option>\
                                <option value="$nin$num">不等于其中任一(数字类型)</option>\
                                <option value="$gt$num">大于(数字类型)</option>\
                                <option value="$gte$num">大于等于(数字类型)</option>\
                                <option value="$lt$num">小于(数字类型)</option>\
                                <option value="$lte$num">小于等于(数字类型)</option>\
                                <option value="$exists">存在</option>\
                                <option value="$nexists">不存在</option>\
                                <option value="$gt">大于</option>\
                                <option value="$gte">大于等于</option>\
                                <option value="$lt">小于</option>\
                                <option value="$lte">小于等于</option>\
                            </select>\
        ');
        var qb_field_name = $('<input type="text" value="" class="uts_query_builder_field_name"/>')
        .autocomplete({ minLength:0, source:this.options.completion_source})
            .css('display','inline');
        var qb_field_btn = $("<button class='mini-btn' style='width:20px'>&nbsp;</button>")
            .attr("tabIndex", -1)
            .attr("title", "显示所有字段")
            .button({
                    icons: {
                        primary: "ui-icon-triangle-1-s"
                    },
                    text: false
                }).removeClass("ui-corner-all")
                .addClass("ui-corner-right ui-button-icon")
                .click(function() {
                    // close if already visible
                    if (qb_field_name.autocomplete("widget").is(":visible")) {
                        qb_field_name.autocomplete("close");
                        return;
                    }
                    // pass empty string as value to search for, displaying all results
                    qb_field_name.autocomplete("search", "");
                    qb_field_name.focus();
                });


        var qb_field_value = $('<textarea type="text" class="uts_query_builder_field_value" />');
        if (this.condition_count == 0){
            var qb_condition_btn = $('<button class="mini-btn mini-icon" title="添加条件" />')
                                        .html('<span class="ui-icon ui-icon-plus"></span>').button()
                                        .click( function() { this_obj.add_query(); } );
            var qb_clear_btn = $('<button class="mini-btn mini-icon" title="清空条件" />')
                                        .html('<span class="ui-icon ui-icon-cancel"></span>').button()
                                        .click( function() { this_obj.clear_query(); } );
       }
        else{
            var qb_condition_btn = $('<button class="mini-btn mini-icon" title="删除" />')
                                        .html('<span class="ui-icon ui-icon-close"></span>').button()
                                        .click( function() { $(this).parent().parent().remove();this_obj.build_query(); } );
            var qb_clear_btn = '';
		}
        var new_row = $('<tr></tr>').html(
                $('<td/>').html($(qb_field_name).add(qb_field_btn))
                    .add( $('<td/>').html(qb_field_condition))
                    .add( $('<td/>').html(qb_field_value))
                    .add( $('<td/>').html(qb_condition_btn).append(qb_clear_btn))
            );
        //$(this.table).find('tr').last().before(new_row);
        $(this.table).append(new_row);
        this.condition_count++;
        var field_name = new_row.find('.uts_query_builder_field_name');
        var field_condition = new_row.find('.uts_query_builder_field_condition');
        var field_value = new_row.find('.uts_query_builder_field_value');
        field_name.blur(function(){this_obj.build_query();});
        field_value.change(function(){this_obj.build_query();});
        field_condition.change(function(){
        	switch(this.value){
        		case '$exists':
        		case '$nexists':
        			field_value.hide();
        			break;
        		default:
        			field_value.show();
        			break;
        	}
        	this_obj.build_query();
        });
        
		if(conditionData.name){
			field_name.val(conditionData.name);
			field_condition.val(conditionData.condition);
			field_value.val(conditionData.value);
		}
        this.build_query();

    },
    clear_query: function() {
        while(rows = $(this.table).find('tr'), rows.length > 1) {
            rows.last().remove();
        }
        $(rows.last().children('td')[0]).children('input').val('');
        $(rows.last().children('td')[1]).children('select').get(0).selectedIndex=0;
        $(rows.last().children('td')[2]).children('input,textarea').val('');

        this.condition_count = 1;
		this.build_query();
    },
    del_query: function() {
        if (this.condition_count > 1) {
            $(this.table).find('tr').last().prev().remove();
            this.condition_count--;
        }
		this.build_query();
    },

    build_query: function() {
    /*
    FIXME: detect if adding new query condition conflicts with existing ones
        function enhance_query(q, f, cond){
            if (!(f in q)) {
                q[f]  = cond;
            } else {
                //check conflicting queries
            };
            return q;
        }*/

        var field_names = $(this.table).find('.uts_query_builder_field_name');
        var field_conditions = $(this.table).find('.uts_query_builder_field_condition');
        var field_values = $(this.table).find('.uts_query_builder_field_value');

        var rows = $(this.table).find('tr');

        var query = {};
        for(var i=0; i<field_names.length; i++)
        {
            var field = $(field_names[i]).val();
            var condition = $(field_conditions[i]).val();
            var value = $(field_values[i]).val();

            if ((field == "" && condition != "$where") || condition =="_ignore") continue;
            switch(condition) {
                case '$exists':
                    q = {}
                    q[field]={$exists: true}
                    $.extend(true, query, q);
                    break;
                case '$nexists':
                    q = {}
                    q[field]={$exists: false}
                    $.extend(true, query, q);
                    break;
                case '$equals$num':
                    value = Number(value);
                case '$equals':
                    //query[field] = value;
                    q = {}
                    q[field]=this.getVal(value)
                    $.extend(true, query, q);
                    break;
                case '$ne$num':
                case '$gt$num' :
                case '$gte$num':
                case '$lt$num' :
                case '$lte$num':
                    value = Number(value);
                    condition = condition.replace('$num','');
                case '$gt' :
                case '$gte':
                case '$lt' :
                case '$lte':
                case '$ne':
                case '$in$query':
                case '$nin$query':
                case '$in$file':
                case '$nin$file':
                    q = {}
                    q[field] = {};
                    q[field][condition] = this.getVal(value);
                    $.extend(true, query, q);
                    break;
                case '$in$num':
                case '$nin$num':
                    condition = condition.replace('$num','');
                    q = {}
                    q[field] = {};
                    q[field][condition] = this.getVal(value).split(/,|\n/).map(function(i){return Number(i)});
                    $.extend(true, query, q);
                    break;
                case '$in':
                case '$nin':
                case '$all':
                    q = {}
                    q[field] = {};
                    q[field][condition] = this.getVal(value).split(/,|\n/);
                    $.extend(true, query, q);
                    break;
                case '$regex':
                    q = {}
					q[field] = {$regex:this.getVal(value)};
                    $.extend(true, query, q);
                    break;
            };

        };
        if(this.options.value_field){
        	$(this.options.value_field).val(JSON.stringify(query));
        }
        return query;
    },
	getVal:function(val){
        if(typeof(val)=='number'){
            return val;
        }
		var result = val.replace(/^\s*/g,'').replace(/\s*$/g,'');
        return result;
	},
    /*
        pass array of values to field name autocomplete widget
    */
    completion_source: function(completions) {
        this.options.completion_source = completions;
        $(this.table).find('tr td input.uts_query_builder_field_name').autocomplete({minLength:0, source: completions});
    }

}); 
$.widget("ui.uts_query_builder", uts_query_builder); 


/**
*
*       Message bus
*
*/

uts_bus = $.extend({}, $.ui.uts_object.prototype,{
    _init: function(){ 
        $.ui.uts_object.prototype._init.call(this); // call the original function 
        this.listeners = new Array();

}, 
    length: function ( ) { return this.listeners.length;  },

    /* add listeners
       params:
           listener: uts_object
    */
    add_listener: function(listener) {
        this.listeners[this.listeners.length] = listener;
    },

    /* send signal
       params:
           signal_name: name of the signal 
           signal_source: uts_object instance originating the signal
           signal_data: json data related to signal (content depends on signal)
    */
    signal: function(signal_name, signal_source, signal_data ) {
        $.ui.uts_object.prototype.signal.call(this);
        for ( var obj in this.listeners)
        {
            this.listeners[obj].signal(signal_name, signal_source, signal_data);
        };
    }
}); 
$.widget("ui.uts_bus", uts_bus); 
//end of message bus


}); //end of function

//} //end of uts_init_mongo_ui


