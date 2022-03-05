function cartadd(div) {    
    id = div['id']
    key = "fabric_"+id
    if (!localStorage[key]) {
        amount = $('#amount').val()
        if (amount > 0) {
            localStorage[key]=id + "_" + amount
            $(div).css('background-color', 'rgb(248, 220, 224)')
            $(div).css('padding-top', '10px')
            $(div).text('Added to cart')
        }
        else {
            alert("Order starts from at least 1 yard")
        }
    }
    else {
        localStorage.removeItem(key)
        $(div).css('background-color', 'rgba(255, 255, 255, .5)')
        $(div).css('padding-top', '2px')
        $(div).html('Add to cart<i class="bi-cart4"></i>')
    }
}

