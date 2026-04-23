const input = document.getElementById('todo-input');
const addBtn = document.getElementById('add-btn');
const todoList = document.getElementById('todo-list');
const taskCount = document.getElementById('task-count');
const filterBtns = document.querySelectorAll('.filter-btn');

let tasks = JSON.parse(localStorage.getItem('tasks')) || [];
let currentFilter = 'all';

// Initialize
renderTasks();

// Add Task
addBtn.addEventListener('click', () => {
    const text = input.value.trim();
    if (text === "") {
        alert("Please enter a task!"); // Requirement: Validate empty input
        return;
    }
    const newTask = { id: Date.now(), text, completed: false };
    tasks.push(newTask);
    saveAndRender();
    input.value = "";
});

// Delete and Toggle Completed
todoList.addEventListener('click', (e) => {
    const id = e.target.parentElement.dataset.id;
    if (e.target.classList.contains('delete-btn')) {
        tasks = tasks.filter(t => t.id != id); // Requirement: Delete tasks
    } else {
        const task = tasks.find(t => t.id == id);
        if (task) task.completed = !task.completed; // Requirement: Mark as completed
    }
    saveAndRender();
});

// Filtering Logic
filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        filterBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        currentFilter = btn.dataset.filter;
        renderTasks();
    });
});

function saveAndRender() {
    localStorage.setItem('tasks', JSON.stringify(tasks)); // Bonus: LocalStorage
    renderTasks();
}

function renderTasks() {
    let filteredTasks = tasks;
    if (currentFilter === 'pending') filteredTasks = tasks.filter(t => !t.completed);
    if (currentFilter === 'completed') filteredTasks = tasks.filter(t => t.completed);

    todoList.innerHTML = "";
    filteredTasks.forEach(task => {
        const li = document.createElement('li');
        li.dataset.id = task.id;
        li.className = task.completed ? 'completed' : '';
        li.innerHTML = `
            <span>${task.text}</span>
            <button class="delete-btn">Delete</button>
        `;
        todoList.appendChild(li); // Requirement: DOM manipulation
    });
    
    taskCount.innerText = tasks.length; // Requirement: Display total count
}