// main.js

document.addEventListener('DOMContentLoaded', () => {
    // Mobile menu toggle (landing)
    const mobileToggle = document.querySelector('.mobile-toggle');
    const navLinks = document.querySelector('.nav-links');
    const navActions = document.querySelector('.nav-actions');

    if (mobileToggle) {
        mobileToggle.addEventListener('click', () => {
            navLinks.classList.toggle('active');
            navActions.classList.toggle('active');
        });
    }

    // Sidebar toggle (dashboard)
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebarClose = document.getElementById('sidebarClose');
    const sidebar = document.getElementById('sidebar');

    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', () => {
            sidebar.classList.add('open');
        });
    }
    if (sidebarClose && sidebar) {
        sidebarClose.addEventListener('click', () => {
            sidebar.classList.remove('open');
        });
    }

    // FAQ Accordion
    const faqItems = document.querySelectorAll('.faq-item');
    faqItems.forEach(item => {
        const q = item.querySelector('.faq-q');
        const a = item.querySelector('.faq-a');
        if (q && a) {
            q.addEventListener('click', () => {
                const isOpen = a.style.display === 'block';
                document.querySelectorAll('.faq-a').forEach(ans => ans.style.display = 'none');
                if (!isOpen) {
                    a.style.display = 'block';
                }
            });
        }
    });

    // Alert Tabs mock
    const tabs = document.querySelectorAll('.tab');
    if (tabs.length > 0) {
        tabs.forEach(tab => {
            tab.addEventListener('click', () => {
                tabs.forEach(t => t.classList.remove('active'));
                tab.classList.add('active');
            });
        });
    }

    // Power Toggle Mock
    const toggles = document.querySelectorAll('.power-toggle');
    toggles.forEach(toggle => {
        toggle.addEventListener('change', (e) => {
            const statusEl = document.getElementById(`status-${e.target.dataset.id}`);
            if (statusEl) {
                if (e.target.checked) {
                    statusEl.className = 'status-indicator online';
                    statusEl.nextSibling.textContent = ' Включено';
                } else {
                    statusEl.className = 'status-indicator offline';
                    statusEl.nextSibling.textContent = ' Выключено';
                }
            }
        });
    });

    // Mock Chart.js init (only if canvas exists)
    const ctxMain = document.getElementById('mainChart');
    if (ctxMain && typeof Chart !== 'undefined') {
        new Chart(ctxMain, {
            type: 'line',
            data: {
                labels: ['00:00', '04:00', '08:00', '12:00', '16:00', '20:00', '24:00'],
                datasets: [{
                    label: 'Потребление (кВт⋅ч)',
                    data: [1.2, 0.8, 3.5, 4.2, 3.8, 2.5, 1.5],
                    borderColor: '#00d084',
                    backgroundColor: 'rgba(0, 208, 132, 0.1)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' } },
                    x: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' } }
                },
                plugins: {
                    legend: { labels: { color: '#f8fafc' } }
                }
            }
        });
    }
});
