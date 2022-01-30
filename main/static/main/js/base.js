function toggleHeader() {
    if (document.getElementById('header').style['top'] === '0em')
    {
        document.getElementById('header').style['top'] = '-3.5em';
        document.getElementById('body-container').style['top'] = '-3.5em';
        document.getElementById('body-container').style['margin-bottom'] = '-3.5em';
    }
    else
    {
      document.getElementById('header').style['top'] = '0em';
      document.getElementById('body-container').style['top'] = '0em';
      document.getElementById('body-container').style['margin-bottom'] = '0em';
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

function toggleSidebar() {
  sidebar = document.querySelector('#sidebar')
  if (sidebar.classList.length == 1) sidebar.classList.add('closed');
  else sidebar.classList.remove('closed');
  toggle = document.querySelector('#sidebartoggle');
  if (toggle.classList.length == 1) toggle.classList.add('toggleclose');
  else toggle.classList.remove('toggleclose');
}

function showDropdown() {
  document.getElementById('fabricDropdown').classList.remove('hidden')
}
function hideDropdown() {
  document.getElementById('fabricDropdown').classList.add('hidden')
}
