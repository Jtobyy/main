window.onload = function() {
    $('.form-step').fadeOut()
    $('.circle').addClass('colorless')
    $('.step1').fadeIn()
    $('.circle1').removeClass('colorless')
    $('.step1 .next').click(() => {
        $('.step1').fadeOut(); 
        $('.circle1').addClass('grey');
        $('.step2').fadeIn()
        $('.circle2').removeClass('colorless');
        $('.circle2').removeClass('grey');
    })
    $('.step2 .next').click(() => {
        $('.step2').fadeOut(); 
        $('.circle2').addClass('grey');
        $('.step3').fadeIn()
        $('.circle3').removeClass('colorless');
        $('.circle3').removeClass('grey');
    })
    $('.step2 .previous').click(() => {
        $('.step2').fadeOut(); 
        $('.circle2').addClass('grey');
        $('.step1').fadeIn()
        $('.circle1').removeClass('grey');
    })
    $('.step3 .next').click(() => {
        $('.step3').fadeOut(); 
        $('.circle3').addClass('grey');
        $('.step4').fadeIn()
        $('.circle4').removeClass('colorless');
        $('.circle4').removeClass('grey');
    })
    $('.step3 .previous').click(() => {
        $('.step3').fadeOut(); 
        $('.circle3').addClass('grey');
        $('.step2').fadeIn()
        $('.circle2').removeClass('grey');
    })
    $('.step4 .previous').click(() => {
        $('.step4').fadeOut(); 
        $('.circle4').addClass('grey');
        $('.step3').fadeIn()
        $('.circle3').removeClass('grey');
    })
}