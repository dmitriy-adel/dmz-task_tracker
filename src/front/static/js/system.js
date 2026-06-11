function showToast(message, duration = 2500, type = 'green') {
    const toast = document.getElementById('toast');
    const toastText = document.getElementById('toast-text');

    if (!toast || !toastText) {
        console.warn('Toast elements not found. Make sure you included system.html or added #toast manually.');
        return;
    }

    toast.classList.remove('toast-blue', 'toast-red');

    if (type === 'red') {
        toast.classList.add('toast-red');
    } else {
        toast.classList.add('toast-green');
    }

    toastText.textContent = message;
    toast.classList.add('show');

    setTimeout(() => {
        toast.classList.remove('show');
    }, duration);
}