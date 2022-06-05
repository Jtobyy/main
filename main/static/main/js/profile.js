$(document).ready(function () {
    current_url = window.location.href
    let url = new URL(current_url);
    let exsection = url.searchParams.get("exsection");
    window.addEventListener('popstate', (e) => {
        if (e.state != null) {
            page = e.state;
            if (page == 'overview') account();
            else if (page == 'inbox') inbox();
            else if (page == 'payment') payment();
            else if (page == 'order') order();
            else if (page == 'logout') logout();
            else if (page == 'accountdetails') edit1();
            else if (page == 'addressbook') addressbook();
            else if (page == 'addressedit') addressedit();
            else if (page == 'addressdelete') addressdelete();
            else if (page == 'newaddress') newaddress();
            else if (page == 'measurement') measurement();
            else if (page == 'steps') measureHowTo();
        }
    })
    userId = $('#userId').val()
    if (exsection == 'order') {
        history.pushState("order", null, userId)    
        order()
    }
    else if (exsection == 'inbox') {
        history.pushState("inbox", null, userId)
        inbox()
    }
    else if (sessionStorage['section'] == 'measurement') {
        history.pushState("measurement", null, userId)        
        measurement()
        sessionStorage.setItem('section', '')
    }
    else if (sessionStorage['section'] == 'account') {
        history.pushState("account", null, userId)        
        account()
        sessionStorage.setItem('section', '')
    }
    else if (sessionStorage['section'] == 'inbox') {
        history.pushState("inbox", null, userId)        
        inbox()
        sessionStorage.setItem('section', '')
    }
    else if (sessionStorage['section'] == 'order') {
        history.pushState("order", null, userId)        
        order()
        sessionStorage.setItem('section', '')
    }
    else if (sessionStorage['section'] == 'addressbook') {
        history.pushState("order", null, userId)        
        addressbook()
        sessionStorage.setItem('section', '')
    }
    else {
        $('#account').addClass('active')
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
    }

    $('#account').click(account)
    $('#inbox').click(inbox)
    $('#payment').click(payment)
    $('#order').click(order)
    $('#wishlist').click(wishlist)
    $('#viewed').click(viewed)
    $('#measurement').click(measurement)
    $('#logout').click(logout)
})

function account() {
    $('#logout').removeClass('active')      
    $('.nav-item').removeClass('active')
    $('#account').addClass('active')
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            $('.overview').html(this.responseText)
            history.pushState("overview", null, null);
            sessionStorage.setItem('section', 'account')
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
            sessionStorage.setItem('section', 'inbox')
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
        sessionStorage.setItem('section', 'order')
        removeLoading();
    }
    else {
        showLoading();
    }
}
xhttp.open("GET", +userId+"?section=orders", true);
xhttp.send();
}

function fabricorderDetails(id) {
    showLoading();
    $.get(userId+"?section=fabricorderdetails&orderid="+id, function(page, textStatus) {
        $('.overview').html(page);
        $('.overview').html(this.responseText)
        history.pushState("order", null, null);
        removeLoading();
    });
}
function cclothorderDetails(id) {
    showLoading();
    $.get(userId+"?section=cclothorderdetails&orderid="+id, function(page, textStatus) {
        $('.overview').html(page);
        $('.overview').html(this.responseText)
        history.pushState("order", null, null);
        removeLoading();
    });
}
function sclothorderDetails(id) {
    showLoading();
    $.get(userId+"?section=sclothorderdetails&orderid="+id, function(page, textStatus) {
        $('.overview').html(page);
        $('.overview').html(this.responseText)
        history.pushState("order", null, null);
        removeLoading();
    });
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
        sessionStorage.setItem('section', 'measurement')
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
function addressbook() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        $('.overview').html(this.responseText)
        history.pushState('addressbook', null, null)
        sessionStorage.setItem('section', 'addressbook')
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
        sessionStorage.setItem('section', 'addressbook')
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

function profilePic() {
    imageInput = document.getElementById('profileImageInput')    
    
    imageInput.click()
    $('#profileImageInput').change(function() {
        const reader = new FileReader()    
        reader.readAsDataURL(imageInput.files[0])
        reader.onload = function(e) {
            $('#profileImage').attr('src', e.target.result)
        }
        $('#profileImageForm').submit()
    })
}
