var catalog = {
    init: function () {

    },
    em_updateOrderPrice: function (data) {
		var priceValue = $('.catalog-order-price');
		priceValue.text(data.price + ' руб.');
    }
};