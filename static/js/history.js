var logoutBtn = document.querySelector('.Clear');

logoutBtn.addEventListener('click', function(event) {
event.preventDefault();
var confirmLogout = confirm('Are you sure you want to Clear all History?');

if (confirmLogout) {
    window.location.href = './clear';
    console.log('History Cleared.');
}
});