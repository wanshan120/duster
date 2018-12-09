// ----------------------------------------
// 二重スクロールバー防止
// ----------------------------------------

// Pure JavaScript
var body = document.body;
var checkbox = document.getElementsByClassName('modalCheck');
for (var i = 0; i < checkbox.length; i++) {
	checkbox[i].addEventListener('click', function(){
		if (this.checked) {
			body.style.overflow = 'hidden';
		} else {
			body.style.overflow = 'visible';
		}
	});
}

// jQuery
/*$('.modalCheck').on('change', function(){
	if($(this).is(':checked')){
		$('body').css('overflow','hidden');
	} else {
		$('body').css('overflow','auto');
	}
});*/