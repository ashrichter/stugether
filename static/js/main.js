// Responsive nav bar burger menu selectors
const burgerMenu = document.querySelector('.burger-menu');
const navLinks = document.querySelector('.nav-links');
const links = document.querySelectorAll('.nav-links li');
const l1 = document.querySelector('.l1');
const l2 = document.querySelector('.l2');
const l3 = document.querySelector('.l3');

// Six links in nav bar
const link1 = document.querySelector('.link1');
const link2 = document.querySelector('.link2');
const link3 = document.querySelector('.link3');
const link4 = document.querySelector('.link4');
const link5 = document.querySelector('.link5');
const link6 = document.querySelector('.link6');

// For the 3 lines of the burger menu
burgerMenu.addEventListener('click', ()=> {
  navLinks.classList.toggle('open');

  l1.classList.toggle('active');
  l2.classList.toggle('active');
  l3.classList.toggle('active');
});

// Using try here to avoid js error whist dynamic nav bar for logged in user and logged out user
try {
    link1.addEventListener('click', () => {
      navLinks.classList.toggle('open');
      links.forEach(link => {
        link.classList.toggle('fade');
      })

      l1.classList.toggle('active');
      l2.classList.toggle('active');
      l3.classList.toggle('active');
    })

    link2.addEventListener('click', () => {
      navLinks.classList.toggle('open');
      links.forEach(link => {
        link.classList.toggle('fade');
      })

      l1.classList.toggle('active');
      l2.classList.toggle('active');
      l3.classList.toggle('active');
    })

    link3.addEventListener('click', () => {
      navLinks.classList.toggle('open');
      links.forEach(link => {
        link.classList.toggle('fade');
      })

      l1.classList.toggle('active');
      l2.classList.toggle('active');
      l3.classList.toggle('active');
    })

    link4.addEventListener('click', () => {
      navLinks.classList.toggle('open');
      links.forEach(link => {
        link.classList.toggle('fade');
      })

      l1.classList.toggle('active');
      l2.classList.toggle('active');
      l3.classList.toggle('active');
    })

    link5.addEventListener('click', () => {
      navLinks.classList.toggle('open');
      links.forEach(link => {
        link.classList.toggle('fade');
      })

      l1.classList.toggle('active');
      l2.classList.toggle('active');
      l3.classList.toggle('active');
    })

    link6.addEventListener('click', () => {
      navLinks.classList.toggle('open');
      links.forEach(link => {
        link.classList.toggle('fade');
      })

      l1.classList.toggle('active');
      l2.classList.toggle('active');
      l3.classList.toggle('active');
    })

} catch(TypeError) {
  // Pass
}
