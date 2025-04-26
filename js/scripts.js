// Ensure DOM is fully loaded before running scripts
document.addEventListener('DOMContentLoaded', () => {
    // Mobile Menu Toggle
    const mobileToggle = document.querySelector('.mobile-toggle');
    const navMenu = document.querySelector('.nav-menu');

    if (!mobileToggle || !navMenu) {
        console.error('Mobile menu elements not found. Check .mobile-toggle and .nav-menu in the HTML.');
        return;
    }

    // Toggle menu on click or touch
    const toggleMenu = () => {
        navMenu.classList.toggle('active');
    };

    mobileToggle.addEventListener('click', toggleMenu);
    mobileToggle.addEventListener('touchstart', (e) => {
        e.preventDefault(); // Prevent default touch behavior
        toggleMenu();
    });

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 80,
                    behavior: 'smooth'
                });
                
                // Close mobile menu if open
                navMenu.classList.remove('active');
            }
        });
    });
});