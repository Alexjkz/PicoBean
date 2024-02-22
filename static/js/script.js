import * as animationsModule from "/static/js/animations.js";

const eyes = document.querySelectorAll(".eye");
// #region DEBUG BUTTONS FOR ACTIONS
let blinkBtn = document.querySelector(".blink");
let listeningBtn = document.querySelector(".listening");
let stopBtn = document.querySelector(".stopListening");
let pauseBtn = document.querySelector(".pause");
let chillBtn = document.querySelector(".chill");
let ideBtn = document.querySelector(".ide");
let menu = document.querySelector(".menu");
//#endregion

const windowHeight = window.screen.height;
let aroma = 1;
let length = 1;
let menuOpened = false;
// #region MENU VAR
let beveragesBtn = document.querySelectorAll(".bevanda");
let beverages = document.querySelector(".beverages");
let beveragesSettings = document.querySelector(".beveragesSettings");

const setLowBtn = document.querySelectorAll(".low");
const setMediumBtn = document.querySelectorAll(".medium");
const setHighBtn = document.querySelectorAll(".high");
const setlengthIcon = document.querySelector(".lengthIcon");
const returnBtn = document.querySelector(".return");
const erogaBtn = document.querySelector(".erogaBtn");
let erogaBtnIcon = erogaBtn.querySelector("img");
// menu header
const menuHeader = document.querySelector(".menuHeader");
// const userIcon = document.querySelector("#user")
// const settingsIcon = document.querySelector("#menuSettings")
// const currentUserIcon = document.querySelector('')
// #endregion

/////////////////////////////////////////////////////////////



document.addEventListener('keydown', function (e) {
  // Disabilita il zoom con Ctrl + '+'
  if ((e.ctrlKey || e.metaKey) && (e.key === '+' || e.key === '=')) {
    e.preventDefault();
  }
  // Disabilita il zoom con Ctrl + '-'
  if ((e.ctrlKey || e.metaKey) && e.key === '-') {
    e.preventDefault();
  }
});


// #region ANIMATIONS
const socket = io();
socket.on("assistant_response", (data) => {
  //console.log(data.text);
  console.log("SONO ENTRATO NEGLI IF");
  // Puoi utilizzare data.animazione per controllare l'animazione nell'HTML
  if (data.animation === "listeningMode") {
    animationsModule.stopAnimations();
    animationsModule.listeningMode(); // Ad esempio, chiama una funzione per avviare l'animazione di ascolto
    console.log("ATTIVO LISTEN");    
  }

  if (data.animation === "STOPlisteningMode") {
    animationsModule.stopAnimations();
    animationsModule.STOPlisteningMode();
    console.log("DISATTIVO LISTEN"); 
  }

  if (data.animation === "idleState") {
    animationsModule.stopAnimations();
    animationsModule.idleState();
  }
  
  if (data.animation === "blinkEyes") {
    animationsModule.stopAnimations();
    animationsModule.blinkEyes();
  }

  if (data.animation === "happyState") {
    animationsModule.stopAnimations();
    animationsModule.happyState();
  }

  if (data.animation === "restState") {
    animationsModule.stopAnimations();
    animationsModule.restState();
  }

  if (data.animation === "wakeState") {
    animationsModule.stopAnimations();
    animationsModule.wakeState();
  }

  if (data.animation === "questState") {
    animationsModule.stopAnimations();
    animationsModule.questState();
  }

  if (data.animation === "winkState") {
    animationsModule.stopAnimations();
    animationsModule.winkState();
  }

  if (data.animation === "talkState") {
    animationsModule.stopAnimations();
    animationsModule.talkState();
  }

  if (data.animation === "unsureState") {
    animationsModule.stopAnimations();
    animationsModule.unsureState();
  }

  if (data.animation === "sadState") {
    animationsModule.stopAnimations();
    animationsModule.sadState();
  }

  if (data.animation === "loadCoffee") {    
    animationsModule.stopAnimations();
    animationsModule.loadCoffee();
  }

  
  // if (data.animation === "Anim_caffe") {
  //   animationsModule.chill();
  // }
  // Aggiorna la visualizzazione della risposta nell'HTML come preferisci
});




// #region MENU

// for each beverage 
beveragesBtn.forEach((button) => {
  button.addEventListener("click", function () {
    erogaBtn.addEventListener("click", function(){
      animationsModule.stopAnimations();
      animationsModule.loadCoffee();
      console.log("invia a backend la bevanda selezionata");
    })
    updateDispenseUI(button);

    // selectedBtn = button.classList;
    // console.log(selectedBtn);
  });
});

window.addEventListener("click", function (e) {
  // console.log(e.clientY);
  if (
    (e.clientY < windowHeight - 180 && e.clientY > 45) ||
    menuOpened == false
  ) {
    showMenu();
  }
});

// Set beverage length to short
setLowBtn.forEach((button) => {
  button.addEventListener("click", function () {
    button.style.backgroundColor = "white";

    if (button.className === "setCircle low len") {
      // This is the reference to the coffe length img
      setlengthIcon.src = "http://127.0.0.1:5000/static/logos/menu/Short.svg";
      setMediumBtn[0].style.backgroundColor = "black";
      setHighBtn[0].style.backgroundColor = "black";
      length = 0;
    } else {
      setMediumBtn[1].style.backgroundColor = "black";
      setHighBtn[1].style.backgroundColor = "black";
      aroma = 0;
    }
  });
});

setMediumBtn.forEach((button) => {
  button.addEventListener("click", function () {
    button.style.backgroundColor = "white";
    if (button.className === "setCircle medium len") {
      setlengthIcon.src = "http://127.0.0.1:5000/static/logos/menu/Medium.svg";
      setHighBtn[0].style.backgroundColor = "black";
      length = 1;
    } else {
      setHighBtn[1].style.backgroundColor = "black";
      aroma = 1;
      console.log("medium");
    }
  });
});

setHighBtn.forEach((button) => {
  button.addEventListener("click", function () {
    button.style.backgroundColor = "white";
    if (button.className === "setCircle high len") {
      setMediumBtn[0].style.backgroundColor = "white";
      setlengthIcon.src = "http://127.0.0.1:5000/static/logos/menu/Long.svg";
      length = 2;
    } else {
      console.log("dioc");
      setMediumBtn[1].style.backgroundColor = "white";
      aroma = 2;
    }
  });
});

returnBtn.addEventListener("click", function () {
  beveragesSettings.style.display = "none";
  beverages.style.display = "block";
  console.log("daje");
});



function showMenu() {
  if (menuOpened === false) {
    menu.style.bottom = "0";
    menuHeader.style.visibility = "visible";
    menuHeader.style.opacity = 1;
    menuOpened = true;
  } else {
    menu.style.bottom = "-10rem";
    menuHeader.style.visibility = "hidden";
    menuHeader.style.opacity = 0;
    menuOpened = false;
  }
}

// change src img of dispense button with the beverage 
function updateDispenseUI(beverageBtn){
  let selBeverage = beverageBtn.querySelector("img");    
  console.log(selBeverage.src); 
  erogaBtnIcon.style.opacity = 0;  
  erogaBtnIcon.src = selBeverage.src;
  setTimeout(() => {erogaBtnIcon.style.opacity = 1;}, 500 );   
  setTimeout(() => {erogaBtnIcon.style.opacity = 0;}, 1500 );       
  setTimeout(() => {erogaBtnIcon.src = "http://127.0.0.1:5000/static/logos/menu/Dispense.svg";
  erogaBtnIcon.style.opacity = 1;  },2000 );        
  beverages.style.display = "none";
  console.log(beverages.style.display);
  beveragesSettings.style.display = "flex";
  console.log("ohhhh");
}
// #endregion
