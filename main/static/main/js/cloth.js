$('document').ready(function() {
    id = $('#object_id').val()
    key = "cloth_"+id
    if (localStorage[key]) {
        $('.cart').css('background-color', 'rgb(248, 220, 224)')
        $('.cart').css('padding-top', '10px')
        $('.cart').text('Remove from cart')
    }
})

function cartadd(div) {    
    id = div['id']
    key = "cloth_"+id
    if (!localStorage[key]) {
        amount = $('#amount').val()
        console.log(amount)
        localStorage[key]=id + "_" + amount
        $(div).css('background-color', 'rgb(248, 220, 224)')
        $(div).css('padding-top', '10px')
        $(div).text('Remove from cart')
    }
    else {
        localStorage.removeItem(key)
        $(div).css('background-color', 'rgb(240, 158, 240)')
        $(div).css('padding-top', '2px')
        $(div).html('Add to cart<i class="bi-cart4"></i>')
    }
}
