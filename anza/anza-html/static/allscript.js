document.querySelector('.navbar-toggler').addEventListener('click', function () {
    const isCollapsed = this.getAttribute('aria-expanded') === 'true';
    const collapsedIcon = document.getElementById('collapsed-icon');
    const expandedIcon = document.getElementById('expanded-icon');

    if (isCollapsed) {
        collapsedIcon.style.display = 'none';
        expandedIcon.style.display = 'inline';
    } else {
        collapsedIcon.style.display = 'inline';
        expandedIcon.style.display = 'none';
    }
});
