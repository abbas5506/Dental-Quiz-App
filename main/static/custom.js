// Home Page Navbar Scrolling JS

$(document).ready(function() {
  var navbar = $('.navbar');

  $(window).scroll(function() {
      if ($(window).scrollTop() <= 50) {
          navbar.removeClass('navbar-scrolled');
      } else {
          navbar.addClass('navbar-scrolled');
      }
  });
});

window.onscroll = function() {
  var navbar = document.getElementById("navbar");
  if (document.body.scrollTop > 50 || document.documentElement.scrollTop > 50) {
    navbar.style.backgroundColor = "#fff"; // change to opaque color
  } else {
    navbar.style.backgroundColor = "transparent"; // change to transparent color
  }
};

// Home Page Navbar Links JS
$(document).ready(function() {
  $('.nav-link').mouseenter(function() {
    $(this).addClass('nav-link-animation');
  }).mouseleave(function() {
    $(this).removeClass('nav-link-animation');
  });
});

// Home Page Navbar Red line on Links JS
$(document).ready(function() {
  $('.nav-link').mouseenter(function() {
    $(this).addClass('nav-link-active');
  }).mouseleave(function() {
    $(this).removeClass('nav-link-active');
  });
});
