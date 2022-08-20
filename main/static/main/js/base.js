$(document).ready(function () {
  //  $('#profileDropdown').popover({    
  //   container: 'body',
  //   html: true,
  //   content: $('#profileDropdownContent').html()
  // })
  // Displays profile dropdown when hovered and hides it when not
  $('.profile-dropdown-title').hover((el) => {
    // el.target return a DOM object ont a jquery object so removeClass won't work here
    el.target.nextElementSibling.classList.remove('hidden')
  })
  $('.profile-dropdown').mouseleave((el) => {
    // el.target return a DOM object ont a jquery object so removeClass won't work here
    $('.profile-dropdown').addClass('hidden');
    // // Make sure parent to hide is not the profile's title
    // arr = Array.from(el.target.parentElement.classList)
    // if (!arr.find((n) => n=='dropdown')) {
    //   console.log('got here')  
    //   el.target.parentElement.classList.add('hidden')
    // }
  })
  $('#link-to-create-account').click(() => {
    $('.popsign-up').removeClass('hidden')
  })

  $('#popFabrics').popover({
    container: 'body',
    html: true,
    content: $('#fabricsDropdownContent').html(),
  })
  $('.dropdown-toggle').dropdown()
  $('.alert').alert()
  $('#search-text').click(() => {
    let searchLink = document.getElementById('search-link')
    query = $('#query').val()
    if (query == '') query = 'search'
    searchLink.setAttribute('href', `/main/search/${query}`)
    searchLink.click()
  })
})
  /*
  gapi.load('auth2', function() {
      gapi.auth2.init();
  })
})*/

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

function showLoading() {
  $('.loading').removeClass('no-display');
}
function removeLoading() {
  $('.loading').addClass('no-display');
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

function submit_form(el) {       
  showLoading()    
  form = document.getElementById('staticpopup')
  $.get('popauth', function(page, textStatus) {    
      $('#popauth').toggleClass('no-display');
      $('.popauth').html(page);
      removeLoading();
  });
}

// Hides the parent of the element passed to it
function hidePopup(e) {
  e.parentElement.classList.add('hidden')
}