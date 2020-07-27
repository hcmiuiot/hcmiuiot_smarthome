var starFive = document.getElementsByClassName("star-five");
    var star = document.getElementsByClassName("star");
    starFive[0].onclick = () => {
        star[1].className = "star d-none";
        star[0].className = "star"; 
    }
    starFive[1].onclick = () => {
        star[0].className = "star d-none";
        star[1].className = "star"; 
    }