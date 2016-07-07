// I have moved this current page variable to the DOM which is provided
// by the server
// var currentPage = 0;
// TODO change this to pull the page_request_var from the DOM

var POSTSAPP = POSTSAPP || {};
var CONTACTAPP = CONTACTAPP || {};

var windowHeight = window.innerHeight;
var windowWidth = window.innerwidth;

// IIFE because I'm getting an attribute which needs to call another function
POSTSAPP.page_request_var = (function() {
    return getAttribute(document.getElementById('post-list'), 'data-page-request-var');
})();
POSTSAPP.last_post_page_name = "last_post_page";
POSTSAPP.read_more_button = document.getElementById("read-more-button");

CONTACTAPP.contact_us_button = document.getElementById('contact-us-button');
CONTACTAPP.page_container = document.getElementById('contact-faded-container');
CONTACTAPP.contact_form = document.getElementById('contact-form');
CONTACTAPP.exit_contact_button = document.getElementById('exit-contact-button');

// we wanrt to add all the event handlers once the page has loaded
// TODO might consider doing that DOM built thing instead
window.onload = function () {
    prepareEventHandlers();
    makeRequest();

}

/** Prepares all the event handlers once the window is loaded **/
function prepareEventHandlers() {
    POSTSAPP.read_more_button.addEventListener("click", makeRequest, false);
    CONTACTAPP.contact_us_button.addEventListener("click", showContactHidePage, false);
    // CONTACTAPP.page_container.addEventListener("click", hideContactPage, false);
    document.getElementsByTagName('body')[0].addEventListener('click', hideContactPage, false);
    CONTACTAPP.exit_contact_button.addEventListener('click', hideContactShowPage, false);
}

/** Hides contact page when the the user clicks away from the contact page **/
function hideContactPage(event) {

    // http://stackoverflow.com/a/3028037
    if (!event.target.closest('#contact-form') && !event.target.closest('#contact-us-button')) {
        if (CONTACTAPP.contact_form.classList.contains("contact-us-visible")) {
            hideContactShowPage();
        }
    }
}

/** Hides the contact page and shows the main page **/
function hideContactShowPage() {
    CONTACTAPP.page_container.classList.remove('faded-element');
    CONTACTAPP.contact_form.classList.remove('contact-us-visible');
    CONTACTAPP.contact_form.classList.add('contact-us-hidden');

}

/** fades the web page and overlays the contact form **/
function showContactHidePage() {
    CONTACTAPP.page_container.classList.add('faded-element');
    CONTACTAPP.contact_form.classList.remove('contact-us-hidden');
    CONTACTAPP.contact_form.classList.add('contact-us-visible');
}


/** This object sets up a Post List HTTP Request.
I decided to go with a constructor function because I want to be able to
re-use this object with different parameters. 
@constructor **/
function PostListHttpRequest() {

    if (document.getElementById(POSTSAPP.last_post_page_name)) {
        this.previous_post_page = document.getElementById(POSTSAPP.last_post_page_name);
        this.requested_page = Number(this.previous_post_page.getAttribute("data-page-number")) + 1;
    } else {
        this.requested_page = "0";
    }
    // No matter if this is the first set of posts or the 2nd, 
    // the target container will always be the first child of the post-list
    // <section> tag
    // Used firstElementChild because firstChild returns a textNode
    this.target_container = document.getElementById("post-list").firstElementChild; 
    this.httpRequest = new XMLHttpRequest();
    this.request_url = "grid/?" + POSTSAPP.page_request_var + "=" + this.requested_page;    
}

/** makeRequest will use the information set-up by PostListHttpRequest to
actually make the request. It then calls addNewPosts to deal with adding the 
response to the DOM. 
**/
function makeRequest() {
    // TODO Look into integrating this into the PostListHttpRequest object.
    var postRequest = new PostListHttpRequest();

    // Not sure why MDN suggesting this statement. If I don't understand why
    // something is in my code, I should p>.5 rm it.
    if (!postRequest.httpRequest) {
        alert('Http Request not made!');
        return false;
    }
    //
    postRequest.httpRequest.onreadystatechange = function(){addNewPosts(postRequest)};
    postRequest.httpRequest.open('GET', postRequest.request_url);
    postRequest.httpRequest.send();
}

function addNewPosts(rqst) {
    if (rqst.httpRequest.readyState === XMLHttpRequest.DONE) {
        if (rqst.httpRequest.status === 200) {
            // i want to put each set of posts in a containing div 
            // so that I can just set the innerHTML of that element and append
            // it to the post container
            post_page_ele = document.createElement("div");
            post_page_ele.setAttribute('class', 'post-page');

            if (rqst.previous_post_page) {
                checkAndRemoveAttribute(rqst.previous_post_page, 'id');
            }

            post_page_ele.setAttribute('id', POSTSAPP.last_post_page_name);
            post_page_ele.setAttribute('data-page-number', rqst.requested_page);
            post_page_ele.innerHTML = rqst.httpRequest.responseText;
            // parent_container is the div containing the post-page div
            // so I can just append another post-page div to that
            rqst.target_container.appendChild(post_page_ele);
        } else if (rqst.httpRequest.status === 204) {
            // TODO Handle by deactivating Read More button
            // alert('There are no more posts!');
        } else {
            // TODO handle this properly - not sure how right now
            alert('There was a problem.');
        }
    }

}

/* Custom error for handling when an attribute in the DOM does not exist.

http://stackoverflow.com/questions/1382107/whats-a-good-way-to-extend-error-in-javascript
https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Error
*/
function AttributeDNEError(attribute) {
    this.name = "AttributeDNEError";
    this.message = (attribute + "does not exist") || "Attribute does not exist.";
    this.stack = (new Error()).stack;
}

AttributeDNEError.prototype = Object.create(Error.prototype);
AttributeDNEError.prototype.constructor = AttributeDNEError;

function getAttribute(ele, attribute) {
    if (ele.hasAttribute(attribute)) {
        return ele.getAttribute(attribute)
    } else {
        throw AttributeDNEError(attribute);
    }
}

function checkAndSetAttribute(ele, attribute, value) {
    if (ele.hasAttribute(attribute)) {
        ele.setAttribute(value);
    } else {
        throw AttributeDNEError(attribute);
    }
}

function checkAndRemoveAttribute(ele, attribute) {
    if (ele.hasAttribute(attribute)) {
        ele.removeAttribute(attribute);
    } else {
        throw AttributeDNEError(attribute);
    }
} 

