function onfirstclick(item) {
    if(item.value == "在此输入") {
        item.value = "";
    }
    item.style.border = "2px solid blue";
}
function myblur(item) {
    if (item.value == "") {
        item.value = "在此输入";
    }
    item.style.border = "";
}
function checksubmit() {
    var objlist = document.getElementsByTagName("*");
    for (var i = 0; i < objlist.length; ++i) {
        var obj = objlist[i];
        if (obj.id == undefined) {continue;}
        if (obj.id.substr(0, 3) != "ch_") {continue;}
        if (obj.value == "在此输入" || obj.value == "") {
            alert("有必填项未填："+obj.name);
            obj.style.border = "2px solid red";
            obj.focus();
            return false;
        }
    }
    var usrname = $("#ch_usrname").val();
    var IsNameValid = false;
    for (var i = 0; i < tips_data.length; ++i) {
        if (usrname == tips_data[i]) {
            IsNameValid = true;
        }
    }
    if (IsNameValid == false) {
        alert("没有你输入的这个名字");
        return false;
    }

    this.form1.submit();
}
function ChangeSelect(obj) {
    $("#item_ex_id").hide();
    $("#ins_ex_id").hide();
    $("#ins_ex_mark").hide();
    $("#ins_ex_level").hide();
    $("#task_tr").hide();
    if (obj.value == "4") {
        $("#item_ex_id").show(300);
        $("#ex_num").show();
    } else if (obj.value == "6") {
        $("#ins_ex_id").show(300);
        $("#ins_ex_mark").show(300);
        $("#ins_ex_level").show(300);
        $("#ex_num").hide();
    } else if (obj.value == "7") {
        $("#task_tr").show(300);
        $("#ex_num").hide();
    } else {
        $("#ex_num").show();
    }
}
$("#ch_usrname").autocomplete({
source: tips_data
    });

$("#ch_type").change(
    function(){
    ChangeSelect(this);
    }
);

$("#ch_usrname").click(
    function(){
    onfirstclick(this);
    }
);

$("#ch_usrname").blur(
    function(){
    myblur(this);
    }
);

$("#num").click(
    function(){
    onfirstclick(this);
    }
);

$("#num").blur(
    function(){
    myblur(this);
    }
);

$("#insmark").click(
    function(){
    onfirstclick(this);
    }
);

$("#insmark").blur(
    function(){
    myblur(this);
    }
);

$("#sub_btn").click(
    function(){
    checksubmit();
    }
);

$(function(){
  var ch_type_obj = document.getElementById("ch_type");
  ChangeSelect(ch_type_obj);
  });









