// new Splide( '.splide' ).mount();
new Splide( '.splide', {
    type   : 'loop',
    autoplay: true,
    interval: 5000,
    pauseOnHover: true,
    speed: 1000,
} ).mount();