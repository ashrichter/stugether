function applyTheme(theme) {
    document.body.classList.remove("theme-light", "theme-dark", "theme-black", "theme-desert");
    document.body.classList.add(`theme-${theme}`);
    if(theme == 'light') {
        document.getElementById("navLogo").src = "../../../../static/logo/logo-light.svg";
    } else if (theme == 'black') {
        document.getElementById("navLogo").src = "../../../../static/logo/logo-black.svg";
    } else if (theme == 'desert') {
        document.getElementById("navLogo").src = "../../../../static/logo/logo-desert.svg";
    } else {
        document.getElementById("navLogo").src = "../../../../static/logo/logo.svg";
    }
}

document.addEventListener("DOMContentLoaded", () => {
   document.querySelector("#selectTheme").addEventListener("change", function() {
        applyTheme(this.value);
   });
});

document.addEventListener("DOMContentLoaded", () => {
    const savedTheme = localStorage.getItem("selectTheme");

    applyTheme(savedTheme);

    for (const optionElement of document.querySelectorAll("#selectTheme option")) {
        optionElement.selected = savedTheme === optionElement.value;
    }

    document.querySelector("#selectTheme").addEventListener("change", function () {
        localStorage.setItem("selectTheme", this.value);
        applyTheme(this.value);

        try {
            $("#selectThemeInPage").val(this.value).trigger("change");
        } catch (TypeError) {
            // pass
        }
    });
});

// For settings page
document.addEventListener("DOMContentLoaded", () => {
    try {
        document.querySelector("#selectThemeInPage").addEventListener("change", function () {
            applyTheme(this.value);
        });
    } catch(TypeError) {
      // Pass
    }
});

document.addEventListener("DOMContentLoaded", () => {
    const savedTheme = localStorage.getItem("selectTheme");

    applyTheme(savedTheme);

    for (const optionElement of document.querySelectorAll("#selectThemeInPage option")) {
        optionElement.selected = savedTheme === optionElement.value;
    }

    try {
        $("#selectThemeInPage").val(savedTheme).trigger("change");

        document.querySelector("#selectThemeInPage").addEventListener("change", function () {
            localStorage.setItem("selectTheme", this.value);
            applyTheme(this.value);

            $("#selectTheme").val(this.value).trigger("change");
        });
        } catch(TypeError) {
          // Pass
        }
});
