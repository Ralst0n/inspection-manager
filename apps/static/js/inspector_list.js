document.addEventListener("DOMContentLoaded", () => {
    
    let inspector_form = false;

    document.querySelector("#inspector-search-button").onclick = () => {
        let certs = selected_certs();

        // Don't run if there are no filters applied
        if (certs.length === 0 && document.querySelector("select[name='classification_search']").value === "none"){
            document.querySelector("#blank-form").innerHTML = "Enter criteria to use search";
            return false;
        }
        document.querySelector("#blank-form").innerHTML = "";
        let formData = new FormData();
        formData.append("classification", document.querySelector("select[name='classification_search']").value);
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
                if (inspector.classification){
                    p.innerHTML = inspector.classification;
                }
                else {
                    p.innerHTML = "Unknown"
                }
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
        {"name":"office", "options": ['None', 'King of Prussia', 'Pittsburgh'] },
        {"name":"classification", "options":['TA-1', 'TA-2', 'TCI-1', 'TCI-2', 'TCI-3', 'TCIS-1', 'TCIS-2', 'None']},
        // 15 miles is what PennDot considers standard commute
        {"name":"radius","type":"number", "value": 15 },
        {"name":"address", "value":"Not Provided"},
        "city",
        {"name":"state", "options": ['Pennsylvania', 'New Jersey', 'Delaware', 'Maryland', 'Ohio', 'New York'] },
        "zip",
        "email",
        {"name":"phone number", "type":"tel"}
    ]
   

    fields.forEach( field => {
        // Create a p that holds a label and a form field
        const sect = document.createElement("p");
        let label = document.createElement("label");
        let formField;

        // set name
        let name;
        field.name ? name = field.name : name = field;
        
        // fill in attributes of label and input
        label.htmlFor = name;
        label.innerHTML = `${name}:`;
        
        // make an exception for select boxes
        if (field.options) {
            formField = document.createElement("select");
            field.options.forEach( option=>{
                // for each option create an option element
                let o = document.createElement("option");
                // make text of option element the option string
                o.textContent = option
                o.value = option
                // append the option to the select element
                formField.append(o);
            });;
        }
        else {
            
            formField = document.createElement("input");

            let value;
            field.value ? value = field.value : value = "";

            // set field type
            let type;
            field.type ? type = field.type : type = "text"; 

            formField.type = type;
            formField.value = value;  
        }
        // Add label and form field to form
        formField.name = name;
        sect.append(label);
        sect.append(formField);
        document.querySelector("#inspector-form").append(sect);
    })
    const button = document.createElement("button");
    button.type = "submit";
    button.innerHTML = "Submit";
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
        // We don't need to check phone number this way so fields.length - 1 is the easy solution for now
        for(i=0; i < fields.length -1; i++){
            let name;
            fields[i].name ? name = fields[i].name : name = fields[i];
            // Don't fire if an input field is left blank but skip select fields
            if (document.querySelector(`[name="${name}"]`).type != "select-one" ) {
                if (document.querySelector(`input[name="${name}"]`).value == '') {
                    document.querySelector("#modal-message").innerHTML = `${name} field can not be blank`;
                    document.querySelector(".modal-body").scrollTop = 0;
                    abort = true;
                    break;
                }
                formData.append(name, document.querySelector(`[name="${name}"]`).value);
                console.log(name);
            }
            else {
                // set the select formdata value equal to the value of the selected index
                let select = document.querySelector(`[name="${name}"]`);
                console.log(select.options[select.selectedIndex].value);
                v = select.options[select.selectedIndex].value;
                console.log(`${name} is a select field with value ${v}`)
                formData.append(name, select.options[select.selectedIndex].value);
            }
        };

        // Check that Phone number is either 10 digits or blank
        let phone = document.querySelector(`[name="phone number"]`).value;
        if (phone.length != 10 && phone.length != 0){
            document.querySelector("#modal-message").innerHTML = `phone number field must be blank or 10 digits`;
            document.querySelector(".modal-body").scrollTop = 0;
            abort = true;
        }
        else {
            formData.append("phone number", document.querySelector(`[name="phone number"]`).value);
            console.log("phone number");
        }

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
            let href = `/inspectors/${response.id}`;
            document.querySelector("#modal-message").innerHTML = `<a href=${href}> ${response.name}</a> added to inspectors`;
            document.querySelector("[name='first name']").focus();
        }
        request.send(formData);
        return false;
    }
}


function clear_fields(array=[]) {
    array.forEach( field =>{
        let name;
        field.name ? name = field.name : name = field;
        // for all non-select fields set value to blank
        if (document.querySelector(`[name="${name}"]`).type != "select-one" ) {
            if (name == "radius") {
                document.querySelector(`[name="${name}"]`).value = 15;
            }
            else if (name == "address") {
                document.querySelector(`[name="${name}"]`).value = "Not Provided";
            }
            else {
                document.querySelector(`[name="${name}"]`).value = '';
            }
        }
        // for select fields change to default value
        else {
            document.querySelector(`[name="${name}"]`).selectedIndex = 0
        }
    })
}


function selected_certs() {
    let checked = [];
    certs = document.querySelectorAll("input[type='checkbox']");
    certs.forEach(box=> box.checked ? checked.push(box.value) : "");
    return checked;
}
