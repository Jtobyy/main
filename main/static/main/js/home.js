const form = document.getElementById('filter_form');
const filter = document.getElementById('filter_toggle');
const filterCont = document.getElementById('filter_container')

window.onload = function () {
    form.addEventListener('submit', function(event) {
        event.preventDefault();
        reload()
    })
    filter.addEventListener('click', function() {
        if (filterCont.classList == 'filter filter_more' ) filterCont.className = 'filter filter_less';
        else filterCont.classList = 'filter filter_more';
    })
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

function reload() {
    let xhttp = new XMLHttpRequest();
    const fd = new FormData(form);

    xhttp.addEventListener('load', function (event) {
        resp = JSON.parse(this.responseText);
        console.log(resp)
        fillImageShow(resp)
    })
    xhttp.addEventListener('error', function (event) {    
        console.log('error retrieving data')
    })
  xhttp.open("POST", "");
  xhttp.send(fd);
}

const category_obj = {
    'M': 'Male',
    'F': 'Female',
    'B': 'Baby',
    'T': 'Traditional',
    'O': 'Modern',
    'Mod': 'Modern',
    'C': 'Classic',
};

function fillImageShow(resp) {
    let container = document.getElementById('image_show');
    let loading = document.createElement('i');
    loading.className = 'bi-arrow-counterclockwise';
    container.innerHTML = " ";

    for (let i = 0; i < 6; i++) 
    {
        if (resp[i] == null) continue;    
        // console.log (resp[i]); 
        for (let j = 0; j < resp[i].length; j++) {
            let arg = resp[i][j];
            let item = document.createElement('div');
            item.className = 'col-sm-6';
            let imageDiv = document.createElement('div');
            imageDiv.className = 'img';
            let image = document.createElement('img');
           
            image.setAttribute('src', '/media/' + arg.fields.image);
            image.setAttribute('alt', " ");
            imageDiv.appendChild(image);
            item.appendChild(imageDiv);
            let info = document.createElement('div');
            info.className = 'info';

            let price = document.createElement('span');
            price.innerHTML = arg.fields.price;
            price.className = 'price';
            info.appendChild(price);

            let company = document.createElement('span');
            let link = document.createElement('a');
            link.setAttribute('href', '/main/tailorProfile/'+arg.name)
            company.innerHTML = arg.name;
            company.className = 'company';
            info.appendChild(link);
            link.appendChild(company);

            let category = document.createElement('span');
            if (arg.fields.category.length === 3)
            {
                category.innerHTML = category_obj[arg.fields.category[0]] + ', ' + category_obj[arg.fields.category[2]];
            }
            else category.innerHTML = category_obj[arg.fields.category[0]];
            category.className = 'category';
            info.appendChild(category);

            item.appendChild(info);
            container.appendChild(item);
        }
    }
}

