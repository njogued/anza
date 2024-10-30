document.addEventListener('DOMContentLoaded', function() {
    // Get the hidden div content
    const popoverContent = document.getElementById('popover-content').innerHTML;

    // Initialize the popover
    const popoverTriggerEl = document.getElementById('profile-icon-link');
    const popover = new bootstrap.Popover(popoverTriggerEl, {
        trigger: 'manual',
        html: true,
        content: popoverContent
    });

    popoverTriggerEl.addEventListener('click', function () {
        popover.toggle();
    });

    document.addEventListener('click', function (e) {
        // Check if the click is outside of the popover and not on the icon
        if (!popoverTriggerEl.contains(e.target) && !document.querySelector('.popover')?.contains(e.target)) {
            popover.hide();
        }

        // Check if the close button inside the popover is clicked
        if (e.target.classList.contains('btn-close')) {
            popover.hide();
        }
    });
    // popoverTriggerEl.addEventListener('shown.bs.popover', function () {
    //     // Use JavaScript to set custom header content
    //     document.querySelector('.popover-header').innerHTML = `
    //         <p class="text-center">You</p>
    //         <button type="button" class="btn-close" aria-label="Close"></button>
    //     `;
    // });
});
