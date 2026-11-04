/**
 * MEHÂFETULLÂH (ALLAH KORKUSU) - E-Book Application Logic
 * Abdülkâdir Geylânî (k.s.)
 */

(function () {
  'use strict';

  // Global App State
  const state = {
    db: null,
    currentPage: 1,
    totalPages: 121,
    theme: 'sepia',
    fontSize: 18,
    fontFamily: 'serif',
    textAlign: 'justify',
    observer: null,
    isManualScroll: false
  };

  // DOM Elements
  const elements = {
    viewport: document.getElementById('readerViewport'),
    progressBar: document.getElementById('readingProgressBar'),
    pageBadge: document.getElementById('currentPageBadge'),
    chapterPreview: document.getElementById('chapterPreview'),
    btnPrev: document.getElementById('btnPrevPage'),
    btnNext: document.getElementById('btnNextPage'),
    btnJumpIndicator: document.getElementById('btnJumpIndicator'),
    
    // Drawers & Modals
    tocDrawer: document.getElementById('tocDrawerBackdrop'),
    settingsDrawer: document.getElementById('settingsDrawerBackdrop'),
    jumpModal: document.getElementById('jumpModalBackdrop'),
    searchModal: document.getElementById('searchModalBackdrop'),
    
    // Controls inside TOC
    tocList: document.getElementById('tocList'),
    tocSearch: document.getElementById('tocSearchInput'),
    
    // Controls inside Jump Modal
    jumpSlider: document.getElementById('jumpSlider'),
    jumpPageDisplay: document.getElementById('jumpPageDisplay'),
    jumpTitlePreview: document.getElementById('jumpTitlePreview'),
    btnConfirmJump: document.getElementById('btnConfirmJump'),
    
    // Controls inside Search Modal
    searchInput: document.getElementById('searchInput'),
    searchResults: document.getElementById('searchResultsList'),
    
    // Controls inside Settings
    fontSizeDisplay: document.getElementById('fontSizeDisplay'),
    btnFontDec: document.getElementById('btnFontDec'),
    btnFontInc: document.getElementById('btnFontInc')
  };

  // 1. Initialization
  function init() {
    // Load Database
    if (window.BOOK_DATABASE) {
      state.db = window.BOOK_DATABASE;
    } else {
      console.error('BOOK_DATABASE not loaded!');
      return;
    }

    state.totalPages = state.db.meta.total_pages || 121;

    // Load persisted settings
    loadSettings();

    // Render all 121 pages
    renderBookPages();

    // Populate TOC Drawer
    renderTOCDrawer();

    // Setup Intersection Observer for scrolling
    setupScrollObserver();

    // Setup Event Listeners
    setupEventListeners();

    // Register Service Worker
    registerSW();

    // Restore last read position
    const savedPage = parseInt(localStorage.getItem('mehafetullah_last_page') || '1', 10);
    if (savedPage > 1 && savedPage <= state.totalPages) {
      setTimeout(() => {
        goToPage(savedPage, false);
      }, 200);
    } else {
      updateHeaderIndicator(1);
    }
  }

  // 2. Settings Management
  function loadSettings() {
    const savedTheme = localStorage.getItem('mehafetullah_theme') || 'sepia';
    const savedFontSize = parseInt(localStorage.getItem('mehafetullah_font_size') || '18', 10);
    const savedFontFamily = localStorage.getItem('mehafetullah_font_family') || 'serif';
    const savedAlign = localStorage.getItem('mehafetullah_text_align') || 'justify';

    setTheme(savedTheme, false);
    setFontSize(savedFontSize, false);
    setFontFamily(savedFontFamily, false);
    setTextAlign(savedAlign, false);
  }

  function setTheme(theme, save = true) {
    state.theme = theme;
    document.body.setAttribute('data-theme', theme);
    document.querySelectorAll('.theme-card-btn').forEach(btn => {
      btn.classList.toggle('active', btn.getAttribute('data-theme') === theme);
    });
    if (save) localStorage.setItem('mehafetullah_theme', theme);
  }

  function setFontSize(size, save = true) {
    state.fontSize = Math.min(28, Math.max(14, size));
    document.documentElement.style.setProperty('--reader-font-size', `${state.fontSize}px`);
    if (elements.fontSizeDisplay) {
      elements.fontSizeDisplay.textContent = `${state.fontSize}px`;
    }
    if (save) localStorage.setItem('mehafetullah_font_size', state.fontSize);
  }

  function setFontFamily(font, save = true) {
    state.fontFamily = font;
    const fontValue = font === 'sans' ? 'var(--font-sans)' : 'var(--font-serif)';
    document.documentElement.style.setProperty('--reader-font', fontValue);
    document.querySelectorAll('.font-family-btn').forEach(btn => {
      btn.classList.toggle('active', btn.getAttribute('data-font') === font);
    });
    if (save) localStorage.setItem('mehafetullah_font_family', font);
  }

  function setTextAlign(align, save = true) {
    state.textAlign = align;
    document.documentElement.style.setProperty('--reader-text-align', align);
    if (save) localStorage.setItem('mehafetullah_text_align', align);
  }

  // 3. Render Book Pages
  function renderBookPages() {
    const container = elements.viewport;
    container.innerHTML = '';

    const fragment = document.createDocumentFragment();

    state.db.pages.forEach(p => {
      const card = document.createElement('article');
      card.className = 'page-card';
      card.id = `page-${p.page}`;
      card.setAttribute('data-page', p.page);
      card.setAttribute('data-title', p.title);

      const header = document.createElement('div');
      header.className = 'page-card-header';
      header.innerHTML = `
        <span class="page-card-title">${escapeHTML(p.title)}</span>
        <span class="page-card-num">Sayfa ${p.page} / ${state.totalPages}</span>
      `;

      const body = document.createElement('div');
      body.className = 'page-card-body';
      body.innerHTML = p.content_html;

      card.appendChild(header);
      card.appendChild(body);
      fragment.appendChild(card);
    });

    container.appendChild(fragment);
  }

  // 4. Render Table of Contents in Drawer
  function renderTOCDrawer() {
    const list = elements.tocList;
    list.innerHTML = '';

    const fragment = document.createDocumentFragment();

    // First add special quick links
    const specials = [
      { title: 'Kapak', page: 1 },
      { title: 'Künye & Yayın Bilgileri', page: 3 },
      { title: 'İçindekiler Fihristi', page: 6 },
      { title: "Abdülkâdir Geylânî'nin Hayatı", page: 10 }
    ];

    specials.forEach(s => {
      const item = document.createElement('li');
      item.className = 'toc-drawer-item';
      item.innerHTML = `
        <span class="toc-drawer-title">📌 ${s.title}</span>
        <span class="toc-drawer-page">S. ${s.page}</span>
      `;
      item.addEventListener('click', () => {
        goToPage(s.page);
        closeAllDrawers();
      });
      fragment.appendChild(item);
    });

    // Divider
    const divider = document.createElement('li');
    divider.className = 'toc-drawer-divider';
    divider.style.padding = '8px 12px';
    divider.style.fontSize = '11px';
    divider.style.fontWeight = '700';
    divider.style.color = 'var(--text-muted)';
    divider.style.letterSpacing = '1px';
    divider.textContent = 'KİTAP BÖLÜM VE BAŞLIKLARI (76 KONU)';
    fragment.appendChild(divider);

    // Add all 69 TOC topics
    state.db.toc.forEach(t => {
      const item = document.createElement('li');
      item.className = 'toc-drawer-item';
      item.setAttribute('data-search', t.title.toLowerCase());
      item.innerHTML = `
        <span class="toc-drawer-title">❦ ${escapeHTML(t.title)}</span>
        <span class="toc-drawer-page">S. ${t.pdf_page}</span>
      `;
      item.addEventListener('click', () => {
        goToPage(t.pdf_page);
        closeAllDrawers();
      });
      fragment.appendChild(item);
    });

    list.appendChild(fragment);
  }

  // 5. Scroll Observer for Live Header Updates
  function setupScrollObserver() {
    const options = {
      root: null,
      rootMargin: '-20% 0px -70% 0px',
      threshold: 0
    };

    state.observer = new IntersectionObserver((entries) => {
      if (state.isManualScroll) return;

      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const pageNum = parseInt(entry.target.getAttribute('data-page'), 10);
          const pageTitle = entry.target.getAttribute('data-title');
          updateHeaderIndicator(pageNum, pageTitle);
        }
      });
    }, options);

    document.querySelectorAll('.page-card').forEach(card => {
      state.observer.observe(card);
    });

    // Scroll progress bar
    window.addEventListener('scroll', () => {
      const winScroll = document.documentElement.scrollTop || document.body.scrollTop;
      const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
      const scrolled = height > 0 ? (winScroll / height) * 100 : 0;
      if (elements.progressBar) {
        elements.progressBar.style.width = `${scrolled}%`;
      }
    }, { passive: true });
  }

  // 6. Navigation Logic
  function updateHeaderIndicator(pageNum, title) {
    state.currentPage = pageNum;
    localStorage.setItem('mehafetullah_last_page', pageNum);

    const titleText = title || (state.db.pages[pageNum - 1] ? state.db.pages[pageNum - 1].title : `Sayfa ${pageNum}`);

    if (elements.pageBadge) {
      elements.pageBadge.textContent = `Sayfa ${pageNum} / ${state.totalPages}`;
    }
    if (elements.chapterPreview) {
      elements.chapterPreview.textContent = titleText;
    }
    if (elements.btnJumpIndicator) {
      elements.btnJumpIndicator.textContent = `Sayfa ${pageNum} / ${state.totalPages}`;
    }

    if (elements.btnPrev) elements.btnPrev.disabled = pageNum <= 1;
    if (elements.btnNext) elements.btnNext.disabled = pageNum >= state.totalPages;

    // Highlight active item in TOC drawer
    document.querySelectorAll('.toc-drawer-item').forEach(el => {
      const p = parseInt(el.querySelector('.toc-drawer-page')?.textContent.replace(/\D/g, '') || '0', 10);
      el.classList.toggle('active', p === pageNum);
    });
  }

  function goToPage(pageNum, smooth = true) {
    const targetNum = Math.min(state.totalPages, Math.max(1, pageNum));
    const targetEl = document.getElementById(`page-${targetNum}`);

    if (targetEl) {
      state.isManualScroll = true;
      const topOffset = targetEl.getBoundingClientRect().top + window.pageYOffset - 66;

      window.scrollTo({
        top: Math.max(0, topOffset),
        behavior: smooth ? 'smooth' : 'auto'
      });

      updateHeaderIndicator(targetNum);

      setTimeout(() => {
        state.isManualScroll = false;
      }, 600);
    }
  }

  window.goToPage = goToPage; // Export for inline onclicks

  // 7. Modals and Drawers
  function openDrawer(drawer) {
    if (!drawer) return;
    closeAllDrawers();
    drawer.classList.add('active');
    document.body.style.overflow = 'hidden';
  }

  function closeAllDrawers() {
    [elements.tocDrawer, elements.settingsDrawer, elements.jumpModal, elements.searchModal].forEach(d => {
      if (d) d.classList.remove('active');
    });
    document.body.style.overflow = '';
  }

  function openJumpModal() {
    const slider = elements.jumpSlider;
    slider.min = 1;
    slider.max = state.totalPages;
    slider.value = state.currentPage;
    updateJumpPreview(state.currentPage);
    openDrawer(elements.jumpModal);
  }

  function updateJumpPreview(pageNum) {
    const p = Math.min(state.totalPages, Math.max(1, parseInt(pageNum, 10)));
    elements.jumpPageDisplay.textContent = `Sayfa ${p}`;
    const pageObj = state.db.pages[p - 1];
    elements.jumpTitlePreview.textContent = pageObj ? pageObj.title : `Mehâfetullâh — Sayfa ${p}`;
  }

  // 8. Full-Text Search
  function performSearch(query) {
    const list = elements.searchResults;
    list.innerHTML = '';

    const q = query.trim().toLowerCase();
    if (!q || q.length < 2) {
      list.innerHTML = '<div style="padding:20px; text-align:center; color:var(--text-muted);">Aramak istediğiniz kelimeyi giriniz (en az 2 harf)...</div>';
      return;
    }

    const results = [];
    const regex = new RegExp(`(${escapeRegex(q)})`, 'gi');

    state.db.pages.forEach(p => {
      const text = p.raw_text || '';
      const lower = text.toLowerCase();
      const idx = lower.indexOf(q);

      if (idx !== -1) {
        // Find snippet around index
        const start = Math.max(0, idx - 45);
        const end = Math.min(text.length, idx + q.length + 55);
        let snippet = text.substring(start, end).replace(/\s+/g, ' ');

        if (start > 0) snippet = '...' + snippet;
        if (end < text.length) snippet = snippet + '...';

        const highlighted = escapeHTML(snippet).replace(regex, '<mark>$1</mark>');

        results.push({
          page: p.page,
          title: p.title,
          snippet: highlighted
        });
      }
    });

    if (results.length === 0) {
      list.innerHTML = `<div style="padding:24px; text-align:center; color:var(--text-muted);">"<strong>${escapeHTML(query)}</strong>" ifadesi bulunamadı.</div>`;
      return;
    }

    const fragment = document.createDocumentFragment();
    const countInfo = document.createElement('div');
    countInfo.style.padding = '4px 8px 12px';
    countInfo.style.fontSize = '12px';
    countInfo.style.fontWeight = 'bold';
    countInfo.style.color = 'var(--accent-color)';
    countInfo.textContent = `${results.length} sonuç bulundu:`;
    fragment.appendChild(countInfo);

    results.forEach(res => {
      const item = document.createElement('div');
      item.className = 'search-result-item';
      item.innerHTML = `
        <div class="search-result-header">
          <span>${escapeHTML(res.title)}</span>
          <span>Sayfa ${res.page}</span>
        </div>
        <div class="search-result-snippet">${res.snippet}</div>
      `;
      item.addEventListener('click', () => {
        closeAllDrawers();
        goToPage(res.page);
      });
      fragment.appendChild(item);
    });

    list.appendChild(fragment);
  }

  // 9. Event Listeners Setup
  function setupEventListeners() {
    // Header buttons
    document.getElementById('btnOpenTOC').addEventListener('click', () => openDrawer(elements.tocDrawer));
    document.getElementById('btnOpenSettings').addEventListener('click', () => openDrawer(elements.settingsDrawer));
    document.getElementById('btnOpenSearch').addEventListener('click', () => {
      openDrawer(elements.searchModal);
      setTimeout(() => elements.searchInput.focus(), 150);
    });
    document.getElementById('headerCenterBtn').addEventListener('click', openJumpModal);

    // Bottom Navigation buttons
    elements.btnPrev.addEventListener('click', () => goToPage(state.currentPage - 1));
    elements.btnNext.addEventListener('click', () => goToPage(state.currentPage + 1));
    elements.btnJumpIndicator.addEventListener('click', openJumpModal);

    // Close drawers via backdrop clicks
    document.querySelectorAll('.drawer-backdrop, .modal-center-backdrop').forEach(bd => {
      bd.addEventListener('click', (e) => {
        if (e.target === bd) closeAllDrawers();
      });
    });

    // Close buttons inside drawers/modals
    document.getElementById('btnCloseTOC').addEventListener('click', closeAllDrawers);
    document.getElementById('btnCloseSettings').addEventListener('click', closeAllDrawers);
    document.getElementById('btnCancelJump').addEventListener('click', closeAllDrawers);
    document.getElementById('btnCloseSearch').addEventListener('click', closeAllDrawers);

    // TOC Search Filter
    elements.tocSearch.addEventListener('input', (e) => {
      const val = e.target.value.toLowerCase().trim();
      document.querySelectorAll('#tocList .toc-drawer-item').forEach(item => {
        const text = item.textContent.toLowerCase();
        item.style.display = text.includes(val) ? 'flex' : 'none';
      });
    });

    // Jump Slider & Quick Buttons
    elements.jumpSlider.addEventListener('input', (e) => {
      updateJumpPreview(e.target.value);
    });

    elements.btnConfirmJump.addEventListener('click', () => {
      const p = parseInt(elements.jumpSlider.value, 10);
      closeAllDrawers();
      goToPage(p);
    });

    document.querySelectorAll('.quick-jump-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const p = parseInt(btn.getAttribute('data-page'), 10);
        elements.jumpSlider.value = p;
        updateJumpPreview(p);
      });
    });

    // Search Input
    let searchDebounce = null;
    elements.searchInput.addEventListener('input', (e) => {
      clearTimeout(searchDebounce);
      searchDebounce = setTimeout(() => {
        performSearch(e.target.value);
      }, 250);
    });

    // Theme selector buttons
    document.querySelectorAll('.theme-card-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        setTheme(btn.getAttribute('data-theme'));
      });
    });

    // Font size buttons
    elements.btnFontDec.addEventListener('click', () => setFontSize(state.fontSize - 1));
    elements.btnFontInc.addEventListener('click', () => setFontSize(state.fontSize + 1));

    // Font family buttons
    document.querySelectorAll('.font-family-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        setFontFamily(btn.getAttribute('data-font'));
      });
    });

    // Keyboard navigation (desktop / bluetooth keyboards)
    window.addEventListener('keydown', (e) => {
      if (document.body.style.overflow === 'hidden') {
        if (e.key === 'Escape') closeAllDrawers();
        return;
      }
      if (e.key === 'ArrowRight' || e.key === 'PageDown') {
        goToPage(state.currentPage + 1);
      } else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {
        goToPage(state.currentPage - 1);
      }
    });
  }

  // Helper functions
  function escapeHTML(str) {
    if (!str) return '';
    return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  function escapeRegex(str) {
    return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  }

  // Service Worker
  function registerSW() {
    if ('serviceWorker' in navigator) {
      window.addEventListener('load', () => {
        navigator.serviceWorker.register('./sw.js').catch(err => {
          console.log('SW registration note:', err);
        });
      });
    }
  }

  // Start app on DOMContentLoaded
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
