
document.addEventListener('DOMContentLoaded',() =>{
    try {
        document.querySelector('#edit_profile').addEventListener('click',() => editProfile());
    } catch (err) {
        console.log(err);    
    }
    
    try {
        document.querySelector('#file').addEventListener('change',() => uplaodProfilePic());
        
    } catch (err) {
        console.log(err)
        
    }
    try {
        document.querySelector('#addGigs').addEventListener('click',() => addGigtToggle());
    } catch (err) {
        console.log(err);
        
    }
    try{
        document.querySelector('#allGigs').addEventListener('click',() => allGigToggle());
    } catch (err){
        console.log(err)
    }
    try{
        document.querySelector('#comment-box-button').addEventListener('click',() => post_comment())
    } catch (err){
        console.log(err);
    }
    try{
        document.querySelector('#i_ur').addEventListener('click',() => add_to_libray())
    } catch (err){
        console.log(err);
    }
    try{
        document.querySelector('#n_ur').addEventListener('click',() => remove_from_libray())
    } catch (err){
        console.log(err);
    }
    try{
        document.querySelector('#d_ur').addEventListener('click',() => disabled_libray())
    } catch (err){
        console.log(err);
    }
})


// getting  cookies

function getCookie(c_name)
{
    if (document.cookie.length > 0)
    {
        c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1)
        {
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1) c_end = document.cookie.length;
            return unescape(document.cookie.substring(c_start,c_end));
        }
    }
    return "";
}


// nav bar resposiveness

const navSlide = () => {
    const cus_burger = document.querySelector('.cus_burger');
    const nav = document.querySelector(".cus-nav-links");
    const navLinks = document.querySelectorAll('.cus-nav-links li');
    cus_burger.addEventListener('click',()=>{
        nav.classList.toggle('cus-nav-active');
        navLinks.forEach((link,index) => {
            if (link.style.animation){
                link.style.animation = ''
            }else{
                link.style.animation = `navLinkFade 0.5s ease forwards ${index / 7 + 0.5}s`;
                console.log(`navLinkFade 0.5s ease forwards ${index / 7 + 2}s`);
            }
        });
    });
    
}

navSlide()

// edit profile details function
function editProfile(){
    // parent element
    let parentdiv = document.querySelector('.profile_details');

    // getting its children
    let children = parentdiv.children;
    console.log(children);

    //getting old data
    let name_div = children[1];
    let location_div = children[2];
    let service =  children[3]
    let old_name = name_div.innerHTML.split(': ')[1]
    let old_location = location_div.innerHTML.split(':')[1]
    let old_service =  service.innerHTML;

    // creating new nodes to replace the old
    let name_div_entry = document.createElement('input');
    name_div_entry.classList = 'inputarea';
    name_div_entry.type = 'text';
    name_div_entry.value = old_name;
    
    let location_div_entry = document.createElement('input');
    location_div_entry.classList = 'inputarea';
    location_div_entry.value = old_location;
   
    let service_options = document.createElement('label');
    service_options.htmlFor = '#editform';
    service_options.innerHTML = 'Select a service';

    let options = document.createElement('select')
    options.id = '#editform';
    options.innerHTML = `<option value="employer">Employer</option>
    <option value="employee">Employie</option>`;

    let save_button = document.createElement('input');
    save_button.classList = 'cus-button';
    save_button.id = 'save_edits';
    save_button.type = 'submit';
    save_button.value = 'save-profile';
   

    
    // replacing the old with new..
    parentdiv.replaceChild(name_div_entry,name_div);
    parentdiv.replaceChild(location_div_entry,location_div);
    parentdiv.replaceChild(service_options,children[3]);
    parentdiv.replaceChild(options,children[4]);
    parentdiv.append(save_button)
    //parentdiv.replaceChild(label_for,children[4]);
    //parentdiv.append(save_button);
    

    // adding eventlistener to save_edit button
    try {
        document.querySelector('#save_edits').addEventListener('click',() => saveEdits());
    } catch (err) {
        console.log(err);
        
    }
}


function saveEdits(){

    event.preventDefault

    // parent element
    let parentdiv = document.querySelector('.profile_details');

    // getting its children
    let children = parentdiv.children;
    console.log(children);

    // getting pk for th user ...
    let location_current = window.location.href;
    let pk = location_current.split('/')[4];
    
    // getting the new details...
    let new_name = children[1].value;
    let new_location = children[2].value;
    let new_service =  children[4].value

    console.log(new_name,new_location,pk,new_service);

    fetch(location_current,{
        method: 'PUT',
        body: JSON.stringify({
            type: 'edit-profile',
            pk: pk,
            name: new_name,
            location:new_location,
            service: new_service,
        }),
        credentials: 'same-origin',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    });
    setTimeout(() => {location.reload();},600);

}

function addGigtToggle(){
    x = document.querySelector('#form-gig');
    y = document.querySelector('#all-gig');
    if (x.style.display === '' || x.style.display == 'none'){
        x.style.display = 'block';
       
        y.style.display = 'none';
    }
    x.scrollIntoView({behavior: "smooth", block: "end", inline: "nearest"});
    //window.scrollBy(0,500);
}

function allGigToggle(){
    x = document.querySelector('#form-gig');
    y = document.querySelector('#all-gig');
    if (y.style.display === '' || y.style.display == 'none'){
        y.style.display = 'block';
       
        x.style.display = 'none';
    }
    y.scrollIntoView({behavior: "smooth", block: "end", inline: "nearest"});
    
}