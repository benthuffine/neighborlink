// Site Scripts
$(document).ready(function(){
	StElmo.initInputHints();
	StElmo.initLogin();
	StElmo.alignFeaturedStandard();
	StElmo.alignContentAndSidebar();
	
	window.onload = function(){
		// Realign after content images have loaded:
		StElmo.alignFeaturedStandard();
		StElmo.alignContentAndSidebar();
	};
});

/**
 * Site Functions
 */
StElmo = {
	/*
	 * Checks for any input fields with a title tag and uses 
	 * the hint jQuery plugin to remove text on focus and add
	 * it back if the input is empty.
	 */
	initInputHints : function(){
		$("input[title!=''],textarea[title!='']").hint();
	},
	
	/*
	 * Initializes the login lightbox. 
	 */
	initLogin : function(){
		$(".loginLink").fancybox({
			href: '#LoginBox',
			modal: true, 
			scrolling: false, 
			overlayColor: '#fff', 
			overlayOpacity: 0.75
		});
		$('#fancybox-content .Close').live('click',function(){
			$.fancybox.close();
		});
	},
	
	/*
	 * Corrects any alignments issues with the frontpage 
	 * featured items.
	 */
	alignFeaturedStandard : function(){
		o = $('#FeaturedPanel .standard');
		if ( !o.length ) return;
		var height = 0;
		o.each(function(){
			if ( $(this).height() > height ){
				height = $(this).height();
			}
		});
		o.height(height);
	},
	
	/*
	 * Corrects any alignments issues on content pages 
	 */
	alignContentAndSidebar : function(){
		var wrapperDiv = $('.span_content');
		var sidebarDiv = $('#SideNavigation');
		var contentDiv = $('#PageContent');
		
		if( !wrapperDiv.length || !sidebarDiv.length || !contentDiv.length ){ return; }
		
		var paddingBias      = 2;
		var newContentHeight = 0;
		var wrapperHeight    = 0;
		var sidebarHeight    = sidebarDiv.height();
		var sidebarHPadding  = sidebarDiv.outerHeight() - sidebarDiv.height();
		var contentHPadding  = contentDiv.outerHeight() - contentDiv.height();
		
		wrapperDiv.children().each(function(){
			wrapperHeight += $(this).outerHeight();
		});
		
		if( sidebarHeight > wrapperHeight ) {
			var otherContentsHeight = 0;
			wrapperDiv.children(':not(#PageContent)').each(function(){
				otherContentsHeight += $(this).outerHeight();
			});
			newContentHeight = sidebarHeight + sidebarHPadding - otherContentsHeight - contentHPadding - paddingBias;
			
			contentDiv.height(newContentHeight);
		} else { 
			$('#SideNavigation').height( wrapperHeight - sidebarHPadding + paddingBias );
		}
		
	}
};

/**
 * jQuery Plugins
 */
(function ($) {
	/**
	* @author Remy Sharp
	* @url http://remysharp.com/2007/01/25/jquery-tutorial-text-box-hints/
	*/
	$.fn.hint = function(blurClass){if(!blurClass){blurClass = 'blur';}return this.each(function(){var $input=$(this),title=$input.attr('title'),$form=$(this.form),$win=$(window);function remove(){if($input.val()===title&&$input.hasClass(blurClass)){$input.val('').removeClass(blurClass);}}if(title){$input.blur(function(){if(this.value===''){$input.val(title).addClass(blurClass);}}).focus(remove).blur();$form.submit(remove);$win.unload(remove);}});};

})(jQuery);