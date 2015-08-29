$(function() {
  RenderLineChart("char_online_day", "/index.char_online_json_day");
  RenderLineChart("char_online_month", "/index.char_online_json_month");
  });

function ReRendChart() {
  var sb = document.getElementById("ch_area");
  var area_id = "?a_id=";
  for(var i = 0; i < sb.options.length; ++i) {
      if (sb.options[i].selected) {
          area_id = area_id + sb.options[i].value + "_";
      }
  }
  RenderLineChart("char_online_day", "/index.char_online_json_day"+area_id);
  RenderLineChart("char_online_month", "/index.char_online_json_month"+area_id);
}

$("#sub_btn").click(
    function(){
        ReRendChart();
    }
);
