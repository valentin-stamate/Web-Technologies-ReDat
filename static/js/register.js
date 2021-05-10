
const registerForm = document.getElementById('register-form');

registerForm.addEventListener('submit', onRegister)

function onRegister(e) {
    e.preventDefault();

    const currentTarget = e.currentTarget;

    console.log(getFormData(currentTarget));
}