(function($) {
	$.fn.extend({
		achat_render : function(type, data){
			var elem = this;
			var render = {
					init : function(data){
						if(data.output != null || typeof(data.output) != 'undefined'){
							$(elem).append(this.func.render_output(data));
						}else{
							var message_input = data.input.text;
							$("<p class='user'><span>"+ message_input + "</span></p>").appendTo(elem);
						}
					},
					func : {
						render_output : function(data){
							
							var values = data.output;
							
							
							
							var result = new Array();
							
							if(values.length == 1){								
								result = values[0].text;
								
								$("<p class='aibril'><span class='box'><span> "+ result +" </span></span></p>").appendTo(elem);

							}else if (values.length > 1){
								result = values[0].text;								
								$("<p class='aibril'><span class='box'><span> "+ result +" </span></span></p>").appendTo(elem);	

								if (values[1].attachment.type == "image") {
									$("<img width='50%' src='"+ values[1].attachment.payload.url + "'>" ).appendTo(elem);
								}

							/*	
							}else if (data.context.achat_ui.ui_type == "url"){
								$('#achat_output_url').tmpl({ result : values, content : data.context.achat_ui.content, img : data.context.achat_ui.img }).appendTo(elem);
							}else if (data.context.achat_ui.ui_type == "list"){
								$('#achat_output_list').tmpl({ result : values, content: data.context.achat_ui.content, img : data.context.achat_ui.img }).appendTo(elem);
								$(elem).find('a[name="lists"]').unbind('click').bind('click',function(){
									achat.func.fnSend(assistant_id, session_id, $(this).attr('response'));
								});
							
							*/
							}else{
								$('#achat_output_text').tmpl({ result : values, img : data.context.achat_ui.img }).appendTo(elem);
							}
							
							
							
						}
					}
			}
			render.init(type,data);
		}
	});
})(jQuery);








