var currentPage = 0;
// TODO change this to pull the page_request_var from the DOM
var page_request_var = "page";
var read_more_button = document.getElementById("read-more-button");

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
            } else {
                alert('There was a problem');
            }
        }
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