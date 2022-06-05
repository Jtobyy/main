var business_info = ''
var userId
$(document).ready(function () 
{
    current_url = window.location.href
    let url = new URL(current_url);
    let exsection = url.searchParams.get("exsection");
    userId = $('#userId').val()
    if (sessionStorage['section'] == 'partnermarkets') {
        $('.nav-item').removeClass('active')
        $('#market').addClass('active')
        quantity()
        sessionStorage.setItem('section', '')
    }
    if (exsection == 'notifications') {
        history.pushState("notification", null, userId)    
        notification()
    }
    else if (exsection == 'specialization') {
        history.pushState("specilization", null, userId)    
        specialization()
    }
    else if (sessionStorage['section'] == 'market') {
        market()
        sessionStorage.setItem('section', '')
    }
    else if (sessionStorage['section'] == 'quantity') {
        quantity()
        sessionStorage.setItem('section', '')
    }
    else if (sessionStorage['section'] == 'specialization') {
        specialization()
        sessionStorage.setItem('section', '')
    }
    else if (sessionStorage['section'] == 'notification') {
        notification()
        sessionStorage.setItem('section', '')
    }
    else if (sessionStorage['section'] == 'security') {
        security()
        sessionStorage.setItem('section', '')
    }
    else if (sessionStorage['section'] == 'payment') {
        payment()
        sessionStorage.setItem('section', '')
    }
    else if (sessionStorage['section'] == 'account') {
        account()
        sessionStorage.setItem('section', '')
    }
    else {
        account()
    }
    window.addEventListener('popstate', (e) => {
        if (e.state != null) {
            page = e.state;
            if (page == 'account') account();
            else if (page == 'specialization') specialization();
            else if (page == 'security') security();
            else if (page == 'notification') notification();
            else if (page == 'portfolio') portfolio();
            else if (page == 'market') market();            
            else if (page == 'payment') payment();
            else if (page == 'logout') logout();
        }
    })

    $('#account').click(account);    
    $('#specialization').click(specialization); 
    $('#security').click(security);
    $('#notification').click(notification);
    $('#portfolio').click(portfolio);
    $('#market').click(market);
    $('#payment').click(payment); 

})

function account() {
    $('.nav-item').removeClass('active')
    $('#account').addClass('active')
    var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            $('.overview').html(this.responseText)
            history.pushState('account', null, null);
            sessionStorage.setItem('section', 'account')
            removeLoading();
        }
        else {
            showLoading();
        }
    }
    xhttp.open("GET", userId+"?section=account", true);
    xhttp.send();
}

function specialization() {
    $('.nav-item').removeClass('active')
    $('#specialization').addClass('active')
    showLoading();        
    $.get(userId+"?section=specialization", function(page, textStatus) {
        $('#overview').html(page);
        history.pushState('specialization', null, null);
        sessionStorage.setItem('section', 'specialization')
        removeLoading();
    });
}

function security() {
    $('.nav-item').removeClass('active')
    $('#security').addClass('active')
    showLoading();        
    $.get(userId+"?section=security", function(page, textStatus) {
        $('#overview').html(page);
        history.pushState('security', null, null);
        sessionStorage.setItem('section', 'security')
        removeLoading();
    });
}

function notification() {
    $('.nav-item').removeClass('active')
    $('#notification').addClass('active')
    showLoading();        
    $.get(userId+"?section=notifications", function(page, textStatus) {
        $('#overview').html(page);
        history.pushState('notification', null, null);
        sessionStorage.setItem('section', 'notification')
        removeLoading();
    });
}

function portfolio() {
    $('.nav-item').removeClass('active')
    $('#portfolio').addClass('active')
}

function market() {
    $('.nav-item').removeClass('active')
    $('#market').addClass('active')
    showLoading();        
    $.get(userId+"?section=market", function(page, textStatus) {
        $('#overview').html(page);
        history.pushState('market', null, null);
        sessionStorage.setItem('section', 'market')
        removeLoading();
    });
}

function payment() {
    $('.nav-item').removeClass('active')
    $('#payment').addClass('active')
    showLoading();
    $.get(userId+"?section=payment", function(page, textStatus) {
        $('#overview').html(page);
        history.pushState('payment', null, null);
        sessionStorage.setItem('section', 'payment')
        removeLoading();
    });
}

function editContactInfo() {    
    showLoading();        
    $.get(userId+"?section=contactinfo", function(page, textStatus) {
        business_info = $('#contactSection').html();
        $('#contactSection').html(page);
        $('.bi-pencil-square').addClass('hidden')
        removeLoading();
    });
}

function changePassword() {
    showLoading()
    $.get(userId+"?section=editpassword", function(page, textStatus) {
        $('.overview').append(page);
        $('.bi-pencil-square').addClass('hidden')
        removeLoading();
    });
}

function cancelEditContact() {
    $('.bi-pencil-square').removeClass('hidden')
    $('#contactSection').html(business_info);
}    
function cancelPasswordChange() {
    $('.bi-pencil-square').removeClass('hidden')    
    $('#passwordSection').remove();
}    

function validatePassword(password) {
    if (password.length === 0) {
        $('#strength').html('')
    }
    let matchedCase = []
    matchedCase.push("[$@$!%*#?&]"); // Special Charector
    matchedCase.push("[A-Z]");      // Uppercase Alpabates
    matchedCase.push("[0-9]");      // Numbers
    matchedCase.push("[a-z]");     // Lowercase Alphabates

    ctr = 0
    matchedCase.forEach((el) => {
        if (new RegExp(el).test(password)) ctr++
    })
    let color = "";
    let strength = "";

    switch (ctr) {
        case 0:
        case 1:
        case 2:
            strength = "very weak";
            color = "red";
            break;
        case 3:
            strength = "medium"
            color = "orange"
            break;
        case 4:
            strength = "strong"
            color = "green"
            break;
    }
    $('#strength').html(strength)
    $('#strength').css('color', color)
}

function preventDefault(e) {
    e.preventDefault();
}

function confirmPassword(password) {
   new_password = $('#new_password').val()
   if (new_password !== password) {
        $('#confirm_password').css('border', '1px solid red')
        $('#passwordForm').bind('submit', preventDefault)
   }
   else {
       $('#confirm_password').css('border', '1px solid green')
       $('#passwordForm').unbind('submit', preventDefault)
   }
}

function delivered() {
    showLoading()
    $.get(userId+"?section=deliveredorders", function(page, textStatus) {
        $('.overview').html(page);
        history.pushState("market", null, null);
        removeLoading();
    });
};

function accepted() {
    showLoading()
    $.get(userId+"?section=acceptedorders", function(page, textStatus) {
        $('.overview').html(page);
        history.pushState("market", null, null);
        removeLoading();
    });
};

function readied() {
    showLoading()
    $.get(userId+"?section=readiedorders", function(page, textStatus) {
        $('.overview').html(page);
        history.pushState("market", null, null);
        removeLoading();
    });
};

function pending() {
    showLoading()
    $.get(userId+"?section=pendingorders", function(page, textStatus) {
        $('.overview').html(page);
        history.pushState("market", null, null);
        removeLoading();
    });
};

function fabricorderDetails(id, source) {
    showLoading();
    if (source === 'order' || source === '') {
        $.get(userId+"?section=fabricorderdetails&orderid="+id, function(page, textStatus) {
            $('.overview').html(page);
            history.pushState("market", null, null);
            removeLoading();
        });
    }
    else {
        $.get(userId+"?section=fabricorderdetails&orderid="+id+"&notificationid="+source, function(page, textStatus) {
            $('.overview').html(page);
            history.pushState("market", null, null);
            removeLoading();
        });
    }
}
function cclothorderDetails(id, source) {
    showLoading();
    if (source === 'order' || source === '') {
        $.get(userId+"?section=cclothorderdetails&orderid="+id, function(page, textStatus) {
            $('.overview').html(page);
            history.pushState("market", null, null);
            removeLoading();
        });
    }
    else {
        $.get(userId+"?section=cclothorderdetails&orderid="+id+"&notificationid="+source, function(page, textStatus) {
            $('.overview').html(page);
            history.pushState("market", null, null);
            removeLoading();
        });
    }
}
function sclothorderDetails(id, source) {
    showLoading();
    if (source === 'order' || source === '') {
        $.get(userId+"?section=sclothorderdetails&orderid="+id, function(page, textStatus) {
            $('.overview').html(page);
            history.pushState("market", null, null);
            removeLoading();
        });
    }
    else {
        $.get(userId+"?section=sclothorderdetails&orderid="+id+"&notificationid="+source, function(page, textStatus) {
            $('.overview').html(page);
            history.pushState("market", null, null);
            removeLoading();
        });
    }
}

function acceptfabricOrder(id) {
    showLoading();
    $.get(userId+"?section=acceptfabricorder&orderid="+id, function(reply, textStatus) {
        if (reply === 'accepted') {
            $('#acceptOrder').addClass('hidden')
            alert('Order Accepted')
            $('#accepted').removeClass('hidden')
        }
        removeLoading();
    });
}
function acceptcclothOrder(id) {
    showLoading();
    $.get(userId+"?section=acceptcclothorder&orderid="+id, function(reply, textStatus) {
        if (reply === 'accepted') {
            $('#acceptOrder').addClass('hidden')
            alert('Order Accepted')
            $('#accepted').removeClass('hidden')
        }
        removeLoading();
    });
}
function acceptsclothOrder(id) {
    showLoading();
    $.get(userId+"?section=acceptsclothorder&orderid="+id, function(reply, textStatus) {
        if (reply === 'accepted') {
            $('#acceptOrder').addClass('hidden')
            alert('Order Accepted')
            $('#accepted').removeClass('hidden')
        }
        removeLoading();
    });
}

function quantity() {    
    showLoading()
    $('.nav-item').removeClass('active')
    $('#market').addClass('active')
    $.get(userId+"?section=marketobjects", function(page, textStatus) {
        $('.overview').html(page);
        sessionStorage.setItem('section', 'quantity')
        removeLoading();
    });
};

function addFabric() {
    showLoading()
    $('.nav-item').removeClass('active')
    $('#market').addClass('active')
    $.get(userId+"?section=addfabric", function(page, textStatus) {
        $('.overview').html(page);
        sessionStorage.setItem('section', 'quantity')
        removeLoading();
    });
};
function addClothSample() {
    showLoading()
    $.get(userId+"?section=addclothsample", function(page, textStatus) {
        $('.overview').html(page);
        sessionStorage.setItem('section', 'quantity')
        removeLoading();
    });
};

function readyfabricOrder(id) {
    showLoading()
    $.get(userId+"?section=readyfabricorder&orderid="+id, function(response, textStatus) {
        if (response == 'readied') {
            market()
            removeLoading();
        }
    });
}
function readycclothOrder(id) {
    showLoading()
    $('.nav-item').removeClass('active')
    $('#market').addClass('active')
    $.get(userId+"?section=readycclothorder&orderid="+id, function(response, textStatus) {
        if (response == 'readied') {
            market()
            removeLoading();
        }
    });
}
function readysclothOrder(id) {
    showLoading()
    $('.nav-item').removeClass('active')
    $('#market').addClass('active')
    $.get(userId+"?section=readysclothorder&orderid="+id, function(response, textStatus) {
        if (response == 'readied') {
            market()
            removeLoading();
        }
    });
}

function navToggle() {
    $('#nav').slideToggle()
}
