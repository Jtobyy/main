slideShow = document.getElementById('wrap')
staticpopup = document.getElementById('staticpopup')

window.onload = function () {
let i = 0;
let j = 0;
slideimgs = document.getElementsByClassName('slideimg')
first = document.getElementById('slide1').classList.add('visible')

$('#profileDropdown').popover({    
    container: 'body',
    html: true,
    content: $('#profileDropdownContent').html()
  })
  $('#popFabrics').popover({
    container: 'body',
    html: true,
    title: $('#title').html(),
    content: $('#fabricsDropdownContent').html(),
    trigger: 'focus'
})
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

function showLoading() {
    $('.loading').removeClass('no-display');
}
function removeLoading() {
    $('.loading').addClass('no-display');
}
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
