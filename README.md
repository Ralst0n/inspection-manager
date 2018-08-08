# inspection-manager

## inspection-manager is a web app created to support the 2-man Pennsylvania teams the way a whole corporate office supports the Syracuse teams. As well as organize information to avoid having to rely on multiple excel files and outlook items.

## Features
    utilizes ajax request to add to databases without unnecessary page request
    uses selenium web driver to scrape for proposed projects and  projects released with information on who applied for it and who won.
    Generates two email reports for management teams both sent via email. One detailing the ytd revenue and projects using svg to create bar graph. 

## Home
The home/index page utilizes html data attributes to pass information such as revenue, revenue goal & goal percentage to date from the django backend into the html template.

Awaiting invoices filters querysets to find invoices in that status that corresponds to the current users duties.
recent activity gives the most recent change in each invoice for that office.

## Inspectors
Inspectors populates by default with the list of inspectors that work for the logged in user. 

Using ajax request the user is able to search the inspectors data table for those that possess a certain classification
level as well as have required certifications.

The page also has an "Add Inspector" button that can produces a form modal to create an inspector there on the page. 
A successful post will respond with a message linking to the inspectors detail page.

## Inspectors-details
--If an inspector is the users employee
Inspectors details populates basic contact, project and work certification info.

--If the inspector doesn't work for the user
They are a prospect the contact information is available but a notes section is provided that via ajax allows a manager/employee to add to the notes table about the prospect.

## Projects
Uses dataTables to sort and paginate basic information about a project. Providing links to each active project.

## Project-details
Each project page provides budget information as well as to date totals aggregated from the Invoice table.

Also uses dataTables to sort and paginate the invoices for a given project and provides links to each project

Finally, like the Inspectors page, provides a button to add an invoice that generates a form modal allowing the asynchronous addition of an invoice to the page. 
Unlike inspectors, invoices aren't added in batches so upon success the user is redirected to the invoice detail page

## Invoice-details

Provides a link to the pdf of the invoice hosted using AWS S3 as well as basic financial information for the invoice

The ability to edit and add comments or reject/approve an invoice are restricted based on the current status of the invoice. Invoice objects have a status of 0 to 3 ranging from "in draft" to "approved to submit" if a users role does not match the status they have no options on the given invoice.

If an invoice moves into a users status by being approved or rejected there the user is notified by email using sendgrids api.

## Devices

Devices tab also uses dataTables to list out each iphone/ipad in the field for the given office as well as who is using it.