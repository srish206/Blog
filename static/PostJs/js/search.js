

$(document).ready(function(){

	// $(document).on('keyup','.input-group',function(){
	$(document).on('search','.form-control',function(){
		debugger
		text = $('.form-control').val()
		$.ajax({
			type:"GET",
			url:"/search-data",
			data:{
					'text_data': text
			},
			success:function(result){
				debugger
				data=result.related_post
				$('.list-cls').remove();
				$(data).each(function(index){
					debugger
					data_index=data[index]
					$(data_index).each(function(row){
						debugger
						// $('.list-cls').remove();
						$('#post-id').append(
							'<li class="list-cls col-md-4" style="background-color:white; width: 50%;" data-post='+data_index.id+'>\
							Post Title: '+data_index.title+'\
					 		<br>Description:'+data_index.description+'<br>\
					 		like count:'+data_index.user_like+'<br></li>')

							// $(selector).pagination({
							//         items: 100,
							//         itemsOnPage: 10,
							//         cssStyle: 'light-theme'
							//     });

							// $(function() {
							//     $(selector).pagination({
							//         items: 100,
							//         itemsOnPage: 10,
							//         cssStyle: 'light-theme'
							//     });
							// });
					})
						
				})




			}
		});
	});

});