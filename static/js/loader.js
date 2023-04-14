let mask = document.querySelector('.mask');

window.addEventListener('load', () => {
    mask.classList.add('hide');
    setTimeout(() => {
     mask.remove();
     }, 600);
});

$('.ref').on('click', function(){
    $('#preload').removeClass('d-none');
});

$(document).on('click', 'input[type=submit]', function () {
    $('#preload').removeClass('d-none');
});
