document.addEventListener("DOMContentLoaded", () => {

    let invoice_form = false;

    document.querySelector("#invoice-button").onclick = () => {
        if (!invoice_form){
            request = new XMLHttpRequest();
            formData = new FormData();
            let project_id = document.querySelector("#project_number").dataset.id;
            formData.append("prudent_number", project_id);
            request.open("POST", "/projects/get_info");
            request.setRequestHeader("X-CSRFToken", document.cookie.substr(10));
            request.onload = () => {
                let response = JSON.parse(request.responseText);
                document.querySelector("input[name='Estimate number']").value = response['estimate_number']
                document.querySelector("input[name='Start date']").value = response['start_date'];
                // start and end dates must be after end date of previous invoice
                document.querySelector("input[name='Start date']").setAttribute("min", response['start_date']);
                document.querySelector("input[name='End date']").setAttribute("min", response['start_date']);
            }
            request.send(formData);
            create_invoice_form();
            invoice_form = true;
        }
        document.querySelector(".modal").style.display = "block";
        document.querySelector("body").style.scroll = "none";
    }
})

function create_invoice_form(){
    // placeholder date is always bosses birthday current year
    let year = new Date().getFullYear();

    // define values for form, default type is text
    const fields = [
        {"name" : "Estimate number", "readonly" : true },
        {"name": "Start date", "type": "date", "placeholder":`09-09-${year}`},
        {"name": "End date", "type": "date", "placeholder":`${year}-10-13`},
        {"name":"Labor cost","type":"number" },
        {"name":"Other cost","type":"number" },
        {"name":"Straight hours","type":"number" },
        {"name":"Overtime hours","type":"number" },
        {"name":"Invoice File","type":"file" },
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

        if (type="number") {
            input.setAttribute("min", 0);
            input.setAttribute("step", "0.01")
        }

        if (field.readonly) { 
            input.readOnly = true 
        }
        sect.append(label);
        sect.append(input);
        document.querySelector("#invoice-form").append(sect);
    })
    const button = document.createElement("button");
    button.type = "submit";
    button.innerHTML = "submit";
    button.classList.add("submit", "button");
    document.querySelector("#invoice-form").append(button);


    // create close button
    const close = document.createElement("button");
    close.innerHTML = "Cancel";
    close.classList.add("cancel", "button");
    close.onclick = () => {
        document.querySelector("#modal-message").innerHTML = "";
        document.querySelector(".modal-body").scrollTop = 0;
        document.querySelector(".modal").style.display = "none";
        
        return false;
    }
    document.querySelector("#invoice-form").append(close);
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
            // don't fire if a field isn't >= minimums
            if (fields[i].type == "number" || fields[i].type == "date") {
                if (document.querySelector(`input[name="${name}"]`).value < document.querySelector(`input[name="${name}"]`).min) {
                    let message = "<p> Negative adjustment or previous dates invoices must be created by an admin via the admin interface</p>";
                    document.querySelector("#modal-message").innerHTML = `${name} field must be greater than ${document.querySelector(`input[name="${name}"]`).min} ${message}`;
                    document.querySelector(".modal-body").scrollTop = 0;
                    abort = true;
                    break;
                }
            }
            // Doesn't fire if end date isn't greater than start date
            if (name == "End date") {
                if (document.querySelector(`input[name="${name}"]`).value < document.querySelector(`input[name="Start date"]`).value) {
                    document.querySelector("#modal-message").innerHTML = `${name} must not be before Start date`;
                    document.querySelector(".modal-body").scrollTop = 0;
                    abort = true;
                    break;
                }
            }

            formData.append(name, document.querySelector(`input[name="${name}"]`).value);
            console.log(name);
        };
        
        if (abort) {
            return false;
        }
        let project_id = document.querySelector("#project_number").dataset.id;
        formData.append("project_id", project_id);
        request = new XMLHttpRequest();
        request.open("POST", "/invoices/create");
        request.setRequestHeader("X-CSRFToken", document.cookie.substr(10))
        request.onload = () => {
            let response = JSON.parse(request.responseText);
            document.querySelector("#modal-message").innerHTML = response['message'];
            document.querySelector(".modal-body").scrollTop = 0;
            
            if (response['valid']){
                document.querySelector("#modal-message").style.color = "green";
                window.location.replace(`/invoices/${response['invoice']}`)
            }
        }
        request.send(formData);
        return false;
    }
}