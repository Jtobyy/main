window.onload = function () {
    $('#account').addClass('active')
    userId = $('#userId').val()
    var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
        $('.overview').html(this.responseText)
        }
    }
    if (sessionStorage.getItem('view') != null) xhttp.open("GET", userId+"?section=account&view="+sessionStorage.getItem('view'), true);
    else xhttp.open("GET", userId+"?section=account&view=overview", true);
    xhttp.send();

    $('#account').click(() => {
        $('#logout').removeClass('active')      
        $('.nav-item').removeClass('active')
        $('#account').addClass('active')
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
        $('.overview').html(this.responseText)
        }
    }
    xhttp.open("GET", userId+"?section=account&view=overview", true);
    xhttp.send();
    })

    $('#inbox').click(() => {
      $('#logout').removeClass('active')      
      $('.nav-item').removeClass('active')
      $('#inbox').addClass('active')
      var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
        $('.overview').html(this.responseText)
        }
    }
    xhttp.open("GET", userId+"?section=inbox", true);
    xhttp.send();
    })
    $('#payment').click(() => {
        $('#logout').removeClass('active')      
        $('.nav-item').removeClass('active')
        $('#payment').addClass('active')
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
        $('.overview').html(this.responseText)
        }
    }
    xhttp.open("GET", userId+"?section=payment", true);
    xhttp.send();
    })
    $('#order').click(() => {
        $('#logout').removeClass('active')      
        $('.nav-item').removeClass('active')
        $('#order').addClass('active')  
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
        $('.overview').html(this.responseText)
        }
    }
    xhttp.open("GET", userId+"?section=orders", true);
    xhttp.send();
    })
    $('#logout').click(() => {
        $('.nav-item').removeClass('active')
        $('#logout').addClass('active')  
    })
}

function profileImage(id) {
    body = document.getElementsByTagName('body')[0]    
    display = document.createElement('div');
    image = document.createElement('img');

    image.setAttribute('src', document.getElementById('profileImage').src);
    close = document.createElement('i');
    close.className = 'bi-x-lg';
    display.appendChild(close);
    display.appendChild(image);
    body.classList.add("dim");
    image.className = 'pimage';
    display.className = 'display';
    body.appendChild(display);

    csrf_token = form.children['csrfmiddlewaretoken'].value;
    form.innerHTML = " ";
    form = document.getElementById('form');
    form.setAttribute('action', '/main/edit/'+id+'/');
    form.setAttribute('method', 'POST');
    form.className = 'form';

    csrf_input = document.createElement('input');
    csrf_input.setAttribute('type', 'hidden');
    csrf_input.setAttribute('name', 'csrfmiddlewaretoken');
    csrf_input.setAttribute('value', csrf_token);
    form.appendChild(csrf_input);
    
    console.log(form.children['csrfmiddlewaretoken'].value)
    
    imageInput = document.createElement('input');

    edit = document.createElement('a');
    editIcon = document.createElement('i');
    editIcon.className = 'bi-camera-fill';
    edit.appendChild(editIcon);
    edit.className = "edit";

    label = document.createElement('label');
    label.setAttribute('for', 'bg_image');
    label.className = 'custom-file-upload';
    label.appendChild(edit);
    imageInput.setAttribute('type', 'file')
    imageInput.setAttribute('id', 'bg_image')
    imageInput.setAttribute('name', 'profile_image')
    submit = document.createElement('input');
    submit.setAttribute('type', 'submit');
    span = document.createElement('span');
    span.setAttribute('id', 'file-selected');

    imageInput.addEventListener('change', function(e) {
        console.log(imageInput.value)
        span.innerHTML = imageInput.value;
        form.appendChild(span);
    })
    form.appendChild(label);
    form.appendChild(imageInput);
    form.appendChild(submit);
    display.appendChild(form);
    
    close.addEventListener('click', () => {
        body.classList.remove('dim');
        display.className = 'display_hidden';
    })    
}