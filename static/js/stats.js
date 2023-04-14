$(document).ready(function(){
    $('#tab2').click(function(){
        $(this).addClass('disabled')
        $('#tab1').removeClass('disabled')
        $('#tab_01').addClass('d-none')
        $('#tab_02').removeClass('d-none')
    })

    $('#tab1').click(function(){
        $(this).addClass('disabled')
        $('#tab2').removeClass('disabled')
        $('#tab_02').addClass('d-none')
        $('#tab_01').removeClass('d-none')
    })
})