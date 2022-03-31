const form = document.getElementById('filter_form');
const filter = document.getElementById('filter_toggle');
const filterCont = document.getElementById('filter_container')

window.onload = function () {
    filter.addEventListener('click', function() {
        if (filterCont.classList == 'filter filter_more' ) filterCont.className = 'filter filter_less';
        else filterCont.classList = 'filter filter_more';
    })

/*
      gapi.load('auth2', function() {
          gapi.auth2.init();
      })*/
      $('.profileDropdown').hover(
        () => { $('.profileItems').removeClass('hidden') },
        () => { $('.profileItems').addClass('hidden') }
      )
      $('.profileItems').mouseover(
        () => { $('.profileItems').removeClass('hidden') }
      )    
}

function cartadd(div) {    
    id = div['id']
    key = "clothe_"+id
    if (!localStorage[key]) {
        localStorage[key]=id
        $(div).css('background-color', 'rgb(248, 220, 224)')
        $(div).css('padding-top', '10px')
        $(div).text('Added to cart')
    }
    else {
        localStorage.removeItem(key)
        $(div).css('background-color', 'rgba(255, 255, 255, .5)')
        $(div).css('padding-top', '2px')
        $(div).html('Add to cart<i class="bi-cart4"></i>')
    }
}

function cartremove(div) {    
    id = div['id']
    key = "clothe_"+id
    localStorage.removeItem(key)
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
