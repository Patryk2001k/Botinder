let currentIdx = 0;
let robots = [];
let matched_robot = []

async function fetchData() {
    const response = await fetch("/get_robots");
    const data = await response.json();
    robots = data;
    displayRobot(currentIdx);
}
const robotImageElement = document.querySelector('.new-user-window-image');
const demoEndAlertElement = document.getElementById('demo-end-alert');
function displayRobot(index) {
    if (robots.length > index) {
        const robot = robots[index];
        document.getElementById('robot-name').innerText = robot.name;
        document.getElementById('distance-to-user').innerText = `Distance to user: ${robot.distance_to_user} km` ;
        document.getElementById('processor-unit').innerText = `Processor Unit: ${robot.procesor_unit}`;
        document.getElementById('type-of-robot').innerText = `Type of Robot: ${robot.type_of_robot}`;
        document.getElementById('robot-description').innerText = robot.description;

        robotImageElement.src = `/static/images/robots/${robot.image_file}`;
        if (index === robots.length - 1) {
            demoEndAlertElement.style.display = 'flex';
        }
    } else {
        document.getElementById('robot-name').innerText = "No more robots available";
    }
}

function addMatch(matched_robot) {
    const container = document.querySelector('.main-match-users-menu');

    // Tworzenie nowego elementu div
    const newDiv = document.createElement('div');
    newDiv.className = 'first-matched-user';
  
    // Tworzenie nowego elementu a (linku)
    const newLink = document.createElement('a');
    newLink.href = `/chatroom/${matched_robot.chatroom_id}`;
  
    // Tworzenie nowego elementu img (obrazu)
    const newImg = document.createElement('img');
    console.log(matched_robot.robot_image);
    const staticUrl = document.querySelector('.main-match-users-menu').getAttribute('data-static-url');
    console.log(staticUrl)
    newImg.src = `${staticUrl}${matched_robot.robot_image}`;
    console.log(newImg.src)

    // Tworzenie nowego elementu p (paragrafu)
    const newParagraph = document.createElement('p');
    newParagraph.textContent = matched_robot.robot_name;
  
    // Dodawanie elementów do struktury DOM
    newLink.appendChild(newImg);
    newLink.appendChild(newParagraph);
    newDiv.appendChild(newLink);
  
    container.appendChild(newDiv);
}


function showAlert() {
    document.getElementById("custom-alert").style.display = "flex";
    addMatch(matched_robot);
    matched_robot = [];
}
  
function closeAlert() {
    document.getElementById("custom-alert").style.display = "none";
}
  
document.addEventListener("DOMContentLoaded", function () {
    const customAlert = document.getElementById("custom-alert");
    const customAlertContent = document.querySelector(".custom-alert-content");
  
    customAlert.addEventListener("click", function (event) {
      if (!customAlertContent.contains(event.target)) {
        closeAlert();
      }
    });
});

function closeDemoEndAlert() {
    document.getElementById("demo-end-alert").style.display = "none";
}

async function nextUserMatch() {

    const data = robots[currentIdx];
    currentIdx++;
    try {
        const response = await fetch('http://127.0.0.1:5000/match', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });
        
        const result = await response.json();
        console.log('Success:', result);
        if (response.status === 200) {
            const matchResult = result.match_result;
            matched_robot = matchResult;
            console.log('Match Result:', matchResult);
            showAlert();
        }
        
        displayRobot(currentIdx);
    } catch (error) {
        console.error('Error:', error);
    }
}

async function nextUserUnmatch() {

    const data = robots[currentIdx];
    currentIdx++;
    try {
        const response = await fetch('http://127.0.0.1:5000/unmatch', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });
        
        const result = await response.json();
        console.log('Success:', result);
        
        displayRobot(currentIdx);
    } catch (error) {
        console.error('Error:', error);
    }
}

function nextUserUnmatch2() {
    const newUserWindow = document.querySelector('.new-user-window');
    newUserWindow.classList.add('move-left');  // Dodaje klasę, która przesuwa okno w lewo
  
    // Reset klasy po animacji
    setTimeout(() => {
      newUserWindow.classList.remove('move-left');
      // Tu możesz załadować kolejnego użytkownika
    }, 300);
  }

  function nextUserMatch2() {
    const newUserWindow = document.querySelector('.new-user-window');
    newUserWindow.classList.add('move-right');  // Dodaje klasę, która przesuwa okno w prawo
  
    // Reset klasy po animacji
    setTimeout(() => {
      newUserWindow.classList.remove('move-right');
      // Tu możesz załadować kolejnego użytkownika
    }, 300);
  }


fetchData();
displayRobot(currentIdx)



