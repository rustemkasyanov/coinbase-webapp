const currency_arr = [];

function updateCurrencyArray(){
    var ticker_elements = $('.ticker__item');
    for(var i = 0; i < ticker_elements.length; i++){
        var item = ticker_elements[i].id;
        currency_arr.push(item.replace("price-", ""));
    }
}

function getCurrencyPrices(currency){
    const options = {method: 'GET', headers: {Accept: 'application/json'}};

    fetch(`https://api.exchange.coinbase.com/products/${currency}-USD/ticker`, options)
        .then(response => response.json())
        .then(response => {
            data = response['price'];
            $(`#price-${currency}`).text(`${currency} ($${data})`);
        })
        .catch(err => {
            console.log(err);
        });
}

function updatePrices(){
    currency_arr.forEach(getCurrencyPrices);
    setTimeout(updatePrices, 3000);
}

updateCurrencyArray();
updatePrices();
