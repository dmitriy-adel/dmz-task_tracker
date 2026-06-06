function switchTab(tab) {
    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');
    const tabLogin = document.getElementById('tab-login');
    const tabRegister = document.getElementById('tab-register');

    if (tab === 'login') {
        loginForm.classList.remove('hidden');
        registerForm.classList.add('hidden');
        tabLogin.classList.add('active', 'border-[#44944A]');
        tabRegister.classList.remove('active', 'border-[#44944A]');
        tabLogin.classList.add('text-white');
        tabRegister.classList.remove('text-white');
        tabRegister.classList.add('text-zinc-400');
    } else {
        loginForm.classList.add('hidden');
        registerForm.classList.remove('hidden');
        tabRegister.classList.add('active', 'border-[#44944A]');
        tabLogin.classList.remove('active', 'border-[#44944A]');
        tabRegister.classList.add('text-white');
        tabLogin.classList.remove('text-white');
        tabLogin.classList.add('text-zinc-400');
    }
}

function togglePassword(inputId, button) {
    const input = document.getElementById(inputId);
    if (input.type === 'password') {
        input.type = 'text';
        button.textContent = '🙈';
    } else {
        input.type = 'password';
        button.textContent = '👁';
    }
}

function handleLogin(e) {
    e.preventDefault();
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;

    alert(`Вход выполнен!\nEmail: ${email}\n(Позже подключим к бэкенду)`);
}

function handleRegister(e) {
    e.preventDefault();
    
    const email = document.getElementById('reg-email').value;
    const username = document.getElementById('reg-username').value;
    const pass = document.getElementById('reg-password').value;
    const pass2 = document.getElementById('reg-password2').value;

    if (pass !== pass2) {
        alert('Пароли не совпадают!');
        return;
    }

    alert(`Регистрация успешна!\nEmail: ${email}\nИмя: ${username}\n(Позже сохраним в базу)`);
    switchTab('login');
}

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    if (loginForm) loginForm.classList.remove('hidden');
});
