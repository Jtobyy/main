$(document).ready(function () {
    showLoading()
    requestCart()
    removeLoading()    
})
  
function requestCart() {    
    basket = {
        'clothes':{},
        'fabrics':{}
    }
    keys = Object.keys(localStorage)   
    keys.forEach((key, index) => {
        if (key.includes('cloth')) {
            basket['clothes'][key] = localStorage[key]
        }
        else if (key.includes('fabric')) {
            basket['fabrics'][key] = localStorage[key]
        }
    });
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
    console.log(category)
    if (category.includes('Fabric')) {
        id = div['id']
        key = "fabric_"+id
        localStorage.removeItem(key)
        requestCart()
    }
    else if (category.includes('Cloth')) {
        id = div['id']
        key = "cloth_"+id
        localStorage.removeItem(key)
        requestCart()
    }
}

function showLoading() {
    $('.loading').removeClass('no-display');
}

function removeLoading() {
$('.loading').addClass('no-display');
}
