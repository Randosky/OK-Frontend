let tabsBtn = document.querySelectorAll('.steps__href');
let tabsItem = document.querySelectorAll('.about__list');

tabsBtn.forEach(function(element){
  element.addEventListener('click', function(e){
    const path = e.currentTarget.dataset.path;

    tabsBtn.forEach(function(btn){
      btn.classList.remove('steps__href--active')});
    e.currentTarget.classList.add('steps__href--active');

    tabsItem.forEach(function(element){ element.classList.remove('about__list--active')});
    document.querySelector(`[data-target="${path}"]`).classList.add('about__list--active');
  });
});