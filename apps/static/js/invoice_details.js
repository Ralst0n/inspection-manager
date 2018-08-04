// document.addEventListener("DOMContentLoaded", () => {
//     let edit_mode = false;
//     let old_values = []
//     document.querySelector("#edit").onclick = () => {
//         edit_mode = !edit_mode;
//         // store the old values for things here incase they cancel
//         if (edit_mode){
//             console.log("edit mode!")
            
//             document.querySelectorAll(".edittable").forEach( element=>{
//                 element.contentEditable = true;
//                 old_values.push(element.innerHTML)
//             })
//             console.log(old_values);
//         }
//         else {
//             console.log(old_values);
//             console.log("edit mode off")
//             let index = 0;
//             document.querySelectorAll(".edittable").forEach( element=>{
//                 element.innerHTML=old_values[index];
//                 index++;
//                 element.contentEditable = false;
//             })
//         }
//         return false;
//     }

//     if (edit_mode){
//         document.querySelector("#labor_cost").addEventListener("blur", () => {
//             let labor = parseFloat(document.querySelector("#labor_cost").innerHTML)
//             let other = parseFloat(document.querySelector("#other_cost"))
//             document.querySelector("#total_cost").innerHTML = labor + other;
//             console.log(labor);
//         })
//     }
// })