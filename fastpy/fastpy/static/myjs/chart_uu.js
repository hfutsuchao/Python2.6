$(function() {
  RenderLineChart("chart_uu", "/index.account_uu_json");
  RenderLineChart("character_uu", "/index.character_uu_json");
  RenderLineChart("div3", "/index.acc_reg_json_day");
  RenderLineChart("div4", "/index.char_reg_json_day");
  RenderLineChart("div5", "/index.char_del_json_day");
  RenderLineChart("div6", "/index.char_login_json_day");
  RenderLineChart("div7", "/index.char_logout_json_day");
  RenderLineChart("div8", "/index.char_login_reward_json_day");
  });

function ReRendChart() {
  var sb = document.getElementById("ch_area");
  var area_id = "?a_id=";
  for(var i = 0; i < sb.options.length; ++i) {
      if (sb.options[i].selected) {
          area_id = area_id + sb.options[i].value + "_";
      }
  }
  RenderLineChart("chart_uu", "/index.account_uu_json"+area_id);
  RenderLineChart("character_uu", "/index.character_uu_json"+area_id);
  RenderLineChart("div3", "/index.acc_reg_json_day"+area_id);
  RenderLineChart("div4", "/index.char_reg_json_day"+area_id);
  RenderLineChart("div5", "/index.char_del_json_day"+area_id);
  RenderLineChart("div6", "/index.char_login_json_day"+area_id);
  RenderLineChart("div7", "/index.char_logout_json_day"+area_id);
  RenderLineChart("div8", "/index.char_login_reward_json_day"+area_id);
}

$("#sub_btn").click(
    function(){
        ReRendChart();
    }
);
