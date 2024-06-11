let titleElement = document.getElementById("task_title")
let descriptionElement = document.getElementById("task_description")

const tableDiv = document.getElementById("main-table")

url = "172.20.10.2"

getTodos = () => {
    fetch(`${url}/static/mock/data.json`)
    .then(response => {
        if (!response.ok) {
            throw new Error("Network sucks")
        }
    
        console.log(response);
    
        return response.json()
    })
    .then(
        data => {
            todos = data.json
            console.log(todos);
        }
    )
    .catch(err => {
        console.error(err);
    })
}

counter = 4

submitInput = () => {
    let titleValue = titleElement.value
    let descriptionValue = descriptionElement.value


    const newTask = document.createElement("tr")

    const taskNum = document.createElement("th")
    taskNum.textContent = counter

    const taskTitle = document.createElement("td")
    taskTitle.textContent = titleValue

    const taskAuthor = document.createElement("td")
    taskAuthor.textContent = "Hudson Jones"

    const taskDescription = document.createElement("td")
    taskDescription.textContent = descriptionValue

    const taskCompleted = document.createElement("td")
    taskCompleted.textContent = "Incomplete"

    newTask.appendChild(taskNum)
    newTask.appendChild(taskTitle)
    newTask.appendChild(taskAuthor)
    newTask.appendChild(taskDescription)
    newTask.appendChild(taskCompleted)
    tableDiv.appendChild(newTask)

    counter ++
}

