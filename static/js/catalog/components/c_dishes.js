var c_dishes = {
	init: function (data) {

	},

	/**
	 *	update displaying dish count
	 * @param data json
	 */
	em_updateDishCount: function (data) {
		var dish = $('#dish_'+data.dish_id);
		if (dish[0] === undefined)
			return false;
		var dishCountValue = dish.find('.dish__count-value');
		if (data.count <= 0) {
			dishCountValue[0].style.display = 'none';
		} else {
			dishCountValue[0].style.display = 'block';
			dishCountValue.text(data.count + ' шт.');
		}
	}
}