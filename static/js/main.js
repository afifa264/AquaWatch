document.addEventListener('DOMContentLoaded', () => {
  const toggle = document.querySelector('.menu-toggle');
  const nav = document.querySelector('.nav-links');
  if (toggle && nav) toggle.addEventListener('click', () => nav.classList.toggle('nav-open'));
  document.querySelectorAll('.dismiss').forEach(button => button.addEventListener('click', () => button.closest('.flash').remove()));
  document.querySelectorAll('form').forEach(form => form.addEventListener('submit', () => {
    const submit = form.querySelector('button[type="submit"]');
    if (submit && form.checkValidity()) { submit.dataset.originalText = submit.innerHTML; submit.innerHTML = 'Please wait…'; }
  }));
});
