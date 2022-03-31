slideShow = document.getElementById('wrap')
staticpopup = document.getElementById('staticpopup')

window.onload = function () {
let i = 0;
let j = 0;
slideimgs = document.getElementsByClassName('slideimg')
first = document.getElementById('slide1').classList.add('visible')

setInterval(() => {
    if (i == 0) {    
        slideimgs[3].classList.remove('visible')    
        slideimgs[0].classList.add('visible') }
    else {
    slideimgs[i-1].classList.remove('visible')
    slideimgs[i].classList.add('visible') }
    i++;
    if (i == slideimgs.length) i = 0;
    }, 5000);

setTimeout(() => {
    staticpopup.classList.remove('invisible')    
    setInterval(() => {
        staticpopup.className='pop';
        setTimeout(() => {
            staticpopup.className='staticpopup';
            }, 500);  
        }, 8000);   
}, 1000);
//15000
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

function scrollV() {
    let anchorlinks = document.querySelectorAll('a[href^="#"]')

    for (let item of anchorlinks) { // relitere 
        item.addEventListener('click', (e)=> {
        let hashval = item.getAttribute('href')
        let target = document.querySelector(hashval)
        target.scrollIntoView({
        behavior: 'smooth'
        })
        history.pushState(null, null, hashval)
        e.preventDefault()
    })
    }
}

function submit_form(el) {       
    form = document.getElementById('staticpopup')
    $.get('popauth', function(page, textStatus) {    
        $('#popauth').toggleClass('no-display');
        $('.popauth').html(page);
    });
}
