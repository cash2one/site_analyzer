var GallerySlider = function(items,animator){
	var self = this;
	this.items = items;
	this.animator = animator;
	$('button.b-gallery__button_type_right').click(function(){self._moveRight()});
	$('button.b-gallery__button_type_left'). click(function(){ self._moveLeft()});
}
GallerySlider.prototype = {
	_disableButtons:function(){
		$('.b-gallery__button_type_right').addClass('b-gallery__button_type_disabled');
		$('.b-gallery__button_type_left').addClass('b-gallery__button_type_disabled');
	},
	_enableButtons:function(){
		$('.b-gallery__button_type_right').removeClass('b-gallery__button_type_disabled');
		$('.b-gallery__button_type_left').removeClass('b-gallery__button_type_disabled');
	},
	_moveLeft : function(){
		if($('button.b-gallery__button_type_left').hasClass('b-gallery__button_type_disabled'))
			return;
		var self = this;
		self._disableButtons();
		var galleryImg = $(this.items);
        var firstImgName = ($(galleryImg).first().children())[0].style.backgroundImage.match('[_0-9a-zA-Z]*\.(jpg|png|gif)')[0];
        $.ajax({
                url:'/ajax/gallery_prev?current='+firstImgName
            })
            .done(function(data){
                $(galleryImg).first().before(data);
                galleryImg = $(self.items);
				$(galleryImg).first().removeClass('b-gallery__img-link_hidden');
				$(self.animator).css('left','-' + $(galleryImg).last().outerWidth(true) + 'px');
				$(self.animator).animate({left:'0px'},500,function(){
        			$(galleryImg).last().detach();
					self._enableButtons();
				});
            });
	},
	_moveRight : function(){
		if($('button.b-gallery__button_type_right').hasClass('b-gallery__button_type_disabled'))
			return;
		var self = this;
		self._disableButtons();
		var galleryImg = $(self.items);
		var lastImgName = ($(galleryImg[galleryImg.length - 1]).children())[0].style.backgroundImage.match('[_0-9a-zA-Z]*\.(jpg|png|gif)')[0];
        $.ajax({
        		url:'/ajax/gallery_next?current='+lastImgName
        }).done(function(data){
        		$(galleryImg).last().after(data);
        		galleryImg = $(self.items);
				$(galleryImg).last().removeClass('b-gallery__img-link_hidden');
				$(self.animator).animate({left:'-' + $(galleryImg).first().outerWidth(true) + 'px'},500,function(){
					$(self.animator).css('left','0px');
        			$(galleryImg).first().detach();
					self._enableButtons();
				});
   	  		});
	}
};

var NewsSlider = function(items,animator){
	var self = this;
	this.items = items;
	this.animator = animator;	
	this.leftButton  = $('button.b-news__button_type_left');
	this.rightButton = $('button.b-news__button_type_right');
	$(this.leftButton) .click(function(){self._moveLeft();});
	$(this.rightButton).click(function(){self._moveRight();});
}
NewsSlider.prototype = {
	_disableButtons : function(){
		$('.b-news__button_type_left').addClass('b-news__button_type_disabled');
		$('.b-news__button_type_right').addClass('b-news__button_type_disabled');
	},
	_enableButtons : function(){
		$('.b-news__button_type_left').removeClass('b-news__button_type_disabled');
		$('.b-news__button_type_right').removeClass('b-news__button_type_disabled');
	},
	_getNewsId : function(news){
		return jQuery(jQuery(jQuery(news).children()[0]).children().first()).text();
	},
	_getLastVisiblePosition : function(news){
		var i =0;
		while(($(news[i]).hasClass('b-news__item_hidden'))&(i<news.length)){
			i++;
		}
		while((!$(news[i]).hasClass('b-news__item_hidden'))&(i<news.length)){
			i++;
		}
		return i;
	},
	_getFirstVisiblePosition : function(news){
		var i =0;
		while(($(news[i]).hasClass('b-news__item_hidden'))&(i<news.length)){
			i++;
		}
		return i;
	},
	_disableLeftButton : function(){
		$('.b-news__button_type_left').addClass('b-news__button_type_disabled');
	},
	_moveLeft : function(){
		var self = this;
		var news = $(self.items);
		if($(self.leftButton).hasClass('b-news__button_type_disabled'))
			return;
		self._disableButtons();
		$.ajax({
			url:'/ajax/news_next?id=' + self._getNewsId($(news).first()) + '&next'
		}).done(function(data){
			$(news).first().before(data);
			news = $(self.items);
			var firstVisiblePosition = self._getFirstVisiblePosition(news);
			$(news[firstVisiblePosition - 1]).removeClass('b-news__item_hidden');
			$(self.animator).css('left','-'+$(self.items).last().outerWidth(true)+'px');
			$(self.animator).animate({left:'0px'},500,function(){
				$(news[self._getLastVisiblePosition(news) - 1]).addClass('b-news__item_hidden');
				self._enableButtons();
				if(firstVisiblePosition == 1){
					self._disableLeftButton();
				}
			});
		});

	},
	_moveRight : function(){
		var self = this;
		var news = $(self.items);
		if($(self.rightButton).hasClass('b-news__button_type_disabled'))
			return;
		if($(self.leftButton).hasClass('b-news__button_type_disabled'))
			$(self.leftButton).removeClass('b-news__button_type_disabled')
		self._disableButtons();
		if(!$(news).last().hasClass('b-news__item_hidden')){
			$.ajax({
				url:'/ajax/news_next?id='+self._getNewsId($(news).last())+'&prev'
			}).done(function(data){
				$(news).last().after(data);
				news = $(self.items);
				$(news[self._getLastVisiblePosition(news)]).removeClass('b-news__item_hidden');
				$(self.animator).animate({left:'-' + $(self.items).first().outerWidth(true) + 'px'},500,function(){
					$(news[self._getFirstVisiblePosition(news)]).addClass('b-news__item_hidden');
					$(self.animator).css('left','0px');
					self._enableButtons();
				});
			});
		}
		else{
			$(news[self._getLastVisiblePosition(news)]).removeClass('b-news__item_hidden');
			$(self.animator).animate({left:'-' + $(self.items).first().outerWidth(true) + 'px'},500,function(){
				$(news[self._getFirstVisiblePosition(news)]).addClass('b-news__item_hidden');
				$(self.animator).css('left','0px');
				self._enableButtons();
			});
		}
	}
}
$(document).ready(function(){
	new GallerySlider('a.b-gallery__img-link','.b-gallery__items-animator');
	new NewsSlider('.b-news__item','.b-news__items-animator');
	var news = $('.b-news__item');
	$(news).removeClass('b-news__item_hidden');
	$(news).last()
		.addClass('b-news__item_hidden');
});
