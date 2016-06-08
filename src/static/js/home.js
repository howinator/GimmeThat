// I have moved this current page variable to the DOM which is provided
// by the server
// var currentPage = 0;
// TODO change this to pull the page_request_var from the DOM

var page_request_var = (function() {
    return getAttribute(document.getElementById('post-list'), 'data-page-request-var');
})();
var last_post_page_name = "last_post_page";
var read_more_button = document.getElementById("read-more-button");

// we wanrt to add all the event handlers once the page has loaded
// TODO might consider doing that DOM built thing instead
window.onload = function () {
    prepareEventHandlers();
    makeRequest();

}

function prepareEventHandlers() {
    // In order to pass an argument to a function in an event listener,
    // you have to use an anonymous function. This is because if you include 
    // just the function with parenthesis, the function will be called
    // right when it is written
    // onload->click->makeRequest->instantiates PostListHttpRequest
    read_more_button.addEventListener("click", makeRequest, false);
}

/** This object sets up a Post List HTTP Request.
I decided to go with a constructor function because I want to be able to
re-use this object with different parameters. 
@constructor **/
function PostListHttpRequest() {

    if (document.getElementById(last_post_page_name)) {
        this.previous_post_page = document.getElementById(last_post_page_name);
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
    this.request_url = "grid/?" + page_request_var + "=" + this.requested_page;    
}

/** makeRequest will use the information set-up by PostListHttpRequest to
actually make the request. It then calls addNewPosts to deal with adding the 
response to the DOM. 

DOM of posts:
<section id="post-list">
  <div class="containter-fluid">
    post_grid:
      {MORE POSTS}
      <div class="row" id="last-post" data-page-number="{{NUMBER}}">
        {{POST}}

How the post appendage works:
1) Event is added to trigger on click of read-more button
2) js:makeRequest instantiates PostListHttpRequest which sets some things up and makes the AJAX request
        a. It gets the div class="row" of the last post
3) js:addNewPosts will add posts to the DOM by:
        a. creating an element
        b. populating this element's innerHTML
        c. appending this element to the DOM**/
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
            // Remember that post_page is set server side
            post_page_ele = document.createElement("div");
            post_page_ele.setAttribute('class', 'post-page');

            if (rqst.previous_post_page) {
                checkAndRemoveAttribute(rqst.previous_post_page, 'id');
            }

            post_page_ele.setAttribute('id', last_post_page_name);
            post_page_ele.setAttribute('data-page-number', rqst.requested_page);
            post_page_ele.innerHTML = rqst.httpRequest.responseText;
            // parent_container is the div containing the post-page div
            // so I can just append another post-page div to that
            rqst.target_container.appendChild(post_page_ele);
        } else if (rqst.httpRequest.status === 204) {
            alert('There are no more posts!');
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

// (function() {
//     var httpRequest;
//     var requested_page = currentPage + 1;
//     request_str = "grid/?" + page_request_var + "=" + requested_page;
//     read_more_button.addEventListener("click", function(){makeRequest(request_str)}, false);
//     // read_more_button.onclick = function() { makeRequest(request_str); };

//     function makeRequest(url) {
//         httpRequest = new XMLHttpRequest();

//         if (!httpRequest) {
//             alert('Ripped this straignt from Mozilla docs - sorry :(');
//             return false;
//         }
//         httpRequest.onreadystatechange = addNewPosts;
//         httpRequest.open('GET', url);
//         httpRequest.send();
//     }

//     function addNewPosts() {
//         if (httpRequest.readyState === XMLHttpRequest.DONE) {
//             if (httpRequest.status === 200) {
//                response_container = document.getElementById("next-set");
//                response_container.innerHTML = httpRequest.responseText;
//                currentPage = requested_page;
//             } else {
//                 alert('There was a problem');
//             }
//         }
//     }
//     function formPostEle(htmlFromServer) {
//         var ele = document.createElement('div');
//         ele.className = "post-list";
//     }

//     function alertContents() {
//         if (httpRequest.readyState === XMLHttpRequest.DONE) {
//             if (httpRequest.status === 200) {
//                 alert(httpRequest.responseText);
//             } else {
//                 alert('There was a problem with the request.');
//             }
//         }
//     }
// })();