function makeEaseOut(timing) {
  return function(timeFraction) {
    return 1 - timing(1 - timeFraction);
  }
}

function makeEaseInOut(timing) {
  return function(timeFraction) {
    if (timeFraction < .5)
      return timing(2 * timeFraction) / 2;
    else
      return (2 - timing(2 * (1 - timeFraction))) / 2;
  }
}

function circ(timeFraction) {
  return 1 - Math.sin(Math.acos(timeFraction));
}

var bounceEaseOut = makeEaseOut(circ);

function showLogIn() {
  animate({
    duration: 1000,
    timing: bounceEaseOut,
    draw: function(progress) {
      loginsplash.style.top = -1*(100 - progress * 100) + '%';
    }
  });
}

function hideLogIn() {
  animate({
    duration: 1000,
    timing: bounceEaseOut,
    draw: function(progress) {
      loginsplash.style.top = -1*(progress * 100) + '%';
    }
  });
}

$(document).ready(function(){
    $("#sign-in").click(function() {
      showLogIn();
    });

    $("#closelogin").click(function() {
      hideLogIn();
    });

    $("#footer").click(function() {
       $(".contact-data").slideDown();
    });

    $("#footer").mouseleave(function() {
      $(".contact-data").slideUp();
    });

    $('#closelogin').mouseenter(function() {
      $(".close-login-text").animate({width: 'toggle'});
    });

    $('#closelogin').mouseleave(function() {
      $(".close-login-text").animate({width: 'toggle'});
    });
});