function validateForm() {
    var email = document.getElementById("email").value;
    var password = document.getElementById("password").value;
    if (email == "") {
        alert("Please enter your email.");
        return false;
    }
    if (password == "") {
        alert("Please enter your password.");
        return false;
    }
    return true;
}

var form = document.querySelector("form");
form.addEventListener("submit", function (event) {
    event.preventDefault();
    if (validateForm()) {
        form.submit();
    }
});
