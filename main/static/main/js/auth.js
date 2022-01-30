window.onload = signIn()

function signUp() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
          document.getElementById('sign-in').style['visibility'] = "visible";  
          document.getElementById('form-container').innerHTML = this.responseText
        }
      };
      xhttp.open("GET", "register", true);
      xhttp.send();
}

function signIn() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
          document.getElementById('form-container').innerHTML = this.responseText
        }
        }
      xhttp.open("GET", "login", true);
      xhttp.send();
}
