// For the multi-step register form
let currentTab = 0; // Current tab is set to be the first tab (0)
showTab(currentTab); // Display the current tab

// Selectors for form, to give placeholder to built-in django forms
const register_form_fields = document.getElementsByTagName('input');
const register_form_select_fields = document.getElementsByTagName('select');
register_form_fields[1].placeholder='First name';
register_form_fields[2].placeholder='Last name';
register_form_fields[3].placeholder='Username';
register_form_fields[4].placeholder='Password';
register_form_fields[5].placeholder='Re-enter password';

register_form_fields[6].placeholder='E-mail';
register_form_select_fields[1].placeholder='Institution';
register_form_select_fields[2].placeholder='Field of study';
register_form_fields[7].placeholder='Date of birth';
register_form_fields[7].type='date';
register_form_fields.oninput="this.className = ''";


function showTab(n) {

    const x = document.getElementsByClassName("tab");
    x[n].style.display = "block";
    if (n == 0) {
        document.getElementById("prevBtn").style.display = "none";
    } else {
        document.getElementById("prevBtn").style.display = "inline";
    }

    if (n == (x.length - 1)) {
        document.getElementById("nextBtn").innerHTML = "Submit";
    } else if (n == (x.length)) {
        document.getElementById("nextBtn").type="submit";
    } else {
        document.getElementById("nextBtn").innerHTML = "Next";
    }
    // and run a function that will display the correct step indicator:
    fixStepIndicator(n)
}

function nextPrev(n) {
    // This function will figure out which tab to display
    const x = document.getElementsByClassName("tab");
    // Exit the function if any field in the current tab is invalid:
    if (n == 1 && !validateForm()) return false;
    // Hide the current tab:
    x[currentTab].style.display = "none";
    // Increase or decrease the current tab by 1:
    currentTab = currentTab + n;
    // if you have reached the end of the form...
    if (currentTab >= x.length) {
        document.getElementById("regForm").submit();
        return false;
    }
    // Otherwise, display the correct tab:
    showTab(currentTab);
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
     // If the valid status is true, mark the step as finished and valid:
    if (valid) {
        document.getElementsByClassName("step")[currentTab].className += " finish";
    }
    return valid; // return the valid status
}

function fixStepIndicator(n) {
    // This function removes the "active" class of all steps...
    let i, x = document.getElementsByClassName("step");
    for (i = 0; i < x.length; i++) {
        x[i].className = x[i].className.replace(" active", "");
    }
    //... and adds the "active" class on the current step:
    x[n].className += " active";
}