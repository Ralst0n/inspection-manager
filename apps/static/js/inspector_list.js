document.addEventListener("DOMContentLoaded", () => {
    
    let inspector_form = false;

    document.querySelector("#inspector-search-button").onclick = () => {
        let certs = selected_certs();

        // Don't run if there are no filters applied
        if (certs.length === 0 && document.querySelector("select[name='classification']").value === "all"){
            return false;
        }
        let formData = new FormData();
        formData.append("classification", document.querySelector("select[name='classification']").value);
        formData.append("certs", certs);
        
        
        // make ajax request to inspector list route
        request = new XMLHttpRequest();
        request.open("POST", "/inspectors/find");
        request.setRequestHeader("X-CSRFToken", document.cookie.substr(10))
        request.send(formData);
        // When the request returns, populate the inspectors fields with inspector cards
        request.onload = () => {
            // loop over each data item creating a card for it
            document.querySelector("#inspectors").innerHTML = '';
            data = JSON.parse(request.responseText);

            // Create results text to enumerate findings
            const results = document.createElement("p")
            results.id = "search-message"
            
            if (data.inspectors.length === 0) {
                results.innerHTML = "0 results found"
            }
            else if (data.inspectors.length === 1) {
                results.innerHTML = `1 result found`;
            }
            else {
                results.innerHTML = `${data.inspectors.length} results found`;
            }
            document.querySelector("#inspectors").append(results)
            // alphabetise the data
            let inspectors = data.inspectors.sort((a,b) => {
                    first_name = a.name.toLowerCase();
                    second_name = b.name.toLowerCase();
                    if (first_name > second_name) {
                        return 1
                    }
                    if (first_name < second_name) {
                        return -1
                    }
                    return 0
                })
            // Add each inspector item to document
            inspectors.forEach( inspector => {
                // Create inspector div
                const div = document.createElement("div");
                div.classList.add("inspector-card")
                // Create & append header and link for div
                const header = document.createElement("h4");
                const link = document.createElement("a");
                link.href = inspector.url;
                link.target = "_blank";
                link.innerHTML = inspector.name;
                header.append(link);
                div.append(header);
                // Create classification paragraph
                const p = document.createElement("p");
                p.innerHTML = inspector.classification;
                div.append(p);
                div.append(document.createElement("hr"));
                const p2 = document.createElement("p");
                p2.innerHTML = inspector.location;
                p2.classList.add("location");
                div.append(p2);
                document.querySelector("#inspectors").append(div);
            })
        }

        return false;
    }
    document.querySelector("#add-inspector-button").onclick = () => {
      // create form modal if it doesn't exist already
      if( !inspector_form){
        create_inspector_form();
        inspector_form = true;
      }
      document.querySelector(".modal").style.display = "block";
      document.querySelector("body").style.scroll = "none";

      return false;
    }; 
    
});

function create_inspector_form(){
    // define values for form, default type is text
    const fields = [
        "first name",
        "last name",
        "office",
        {"name":"classification", "placeholder":"TCI-2"},
        {"name":"radius","type":"number" },
        {"name":"address", "placeholder":"321 Atwood St."},
        "city",
        "state",
        "zip",
        "email",
        {"name":"phone number", "type":"tel"}
    ]
   

    fields.forEach( field => {
        // Create a p that holds a label and an input
        const sect = document.createElement("p");
        let label = document.createElement("label");
        let input = document.createElement("input");

        let placeholder;
        field.placeholder ? placeholder = field.placeholder : placeholder = "";
        // set field type
        let type;
        field.type ? type = field.type : type = "text"; 
        // set name
        let name;
        field.name ? name = field.name : name = field;

        // fill in attributes of label and input
        label.htmlFor = name;
        label.innerHTML = `${name}:`;

        input.type = type;
        input.name = name;
        input.placeholder = placeholder;

        sect.append(label);
        sect.append(input);
        document.querySelector("#inspector-form").append(sect);
    })
    const button = document.createElement("button");
    button.type = "submit";
    button.innerHTML = "submit";
    button.classList.add("submit", "button");
    document.querySelector("#inspector-form").append(button);


    // create close button
    const close = document.createElement("button");
    close.innerHTML = "Cancel";
    close.classList.add("cancel", "button");
    close.onclick = () => {
        // clear all values in form and hide the modal
        clear_fields(fields)
        document.querySelector("#modal-message").innerHTML = "";
        document.querySelector(".modal-body").scrollTop = 0;
        document.querySelector(".modal").style.display = "none";
        
        return false;
    }
    document.querySelector("#inspector-form").append(close);
    button.onclick = () => {
         // also add it to form data
        let abort = false;
        let formData = new FormData();
        for(i=0; i < fields.length; i++){
            let name;
            fields[i].name ? name = fields[i].name : name = fields[i];
            // don't fire if a field is left blank
            if (document.querySelector(`input[name="${name}"]`).value == '') {
                document.querySelector("#modal-message").innerHTML = `${name} field can not be blank`;
                document.querySelector(".modal-body").scrollTop = 0;
                abort = true;
                break;
            }
            formData.append(name, document.querySelector(`input[name="${name}"]`).value);
            console.log(name);
        };
        
        if (abort) {
            return false;
        }
        request = new XMLHttpRequest();
        request.open("POST", "/inspectors/create_person");
        request.setRequestHeader("X-CSRFToken", document.cookie.substr(10))
        request.onload = () => {
            let response = JSON.parse(request.responseText);
            clear_fields(fields);
            document.querySelector(".modal-body").scrollTop = 0;
            document.querySelector("#modal-message").style.color = "green";
            document.querySelector("#modal-message").innerHTML = response['message'];
        }
        request.send(formData);
        return false;
    }
}


function clear_fields(array=[]) {
    array.forEach( field =>{
        let name;
        field.name ? name = field.name : name = field;
        document.querySelector(`input[name="${name}"]`).value = '';
    })
}


function selected_certs() {
    let checked = [];
    certs = document.querySelectorAll("input[type='checkbox']");
    certs.forEach(box=> box.checked ? checked.push(box.value) : "");
    return checked;
}
