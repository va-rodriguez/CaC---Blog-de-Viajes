function showLogin() {
    document.getElementById('login').style.display = 'block';
    document.getElementById('register').style.display = 'none';
}

function showRegister() {
    document.getElementById('login').style.display = 'none';
    document.getElementById('register').style.display = 'block';
}

document.addEventListener('DOMContentLoaded', (event) => {
    showLogin();
});

document.getElementById('loginBtn').addEventListener('click', (event) => {
    event.preventDefault();
    const username = document.getElementById('loginUsername').value;
    const password = document.getElementById('loginPassword').value;

    const storedUsers = JSON.parse(localStorage.getItem('users')) || [];
    const user = storedUsers.find(user => user.username === username && user.password === password);

    if (user) {
        Swal.fire({
            title: '¡Bienvenido!',
            text: 'Inicio de sesión exitoso',
            icon: 'success',
            confirmButtonText: 'Continuar'
        }).then(() => {
            window.location.href = 'index.html';
        });
    } else {
        Swal.fire({
            title: 'Error',
            text: 'Nombre de usuario o contraseña incorrectos',
            icon: 'error',
            confirmButtonText: 'Intentar nuevamente'
        });
    }
});

document.getElementById('registerBtn').addEventListener('click', (event) => {
    event.preventDefault();
    const username = document.getElementById('regUsername').value;
    const password = document.getElementById('regPassword').value;

    const storedUsers = JSON.parse(localStorage.getItem('users')) || [];
    const userExists = storedUsers.some(user => user.username === username);

    if (userExists) {
        Swal.fire({
            title: 'Error',
            text: 'El nombre de usuario ya está en uso',
            icon: 'error',
            confirmButtonText: 'Intentar nuevamente'
        });
    } else {
        storedUsers.push({ username: username, password: password });
        localStorage.setItem('users', JSON.stringify(storedUsers));
    Swal.fire({
        title: 'Registro exitoso',
        text: `Usuario ${username} registrado correctamente`,
        icon: 'success',
        confirmButtonText: 'Continuar'
    });
    showLogin();
}    
});
