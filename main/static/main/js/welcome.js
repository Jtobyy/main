slideShow = document.getElementById('wrap')
window.onload = function () {    
let i = 0;
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