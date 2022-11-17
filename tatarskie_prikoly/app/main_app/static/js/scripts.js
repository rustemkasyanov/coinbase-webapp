function confirm_delete() {
    return confirm('Are you sure you want delete this?');
}

// Get all single currencies
function getCurrencies() {
    const options = {method: 'GET', headers: {Accept: 'application/json'}};
    const currency_id_arr = [];

    fetch('https://api.exchange.coinbase.com/currencies', options)
        .then(response => response.json())
        .then(response => {
            for (let i = 0; i < response.length; i++) {
                currency_id_arr[i] = response[i]['id'];
            }
        })
        .catch(err => console.error(err));

    return currency_id_arr;
}

// Navbar Currecny Price form 
$('#navbar-currency-price').click(function(){
    const options = {method: 'GET', headers: {Accept: 'application/json'}};
    const currency = $('#navbar-currency-price-input').val();

    fetch(`https://api.coinbase.com/v2/prices/${currency}-USD/buy`, options)
        .then(response => response.json())
        .then(response => {
            data = response['data']['amount'];
            alert(`$ ${data}`);
        })
        .catch(err => {
            alert('Wrong currency');
        });
});

// Calculating min amount for sell 
$(function(){
    var typingTimer;
    $('.tradeform-predetermined').keyup(function(){
        if($('#tradeform_buy_currency').val() && $('#tradeform_buy_amount').val() && $('#tradeform_sell_currency').val()) {
            const buy_currency = $('#tradeform_buy_currency').val();
            const sell_currency = $('#tradeform_sell_currency').val();
            const buy_amount = $('#tradeform_buy_amount').val();

            const requestPrices = async () => {
                const options = {method: 'GET', headers: {Accept: 'application/json'}};
                try {
                    const response = await fetch(`https://api.coinbase.com/v2/exchange-rates?currency=${buy_currency}`, options);
                    const json = await response.json();
                    const rate = json['data']['rates'][`${sell_currency}`];
                    const total_value = parseFloat(rate) * parseFloat(buy_amount);
                    $('#tradeform_sell_amount').text(`${total_value} (${sell_currency})`);
                } catch (error) {
                    console.error(error);
                }
            }

            clearTimeout(typingTimer);
            typingTimer = setTimeout(requestPrices, 500);
        }
    });

    $('.tradeform-predetermined').keydown(function(){
        clearTimeout(typingTimer);
    });
});

// Autocomplete single currencies
$(function(){
    const currency_arr = getCurrencies();
    $('.currency-autocomplete').autocomplete({
        source: currency_arr,
    });
});
