document.addEventListener('DOMContentLoaded', function () {
    const modal = document.getElementById('refModal');
    if (!modal) return;
    const overlay = modal.querySelector('.modal-overlay');
    const closeBtn = modal.querySelector('.modal-close');

    function showValue(id, value) {
        const el = document.getElementById(id);
        if (!el) return;
        el.textContent = value ? value : '-';
    }

    function openModal(data) {
        showValue('m-id', data.id);
        showValue('m-keyword', data.keyword);
        showValue('m-category', data.category);
        showValue('m-type', data.type);
        showValue('m-author', data.author);
        showValue('m-title', data.title);
        showValue('m-year', data.year);
        showValue('m-doi', data.doi);
        showValue('m-journal', data.journal);
        showValue('m-volume', data.volume);
        showValue('m-pages', data.pages);
        showValue('m-publisher', data.publisher);
        showValue('m-booktitle', data.booktitle);

        modal.style.display = 'flex';
        modal.setAttribute('aria-hidden', 'false');
        closeBtn && closeBtn.focus();
    }

    function closeModal() {
        modal.style.display = 'none';
        modal.setAttribute('aria-hidden', 'true');
    }

    document.querySelectorAll('.info-btn').forEach(function (btn) {
        btn.addEventListener('click', function () {
            const d = btn.dataset;
            openModal(d);
        });
    });

    closeBtn && closeBtn.addEventListener('click', closeModal);
    overlay && overlay.addEventListener('click', closeModal);
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeModal(); });
});
