// Sticky Navigation and Smooth Scrolling
document.addEventListener('DOMContentLoaded', function() {
    const stickyNav = document.getElementById('sticky-nav');
    const heroSection = document.querySelector('.hero');
    const navLinks = document.querySelectorAll('.nav-link');
    const mobileMenuToggle = document.getElementById('mobile-menu-toggle');
    const mobileMenu = document.getElementById('mobile-menu');
    const mobileNavLinks = document.querySelectorAll('.mobile-nav-link');
    
    // Mobile menu toggle
    if (mobileMenuToggle && mobileMenu) {
        mobileMenuToggle.addEventListener('click', function() {
            const isExpanded = mobileMenuToggle.getAttribute('aria-expanded') === 'true';
            mobileMenuToggle.classList.toggle('active');
            mobileMenu.classList.toggle('active');
            
            // Update aria-expanded attribute
            mobileMenuToggle.setAttribute('aria-expanded', !isExpanded);
            
            // Update aria-label based on state
            if (!isExpanded) {
                mobileMenuToggle.setAttribute('aria-label', 'Close navigation menu');
            } else {
                mobileMenuToggle.setAttribute('aria-label', 'Open navigation menu');
            }
        });
        
        // Close mobile menu when clicking on a link
        mobileNavLinks.forEach(link => {
            link.addEventListener('click', function() {
                mobileMenuToggle.classList.remove('active');
                mobileMenu.classList.remove('active');
                mobileMenuToggle.setAttribute('aria-expanded', 'false');
                mobileMenuToggle.setAttribute('aria-label', 'Open navigation menu');
            });
        });
        
        // Close mobile menu when clicking outside
        document.addEventListener('click', function(e) {
            if (!stickyNav.contains(e.target)) {
                mobileMenuToggle.classList.remove('active');
                mobileMenu.classList.remove('active');
                mobileMenuToggle.setAttribute('aria-expanded', 'false');
                mobileMenuToggle.setAttribute('aria-label', 'Open navigation menu');
            }
        });
    }
    
    // Throttle function for better performance
    function throttle(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
    
    // Combined scroll handler (throttled for performance)
    const handleScroll = throttle(() => {
        // Show/hide sticky navigation
        if (heroSection) {
            const heroBottom = heroSection.offsetTop + heroSection.offsetHeight;
            
            if (window.scrollY > heroBottom - 100) {
                stickyNav.classList.add('visible');
            } else {
                stickyNav.classList.remove('visible');
            }
        }
        
        // Update active navigation link
        updateActiveNavLink();
        
        // Subtle parallax effect for hero section (disabled on mobile for performance)
        if (window.innerWidth > 768) {
            const scrolled = window.pageYOffset;
            const hero = document.querySelector('.hero');
            if (hero && scrolled < hero.offsetHeight) {
                hero.style.transform = `translateY(${scrolled * 0.5}px)`;
            }
        }
    }, 16); // ~60fps
    
    window.addEventListener('scroll', handleScroll);
    
    // Smooth scrolling for anchor links with offset for sticky nav
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const target = document.querySelector(targetId);
            if (target) {
                const offset = 80; // Account for sticky nav height
                const targetPosition = target.offsetTop - offset;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
                
                // Close mobile menu if open
                if (mobileMenuToggle && mobileMenu) {
                    mobileMenuToggle.classList.remove('active');
                    mobileMenu.classList.remove('active');
                }
            }
        });
    });
    
    // Update active navigation link based on scroll position
    function updateActiveNavLink() {
        const sections = document.querySelectorAll('section[id]');
        const scrollPos = window.scrollY + 120; // Offset for sticky nav
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.offsetHeight;
            const sectionId = section.getAttribute('id');
            const navLink = document.querySelector(`.nav-link[href="#${sectionId}"]`);
            const mobileNavLink = document.querySelector(`.mobile-nav-link[href="#${sectionId}"]`);
            
            if (scrollPos >= sectionTop && scrollPos < sectionTop + sectionHeight) {
                // Remove active class from all nav links
                navLinks.forEach(link => link.classList.remove('active'));
                mobileNavLinks.forEach(link => link.classList.remove('active'));
                
                // Add active class to current nav links
                if (navLink) {
                    navLink.classList.add('active');
                }
                if (mobileNavLink) {
                    mobileNavLink.classList.add('active');
                }
            }
        });
    }
});

// Improved animation with Intersection Observer (better for mobile and content visibility)
const observerOptions = {
    threshold: 0.05, // Trigger when just 5% is visible
    rootMargin: '100px 0px 200px 0px' // Large margins to load content early
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            // Immediate animation - no delay
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
            entry.target.classList.add('animated');
        } else {
            // Keep content visible when scrolling back up
            // Only add subtle effect when moving out of view
            if (entry.boundingClientRect.top > window.innerHeight) {
                // Content is below viewport
                entry.target.style.opacity = '0.8';
                entry.target.style.transform = 'translateY(10px)';
            } else {
                // Content is above viewport - keep it fully visible
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        }
    });
}, observerOptions);

// Observe all sections for animation with better mobile handling
document.querySelectorAll('section').forEach((section, index) => {
    // Set initial state - content is visible but slightly offset
    section.style.opacity = '0.8'; // Start partially visible instead of completely hidden
    section.style.transform = 'translateY(10px)'; // Minimal offset
    section.style.transition = 'opacity 0.4s ease, transform 0.4s ease'; // Faster animation
    section.style.transitionDelay = `${index * 0.05}s`; // Faster stagger
    
    observer.observe(section);
});

// Fallback: Ensure all content is visible after page load
window.addEventListener('load', function() {
    setTimeout(() => {
        document.querySelectorAll('section').forEach(section => {
            if (section.style.opacity !== '1') {
                section.style.opacity = '1';
                section.style.transform = 'translateY(0)';
            }
        });
    }, 1000); // Give animations time to trigger naturally first
});

// Add hover effect to profile picture
const profilePic = document.getElementById('profile-pic');
if (profilePic) {
    profilePic.addEventListener('click', function() {
        // You can add a modal or lightbox here if you want
        console.log('Profile picture clicked!');
    });
}

// Dynamic year in footer
const currentYear = new Date().getFullYear();
const footerText = document.querySelector('footer p');
if (footerText) {
    footerText.innerHTML = footerText.innerHTML.replace('2025', currentYear);
}

// Add click tracking for project links (for analytics)
document.querySelectorAll('.project-links a').forEach(link => {
    link.addEventListener('click', function(e) {
        // Add your analytics tracking here
        console.log('Project link clicked:', this.textContent, this.href);
    });
});

// Simple form validation if you add a contact form later
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// Easter egg: Konami code (disabled on mobile for performance)
if (window.innerWidth > 768) {
    let konamiCode = [];
    const konami = [38, 38, 40, 40, 37, 39, 37, 39, 66, 65]; // ↑↑↓↓←→←→BA

    document.addEventListener('keydown', function(e) {
        konamiCode.push(e.keyCode);
        if (konamiCode.length > konami.length) {
            konamiCode.shift();
        }
        
        if (konamiCode.toString() === konami.toString()) {
            // Easter egg activated!
            document.body.style.transform = 'rotate(180deg)';
            setTimeout(() => {
                document.body.style.transform = 'rotate(0deg)';
            }, 2000);
            konamiCode = [];
        }
    });
}

// Add smooth transitions when page loads
window.addEventListener('load', function() {
    document.body.style.opacity = '1';
    document.body.style.transition = 'opacity 0.5s ease-in-out';
    console.log('About Me website loaded successfully! 🚀');
});
