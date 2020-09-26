/*
Title:		OEngine: a SK Conversation Chatbot Plugin
Author:		Choi jaecheol
Version:	0.2.0
Website:
License: 	the MIT and GPL licenses.
*/

(function($) {
	$.fn.extend({
        aesSDK : function(options) {
        	var elem = this;
        	var defaults =  {
    			'width' : '25%',
    			'height' : '100%',
    			'bgColor' : '#2e3951',
    			'ctitle' : ' Chatbot',
    			'firstMsg' : '안녕하세요.  Chatbot 입니다.',
    			'anythingMsg'  :  '죄송합니다. 알아듣기 쉽게 다시 말씀해주시면 좋겠어요.',
    			'api_key' : '',
    			'user_info' : null,
    			'url' : 'http://localhost:5000'

    		}
            if (options && typeof(options) == 'object') {
                options = $.extend( {}, defaults, options );
            }
        	achat.init(elem, options);
            return;
        }
    });

})(jQuery);
var assistant_id = null;
var session_id = null;

var achat = {
		variable : {
			conText : {},
			messagesendFlag : true
		},
		
		target : null,
		options : {},
		init : function(target, options){
			//크로스도메인허용
	        $.support.cors = true;
			this.target = target;
			this.options = options;
			this.event();

			if(achat.options.wrkMode == 'OP'){
				if(achat.options.workspaceId){
					this.func.fnSend(achat.options.api_key, '', true);
				}else{
					this.func.init(achat.options.api_key);
				}
			}else{
				this.func.fnSend(achat.options.api_key, '', true);
			}
//			this.func.fnSend(achat.options.api_key, '', true);
			$(this.target).find('#achat_date').html('Today , ' + this.func.convertDate(new Date()));
		},
		event : function(){
			$(this.target).find("#achat_input_message").unbind('keypress').keypress(function(e){
				//key 초기화
				var result = "";
				//크롬 계열
				if(typeof(e) != "undefined") {
					result = e.which;
				}else {
					result = event.keyCode;
				}
				if (result == 13){
					//엔터 입력시 실행 함수
					var msg = $(achat.target).find("#achat_input_message").val();
					achat.func.fnSend(assistant_id, session_id, msg);
					console.log(msg);
				}
			});
			$(this.target).find("#achat_send_message").unbind('click').click(function(){
				var msg = $(achat.target).find("#achat_input_message").val();
				achat.func.fnSend(assistant_id, session_id, msg);
			});
			
			$(this.target).find("#aisResetBtn").unbind('click').click(function(){
				location.reload();
			});
			
			$(this.target).find("#aisClearBtn").unbind('click').click(function(){
				$("#achat_talk_body").html($("#achat_talk_body").find('div').first());
			});
		},
		func : {
			convertDate : function(date){
				var yyyy = date.getFullYear().toString();
				var mm = (date.getMonth()+1).toString();
				var dd  = date.getDate().toString();
				var mmChars = mm.split('');
				var ddChars = dd.split('');
				return yyyy + '-' + (mmChars[1]?mm:"0"+mmChars[0]) + '-' + (ddChars[1]?dd:"0"+ddChars[0]);
			},
			init : function(api_key){
				console.log("대화시작...세션정보생성");
				
				var _url = achat.options.url;
				$.ajax({
						type : 'GET',
						crossDomain: true,
						cache: false,
						url : _url + '/start_question',
						dataType : 'json',
						beforeSend:function(){
			            },
						success : function(result){
							console.log(result);
							

							if(Object.keys(result).length > 0){
								
								var msg = '';
								$('#achat_init').css('display','none');
								assistant_id = result.assistant_id;
								session_id   = result.session_id;
								//achat.func.fnSend(assistant_id, session_id, msg); //빈값 보내기.
							}else{
								$('#achat_init').addClass('tagArea3');
								$(achat.target).find('#achat_talk_body').achat_render(result);
							}
							
							
						},
						complete:function(){
							$(achat.target).find("#achat_input_message").val("");
							$(achat.target).find('#achat_input_message').attr('readonly', false);
							$(achat.target).find("#achat_talk_body").scrollTop(999999);  //scroll Y 재조정.
							achat.variable.messagesendFlag = true;
			            },
						error : function(xhr, status, error){
							alert('error' + JSON.stringify(xhr) );
							console.log(error);
						}
				});
			},
			fnSend : function(assistant_id, session_id, msg){
				
				if( (msg.indexOf("<script>") != -1) || (msg.indexOf("</script>") != -1)) {
					alert("스크립트 언어를 사용하실 수 없습니다.");
					return false;
				}
				
				var data ={
						assistant_id : assistant_id,
						session_id   : session_id,
						//channel : achat.options.user_info,
						channel : achat.options.channel,
						chatUserId : achat.options.chatUserId,
						message_input : msg,
						workspaceId : achat.options.workspaceId,
						context : achat.variable.conText
				};

				var _url = achat.options.url;
				var endUrl = _url + '/question';
//				
//				if(typeof(achat.options.workspaceId) == 'undefined' || achat.options.workspaceId == ""){
//					alert("프로젝트 설정에 워크스페이스를 추가 해주세요.");
//					return false;
//				}
				
				
				$.ajax({
						type : 'POST',
						crossDomain: true,
						cache: false,
//						url : _url + '/chatbot/'+api_key,
//						url : _url + '/api/message/'+api_key,
						url : endUrl,
						dataType : 'json',
						contentType: "application/json; charset=utf-8",
						data: JSON.stringify(data),
						beforeSend:function(){
							//사용자 메시지 출력창.
							
							var param = {
									input : {
										text : msg
									}
							};

							$(achat.target).find("#achat_talk_body").achat_render(param);
							$(achat.target).find("#achat_input_message").val("Loading...");
							$(achat.target).find('#achat_input_message').attr('readonly', true);
							
			            },
						success : function(result){
							console.log("result : " + JSON.stringify(result));
							console.log("result.resultCode : " + result.resultCode);
							
							

							result.anythingMsg = achat.options.anythingMsg;
							$(achat.target).find('#achat_talk_body').achat_render(result);
							
							//achat.variable.conText = result.context;
						},
						complete:function(){
							$(achat.target).find("#achat_input_message").val("");
							$(achat.target).find('#achat_input_message').attr('readonly', false);
							$(achat.target).find("#achat_talk_body").scrollTop(999999);  //scroll Y 재조정.
							achat.variable.messagesendFlag = true;
							if( (achat.options && achat.options.wrkMode != 'OP') || (achat.options && achat.options.workspaceId) ){
								$("#achat_input_message").removeAttr('disabled');
							}
			            },
						error : function(xhr, status, error){
							//alert('error' + JSON.stringify(xhr) );
							console.log("xhr : " + xhr);
							console.log(error);
						}
				});
			}
		}
}