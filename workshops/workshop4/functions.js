async function callMessage() {
    try {
        const response = await fetch('http://localhost:8000/hello_ud');
        const data = await response.text();
        document.getElementById('result').textContent = data;
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('result').textContent = error;
    }
}

async function callTable() {
    try {
        const response = await fetch('http://localhost:8000/data');
        const data = await response.json();

        let table = '<table>';
        table += '<tr><th>ID</th><th>Name</th><th>Description</th></tr>';

        data.forEach(item => {
            table += `<tr><td>${item.id}</td><td>${item.name}</td><td>${item.description}</td></tr>`;
        });

        table += '</table>';

        document.getElementById('result').innerHTML = table;
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('result').textContent = error;
    }
}

//added a showForm function
async function showForm() {
    try {
        let form = '<form>';
        form += '<label for="name">Name:</label>';
        form += '<input type="text" id="name" name="name"><br>';
        form += '<label for="description">Description:</label>';
        form += '<input type="text" id="description" name="description"><br>';
        form += '<button type="button" onclick="submitForm()">Submit</button>';
        form += '</form>';
        document.getElementById('result').innerHTML = form;
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('result').textContent = error;
    }
}
//added a submitForm function
async function submitForm() {
    try {
        const name = document.getElementById('name').value;
        const description = document.getElementById('description').value;
        
        const response = await fetch('http://0.0.0.0:8000/create_product', {name, description});
        
        const data = await response.json();
        document.getElementById('result').textContent = data.message;
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('result').textContent = error;
    }
}
//callMessage();
// fetch('http://localhost/data') -> rename to fetch('http://localhost:8000/data')