window.onload = function() {
    console.log(localStorage)
    clothes = {}
    keys = Object.keys(localStorage)   
    keys.forEach((key, index) => {
        if (key.includes('clothe')) {
            clothes[key] = localStorage[key]
        }
    });
    if (clothes.length != {}) {
        thestorage = JSON.stringify(clothes)
        $.get('?thestorage='+thestorage, function(page, textStatus) {
            $('.content').html(page)
        })
    }
}
