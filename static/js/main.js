/**
* Template Name: Yummy
* Template URL: https://bootstrapmade.com/yummy-bootstrap-restaurant-website-template/
* Updated: Aug 07 2024 with Bootstrap v5.3.3
* Author: BootstrapMade.com
* License: https://bootstrapmade.com/license/
*/

(function() {
  "use strict";

  /**
   * Apply .scrolled class to the body as the page is scrolled down
   */
  function toggleScrolled() {
    const selectBody = document.querySelector('body');
    const selectHeader = document.querySelector('#header');
    if (!selectHeader.classList.contains('scroll-up-sticky') && !selectHeader.classList.contains('sticky-top') && !selectHeader.classList.contains('fixed-top')) return;
    window.scrollY > 100 ? selectBody.classList.add('scrolled') : selectBody.classList.remove('scrolled');
  }

  document.addEventListener('scroll', toggleScrolled);
  window.addEventListener('load', toggleScrolled);

  /**
   * Mobile nav toggle
   */
  const mobileNavToggleBtn = document.querySelector('.mobile-nav-toggle');

  function mobileNavToogle() {
    document.querySelector('body').classList.toggle('mobile-nav-active');
    mobileNavToggleBtn.classList.toggle('bi-list');
    mobileNavToggleBtn.classList.toggle('bi-x');
  }
  mobileNavToggleBtn.addEventListener('click', mobileNavToogle);

  /**
   * Hide mobile nav on same-page/hash links
   */
  document.querySelectorAll('#navmenu a').forEach(navmenu => {
    navmenu.addEventListener('click', () => {
      if (document.querySelector('.mobile-nav-active')) {
        mobileNavToogle();
      }
    });

  });

  /**
   * Toggle mobile nav dropdowns
   */
  document.querySelectorAll('.navmenu .toggle-dropdown').forEach(navmenu => {
    navmenu.addEventListener('click', function(e) {
      e.preventDefault();
      this.parentNode.classList.toggle('active');
      this.parentNode.nextElementSibling.classList.toggle('dropdown-active');
      e.stopImmediatePropagation();
    });
  });

  /**
   * Preloader
   */
  const preloader = document.querySelector('#preloader');
  if (preloader) {
    window.addEventListener('load', () => {
      preloader.remove();
    });
  }

  /**
   * Scroll top button
   */
  let scrollTop = document.querySelector('.scroll-top');

  function toggleScrollTop() {
    if (scrollTop) {
      window.scrollY > 100 ? scrollTop.classList.add('active') : scrollTop.classList.remove('active');
    }
  }
  scrollTop.addEventListener('click', (e) => {
    e.preventDefault();
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    });
  });

  window.addEventListener('load', toggleScrollTop);
  document.addEventListener('scroll', toggleScrollTop);

  /**
   * Animation on scroll function and init
   */
  function aosInit() {
    AOS.init({
      duration: 600,
      easing: 'ease-in-out',
      once: true,
      mirror: false
    });
  }
  window.addEventListener('load', aosInit);

  /**
   * Initiate glightbox
   */
  const glightbox = GLightbox({
    selector: '.glightbox'
  });

  /**
   * Initiate Pure Counter
   */
  new PureCounter();

  /**
   * Init swiper sliders
   */
  function initSwiper() {
    document.querySelectorAll(".init-swiper").forEach(function(swiperElement) {
      let config = JSON.parse(
        swiperElement.querySelector(".swiper-config").innerHTML.trim()
      );

      if (swiperElement.classList.contains("swiper-tab")) {
        initSwiperWithCustomPagination(swiperElement, config);
      } else {
        new Swiper(swiperElement, config);
      }
    });
  }

  window.addEventListener("load", initSwiper);

  /**
   * Correct scrolling position upon page load for URLs containing hash links.
   */
  window.addEventListener('load', function(e) {
    if (window.location.hash) {
      if (document.querySelector(window.location.hash)) {
        setTimeout(() => {
          let section = document.querySelector(window.location.hash);
          let scrollMarginTop = getComputedStyle(section).scrollMarginTop;
          window.scrollTo({
            top: section.offsetTop - parseInt(scrollMarginTop),
            behavior: 'smooth'
          });
        }, 100);
      }
    }
  });

  /**
   * Navmenu Scrollspy
   */
  let navmenulinks = document.querySelectorAll('.navmenu a');

  function navmenuScrollspy() {
    navmenulinks.forEach(navmenulink => {
      if (!navmenulink.hash) return;
      let section = document.querySelector(navmenulink.hash);
      if (!section) return;
      let position = window.scrollY + 200;
      if (position >= section.offsetTop && position <= (section.offsetTop + section.offsetHeight)) {
        document.querySelectorAll('.navmenu a.active').forEach(link => link.classList.remove('active'));
        navmenulink.classList.add('active');
      } else {
        navmenulink.classList.remove('active');
      }
    })
  }
  window.addEventListener('load', navmenuScrollspy);
  document.addEventListener('scroll', navmenuScrollspy);


  /**
 * Why Us scroll-driven cards
 */
function initWhyUsScroll() {
  const section = document.querySelector('#why-us');

  if (!section) return;

  const sticky = section.querySelector('.why-sticky');
  const cards = section.querySelectorAll('.why-card');

  if (!sticky || !cards.length) return;

  let ticking = false;

  function clamp(value, min, max) {
    return Math.min(Math.max(value, min), max);
  }

  function updateCards() {
    ticking = false;

    if (window.innerWidth < 992) {
      return;
    }

    const sectionRect = section.getBoundingClientRect();
    const stickyRect = sticky.getBoundingClientRect();

    /*
     * Calculate how far the sticky section has progressed.
     *
     * 0 = first card
     * 1 = last card
     */
    const scrollDistance =
      sectionRect.height - stickyRect.height;

    if (scrollDistance <= 0) return;

    const stickyTop = parseFloat(
      getComputedStyle(sticky).top
    ) || 0;

    const progress = clamp(
      (stickyTop - sectionRect.top) / scrollDistance,
      0,
      1
    );

    /*
     * Convert section progress into card progress.
     *
     * 0 -> Card 1
     * 1 -> Card 2
     * 2 -> Card 3
     */
    const cardProgress = progress * (cards.length - 1);

    cards.forEach((card, index) => {
      const distance = index - cardProgress;
      const absoluteDistance = Math.abs(distance);

      /*
       * Each card independently moves through the viewport.
       */
      const offset = distance * 105;

      /*
       * Fade cards as they move away from the active position.
       */
      const opacity = clamp(
        1 - absoluteDistance * 1.35,
        0,
        1
      );

      const scale = 1 - Math.min(
        absoluteDistance,
        1
      ) * 0.035;

      card.style.setProperty(
        '--card-offset',
        offset
      );

      card.style.setProperty(
        '--card-opacity',
        opacity
      );

      card.style.transform =
        `translate3d(0, ${offset}%, 0) scale(${scale})`;

      card.style.zIndex =
        String(100 - Math.round(absoluteDistance * 10));

      card.setAttribute(
        'aria-hidden',
        absoluteDistance > 0.75 ? 'true' : 'false'
      );
    });
  }

  function requestUpdate() {
    if (ticking) return;

    ticking = true;

    requestAnimationFrame(updateCards);
  }

  window.addEventListener('scroll', requestUpdate, {
    passive: true
  });

  window.addEventListener('resize', requestUpdate);

  updateCards();
}

window.addEventListener('load', initWhyUsScroll);

})();