// prerequist
const q1 = document.getElementById("q1");
const q2 = document.getElementById("q2");
const q3 = document.getElementById("q3");
const q4 = document.getElementById("q4");


const tryagain = document.getElementById("tryagain");
const tryagainBtn = document.getElementById("tryagainBtn");

// hide all questions
q1.style.display = "none";
q2.style.display = "none";
q3.style.display = "none";
q4.style.display = "none";
tryagain.style.display = "none";

// start the first question
const startBtn = document.getElementById("startBtn");

startBtn.onclick = function () {
    q1.style.display = "block";
    startBtn.style.display = 'none';
}

// the 1st question
const q1radio = document.forms["q1radio"].elements['hemi'];
const q1hint = document.getElementById('hintQ1')

for (let i = 0; i < 2; i++) {
    q1radio[i].onclick = function () {
        if (rst['hemi'] == this.id) {
            q1hint.style.color = "green";
            q1hint.innerHTML = "CORRECT";

            q2.style.display = 'block';
        }
        else {
            q1hint.style.color = "red";
            q1hint.innerHTML = "INCORRECT";
        }
    }
}

// the 2nd question

const q2radio = document.forms['q2radio'].elements['cont'];
const q2hint = document.getElementById('hintQ2')

for (let i = 0; i < 7; i++) {
    q2radio[i].onclick = function () {
        if (rst['continent'] == this.id) {
            q2hint.style.color = 'green';
            q2hint.innerHTML = 'CORRECT'

            q3.style.display = 'block';
        } else {
            q2hint.style.color = "red";
            q2hint.innerHTML = "INCORRECT";
        }
    }
}

const q3radio = document.forms['q3radio'].elements['state'];
const q3hint = document.getElementById('hintQ3')

for (let i = 0; i < 4; i++) {
    q3radio[i].onclick = function () {
        if (rst['state'][this.value][1]) {
            q3hint.style.color = 'green';
            q3hint.innerHTML = 'CORRECT'

            q4.style.display = 'block';
        } else {
            q3hint.style.color = "red";
            q3hint.innerHTML = "INCORRECT";
        }
    }
}

if (rst['division'] == 1 || rst['division'] == 2) {

    const q4next = document.getElementById('q4next');

    q4next.onclick = function () {
        tryagain.style.display = "block";
    }

} else {

    const q4radio = document.forms['q4radio'].elements['division'];
    const q4hint = document.getElementById('hintQ4');

    for (let i = 0; i < 4; i++) {
        q4radio[i].onclick = function () {
            if (rst['division'][this.value][1]) {
                q4hint.style.color = 'green';
                q4hint.innerHTML = 'CORRECT'

                tryagain.style.display = 'block';
            } else {
                q4hint.style.color = "red";
                q4hint.innerHTML = "INCORRECT";
            }
        }
    }   

}


tryagainBtn.onclick = function () {
    window.location.href = "/";
}

