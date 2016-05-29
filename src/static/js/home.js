// I have moved this current page variable to the DOM which is provided
// by the server
// var currentPage = 0;
// TODO change this to pull the page_request_var from the DOM
var page_request_var = "page";
var read_more_button = document.getElementById("read-more-button");

window.onload = function () {
    prepareEventHandlers();
}

function prepareEventHandlers() {
    // In order to pass an argument to a function in an event listener,
    // you have to use an anonymous function. This is because if you include 
    // the function with parenthesis, the function will be called at that time
    // onload->click->makeRequest->instantiates PostListHttpRequest
    read_more_button.addEventListener("click", function(){makeRequest(request_str)}, false);
}

/** This object sets up a Post List HTTP Request.
I decided to go with a constructor function because I want to be able to
re-use this object with different parameters. 
@constructor **/
function PostListHttpRequest() {

    this.last_post = document.getElementById("last-post");

    this.requested_page = last_post.getAttribute("data-page-number") + 1;
    this.httpRequest = new XMLHttpRequest();
    this.request_url = "grid/?" + page_request_var + "=" + requested_page;    
}

/** makeRequest will use the information set-up by PostListHttpRequest to
actually make the request. It then calls addNewPosts to deal with adding the 
response to the DOM. **/
function makeRequest() {
    // TODO Look into integrating this into the PostListHttpRequest object.
    var postRequest = new PostListHttpRequest();

    // Not sure why MDN suggesting this statement. If I don't understand why
    // something is in my code, I should p>.5 rm it.
    if (!PostRequest.httpRequest) {
        alert('Http Request not made!');
        return false;
    }
    //
    postRequest.httpRequest.onreadystatechange = function(){addNewPosts(postRequest)};
    postRequest.httpRequest.open('GET', PostRequest.request_url);
    postRequest.send();
}

function addNewPosts(rqst) {
    if (rqst.httpRequest.readyState === XMLHttpRequest.DONE) {
        if (rqst.status === 200) {
            // Since the last post is contained in a container
            // from the below DOM manipulation we need to target the div containing
            // the page of posts div (one level above class="post-page")
            parent_container = rqst.last_post.parentElement.parentElement;
            // i want to put each set of posts in a containing div 
            // so that I can just set the innerHTML of that element and append
            // it to the post container
            post_page_ele = document.createElement("div");
            post_page_ele.setAttribute('class', 'post-page');
            post_page_ele.innerHTML = rqst.httpRequest.responseText;
            // parent_container is the div containing the post-page div
            // so I can just append another post-page div to that
            parent_container.appendChild(post_page_ele);
        } else {
            // TODO handle this properly - not sure how right now
            alert('There was a problem.')
        }
    }

}

(function() {
    var httpRequest;
    var requested_page = currentPage + 1;
    request_str = "grid/?" + page_request_var + "=" + requested_page;
    read_more_button.addEventListener("click", function(){makeRequest(request_str)}, false);
    // read_more_button.onclick = function() { makeRequest(request_str); };

    function makeRequest(url) {
        httpRequest = new XMLHttpRequest();

        if (!httpRequest) {
            alert('Ripped this straignt from Mozilla docs - sorry :(');
            return false;
        }
        httpRequest.onreadystatechange = addNewPosts;
        httpRequest.open('GET', url);
        httpRequest.send();
    }

    function addNewPosts() {
        if (httpRequest.readyState === XMLHttpRequest.DONE) {
            if (httpRequest.status === 200) {
               response_container = document.getElementById("next-set");
               response_container.innerHTML = httpRequest.responseText;
               currentPage = requested_page;
            } else {
                alert('There was a problem');
            }
        }
    }
    function formPostEle(htmlFromServer) {
        var ele = document.createElement('div');
        ele.className = "post-list";
    }

    function alertContents() {
        if (httpRequest.readyState === XMLHttpRequest.DONE) {
            if (httpRequest.status === 200) {
                alert(httpRequest.responseText);
            } else {
                alert('There was a problem with the request.');
            }
        }
    }
})();

/* Custom error for handling when an attribute in the DOM does not exist.

http://stackoverflow.com/questions/1382107/whats-a-good-way-to-extend-error-in-javascript
https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Error
*/
function AttributeDNEError(attribute) {
    this.name = "AttributeDNEError";
    this.message = (attribute + "does not exist") || "Attribute does not exist.";
    this.stack = (new Errow()).stack;
}

AttributeDNEError.prototype = Object.create(Error.prototype);
AttributeDNEError.prototype.constructor = AttributeDNEError;

function checkAndSetAttribute(ele, attribute, value) {
    if (ele.hasAttribute(attribute)) {
        ele.setAttribute(value);
    } else {
        throw AttributeDNEError(attribute);
    }
}

function checkAndRemoveAttribute(ele, attribute) {
    if (ele.hasAttribute(attribute)) {
        ele.removeAttribute();
    } else {
        throw AttributeDNEError(attribute);
    }
} 