function showfeats(thisdiv) {
    element = $(thisdiv).parent().children('.feats')
    $(element).css('display', 'flex')
}

function hidefeats(thisdiv) {
    element = $(thisdiv).parent().children('.feats')
    $(element).css('display', 'none')
}

function heart(el) {
    $(el).toggleClass("bi-heart-fill")
    $(el).toggleClass("bi-heart")
}
function cart(el) {
    $(el).toggleClass("bi-cart-fill")
    $(el).toggleClass("bi-cart")
}

function fabriccartadd(div) {
    id = div['id']
    key = "fabric_"+id
    console.log($(div).attr('class'))
    if ($(div).attr('class') == 'bi-cart-fill') {
    if (!localStorage[key]) localStorage[key]=id
    else localStorage.removeItem(key)
    }
}

function fabriccartremove(div) {    
    id = div['id']
    key = "fabric_"+id
    localStorage.removeItem(key)
}
