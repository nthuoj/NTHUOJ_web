$(function() {
    $('.open-popup-link').magnificPopup({
        // Class that is added to popup wrapper and background
        // make it unique to apply your CSS animations just to this exact popup
        removalDelay: 500,
        mainClass: 'mfp-fade',
        type: 'inline',
        midClick: true // Allow opening popup on middle mouse click. Always set it to true if you don't provide alternative source in href.
    });
    $('.code-link').magnificPopup({
        // Class that is added to popup wrapper and background
        // make it unique to apply your CSS animations just to this exact popup
        removalDelay: 500,
        mainClass: 'mmfp-fade',
        type: 'inline',
        midClick: true, // Allow opening popup on middle mouse click. Always set it to true if you don't provide alternative source in href.
        callbacks: {
            open: function() {
                setTimeout(function() {
                    editor.refresh()
                }, 10);
            }
        }
    });
})