const modalCall = $('[data-modal]');

modalCall.on('click', function(e){
    e.preventDefault();

    let $this = $(this);
    let modalId = $this.data('modal');
    $(modalId).fadeIn(300);
    $('html').addClass('no-scroll');
});

$('.close-popup').click(function(e) {
    e.preventDefault();
    $('.popup-bg').fadeOut(300);
    $('html').removeClass('no-scroll');
});