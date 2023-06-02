var logoutBtn = document.querySelector('#Logout');

logoutBtn.addEventListener('click', function(event) {
  event.preventDefault();
  var confirmLogout = confirm('Are you sure you want to logout?');
  
if (confirmLogout) {
    window.location.href = './logout';    
    console.log('User has logged out.');
  }
});
var editor = CodeMirror.fromTextArea(cppcode, {
  lineNumbers: true,
  mode: "text/x-c++src",
  indentUnit: 4,
  matchBrackets: true,
  scrollbarStyle: "overlay",
  autoCloseBrackets:true,
  theme: "dracula"
});

function codecheck() {
  var cppcode = editor.getValue();
  if (cppcode.includes("main")) {
      return false;
  }
  return true;
}

var form = document.querySelector("form");
form.addEventListener("submit", function (e) {
  e.preventDefault();
  if (codecheck()) {
      alert("The code must contain main() to execute");
  } else {
      form.submit();
  }
});