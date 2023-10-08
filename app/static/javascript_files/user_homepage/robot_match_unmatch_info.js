let currentIdx = 0;
let robots = [];

async function fetchData() {
    const response = await fetch("/get_robots");
    const data = await response.json();
    robots = data;
    displayRobot(currentIdx);
}
const robotImageElement = document.querySelector('.new-user-window-image');
function displayRobot(index) {
    if (robots.length > index) {
        const robot = robots[index];
        document.getElementById('robot-name').innerText = robot.name;
        document.getElementById('distance-to-user').innerText = `Distance to user: ${robot.distance_to_user} km` ;
        document.getElementById('processor-unit').innerText = `Processor Unit: ${robot.procesor_unit}`;
        document.getElementById('type-of-robot').innerText = `Type of Robot: ${robot.type_of_robot}`;
        document.getElementById('robot-description').innerText = robot.description;

        robotImageElement.src = `/static/images/robots/${robot.image_file}`;

    } else {
        document.getElementById('robot-name').innerText = "No more robots available";
    }
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



