const openbar = () => {
    document.querySelector('#bar').classList.toggle('fa-xmark');

// document.querySelector('.sc').classList.add('scrl');
document.querySelector('.scrl').classList.toggle('sc');
}
const home = () => {
document.querySelector('.scrl').classList.remove('sc');
document.querySelector('#bar').classList.remove('fa-xmark');
}
const about = () => {
document.querySelector('.scrl').classList.remove('sc');
document.querySelector('#bar').classList.remove('fa-xmark');

}

const heads = document.querySelector('.header');

window.addEventListener('scroll', () => {
if (window.scrollY > 50){
    heads.classList.add('header-scrolled');
    document.querySelector('.logo').style.color = 'black';
    document.querySelector('.link1').style.color = 'black';
    document.querySelector('.link2').style.color = 'black';
    document.querySelector('.link3').style.color = 'black';
    document.querySelector('.link4').style.color = 'black';
    document.querySelector('.link5').style.color = 'black';
    document.querySelector('.link6').style.color = 'black';
    document.querySelector('.link7').style.color = 'black';
}
else if (window.screenY <= 50){
    heads.classList.remove('header-scrolled')
    document.querySelector('.logo').style.color = 'white';
    document.querySelector('.link1').style.color = 'white';
    document.querySelector('.link2').style.color = 'white';
    document.querySelector('.link3').style.color = 'white';
    document.querySelector('.link4').style.color = 'white';
    document.querySelector('.link5').style.color = 'white';
    document.querySelector('.link6').style.color = 'white';
    document.querySelector('.link7').style.color = 'white';
}
})


