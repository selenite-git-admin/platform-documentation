document.addEventListener('DOMContentLoaded', function() {
  // Add link to DataTables CSS
  const link = document.createElement('link');
  link.rel = 'stylesheet';
  link.href = 'https://cdn.datatables.net/1.13.7/css/jquery.dataTables.min.css';
  document.head.appendChild(link);

  // Load jQuery and DataTables
  const jquery = document.createElement('script');
  jquery.src = 'https://code.jquery.com/jquery-3.7.1.min.js';
  jquery.onload = function() {
    const datatables = document.createElement('script');
    datatables.src = 'https://cdn.datatables.net/1.13.7/js/jquery.dataTables.min.js';
    datatables.onload = function() {
      // Initialize DataTables on tables with .datatable class
      $('.datatable').DataTable({
        pageLength: 10,
        lengthMenu: [[10, 25, 50, -1], [10, 25, 50, "All"]],
        language: {
          search: "Filter:",
          lengthMenu: "Show _MENU_ rows"
        }
      });
    };
    document.head.appendChild(datatables);
  };
  document.head.appendChild(jquery);
});