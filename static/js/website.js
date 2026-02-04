document.getElementById('menu-btn').addEventListener('click', () => {
    document.getElementById('mobile-menu').classList.toggle('hidden');
});

const privacyCheckbox = document.getElementById('privacy-policy');
const submitBtn = document.getElementById('submit-btn');

if (privacyCheckbox && submitBtn) {
    privacyCheckbox.addEventListener('change', function() {
        submitBtn.disabled = !this.checked;
    });
}

const testimonialsTrack = document.getElementById('testimonials-track');
const prevBtn = document.getElementById('testimonials-prev');
const nextBtn = document.getElementById('testimonials-next');
const dots = document.querySelectorAll('.testimonial-dot');
let currentIndex = 0;
const totalSlides = 3;

function updateCarousel() {
    const offset = -currentIndex * 100;
    testimonialsTrack.style.transform = `translateX(${offset}%)`;
    
    dots.forEach((dot, index) => {
        if (index === currentIndex) {
            dot.style.backgroundColor = '#dbc693';
        } else {
            dot.style.backgroundColor = '#d1d5db';
        }
    });
}

if (prevBtn) {
    prevBtn.addEventListener('click', () => {
        currentIndex = (currentIndex - 1 + totalSlides) % totalSlides;
        updateCarousel();
    });
}

if (nextBtn) {
    nextBtn.addEventListener('click', () => {
        currentIndex = (currentIndex + 1) % totalSlides;
        updateCarousel();
    });
}

dots.forEach(dot => {
    dot.addEventListener('click', () => {
        currentIndex = parseInt(dot.getAttribute('data-index'));
        updateCarousel();
    });
});

const filterBtns = document.querySelectorAll('.filter-btn');
const portfolioItems = document.querySelectorAll('.portfolio-item');

filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        filterBtns.forEach(b => {
            b.style.backgroundColor = 'transparent';
            b.style.borderColor = 'black';
            b.classList.remove('text-white');
            b.classList.add('text-black');
        });
        btn.style.backgroundColor = '#dbc693';
        btn.style.borderColor = '#dbc693';
        btn.classList.remove('text-black');
        btn.classList.add('text-white');
        
        const filter = btn.getAttribute('data-filter');
        portfolioItems.forEach(item => {
            if (filter === 'all' || item.getAttribute('data-category') === filter) {
                item.style.display = 'block';
            } else {
                item.style.display = 'none';
            }
        });
    });
});

document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    });
});

const navbar = document.getElementById('navbar');
const logoMain = document.getElementById('logo-main');
const logoSub = document.getElementById('logo-sub');
const navLinks = document.querySelectorAll('.nav-link');
const menuIcon = document.querySelector('.menu-icon');
const heroSection = document.getElementById('inicio');

window.addEventListener('scroll', function() {
    const heroHeight = heroSection.offsetHeight;
    
    if (window.scrollY > heroHeight - 100) {
        navbar.classList.add('bg-white', 'shadow-md');
        navbar.classList.remove('bg-transparent');
        logoMain.style.color = '#dbc693';
        logoSub.classList.remove('text-gray-300');
        logoSub.classList.add('text-gray-900');
        navLinks.forEach(link => {
            link.classList.remove('text-white');
            link.classList.add('text-gray-900');
        });
        if (menuIcon) {
            menuIcon.classList.remove('text-white');
            menuIcon.classList.add('text-gray-900');
        }
    } else {
        navbar.classList.remove('bg-white', 'shadow-md');
        navbar.classList.add('bg-transparent');
        logoMain.style.color = '';
        logoMain.classList.add('text-white');
        logoSub.classList.add('text-gray-300');
        logoSub.classList.remove('text-gray-900');
        navLinks.forEach(link => {
            link.classList.add('text-white');
            link.classList.remove('text-gray-900');
        });
        if (menuIcon) {
            menuIcon.classList.add('text-white');
            menuIcon.classList.remove('text-gray-900');
        }
    }
});

// ========================================
// LANGUAGE SELECTOR
// ========================================

// Function to get current language from localStorage or URL
function getCurrentLanguage() {
    // Check localStorage first
    const savedLang = localStorage.getItem('preferredLanguage');
    if (savedLang) {
        return savedLang;
    }
    
    // Check URL parameter
    const urlParams = new URLSearchParams(window.location.search);
    const urlLang = urlParams.get('lang');
    if (urlLang) {
        return urlLang;
    }
    
    // Default to Portuguese
    return 'pt';
}

// Function to change language
function changeLanguage(lang) {
    // Save to localStorage
    localStorage.setItem('preferredLanguage', lang);
    
    // Reload page with language parameter
    const url = new URL(window.location.href);
    url.searchParams.set('lang', lang);
    window.location.href = url.toString();
}

// Set initial language on page load
document.addEventListener('DOMContentLoaded', function() {
    const currentLang = getCurrentLanguage();
    
    // Set desktop selector
    const desktopSelector = document.getElementById('language-selector');
    if (desktopSelector) {
        desktopSelector.value = currentLang;
        
        desktopSelector.addEventListener('change', function() {
            changeLanguage(this.value);
        });
    }
    
    // Set mobile selector
    const mobileSelector = document.getElementById('language-selector-mobile');
    if (mobileSelector) {
        mobileSelector.value = currentLang;
        
        mobileSelector.addEventListener('change', function() {
            changeLanguage(this.value);
        });
    }
    
    // If language is set in localStorage but not in URL, update URL
    if (localStorage.getItem('preferredLanguage') && !new URLSearchParams(window.location.search).get('lang')) {
        const url = new URL(window.location.href);
        url.searchParams.set('lang', currentLang);
        window.history.replaceState({}, '', url.toString());
    }
});
