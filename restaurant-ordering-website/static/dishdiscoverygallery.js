const container = document.querySelector(".slider");
const btns = document.querySelectorAll(".btn");
const imgList = ['slide1', 'slide2', 'slide3', 'slide4', 'slide5', 'slide6'];

let index = 0;
btns.forEach((button) => {
    button.addEventListener('click', () => {
        if (button.classList.contains('btn-left')) {
            index--;
            if (index < 0) {
                index = imgList.length - 1;
            }
        } else {
            index++;
            if (index >= imgList.length) {
                index = 0;
            }
        }
        container.style.background = `url("static/${imgList[index]}.jpg") center/cover no-repeat`;
    });
});

