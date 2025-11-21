document.addEventListener('DOMContentLoaded', function() {
    // Элементы
    const navbarToggle = document.querySelector('.navbar-toggle');
    const mobileMenu = document.querySelector('.mobile-menu');
    const userDropdown = document.querySelector('.user-dropdown');
    const userTrigger = document.querySelector('.user-trigger');
    const dropdownMenu = document.querySelector('.dropdown-menu');
    const mobileOverlay = document.createElement('div');

    // Создаем оверлей
    mobileOverlay.className = 'mobile-overlay';
    document.body.appendChild(mobileOverlay);

    // Переключение мобильного меню
    navbarToggle.addEventListener('click', function() {
        this.classList.toggle('active');
        mobileMenu.classList.toggle('active');
        mobileOverlay.classList.toggle('active');
        document.body.style.overflow = mobileMenu.classList.contains('active') ? 'hidden' : '';
    });

    // Закрытие мобильного меню по клику на оверлей
    mobileOverlay.addEventListener('click', function() {
        navbarToggle.classList.remove('active');
        mobileMenu.classList.remove('active');
        this.classList.remove('active');
        document.body.style.overflow = '';
    });

    // Выпадающее меню пользователя
    userTrigger.addEventListener('click', function(e) {
        e.stopPropagation();
        userDropdown.classList.toggle('active');
        dropdownMenu.classList.toggle('show');
    });

    // Закрытие выпадающего меню при клике вне его
    document.addEventListener('click', function() {
        userDropdown.classList.remove('active');
        dropdownMenu.classList.remove('show');
    });

    // Предотвращаем закрытие при клике внутри меню
    dropdownMenu.addEventListener('click', function(e) {
        e.stopPropagation();
    });

    // Адаптация к изменению размера окна
    window.addEventListener('resize', function() {
        if (window.innerWidth > 768) {
            navbarToggle.classList.remove('active');
            mobileMenu.classList.remove('active');
            mobileOverlay.classList.remove('active');
            document.body.style.overflow = '';
        }
    });
});