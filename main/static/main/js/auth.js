var a = document.getElementsByClassName('request')[0]
opt = {opt1: measuredetails, 
      opt2: howtoselfmeasure,
      opt3: requestpro,
}

window.onload = function() {
  formtype = document.getElementById('formtype').value
  if (formtype == "" || formtype == 'signin') signIn();
  if (formtype == "signup") signUp();
  else if (formtype == "measureopt") {measureOpt();}
  else {opt[formtype]()};
}

function signUp() {
    a.style['display'] = 'block';
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
          document.getElementById('form-container').innerHTML = this.responseText
          document.getElementById('sign-up').style['visibility'] = "visible";  
        }
      };
      xhttp.open("GET", "register", true);
      xhttp.send();
}

function signIn() {
    a.style['display'] = 'none';  
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
          document.getElementById('form-container').innerHTML = this.responseText
        }
        }
      xhttp.open("GET", "login", true);
      xhttp.send();
}

function measureOpt() {
  a.style['display'] = 'none';
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
        document.getElementById('form-container').innerHTML = this.responseText
      }
      }
    xhttp.open("GET", "measureopt", true);
    xhttp.send();
}

//measurement options
function measuredetails(){
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
        document.getElementById('form-container').innerHTML = this.responseText
      }
      }
    xhttp.open("GET", "measuredetails", true);
    xhttp.send();  
}      

function howtoselfmeasure(){
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
        document.getElementById('form-container').innerHTML = this.responseText
      }
      }
    xhttp.open("GET", "measurehowto", true);
    xhttp.send();  
}  
function requestpro(){
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
        document.getElementById('form-container').innerHTML = this.responseText
      }
      }
    xhttp.open("GET", "promeasure", true);
    xhttp.send();  
}

function malebtn() {
  if ($('#maledetails').css('display') == 'none') {
    $('#maledetails').slideToggle()
    $('#femaledetails').slideToggle() }
}
function femalebtn() {  
  if ($('#maledetails').css('display') != 'none') {
    $('#femaledetails').slideToggle()
    $('#maledetails').slideToggle() }
}
