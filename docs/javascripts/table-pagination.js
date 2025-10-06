document.addEventListener('DOMContentLoaded', function() {
  // Find all tables with data-paginate attribute
  document.querySelectorAll('table[data-paginate]').forEach(table => {
    const rowsPerPage = parseInt(table.getAttribute('data-paginate')) || 10;
    paginateTable(table, rowsPerPage);
  });
});

function paginateTable(table, rowsPerPage) {
  const tbody = table.querySelector('tbody');
  if (!tbody) return;

  const rows = Array.from(tbody.querySelectorAll('tr'));
  const pageCount = Math.ceil(rows.length / rowsPerPage);
  let currentPage = 1;

  // Create pagination controls
  const paginationDiv = document.createElement('div');
  paginationDiv.className = 'table-pagination';
  paginationDiv.style.cssText = 'display: flex; justify-content: center; align-items: center; gap: 0.5rem; margin-top: 1rem; font-size: 0.8rem;';

  const pageInfo = document.createElement('span');
  pageInfo.className = 'page-info';

  const prevBtn = createButton('← Prev', () => changePage(currentPage - 1));
  const nextBtn = createButton('Next →', () => changePage(currentPage + 1));

  paginationDiv.appendChild(prevBtn);
  paginationDiv.appendChild(pageInfo);
  paginationDiv.appendChild(nextBtn);
  table.parentNode.insertBefore(paginationDiv, table.nextSibling);

  function createButton(text, onClick) {
    const btn = document.createElement('button');
    btn.textContent = text;
    btn.className = 'pagination-btn';
    btn.style.cssText = 'padding: 0.3rem 0.7rem; border: 1px solid var(--cf-border); border-radius: 4px; background: var(--cf-bg); cursor: pointer; transition: background 0.2s;';
    btn.onclick = onClick;
    return btn;
  }

  function showPage(page) {
    const start = (page - 1) * rowsPerPage;
    const end = start + rowsPerPage;

    rows.forEach((row, index) => {
      row.style.display = (index >= start && index < end) ? '' : 'none';
    });

    pageInfo.textContent = `Page ${page} of ${pageCount} (${rows.length} rows)`;
    prevBtn.disabled = page === 1;
    nextBtn.disabled = page === pageCount;

    prevBtn.style.opacity = page === 1 ? '0.5' : '1';
    nextBtn.style.opacity = page === pageCount ? '0.5' : '1';
    prevBtn.style.cursor = page === 1 ? 'not-allowed' : 'pointer';
    nextBtn.style.cursor = page === pageCount ? 'not-allowed' : 'pointer';
  }

  function changePage(page) {
    if (page < 1 || page > pageCount) return;
    currentPage = page;
    showPage(currentPage);
  }

  showPage(1);
}