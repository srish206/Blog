
$(document).ready(function(){

	$(document).on('click','.delete-cls',function(){
			debugger
			comment_id = $(this).attr('data-id')
			$.ajax({
				type:"GET",
				url:"/delete-comment/" + comment_id,
				data:comment_id,
				success:function(result){
					debugger
					post_id = result.results.comment.post
					result_id = result.result
					debugger
					$(".list-cls[data-post] ").each(function(index){
						debugger
						if($(this).data('post') == post_id){
							debugger
							ab=$(this).children('div').children()
							$(ab).each(function(index){
								$(".delete-cls[data-id]").each(function(index){
									if($(this).data('id') == result_id){
										$(this).parent().remove()
										}
								});
							});
						}
					});
				}
			});

		})
	
});

