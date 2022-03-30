window.onload = function () {
  gapi.load('auth2', function() {
    gapi.auth2.init();
  })
}

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
function validate() {
  'use strict'

  //Fetch forms to apply validation
  var forms = document.querySelectorAll('.needs-validation')    

  //Loovp over them and prevent submission
  Array.prototype.slice.call(forms).forEach(function(form) {
    form.addEventListener('submit', function (event) {
      if (!form.checkValidity()) {
        event.preventDefault()
        event.stopPropagation()
      }
      form.classList.add('was-validated')
      if ($('#password2').val() != $('#password1').val()) {
          event.preventDefault()
          event.stopPropagation()
          alert('password missmatch')
        }
    }, false)
  })
}

function onSignIn(googleUser) {
  var profile = googleUser.getBasicProfile();
  console.log('ID: ' + profile.getId()); // Do not send to your backend! Use an ID token instead.
  console.log('Name: ' + profile.getName());
  console.log('Image URL: ' + profile.getImageUrl());
  console.log('Email: ' + profile.getEmail()); // This is null if the 'email' scope is not present.
}