
;(function( $ ){
	$.fn.AutoProvince = function( options ) {
		var Setting = $.extend( {
			PROVINCE:		'#province', // select div สำหรับรายชื่อจังหวัด
			AMPHUR:			'#amphur', // select div สำหรับรายชื่ออำเภอ
			DISTRICT:		'#district', // select div สำหรับรายชื่อตำบล
			POSTCODE:		'#postcode', // input field สำหรับรายชื่อรหัสไปรษณีย์
			arrangeByName:		false // กำหนดให้เรียงตามตัวอักษร
		}, options);
		
		return this.each(function() {
			var xml;
			var dataUrl = "thailand.xml";
			
			
			$(function() {
				initialize();
			});
			
			function initialize(){
				$.ajax({
					type: "GET",
					url: dataUrl,
					dataType: "xml",
					success: function(xmlDoc) {
						xml = $(xmlDoc);
						
						_loadProvince();
						addEventList();
					},
					error: function() {
						console.log("Failed to get xml");
					}
				});  
			}
			
			function _loadProvince()
			{
				var list = [];
				xml.find('table').each(function(index){
					if($(this).attr("name") == Setting.PROVINCE.split("#")[1]){
						var PROVINCE_ID = $(this).children().eq(0).text();
						var PROVINCE_NAME = $(this).children().eq(2).text();
						if(PROVINCE_ID)list.push({id:PROVINCE_ID,name:PROVINCE_NAME});
						
					}
				});
				if(Setting.arrangeByName){
					AddToView(list.sort(SortByName),Setting.PROVINCE);
				}else{
					AddToView(list,Setting.PROVINCE);
				}
			}
			
			function _loadAmphur(PROVINCE_ID_SELECTED)
			{
				var list = [];
				var isFirst = true;
				$(Setting.AMPHUR).empty();
				xml.find('table').each(function(index){
					if($(this).attr("name") == Setting.AMPHUR.split("#")[1]){
						var AMPHUR_ID = $(this).children().eq(0).text();
						var AMPHUR_NAME = $(this).children().eq(2).text();
						var POSTCODE = $(this).children().eq(3).text();
						var PROVINCE_ID = $(this).children().eq(5).text();
						if(PROVINCE_ID_SELECTED == PROVINCE_ID && AMPHUR_ID){
							if(isFirst)_loadDistrict(AMPHUR_ID);
							isFirst = false;
							list.push({id:AMPHUR_ID,name:AMPHUR_NAME,postcode:POSTCODE});
							$(Setting.POSTCODE).val(POSTCODE);
						}
					}
				});
				if(Setting.arrangeByName){
					AddToView(list.sort(SortByName),Setting.AMPHUR);
				}else{
					AddToView(list,Setting.AMPHUR);
				}
			}
			
			function _loadDistrict(AMPHUR_ID_SELECTED)
			{
				var list = [];
				$(Setting.DISTRICT).empty();
				xml.find('table').each(function(index){
					if($(this).attr("name") == Setting.DISTRICT.split("#")[1]){
						var DISTRICT_ID = $(this).children().eq(0).text();
						var DISTRICT_NAME = $(this).children().eq(2).text();
						var AMPHUR_ID = $(this).children().eq(3).text();
						if(AMPHUR_ID_SELECTED == AMPHUR_ID && DISTRICT_ID){
							list.push({id:DISTRICT_ID,name:DISTRICT_NAME});
						}
					}
				});
				if(Setting.arrangeByName){
					AddToView(list.sort(SortByName),Setting.DISTRICT);
				}else{
					AddToView(list,Setting.DISTRICT);
				}
			}
			
			function addEventList(){
				$(Setting.PROVINCE).change(function(e) {
					var PROVINCE_ID = $(this).val();
					_loadAmphur(PROVINCE_ID);
				});
				$(Setting.AMPHUR).change(function(e) {
					var AMPHUR_ID = $(this).val();
					$(Setting.POSTCODE).val($(this).find('option:selected').attr("POSTCODE"));
					_loadDistrict(AMPHUR_ID);
				});	
			}
			function AddToView(list,key){
				for (var i = 0;i<list.length;i++) {
					if(key != Setting.AMPHUR){
						$(key).append("<option value='"+list[i].id+"'>"+list[i].name+"</option>");	
					}else{
						$(key).append("<option value='"+list[i].id+"' POSTCODE='"+list[i].postcode+"'>"+list[i].name+"</option>");	
					}
				}
			}
			
			function SortByName(a, b){
			var aName = a.name.toLowerCase();
			var bName = b.name.toLowerCase(); 
			return ((aName < bName) ? -1 : ((aName > bName) ? 1 : 0));
			}
		});
	};
})( jQuery );
