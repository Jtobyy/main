window.onload = function () {
    window.addEventListener('popstate', (e) => {
        if (e.state != null) {
            page = e.state;
            if (page == 'overview') account();
            else if (page == 'inbox') inbox();
            else if (page == 'payment') payment();
            else if (page == 'order') order();
            else if (page == 'logout') logout();
            else if (page == 'accountdetails') edit1();
            else if (page == 'addressbook') edit2();
            else if (page == 'addressedit') addressedit();
            else if (page == 'addressdelete') addressdelete();
            else if (page == 'newaddress') newaddress();
        }
    })    
    $('#account').addClass('active')
    userId = $('#userId').val()
    var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            $('.overview').html(this.responseText)
            url = 'overview'
            history.pushState(url, null, null);
        }
    }
    xhttp.open("GET", userId+"?section=account&view=overview", true);
    xhttp.send();

    $('#account').click(account)
    
    function account() {
        $('#logout').removeClass('active')      
        $('.nav-item').removeClass('active')
        $('#account').addClass('active')
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                $('.overview').html(this.responseText)
                history.pushState("overview", null, null);
            }
        }
        xhttp.open("GET", userId+"?section=account&view=overview", true);
        xhttp.send();    
    }


    $('#inbox').click(inbox)

    function inbox() {
      $('#logout').removeClass('active')      
      $('.nav-item').removeClass('active')
      $('#inbox').addClass('active')
      var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                $('.overview').html(this.responseText)
                history.pushState("inbox", null, null);
            }
        }
        xhttp.open("GET", userId+"?section=inbox", true);
        xhttp.send();
    }


    $('#payment').click(payment)

    function payment() {
        $('#logout').removeClass('active')      
        $('.nav-item').removeClass('active')
        $('#payment').addClass('active')
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            $('.overview').html(this.responseText)
            history.pushState("payment", null, null);
        }
    }
    xhttp.open("GET", userId+"?section=payment", true);
    xhttp.send();
    }

    $('#order').click(order)
    
    function order() {
        $('#logout').removeClass('active')      
        $('.nav-item').removeClass('active')
        $('#order').addClass('active')  
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            $('.overview').html(this.responseText)
            history.pushState("order", null, null);
        }
    }
    xhttp.open("GET", userId+"?section=orders", true);
    xhttp.send();
    }

    $('#logout').click(logout)
    
    function logout() {
        $('.nav-item').removeClass('active')
        $('#logout').addClass('active')  
        history.pushState("logout", null, null);
    }

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

// details section
// basic accout details
function edit1() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        $('.overview').html(this.responseText)
        history.pushState('accountdetails', null, null)
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
        history.pushState('addressbook', null, null)
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

function addressedit(address) {
    $.get(userId+"?section=account&view=addressedit&id="+address['id'], function(page, textStatus) {    
        $('.overview').html(page);
        history.pushState('addressedit', null, null)
    });
};

function addressdelete(address) {
    $.get(userId+"?section=account&view=addressedit&action=delete&id="+address['id'], function(page, textStatus) {    
        $('.overview').html(page);
        history.pushState('addressdelete', null, null)
    });
};

function newaddress() {
    $.get(userId+"?section=account&view=newaddress", function(page, textStatus) {
        $('.overview').html(page);
        history.pushState('newaddress', null, null)
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

function navToggle() {
    $('#nav').fadeToggle()
}