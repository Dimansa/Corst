const slidedownCall = $('[data-slidedown]');
let flag = false;
slidedownCall.on('click', function(e){
    e.preventDefault();
    let $this = $(this);
    let arrow = $this.find('img');
    let slidedownId = $this.data('slidedown');
    if (!flag){
        $(slidedownId).slideDown(duration=1000);
        arrow.toggleClass('transform');
    } else{
        $(slidedownId).slideUp(duration=1000);
        arrow.toggleClass('transform');
    }
    flag = !flag;
})