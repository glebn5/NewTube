// function addClassOnClick(elementId, className) {
//     // Находим элемент по id
//     var element = document.getElementById(elementId);
    
//     // Проверяем, существует ли элемент
//     element.addEventListener('click', function() {
//         element.classList.add(className);
//     });
    
// }

// // Использование функции
// addClassOnClick('menu', 'show');

let burger = document.querySelector(".burger");
let menu = document.querySelector(".menu");
burger.addEventListener('click', ()=> {
    menu.classList.toggle("show")
})

