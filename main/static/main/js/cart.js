
window.onload = requestCart()

function requestCart() {
console.log('got here')    
    basket = {
        'clothes':{},
        'fabrics':{}
    }
    keys = Object.keys(localStorage)   
    keys.forEach((key, index) => {
        if (key.includes('clothe')) {
            basket['clothes'][key] = localStorage[key]
        }
        else if (key.includes('fabric')) {
            basket['fabrics'][key] = localStorage[key]
        }
    });
    /* console.log(basket['fabrics'])
    console.log(basket['clothes'])*/
    if (basket['clothes'] == {} && basket['fabrics'] == {}) {}
    else {
        thestorage = JSON.stringify(basket)
        $.get('?thestorage='+thestorage, function(page, textStatus) {
            $('.content').html(page)
        })
    }
}   

function cartremove(div) {   
    category = div.dataset.name
    if (category.includes('Fabric')) {
        id = div['id']
        key = "fabric_"+id
        localStorage.removeItem(key)
        requestCart()
    }
    else if (category.includes('Clothe')) {
        id = div['id']
        key = "fabric_"+id
        localStorage.removeItem(key)
        requestCart()
    }
}