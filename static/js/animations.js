//function to add events to buttons and manage animations
// document.addEventListener("DOMContentLoaded", function () {
    const eyesContainer = document.querySelector(".eye-container");
    const leftEye = eyesContainer.querySelector(".left-eye");
    const rightEye = eyesContainer.querySelector(".right-eye");
    const leftEyeBrown = eyesContainer.querySelector(".left-eyeBrown");
    const rightEyeBrown = eyesContainer.querySelector(".right-eyeBrown");
    const coffeeCup = document.querySelector(".cup");
    const handleCup = document.querySelector(".handle");

    const buttons = [
        { id: "blink-button", action: blinkEyes },
        { id: "idle-button", action: idleState },
        { id: "listening-button", action: listeningMode },
        { id: "STOPlistening-button", action: STOPlisteningMode },
        { id: "happy-button", action: happyState },
        { id: "rest-button", action: restState },
        { id: "quest-button", action: questState },
        { id: "wink-button", action: winkState },
        { id: "talk-button", action: talkState },
        { id: "unsure-button", action: unsureState },
        { id: "sad-button", action: sadState },
        { id: "wake-button", action: wakeState },
        { id: "loading-coffee", action: loadCoffee }
    ];
    
    

    buttons.forEach((button) => {
        const btn = document.getElementById(button.id);
        btn.addEventListener("click", function () {
            stopAnimations();
            button.action();
        });
    });


    //Stop Animations (allows to change anims while being played)
    function stopAnimations() {
        leftEye?.classList.remove("blink", "listenL", "happyEyes", "restEyes","wakeEyesL", "questEyesL", "winkEyesL", "STOPlistenL", "talkEyesL","unsureEyesL","sadEyesL");
        rightEye?.classList.remove("blink", "listenR", "happyEyes", "restEyes","wakeEyesR", "questEyesR", "winkEyesR", "STOPlistenR", "talkEyesR","unsureEyesR","sadEyesR");
        
        leftEyeBrown?.classList.remove("happyEBL", "questLEB", "winkLEB", "talkEyesLEB","unsureEyesLEB","sadEyesLEB");
        rightEyeBrown?.classList.remove("happyEBR", "questREB", "winkREB", "talkEyesREB","unsureEyesREB","sadEyesREB");
        
        if (coffeeCup) {
            coffeeCup.classList.remove("animate", "fill");
            coffeeCup.style.display = "none";
            
            leftEye.style.display = "block";
            rightEye.style.display = "block";
            
            leftEyeBrown.style.display = "none";
            rightEyeBrown.style.display = "none";
        }
    }

    //---------------elements <---> animations---------------//
    


    //Default
    function idleState() {
        leftEye.style.display = "block";
        rightEye.style.display = "block";
        
        leftEyeBrown.style.display = "none";
        rightEyeBrown.style.display = "none";
    }

    //Blink
    function blinkEyes() {
        leftEye.classList.add("blink");
        rightEye.classList.add("blink");
        
        leftEyeBrown.style.display = "none";
        rightEyeBrown.style.display = "none";
    }

    //Listening Mode (User is speaking)
    function listeningMode() {
        leftEye.classList.add("listenL");
        rightEye.classList.add("listenR");
        
        leftEyeBrown.style.display = "none";
        rightEyeBrown.style.display = "none";

        console.log("HO INVIATO COMANDO LISTEN AL CSS");
    }

    //Interrupt Listening Mode (Use only if Listening Mode is playing)
    function STOPlisteningMode() {
        leftEye.classList.add("STOPlistenL");
        rightEye.classList.add("STOPlistenR");
        
        leftEyeBrown.style.display = "none";
        rightEyeBrown.style.display = "none";

        console.log("HO INVIATO COMANDO STOP LISTEN AL CSS");
    }

    //Happy Expression
    function happyState() {
        leftEye.classList.add("happyEyes");
        rightEye.classList.add("happyEyes");

        leftEyeBrown.style.display = "flex";
        leftEyeBrown.classList.add("happyEBL");

        rightEyeBrown.style.display = "flex";
        rightEyeBrown.classList.add("happyEBR");
    }

    //Standby Mode
    function restState() {
        leftEye.classList.add("restEyes");
        rightEye.classList.add("restEyes");
        
        leftEyeBrown.style.display = "none";
        rightEyeBrown.style.display = "none";
    }

    //Wake Up after Standby
    function wakeState() {
        leftEye.classList.add("wakeEyesL");
        rightEye.classList.add("wakeEyesR");
        
        leftEyeBrown.style.display = "none";
        rightEyeBrown.style.display = "none";
    }

    //If AI does not understand user's commands
    function questState() {
        leftEye.classList.add("questEyesL");
        rightEye.classList.add("questEyesR");

        leftEyeBrown.style.display = "flex";
        leftEyeBrown.classList.add("questLEB");

        rightEyeBrown.style.display = "flex";
        rightEyeBrown.classList.add("questREB");
    }

    //Wink
    function winkState() {
        leftEye.classList.add("winkEyesL");
        rightEye.classList.add("winkEyesR");

        leftEyeBrown.style.display = "flex";
        leftEyeBrown.classList.add("winkLEB");

        rightEyeBrown.style.display = "flex";
        rightEyeBrown.classList.add("winkREB");
    }

    //To use when AI is answering to user
    function talkState() {
        leftEye.classList.add("talkEyesL");
        rightEye.classList.add("talkEyesR");

        leftEyeBrown.style.display = "flex";
        leftEyeBrown.classList.add("talkEyesLEB");

        rightEyeBrown.style.display = "flex";
        rightEyeBrown.classList.add("talkEyesREB");
    }

    //Unsure
    function unsureState () {
        leftEye.classList.add("unsureEyesL")
        rightEye.classList.add("unsureEyesR")

        leftEyeBrown.style.display = "flex";
        leftEyeBrown.classList.add("unsureEyesLEB");

        rightEyeBrown.style.display = "flex";
        rightEyeBrown.classList.add("unsureEyesREB");
    }

    //Sad
    function sadState () {
        leftEye.classList.add("sadEyesL")
        rightEye.classList.add("sadEyesR")

        leftEyeBrown.style.display = "flex";
        leftEyeBrown.classList.add("sadEyesLEB");

        rightEyeBrown.style.display = "flex";
        rightEyeBrown.classList.add("sadEyesREB");
    }

    //Coffee preparation
    function loadCoffee() {        
        if (coffeeCup) {
            coffeeCup.style.display = "block";
            coffeeCup.classList.add("fill");
            leftEye.style.display = "none";
            rightEye.style.display = "none";
        }

        if (coffeeCup) {
            coffeeCup.addEventListener("animationend", function () {
                coffeeCup.style.display = "none";
                coffeeCup.classList.remove("animate", "fill");
                leftEye.style.display = "block";
                rightEye.style.display = "block";
            });
        }
    }

    export {
        stopAnimations,
        idleState,
        blinkEyes,
        listeningMode,
        STOPlisteningMode,
        happyState,
        restState,
        wakeState,
        questState,
        winkState,
        talkState,
        unsureState,
        sadState,
        loadCoffee
    };
//  });

 