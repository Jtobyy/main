window.onload = function () {
    $('#account').addClass('active')
    userId = $('#userId').val()
    var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
        $('.overview').html(this.responseText)
        }
    }
    xhttp.open("GET", userId+"?section=account&view="+localStorage.getItem('view', 'overview'), true);
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
// details section
// basic accout details
function edit1() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
    $('.overview').html(this.responseText)
    }
}
xhttp.open("GET", userId+"?section=account&view=accountdetails", true);
xhttp.send();
}

//address details
function edit2() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
    $('.overview').html(this.responseText)
    }
}
xhttp.open("GET", userId+"?section=account&view=addressbook", true);
xhttp.send();
}   
function edit3() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        $('.overview').html(this.responseText);
    }
}
xhttp.open("GET", userId+"?section=account&view=accountdetails", true);
xhttp.send();
}

function addressedit1() {
    $.get(userId+"?section=account&view=defaultaddress", function(page, textStatus) {
        $('.overview').html(page);
    });
};

function addressedit(address) {
    $.get(userId+"?section=account&view=addressedit&id="+address['id'], function(page, textStatus) {    
        $('.overview').html(page);
    });
};

function addressdelete(address) {
    $.get(userId+"?section=account&view=addressedit&action=delete&id="+address['id'], function(page, textStatus) {    
        $('.overview').html(page);
    });
};

function newaddress() {
    $.get(userId+"?section=account&view=newaddress", function(page, textStatus) {
        $('.overview').html(page);
    });
};

function changep() {
    $('#changep').toggleClass('changep');
}

function validatepass() {
    console.log('got here')
    $('#changepassbtn').click((event) => {
        if ($('#newp').text() !== $('#confirmp').text()) {
            event.preventDefault()
            alert(insimilarities)
        }
    })
}
