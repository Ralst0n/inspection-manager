document.addEventListener("DOMContentLoaded", () => {
    document.querySelector("#add-note").onclick = () => {
        let message = document.querySelector("#note-textarea");
        let id = document.querySelector("h1").dataset.id;

        // create a post request to the server that uses id and message to make a note
        formData = new FormData();
        formData.append("body", message.value);
        formData.append("id", id);
        request = new XMLHttpRequest();
        request.open("POST", "/inspectors/create_note")
        request.setRequestHeader("X-CSRFToken", document.cookie.substr(10));
        request.onload = () => {
            response = JSON.parse(request.responseText);
            if (response.error) {
                alert(response.error);
            }
            let comments = document.querySelector("#comments");
            // Create the new message div
            let messageDiv = document.createElement("div");

            // Add paragrahs to the new message div for creator, message and timestamp


            // p for user submitting the message 
            let commentor = document.createElement("p");
            commentor.innerHTML = response.commentor
            commentor.classList.add("commentor");
            messageDiv.append(commentor);

            // create and append p for comment body
            let commentBody = document.createElement("p");
            commentBody.innerHTML = response.comment;
            commentBody.classList.add("comment-body");
            messageDiv.append(commentBody);

            // create and append p for comment date
            let date = document.createElement("p");
            date.innerHTML = response.date;
            date.classList.add("date");
            messageDiv.append(date);

            // Have new message flash onto screen and inserted at top of comments
            // Give focus back to text area
            messageDiv.classList.add("comment", "flash");
            comments.insertBefore(messageDiv, comments.firstChild);
            message.value = '';
            message.focus();

        }
        if (message.value == '') {
            alert("empty message me no send");
        }
        request.send(formData);
    
    }
})