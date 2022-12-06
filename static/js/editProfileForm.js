// Selectors for form, to give placeholder to built-in django forms

const edit_form_fields = document.getElementsByTagName('input');
edit_form_fields[6].type='date';

function submit(n) {
    // This function will figure out which tab to display
    // Exit the function if any field in the current tab is invalid:
    if (!validateForm()) return false;
    // Hide the current tab:
    document.getElementById("edit_profile_form").submit();
    return false;
}

function validateForm() {
    // This function deals with validation of the form fields
    let x, y, i, valid = true;
    x = document.getElementsByClassName("tab");
    y = x[currentTab].getElementsByTagName("input");
    // A loop that checks every input field in the current tab:
     for (i = 0; i < y.length; i++) {
        // If a field is empty...
        if (y[i].value == "") {
            // add an "invalid" class to the field:
            y[i].className += " invalid";
            // and set the current valid status to false
            valid = false;
        }
     }
    return valid; // return the valid status
}