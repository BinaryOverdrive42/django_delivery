var c_basket = {
    init: function () {
        this.context = $("#c_basket");
        this.basketHeader = this.context.find(".c_basket__header");

        var basketOpen = sessionStorage.getItem('basket_open');
        if (parseInt(basketOpen) === 1) {
            this.basketHeader.on('click', this.closeBasket);
            this.context.addClass('c_basket_active');
        } else {
            this.basketHeader.on('click', this.openBasket);
        }
    },

    openBasket: function () {
        var self = c_basket;
        self.basketHeader.off('click').on('click', self.closeBasket);
        self.context.addClass('c_basket_active');
        sessionStorage.setItem('basket_open', '1');
    },

    closeBasket: function () {
        var self = c_basket;
        self.basketHeader.off('click').on('click', self.openBasket);
        self.context.removeClass('c_basket_active');
        sessionStorage.setItem('basket_open', '0');
    },

};