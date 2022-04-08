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
            else if (page == 'measurement') measurement();
            else if (page == 'steps') measureHowTo();
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
            removeLoading();
        }
        else {
            showLoading();
        }
    }
    xhttp.open("GET", userId+"?section=account&view=overview", true);
    xhttp.send();

    $('#account').click(account)
    $('#inbox').click(inbox)
    $('#payment').click(payment)
    $('#order').click(order)
    $('#wishlist').click(wishlist)
    $('#viewed').click(viewed)
    $('#measurement').click(measurement)
    $('#logout').click(logout)
    

    function account() {
        $('#logout').removeClass('active')      
        $('.nav-item').removeClass('active')
        $('#account').addClass('active')
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                $('.overview').html(this.responseText)
                history.pushState("overview", null, null);
                removeLoading();
            }
            else {
                showLoading();
            }
        }
        xhttp.open("GET", userId+"?section=account&view=overview", true);
        xhttp.send();    
    }

    function inbox() {
      $('#logout').removeClass('active')      
      $('.nav-item').removeClass('active')
      $('#inbox').addClass('active')
      var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                $('.overview').html(this.responseText)
                history.pushState("inbox", null, null);
                removeLoading();
            }
            else {
                showLoading();
            }
        }
        xhttp.open("GET", userId+"?section=inbox", true);
        xhttp.send();
    }

    function payment() {
        $('#logout').removeClass('active')      
        $('.nav-item').removeClass('active')
        $('#payment').addClass('active')
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            $('.overview').html(this.responseText)
            history.pushState("payment", null, null);
            removeLoading();
        }
        else {
            showLoading();
        }
    }
    xhttp.open("GET", userId+"?section=payment", true);
    xhttp.send();
    }

    function order() {
        $('#logout').removeClass('active')      
        $('.nav-item').removeClass('active')
        $('#order').addClass('active')  
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            $('.overview').html(this.responseText)
            history.pushState("order", null, null);
            removeLoading();
        }
        else {
            showLoading();
        }
    }
    xhttp.open("GET", userId+"?section=orders", true);
    xhttp.send();
    }
    
    function wishlist() {
        $('#logout').removeClass('active')      
        $('.nav-item').removeClass('active')
        $('#wishlist').addClass('active')  
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            $('.overview').html(this.responseText)
            history.pushState("order", null, null);
            removeLoading();
        }
        else {
            showLoading();
        }
    }
    xhttp.open("GET", userId+"?section=orders", true);
    xhttp.send();
    }

    function viewed() {
        $('#logout').removeClass('active')      
        $('.nav-item').removeClass('active')
        $('#viewed').addClass('active')  
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            $('.overview').html(this.responseText)
            history.pushState("order", null, null);
            removeLoading();
        }
        else {
            showLoading();
        }
    }
    xhttp.open("GET", userId+"?section=orders", true);
    xhttp.send();
    }

    function measurement() {
        $('#logout').removeClass('active')      
        $('.nav-item').removeClass('active')
        $('#measurement').addClass('active')  
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            $('.overview').html(this.responseText)
            history.pushState("measurement", null, null);
            removeLoading();
        }
        else {
            showLoading();
        }
    }
    xhttp.open("GET", userId+"?section=measurement", true);
    xhttp.send();
    }    


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

function showLoading() {
    $('.loading').removeClass('no-display');
}
function removeLoading() {
    $('.loading').addClass('no-display');
}

// details section
// basic accout details
function edit1() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        $('.overview').html(this.responseText)
        history.pushState('accountdetails', null, null)
        removeLoading();
    }
    else {
        showLoading();
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
        removeLoading();
    }
    else {
        showLoading();
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
        removeLoading();
    }
    else {
        showLoading();
    }
}
xhttp.open("GET", userId+"?section=account&view=accountdetails", true);
xhttp.send();
}

function addressedit(address) {
    showLoading();
    $.get(userId+"?section=account&view=addressedit&id="+address['id'], function(page, textStatus) {    
        $('.overview').html(page);
        history.pushState('addressedit', null, null)
        removeLoading();
    });
};

function addressdelete(address) {
    showLoading();    
    $.get(userId+"?section=account&view=addressedit&action=delete&id="+address['id'], function(page, textStatus) {    
        $('.overview').html(page);
        history.pushState('addressdelete', null, null)
        removeLoading();
    });
};

function newaddress() {
    showLoading();        
    $.get(userId+"?section=account&view=newaddress", function(page, textStatus) {
        $('.overview').html(page);
        history.pushState('newaddress', null, null)
        removeLoading();
    });
};

function changep() {
    showLoading();
    $('#changep').toggleClass('changep');
    removeLoading();
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
    $('#nav').slideToggle()
}

function measureHowTo() {
    showLoading();        
    $.get(userId+"?section=measurement&view=steps", function(page, textStatus) {
        $('.overview').html(page);
        history.pushState('steps', null, null)
        let promise = new Promise((resolve, reject) => {
            document.getElementById('topmost').scrollIntoView({
            behavior: 'smooth'
        })
        resolve()}) 
        promise.then(removeLoading)
    });    
}
function measureRequest() {
    showLoading();        
    $.get(userId+"?section=measurement&view=requestpro", function(page, textStatus) {
        $('.overview').html(page);
        history.pushState('steps', null, null)
        document.getElementById('topmost').scrollIntoView({
            behavior: 'smooth'
        })
        removeLoading();
    });        
}