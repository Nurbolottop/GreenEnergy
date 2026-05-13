// main.js — Green Energy

function getCookie(name) {
    let v = null;
    if (document.cookie) {
        document.cookie.split(';').forEach(c => {
            c = c.trim();
            if (c.startsWith(name + '=')) v = decodeURIComponent(c.substring(name.length + 1));
        });
    }
    return v;
}

document.addEventListener('DOMContentLoaded', () => {

    /* ===== THEME TOGGLE ===== */
    const saved = localStorage.getItem('ge-theme') || 'dark';
    document.documentElement.setAttribute('data-theme', saved);
    updateThemeIcons(saved);

    document.querySelectorAll('.theme-toggle').forEach(btn => {
        btn.addEventListener('click', () => {
            const cur = document.documentElement.getAttribute('data-theme') || 'dark';
            const next = cur === 'dark' ? 'light' : 'dark';
            document.documentElement.setAttribute('data-theme', next);
            localStorage.setItem('ge-theme', next);
            updateThemeIcons(next);
        });
    });

    function updateThemeIcons(theme) {
        document.querySelectorAll('.theme-toggle').forEach(btn => {
            btn.textContent = theme === 'dark' ? '☀️' : '🌙';
        });
    }

    /* ===== MOBILE DRAWER (Landing) ===== */
    const burger = document.getElementById('burger');
    const drawer = document.getElementById('mobileDrawer');
    const drawerOverlay = document.getElementById('drawerOverlay');

    function openDrawer() { if (drawer) drawer.classList.add('open'); }
    function closeDrawer() { if (drawer) drawer.classList.remove('open'); }

    if (burger) burger.addEventListener('click', openDrawer);
    if (drawerOverlay) drawerOverlay.addEventListener('click', closeDrawer);
    if (drawer) {
        drawer.querySelectorAll('a').forEach(a => a.addEventListener('click', closeDrawer));
    }

    /* ===== SIDEBAR (Dashboard) ===== */
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebarClose = document.getElementById('sidebarClose');
    const sidebar = document.getElementById('sidebar');
    const sidebarOverlay = document.getElementById('sidebarOverlay');

    function openSidebar() {
        if (sidebar) sidebar.classList.add('open');
        if (sidebarOverlay) sidebarOverlay.classList.add('active');
    }
    function closeSidebar() {
        if (sidebar) sidebar.classList.remove('open');
        if (sidebarOverlay) sidebarOverlay.classList.remove('active');
    }

    if (sidebarToggle) sidebarToggle.addEventListener('click', openSidebar);
    if (sidebarClose) sidebarClose.addEventListener('click', closeSidebar);
    if (sidebarOverlay) sidebarOverlay.addEventListener('click', closeSidebar);
    if (sidebar) {
        sidebar.querySelectorAll('.nav-item').forEach(l => {
            l.addEventListener('click', () => { if (window.innerWidth <= 1024) closeSidebar(); });
        });
    }

    /* ===== ESC CLOSE ===== */
    document.addEventListener('keydown', e => {
        if (e.key === 'Escape') { closeDrawer(); closeSidebar(); }
    });

    /* ===== FAQ ACCORDION ===== */
    document.querySelectorAll('.faq-item').forEach(item => {
        item.querySelector('.faq-q')?.addEventListener('click', () => {
            const wasOpen = item.classList.contains('open');
            document.querySelectorAll('.faq-item').forEach(i => i.classList.remove('open'));
            if (!wasOpen) item.classList.add('open');
        });
    });

    /* ===== TABS ===== */
    document.querySelectorAll('.tabs').forEach(tabGroup => {
        tabGroup.querySelectorAll('.tab').forEach(tab => {
            tab.addEventListener('click', () => {
                tabGroup.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
                tab.classList.add('active');
            });
        });
    });

    /* ===== LANGUAGE SWITCH (AJAX) ===== */
    document.querySelectorAll('.lang-btn').forEach(btn => {
        btn.addEventListener('click', e => {
            e.preventDefault();
            const lang = btn.dataset.lang;
            if (!lang || btn.classList.contains('active')) return;

            document.querySelectorAll('.lang-btn').forEach(b => b.classList.add('loading'));

            fetch('/set-language-ajax/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: JSON.stringify({ language: lang })
            })
            .then(r => r.json())
            .then(data => {
                if (data.success) {
                    const path = window.location.pathname;
                    const re = /^\/(ru|en|ky)\//;
                    if (re.test(path)) {
                        window.location.href = path.replace(re, `/${data.language}/`) + window.location.search;
                    } else {
                        window.location.reload();
                    }
                } else {
                    document.querySelectorAll('.lang-btn').forEach(b => b.classList.remove('loading'));
                }
            })
            .catch(() => {
                document.querySelectorAll('.lang-btn').forEach(b => b.classList.remove('loading'));
            });
        });
    });

    /* ===== POWER TOGGLE (mock) ===== */
    document.querySelectorAll('.power-toggle').forEach(toggle => {
        toggle.addEventListener('change', e => {
            const id = e.target.dataset.id;
            const dot = document.getElementById(`dot-${id}`);
            const label = document.getElementById(`plabel-${id}`);
            if (dot) dot.className = e.target.checked ? 'status-dot on' : 'status-dot off';
            if (label) label.textContent = e.target.checked ? 'Вкл' : 'Выкл';
        });
    });

    /* ===== CHART.JS (mock) ===== */
    const chartEl = document.getElementById('mainChart');
    if (chartEl && typeof Chart !== 'undefined') {
        const style = getComputedStyle(document.documentElement);
        new Chart(chartEl, {
            type: 'line',
            data: {
                labels: ['00:00','04:00','08:00','12:00','16:00','20:00','24:00'],
                datasets: [{
                    label: 'кВт⋅ч',
                    data: [1.2, 0.8, 3.5, 4.2, 3.8, 2.5, 1.5],
                    borderColor: '#00d084',
                    backgroundColor: 'rgba(0,208,132,0.08)',
                    borderWidth: 2, fill: true, tension: 0.4, pointRadius: 3
                }]
            },
            options: {
                responsive: true, maintainAspectRatio: false,
                scales: {
                    y: { grid: { color: 'rgba(255,255,255,0.04)' }, ticks: { color: '#8892a4' } },
                    x: { grid: { color: 'rgba(255,255,255,0.04)' }, ticks: { color: '#8892a4' } }
                },
                plugins: { legend: { labels: { color: '#8892a4' } } }
            }
        });
    }

    /* ===== SMOOTH SCROLL ===== */
    document.querySelectorAll('a[href^="#"]').forEach(a => {
        a.addEventListener('click', e => {
            const target = document.querySelector(a.getAttribute('href'));
            if (target) { e.preventDefault(); target.scrollIntoView({ behavior: 'smooth' }); }
        });
    });
});
