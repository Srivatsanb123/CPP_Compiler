var logoutBtn = document.querySelector('.Logout');

logoutBtn.addEventListener('click', function(event) {
  event.preventDefault();
  var confirmLogout = confirm('Are you sure you want to logout?');
  
if (confirmLogout) {
    window.location.href = './logout';    
    console.log('User has logged out.');
  }
});
