let currentEmail = '';

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

async function handleRegister(e) {
    e.preventDefault();

    const email = document.getElementById('reg-email').value.trim();
    const username = document.getElementById('reg-username').value.trim();
    const password = document.getElementById('reg-password').value;
    const password2 = document.getElementById('reg-password2').value;

    if (password !== password2) {
        alert('Пароли не совпадают!');
        return;
    }

    currentEmail = email;

    const submitBtn = e.target.querySelector('button[type="submit"]');
    const originalText = submitBtn.textContent;
    submitBtn.disabled = true;
    submitBtn.textContent = 'Отправка кода...';

    try {
        const response = await fetch('http://127.0.0.1:8001/send_vercode', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: email })
        });

        if (response.ok) {
            openVerificationModal(email);
        } else {
            const errorData = await response.json().catch(() => ({}));
            alert(errorData.detail || 'Не удалось отправить код подтверждения');
        }
    } catch (error) {
        console.error(error);
        alert('Ошибка соединения с сервером');

    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = originalText;
    }
}

function openVerificationModal(email) {
    const modal = document.getElementById('verification-modal');
    const emailSpan = document.getElementById('modal-email');
    emailSpan.textContent = email;

    modal.classList.remove('hidden');
    modal.classList.add('flex');

    const inputs = modal.querySelectorAll('.code-input');
    inputs.forEach(input => input.value = '');
    inputs[0].focus();
}

function closeVerificationModal() {
    const modal = document.getElementById('verification-modal');
    modal.classList.remove('flex');
    modal.classList.add('hidden');

    document.getElementById('verification-error').classList.add('hidden');
}

function setupCodeInputs() {
    const inputs = document.querySelectorAll('.code-input');

    inputs.forEach((input, index) => {
        input.addEventListener('input', () => {
            if (input.value.length === 1 && index < inputs.length - 1) {
                inputs[index + 1].focus();
            }
        });

        input.addEventListener('keydown', (e) => {
            if (e.key === 'Backspace' && input.value === '' && index > 0) {
                inputs[index - 1].focus();
            }
        });

        input.addEventListener('paste', (e) => {
            const pasteData = e.clipboardData.getData('text');
            if (pasteData.length === 4 && /^\d+$/.test(pasteData)) {
                e.preventDefault();
                inputs.forEach((inp, i) => inp.value = pasteData[i]);
                inputs[3].focus();
            }
        });
    });
}

async function submitVerificationCode() {
    const inputs = document.querySelectorAll('.code-input');
    const code = Array.from(inputs).map(input => input.value).join('');
    const errorEl = document.getElementById('verification-error');

    const username = document.getElementById('reg-username').value.trim();
    const password = document.getElementById('reg-password').value;

    if (code.length !== 4) {
        errorEl.textContent = 'Введите все 4 цифры кода';
        errorEl.classList.remove('hidden');
        return;
    }

    errorEl.classList.add('hidden');

    const confirmBtn = document.getElementById('confirm-btn');
    const originalText = confirmBtn.textContent;
    confirmBtn.disabled = true;
    confirmBtn.textContent = 'Проверка...';

    try {
        const response = await fetch('http://127.0.0.1:8001/check_vercode_and_add_user', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                user_email: currentEmail,
                user_name: username,
                user_pswd: password,
                verification_code: code
            })
        });

        const data = await response.json();

        if (response.ok && data.status) {
            closeVerificationModal();
            alert('Регистрация успешно завершена!');
            switchTab('login'); 
        } else {
            errorEl.textContent = data.detail || 'Неверный код подтверждения';
            errorEl.classList.remove('hidden');
        }
    } catch (error) {
        console.error(error);
        errorEl.textContent = 'Ошибка соединения с сервером';
        errorEl.classList.remove('hidden');
    } finally {
        confirmBtn.disabled = false;
        confirmBtn.textContent = originalText;
    }
}


document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    if (loginForm) loginForm.classList.remove('hidden');

    setupCodeInputs();
});
