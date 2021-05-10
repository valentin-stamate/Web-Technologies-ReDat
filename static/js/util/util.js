
export function getFormData(form) {
    return Object.fromEntries(new FormData(form));
}