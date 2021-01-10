//content to be loaded after page finished loading
document.addEventListener('DOMContentLoaded', function() {

    //by default, load all posts and begin with page 1
    load_allPosts(1);

    //advise user of remaining characters available
    document.querySelector('#newPostContent').onkeyup = function() {
        var maxLength = 280;
        var textarea = document.querySelector('#newPostContent');
        document.querySelector('#charactersRemaining').innerHTML = maxLength - textarea.value.length + " characters remaining";
    }

    //run submit post function on submission of form
    document.querySelector('form').onsubmit = function () {
        submitPost();

        //prevent default submission of form
        return false;
    };
});


//load all posts function
function load_allPosts(pageNumber) {
    let postsDisplayArea = document.querySelector('#displayPosts');

    //set head of post box container
    postsDisplayArea.innerHTML = '<h5>All Posts</h5>';

    //fetch posts
    fetch(`posts/allposts/${pageNumber}`)
        .then(response => response.json())
        .then(posts => {

        // Print posts received
        console.log(posts);

        //select larger container to display posts
        const postContainer = document.querySelector('#displayPosts');
        const paginationButtons = document.querySelector('#pageButtons');
        paginationButtons.innerHTML = '';
        
        //previous button for pagnation 
        if (posts["0"]["pageNumber"] > 1) {
            const previousButton = document.createElement('li');
            previousButton.className = "page-item page-link";
            previousButton.innerHTML = `Previous`;
            paginationButtons.appendChild(previousButton);
    
            //attach event listener to link to post author profile
            previousButton.addEventListener('click', function() {
                load_allPosts(posts["0"]["pageNumber"] - 1);
            });
        }

        //next button pagnation
        if (posts["0"]["pageNumber"] < posts["3"]["totalPages"]) {
            const nextButton = document.createElement('li');
            nextButton.className = "page-item page-link";
            nextButton.innerHTML = `Next`;
            paginationButtons.appendChild(nextButton);
    
            //attach event listener to link to post author profile
            nextButton.addEventListener('click', function() {
                load_allPosts(posts["0"]["pageNumber"] + 1);
            });
        }

        //iterate over all posts received from fetch request, -5 because of characters to be used above
        for (i = 5; i < posts.length; i++) {

            //create a sub-container to display posts in
            const newPostContainer = document.createElement('div');
            newPostContainer.className = "container border rounded my-1 py-2 font-weight-normal";
            newPostContainer.id = posts[i]["id"];
            newPostContainer.innerHTML = ``;

            //set post text, used later to change after edit function
            const postText = document.createElement('div');
            postText.innerHTML = `<p>${posts[i]["content"]}</p>`;

            //like counter row
            const likeCount = document.createElement('small');
            likeCount.className = "font-weight-light";

            //first part of subtext
            const newPostSubtext = document.createElement('small');
            newPostSubtext.className = "font-weight-light text-secondary";
            newPostSubtext.innerHTML = `Posted by `;
            
            //author
            const postAuthor = document.createElement('span');
            postAuthor.className = "text-primary";
            postAuthor.id = posts[i]["posterUsername"];
            postAuthor.innerHTML = `${posts[i]["posterUsername"]}`;

            //second part of subtext
            const newPostSubtext2 = document.createElement('span');
            newPostSubtext2.className = "font-weight-light text-secondary";
            newPostSubtext2.innerHTML = ` on ${posts[i]["timestamp"]}.` + "<br/>";

            //merging all above to display one post
            newPostContainer.appendChild(postText);
            newPostContainer.appendChild(likeCount);
            postAuthor.appendChild(newPostSubtext2);
            newPostSubtext.appendChild(postAuthor);
            newPostContainer.appendChild(newPostSubtext);
            postContainer.appendChild(newPostContainer);

            //attach event listener to link to post's author profile
            postAuthor.addEventListener('click', function() {
                userProfile(postAuthor.id, 1);
            });

            //show edit button if user is author of the post
            if (posts["4"]["currentUsername"] == posts[i]["posterUsername"]) {
                const editButton = document.createElement('button');
                editButton.className = "btn btn-outline-info btn-sm my-1";
                editButton.innerHTML = "Edit post";
                newPostContainer.appendChild(editButton);
                const placeholderText = `${posts[i]["content"]}`;
                
                //create save button to save edits, initialise style to hidden
                const saveButton = document.createElement('button');
                saveButton.className = "btn btn-success btn-sm my-1";
                saveButton.innerHTML = "Save edits";
                newPostContainer.appendChild(saveButton);
                saveButton.style.display = 'none';

                //create textarea to edit post
                const textboxEdit = document.createElement('textarea');
                textboxEdit.className = "form-control";

                //if edit button is clicked showtext box, hide edit button and show save button
                editButton.addEventListener('click', function() {
                    editButton.id = 'clickedEdit';
                    postText.innerHTML = '';
                    textboxEdit.innerHTML = placeholderText;
                    postText.appendChild(textboxEdit);
                    editButton.style.display = 'none';
                    saveButton.style.display = 'block';
                });

                //if save button is clicked save edit, show edit button, hide save button
                saveButton.addEventListener('click', function() {
                    editPost(newPostContainer.id, textboxEdit.value);
                    editButton.style.display = 'block';
                    saveButton.style.display = 'none';
                    postText.innerHTML = `${textboxEdit.value}`;
                });

            };

            //fetch number of likes on post
            const postIDLikeButton = posts[i]["id"]
            fetch(`like/${posts[i]["id"]}`)
                .then(response => response.json())
                .then(likes => {

                    //print what is returned
                    console.log(likes);

                    //display number of likes and like button
                    likeCount.innerHTML = `	&#10084; ${likes["likeCount"]}` + "<br/>";
                    const likeButton = document.createElement('button');

                    //check if user is logged in and has liked the post
                    let likeStatus = true;
                    if (likes["userlogedIn"] == true) {

                        //if user has not liked the post display like in like button
                        if (likes["userLikeStatus"] == false) {
                            likeButton.className = "btn btn-outline-success btn-sm m-1";
                            likeButton.innerHTML = "Like";
                            likeStatus = true;
                        }

                        //if user has liked the post display unlike button
                        else {
                            likeButton.className = "btn btn-outline-secondary btn-sm m-1";
                            likeButton.innerHTML = "Unlike";
                            likeStatus = false;
                        }

                        //add like button to post
                        newPostContainer.appendChild(likeButton);
                    }

                    //if like button is clicked, save like and update like count and switch to unlike button
                    likeButton.addEventListener('click', function() {
                        likePost(newPostContainer.id, likeStatus);
                        if (likeStatus == true) {
                            likeButton.className = "btn btn-outline-secondary btn-sm m-1";
                            likeButton.innerHTML = "Unlike";
                            likeStatus = false;
                        }

                        //if unlike is clicked switch to unlike
                        else {
                            likeButton.className = "btn btn-outline-success btn-sm m-1";
                            likeButton.innerHTML = "Like";
                            likeStatus = true;
                        }

                        //fetch update like count after delay for database
                        setTimeout(function() {
                            fetch(`like/${postIDLikeButton}`)
                                .then(response => response.json())
                                .then(likes => {
                                    console.log(likes);
                                    likeCount.innerHTML = `	&#10084; ${likes["likeCount"]}` + "<br/>";
                            });
                        }, 50);
                    })
                });
        }
      })
      .catch(error => {
            console.log('Error: ', error);
      });
}


//load all posts function
function load_following() {
    // document.querySelector('#newPostBox').style.display = 'block';
    let postsDisplayArea = document.querySelector('#displayPosts');

    postsDisplayArea.innerHTML = '<h5>Posts from people you are following</h5>';
    fetch('posts/following')
        .then(response => response.json())
        .then(posts => {
        // Print posts received
        console.log(posts);

        //select larger container to display posts
        const postContainer = document.querySelector('#displayPosts');

        //iterate over all posts received from fetch request, -5 because of characters to be used above
        for (i = 5; i < posts.length; i++) {

            //create a sub-container to display posts in
            const newPostContainer = document.createElement('div');
            newPostContainer.className = "container border rounded my-1 py-2 font-weight-normal";
            newPostContainer.id = posts[i]["id"];
            newPostContainer.innerHTML = ``;

            //set post text, used later to change after edit function
            const postText = document.createElement('div');
            postText.innerHTML = `<p>${posts[i]["content"]}</p>`;

            //like counter row
            const likeCount = document.createElement('small');
            likeCount.className = "font-weight-light";

            //first part of subtext
            const newPostSubtext = document.createElement('small');
            newPostSubtext.className = "font-weight-light text-secondary";
            newPostSubtext.innerHTML = `Posted by `;
            
            //author
            const postAuthor = document.createElement('span');
            postAuthor.className = "text-primary";
            postAuthor.id = posts[i]["posterUsername"];
            postAuthor.innerHTML = `${posts[i]["posterUsername"]}`;

            //second part of subtext
            const newPostSubtext2 = document.createElement('span');
            newPostSubtext2.className = "font-weight-light text-secondary";
            newPostSubtext2.innerHTML = ` on ${posts[i]["timestamp"]}.` + "<br/>";

            //merging all above to display one post
            newPostContainer.appendChild(postText);
            newPostContainer.appendChild(likeCount);
            postAuthor.appendChild(newPostSubtext2);
            newPostSubtext.appendChild(postAuthor);
            newPostContainer.appendChild(newPostSubtext);
            postContainer.appendChild(newPostContainer);

            //attach event listener to link to post's author profile
            postAuthor.addEventListener('click', function() {
                userProfile(postAuthor.id, 1);
            });

            //show edit button if user is author of the post
            if (posts["4"]["currentUsername"] == posts[i]["posterUsername"]) {
                const editButton = document.createElement('button');
                editButton.className = "btn btn-outline-info btn-sm my-1";
                editButton.innerHTML = "Edit post";
                newPostContainer.appendChild(editButton);
                const placeholderText = `${posts[i]["content"]}`;
                
                //create save button to save edits, initialise style to hidden
                const saveButton = document.createElement('button');
                saveButton.className = "btn btn-success btn-sm my-1";
                saveButton.innerHTML = "Save edits";
                newPostContainer.appendChild(saveButton);
                saveButton.style.display = 'none';

                //create textarea to edit post
                const textboxEdit = document.createElement('textarea');
                textboxEdit.className = "form-control";

                //if edit button is clicked showtext box, hide edit button and show save button
                editButton.addEventListener('click', function() {
                    editButton.id = 'clickedEdit';
                    postText.innerHTML = '';
                    textboxEdit.innerHTML = placeholderText;
                    postText.appendChild(textboxEdit);
                    editButton.style.display = 'none';
                    saveButton.style.display = 'block';
                });

                //if save button is clicked save edit, show edit button, hide save button
                saveButton.addEventListener('click', function() {
                    editPost(newPostContainer.id, textboxEdit.value);
                    editButton.style.display = 'block';
                    saveButton.style.display = 'none';
                    postText.innerHTML = `${textboxEdit.value}`;
                });

            };

            //fetch number of likes on post
            const postIDLikeButton = posts[i]["id"]
            fetch(`like/${posts[i]["id"]}`)
                .then(response => response.json())
                .then(likes => {

                    //print what is returned
                    console.log(likes);

                    //display number of likes and like button
                    likeCount.innerHTML = `	&#10084; ${likes["likeCount"]}` + "<br/>";
                    const likeButton = document.createElement('button');

                    //check if user is logged in and has liked the post
                    let likeStatus = true;
                    if (likes["userlogedIn"] == true) {

                        //if user has not liked the post display like in like button
                        if (likes["userLikeStatus"] == false) {
                            likeButton.className = "btn btn-outline-success btn-sm m-1";
                            likeButton.innerHTML = "Like";
                            likeStatus = true;
                        }

                        //if user has liked the post display unlike button
                        else {
                            likeButton.className = "btn btn-outline-secondary btn-sm m-1";
                            likeButton.innerHTML = "Unlike";
                            likeStatus = false;
                        }
                    }

                    //add like button to post
                    newPostContainer.appendChild(likeButton);

                    //if like button is clicked, save like and update like count and switch to unlike button
                    likeButton.addEventListener('click', function() {
                        likePost(newPostContainer.id, likeStatus);
                        if (likeStatus == true) {
                            likeButton.className = "btn btn-outline-secondary btn-sm m-1";
                            likeButton.innerHTML = "Unlike";
                            likeStatus = false;
                        }

                        //if unlike is clicked switch to unlike
                        else {
                            likeButton.className = "btn btn-outline-success btn-sm m-1";
                            likeButton.innerHTML = "Like";
                            likeStatus = true;
                        }

                        //fetch update like count after delay for database
                        setTimeout(function() {
                            fetch(`like/${postIDLikeButton}`)
                                .then(response => response.json())
                                .then(likes => {
                                    console.log(likes);
                                    likeCount.innerHTML = `	&#10084; ${likes["likeCount"]}` + "<br/>";
                            });
                        }, 50);
                    })
                });
        }
      })
      .catch(error => {
            console.log('Error: ', error);
      });
}


//function to change following status
function followUser(username, followingStatus) {
    let csrftoken = getCookie('csrftoken');
    fetch(`followers/${username}`, {
        method: 'PUT',
        headers: {
            "X-CSRFToken": csrftoken
        },
        body: JSON.stringify({
            followingStatusUpdate: followingStatus
        })
    });
}


//function to change following status
function likePost(postID, likeStatus) {
    let csrftoken = getCookie('csrftoken');
    fetch(`like/${postID}`, {
        method: 'PUT',
        headers: {
            "X-CSRFToken": csrftoken
        },
        body: JSON.stringify({
            likeStatusUpdate: likeStatus
        })
    });
}


//display user profile
function userProfile(username, pageNumber) {

    let postsDisplayArea = document.querySelector('#displayPosts');

    //display user information at the top
    fetch(`followers/${username}`)
        .then(response => response.json())
        .then(followers => {
            console.log(followers);
            postsDisplayArea.innerHTML = `<h5>${username}</h5><p>${followers["followers"]} followers, ${followers["following"]} following</p>`;

            //add follow/unfollow button if viewing profile is different from current user
            if (followers["sameUser"] == false && followers["followingStatus"] != "sameUser") {
                const followButton = document.createElement('button');

                if (followers["followingStatus"] == false) {
                    followButton.className = "btn btn-success btn-sm my-1";
                    followButton.innerHTML = "Follow";
                    followingStatus = true;
                }
                
                else {
                    followButton.className = "btn btn-secondary btn-sm my-1";
                    followButton.innerHTML = "Unfollow";
                    followingStatus = false;
                }

                displayPosts.appendChild(followButton);

                //attach event handler to button to process follow/unfollow request and reload button/followers count
                followButton.addEventListener('click', function() {
                    followUser(username, followingStatus);
                    //set delay to ensure time for database
                    setTimeout(function() {
                        userProfile(username, pageNumber);
                      }, 50);
                });
            };

            //get data to display posts
            fetch(`user/${username}/${pageNumber}`)
            .then(response => response.json())
            .then(posts => {
            // Print posts received
            console.log(posts);

            //select larger container to display posts
            const postContainer = document.querySelector('#displayPosts');
            const paginationButtons = document.querySelector('#pageButtons');
            paginationButtons.innerHTML = '';
            
            //previous button for pagnation 
            if (posts["0"]["pageNumber"] > 1) {
                const previousButton = document.createElement('li');
                previousButton.className = "page-item page-link";
                previousButton.innerHTML = `Previous`;
                paginationButtons.appendChild(previousButton);
        
                //attach event listener to link to previous page
                previousButton.addEventListener('click', function() {
                    userProfile(username, posts["0"]["pageNumber"] - 1);
                });
            }

            //next button pagnation
            if (posts["0"]["pageNumber"] < posts["3"]["totalPages"]) {
                const nextButton = document.createElement('li');
                nextButton.className = "page-item page-link";
                nextButton.innerHTML = `Next`;
                paginationButtons.appendChild(nextButton);
        
                //attach event listener to link next page
                nextButton.addEventListener('click', function() {
                    userProfile(username, posts["0"]["pageNumber"] + 1);
                });
            }

            //iterate over all posts received from fetch request, -5 because of characters to be used above
        for (i = 5; i < posts.length; i++) {

            //create a sub-container to display posts in
            const newPostContainer = document.createElement('div');
            newPostContainer.className = "container border rounded my-1 py-2 font-weight-normal";
            newPostContainer.id = posts[i]["id"];
            newPostContainer.innerHTML = ``;

            //set post text, used later to change after edit function
            const postText = document.createElement('div');
            postText.innerHTML = `<p>${posts[i]["content"]}</p>`;

            //like counter row
            const likeCount = document.createElement('small');
            likeCount.className = "font-weight-light";

            //first part of subtext
            const newPostSubtext = document.createElement('small');
            newPostSubtext.className = "font-weight-light text-secondary";
            newPostSubtext.innerHTML = `Posted by `;
            
            //author
            const postAuthor = document.createElement('span');
            postAuthor.className = "text-primary";
            postAuthor.id = posts[i]["posterUsername"];
            postAuthor.innerHTML = `${posts[i]["posterUsername"]}`;

            //second part of subtext
            const newPostSubtext2 = document.createElement('span');
            newPostSubtext2.className = "font-weight-light text-secondary";
            newPostSubtext2.innerHTML = ` on ${posts[i]["timestamp"]}.` + "<br/>";

            //merging all above to display one post
            newPostContainer.appendChild(postText);
            newPostContainer.appendChild(likeCount);
            postAuthor.appendChild(newPostSubtext2);
            newPostSubtext.appendChild(postAuthor);
            newPostContainer.appendChild(newPostSubtext);
            postContainer.appendChild(newPostContainer);

            //attach event listener to link to post's author profile
            postAuthor.addEventListener('click', function() {
                userProfile(postAuthor.id, 1);
            });

            //show edit button if user is author of the post
            if (posts["4"]["currentUsername"] == posts[i]["posterUsername"]) {
                const editButton = document.createElement('button');
                editButton.className = "btn btn-outline-info btn-sm my-1";
                editButton.innerHTML = "Edit post";
                newPostContainer.appendChild(editButton);
                const placeholderText = `${posts[i]["content"]}`;
                
                //create save button to save edits, initialise style to hidden
                const saveButton = document.createElement('button');
                saveButton.className = "btn btn-success btn-sm my-1";
                saveButton.innerHTML = "Save edits";
                newPostContainer.appendChild(saveButton);
                saveButton.style.display = 'none';

                //create textarea to edit post
                const textboxEdit = document.createElement('textarea');
                textboxEdit.className = "form-control";

                //if edit button is clicked showtext box, hide edit button and show save button
                editButton.addEventListener('click', function() {
                    editButton.id = 'clickedEdit';
                    postText.innerHTML = '';
                    textboxEdit.innerHTML = placeholderText;
                    postText.appendChild(textboxEdit);
                    editButton.style.display = 'none';
                    saveButton.style.display = 'block';
                });

                //if save button is clicked save edit, show edit button, hide save button
                saveButton.addEventListener('click', function() {
                    editPost(newPostContainer.id, textboxEdit.value);
                    editButton.style.display = 'block';
                    saveButton.style.display = 'none';
                    postText.innerHTML = `${textboxEdit.value}`;
                });

            };

            //fetch number of likes on post
            const postIDLikeButton = posts[i]["id"]
            fetch(`like/${posts[i]["id"]}`)
                .then(response => response.json())
                .then(likes => {

                    //print what is returned
                    console.log(likes);

                    //display number of likes and like button
                    likeCount.innerHTML = `	&#10084; ${likes["likeCount"]}` + "<br/>";
                    const likeButton = document.createElement('button');

                    //check if user is logged in and has liked the post
                    let likeStatus = true;
                    if (likes["userlogedIn"] == true) {

                        //if user has not liked the post display like in like button
                        if (likes["userLikeStatus"] == false) {
                            likeButton.className = "btn btn-outline-success btn-sm m-1";
                            likeButton.innerHTML = "Like";
                            likeStatus = true;
                        }

                        //if user has liked the post display unlike button
                        else {
                            likeButton.className = "btn btn-outline-secondary btn-sm m-1";
                            likeButton.innerHTML = "Unlike";
                            likeStatus = false;
                        }

                        //add like button to post
                        newPostContainer.appendChild(likeButton);
                    }

                    

                    //if like button is clicked, save like and update like count and switch to unlike button
                    likeButton.addEventListener('click', function() {
                        likePost(newPostContainer.id, likeStatus);
                        if (likeStatus == true) {
                            likeButton.className = "btn btn-outline-secondary btn-sm m-1";
                            likeButton.innerHTML = "Unlike";
                            likeStatus = false;
                        }

                        //if unlike is clicked switch to unlike
                        else {
                            likeButton.className = "btn btn-outline-success btn-sm m-1";
                            likeButton.innerHTML = "Like";
                            likeStatus = true;
                        }

                        //fetch update like count after delay for database
                        setTimeout(function() {
                            fetch(`like/${postIDLikeButton}`)
                                .then(response => response.json())
                                .then(likes => {
                                    console.log(likes);
                                    likeCount.innerHTML = `	&#10084; ${likes["likeCount"]}` + "<br/>";
                            });
                        }, 50);
                    })
                });
            }
        })
        .catch(error => {
                console.log('Error: ', error);
        });
        })
        .catch(error => {
            console.log('Error: ', error);
            postsDisplayArea.innerHTML = `<h5>User not found</h5>`;
        });
}


function editPost(postID, newText) {
    let csrftoken = getCookie('csrftoken');
    fetch(`edit/${postID}`, {
        method: 'POST',
        //security for CSRF token
        headers: {
            "X-CSRFToken": csrftoken
        },
        body: JSON.stringify({
            content: newText
        })
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log(result);
    })
    .catch(error => {
          console.log('Error: ', error);
    });
}


//submit post function
function submitPost() {

    //get new text content and CSRF token
    let newPostContent = document.querySelector('#newPostContent').value;
    let csrftoken = getCookie('csrftoken');

    //submit post
    fetch('posts', {
        method: 'POST',
        //security for CSRF token
        headers: {
            "X-CSRFToken": csrftoken
        },
        body: JSON.stringify({
            content: newPostContent
        })
      })
      .then(response => response.json())
      .then(result => {
            // Print result
            console.log(result);

            //clear textarea once post successfully sent
            document.querySelector('#newPostContent').value = '';
            
            //reload all posts after submission
            load_allPosts(1);
      })
      .catch(error => {
            console.log('Error: ', error);
      });
}


//get CSRF token, taken from Django docs - https://docs.djangoproject.com/en/1.11/ref/csrf/#ajax
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}