document.addEventListener('DOMContentLoaded', () => {
    // Smooth scrolling for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                const headerOffset = 80;
                const elementPosition = target.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.scrollY - headerOffset;
                
                window.scrollTo({
                    top: offsetPosition,
                    behavior: "smooth"
                });
            }
        });
    });

    // Intersection Observer for scroll animations
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('is-visible');
                observer.unobserve(entry.target); // Only animate once
            }
        });
    }, observerOptions);

    // Observe all elements with animation classes
    document.querySelectorAll('.fade-in, .slide-up').forEach((el) => {
        observer.observe(el);
    });
    
    // Add 3D tilt effect to the code window
    const codeWindow = document.querySelector('.code-window');
    const heroVisual = document.querySelector('.hero-visual');
    
    if (codeWindow && heroVisual) {
        heroVisual.addEventListener('mousemove', (e) => {
            const rect = heroVisual.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            
            const rotateX = ((y - centerY) / centerY) * -10;
            const rotateY = ((x - centerX) / centerX) * 10;
            
            codeWindow.style.transform = `rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
            codeWindow.style.transition = 'transform 0.1s ease';
        });
        
        heroVisual.addEventListener('mouseleave', () => {
            codeWindow.style.transform = `rotateX(5deg) rotateY(-5deg)`;
            codeWindow.style.transition = 'transform 0.5s ease';
        });
    }
});
