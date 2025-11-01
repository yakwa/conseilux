// Calcule dynamiquement la hauteur de l'entête et l'applique à la variable CSS
function updateHeaderOffset() {
    try {
        const header = document.querySelector('.header');
        if (!header) return;
        // Hauteur réelle de l'entête + petit tampon
        const buffer = 0; // px (tampon supprimé pour éliminer l'espace vide)
        const height = header.offsetHeight + buffer;
        document.documentElement.style.setProperty('--header-offset', `${height}px`);
    } catch (_) {}
}

// Fonction pour initialiser le menu mobile
function initMobileMenu() {
    const menuToggle = document.getElementById('mobile-menu');
    const navMenu = document.querySelector('.nav-menu');
    const navClose = document.querySelector('.nav-close');
    const navLinks = document.querySelectorAll('.nav-link');

    if (!menuToggle || !navMenu) {
        console.warn('Menu mobile non trouvé, tentative de réinitialisation...');
        return false;
    }

    // Toggle menu mobile
    menuToggle.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        menuToggle.classList.toggle('active');
        navMenu.classList.toggle('active');
        document.body.classList.toggle('no-scroll');
        
        // Amélioration pour l'accessibilité
        const isOpen = navMenu.classList.contains('active');
        menuToggle.setAttribute('aria-expanded', isOpen);
        navMenu.setAttribute('aria-hidden', !isOpen);
        
        // Recalculer la hauteur si le menu mobile s'ouvre
        updateHeaderOffset();
    });

    // Bouton de fermeture explicite dans le menu
    if (navClose) {
        navClose.addEventListener('click', (e) => {
            e.preventDefault();
            menuToggle.classList.remove('active');
            navMenu.classList.remove('active');
            document.body.classList.remove('no-scroll');
            menuToggle.setAttribute('aria-expanded', 'false');
            navMenu.setAttribute('aria-hidden', 'true');
        });
    }

    // Fermer le menu en cliquant à l'extérieur
    document.addEventListener('click', (e) => {
        if (!navMenu.contains(e.target) && !menuToggle.contains(e.target)) {
            menuToggle.classList.remove('active');
            navMenu.classList.remove('active');
            document.body.classList.remove('no-scroll');
            menuToggle.setAttribute('aria-expanded', 'false');
            navMenu.setAttribute('aria-hidden', 'true');
        }
    });

    // Fermer le menu avec la touche Escape
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && navMenu.classList.contains('active')) {
            menuToggle.classList.remove('active');
            navMenu.classList.remove('active');
            document.body.classList.remove('no-scroll');
            menuToggle.setAttribute('aria-expanded', 'false');
            navMenu.setAttribute('aria-hidden', 'true');
            menuToggle.focus();
        }
    });

    // Fermer le menu au clic sur un lien
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            if (window.innerWidth <= 768) {
                menuToggle.classList.remove('active');
                navMenu.classList.remove('active');
                document.body.classList.remove('no-scroll');
                menuToggle.setAttribute('aria-expanded', 'false');
                navMenu.setAttribute('aria-hidden', 'true');
            }
        });
    });

    return true;
}

// Attendre que le DOM soit chargé
document.addEventListener('DOMContentLoaded', function() {
    // Calcul initial de l'offset de l'entête
    updateHeaderOffset();

    // Initialiser le menu mobile
    if (!initMobileMenu()) {
        // Si l'initialisation échoue, réessayer après un délai
        setTimeout(initMobileMenu, 100);
    }

    // Recalculer à chaque redimensionnement (orientation mobile incluse)
    window.addEventListener('resize', () => {
        updateHeaderOffset();
    });

    // Recalculer après chargement complet (polices/images)
    window.addEventListener('load', () => {
        updateHeaderOffset();
        setTimeout(updateHeaderOffset, 50);
        setTimeout(updateHeaderOffset, 250);
    });

    // Recalculer quand les polices web sont prêtes (peut changer la hauteur du header)
    if (document.fonts && document.fonts.ready) {
        document.fonts.ready.then(() => {
            updateHeaderOffset();
        });
    }

    // Observer les changements de taille de l'entête (si le contenu se réorganise)
    try {
        const header = document.querySelector('.header');
        if (header && 'ResizeObserver' in window) {
            const ro = new ResizeObserver(() => updateHeaderOffset());
            ro.observe(header);
        }
    } catch (_) {}

    // Gestion des sous-menus sur mobile
    document.querySelectorAll('.has-submenu').forEach(item => {
        const link = item.querySelector('.nav-link');
        const submenu = item.querySelector('.megamenu, .submenu');
        if (link && submenu) {
            link.addEventListener('click', (e) => {
                if (window.innerWidth <= 768) {
                    e.preventDefault();
                    const expanded = item.classList.toggle('active');
                    submenu.classList.toggle('active', expanded);
                    link.setAttribute('aria-expanded', String(expanded));
                }
            });
        }
    });

    // Amélioration du scroll fluide
    function smoothScroll(target) {
        const element = document.querySelector(target);
        if (element) {
            const headerHeight = document.querySelector('.header')?.offsetHeight || 0;
            const targetPosition = element.offsetTop - headerHeight - 20;
            
            window.scrollTo({
                top: targetPosition,
                behavior: 'smooth'
            });
        }
    }

    // Appliquer le smooth scroll aux liens d'ancrage
    document.querySelectorAll('a[href^="#"]').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = this.getAttribute('href');
            if (target && target !== '#') {
                smoothScroll(target);
            }
        });
    });

    // Gestion "Lire la suite" sur les cartes événements
    document.addEventListener('click', (e) => {
        const link = e.target.closest('.event-read');
        if (!link) return;
        e.preventDefault();
        const body = link.closest('.event-body');
        if (!body) return;
        const more = body.querySelector('.event-more');
        if (!more) return;
        const isHidden = more.hasAttribute('hidden');
        if (isHidden) {
            more.removeAttribute('hidden');
            link.textContent = 'Lire moins';
        } else {
            more.setAttribute('hidden', '');
            link.textContent = 'Lire la suite';
        }
    });

    // Gestion des images manquantes (partenaires et certifications)
    function handleImageError(img) {
        const isPartner = img.src.includes('images/');
        const isCertification = img.src.includes('logos/');
        
        if (isPartner || isCertification) {
            // Extraire le nom du fichier sans extension
            const fileName = img.src.split('/').pop().split('.')[0];
            const displayName = fileName.replace(/[-_]/g, ' ').toUpperCase();
            
            // Créer un SVG de remplacement
            const svgContent = isPartner 
                ? `<svg width="120" height="60" xmlns="http://www.w3.org/2000/svg">
                     <rect width="120" height="60" fill="#f8f9fa" stroke="#e9ecef" stroke-width="1" rx="8"/>
                     <text x="60" y="35" font-family="Arial, sans-serif" font-size="10" font-weight="bold" text-anchor="middle" fill="#495057">${displayName}</text>
                   </svg>`
                : `<svg width="100" height="80" xmlns="http://www.w3.org/2000/svg">
                     <rect width="100" height="80" fill="#4169e1" stroke="#2740d1" stroke-width="2" rx="8"/>
                     <text x="50" y="45" font-family="Arial, sans-serif" font-size="9" font-weight="bold" text-anchor="middle" fill="white">${displayName}</text>
                   </svg>`;
            
            // Convertir le SVG en data URL
            const svgDataUrl = 'data:image/svg+xml;base64,' + btoa(svgContent);
            img.src = svgDataUrl;
            img.style.backgroundColor = '#f8f9fa';
            img.style.border = '1px solid #e9ecef';
            img.style.borderRadius = '8px';
            img.style.padding = '5px';
        }
    }

    // Désactivé temporairement pour permettre l'affichage des vraies images
    // document.querySelectorAll('img[src*="images/"], img[src*="logos/"]').forEach(img => {
    //     img.addEventListener('error', () => handleImageError(img));
    //     
    //     // Vérifier si l'image est déjà cassée
    //     if (!img.complete || img.naturalHeight === 0) {
    //         handleImageError(img);
    //     }
    // });

    // Observer désactivé temporairement pour permettre l'affichage des vraies images
    // const imageObserver = new MutationObserver((mutations) => {
    //     mutations.forEach((mutation) => {
    //         mutation.addedNodes.forEach((node) => {
    //             if (node.nodeType === 1) { // Element node
    //                 const images = node.querySelectorAll ? node.querySelectorAll('img[src*="images/"], img[src*="logos/"]') : [];
    //                 images.forEach(img => {
    //                     img.addEventListener('error', () => handleImageError(img));
    //                     if (!img.complete || img.naturalHeight === 0) {
    //                         handleImageError(img);
    //                     }
    //                 });
    //             }
    //         });
    //     });
    // });

    // // Observer les changements dans le DOM
    // imageObserver.observe(document.body, {
    //     childList: true,
    //     subtree: true
    // });

    // ========== LAZY LOADING DES IMAGES ==========
    // Améliore les performances en chargeant les images uniquement quand elles sont visibles
    function initLazyLoading() {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    
                    // Charger l'image
                    if (img.dataset.src) {
                        img.src = img.dataset.src;
                        img.removeAttribute('data-src');
                    }
                    
                    // Charger le background-image
                    if (img.dataset.bg) {
                        img.style.backgroundImage = `url('${img.dataset.bg}')`;
                        img.removeAttribute('data-bg');
                    }
                    
                    // Ajouter une classe pour les animations
                    img.classList.add('loaded');
                    
                    // Arrêter d'observer cette image
                    observer.unobserve(img);
                }
            });
        }, {
            rootMargin: '50px' // Charger 50px avant que l'image soit visible
        });

        // Observer toutes les images avec data-src ou data-bg
        document.querySelectorAll('img[data-src], [data-bg]').forEach(img => {
            imageObserver.observe(img);
        });
    }

    // Initialiser le lazy loading si le navigateur supporte IntersectionObserver
    if ('IntersectionObserver' in window) {
        initLazyLoading();
    } else {
        // Fallback pour les anciens navigateurs : charger toutes les images immédiatement
        document.querySelectorAll('img[data-src]').forEach(img => {
            img.src = img.dataset.src;
        });
        document.querySelectorAll('[data-bg]').forEach(el => {
            el.style.backgroundImage = `url('${el.dataset.bg}')`;
        });
    }

}); // Fin de DOMContentLoaded
