console.log('Fuet Mágico - Static JS loaded');

// Disable browser autocomplete globally for all inputs
document.addEventListener('DOMContentLoaded', function() {
    // Disable autocomplete for all input, textarea, and select elements
    const formElements = document.querySelectorAll('input, textarea, select');
    formElements.forEach(element => {
        element.setAttribute('autocomplete', 'off');
    });
    
    // Also observe for dynamically added elements
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            mutation.addedNodes.forEach(function(node) {
                if (node.nodeType === 1) { // Element node
                    if (node.matches && (node.matches('input') || node.matches('textarea') || node.matches('select'))) {
                        node.setAttribute('autocomplete', 'off');
                    }
                    // Also check children
                    const children = node.querySelectorAll && node.querySelectorAll('input, textarea, select');
                    if (children) {
                        children.forEach(child => child.setAttribute('autocomplete', 'off'));
                    }
                }
            });
        });
    });
    
    // Start observing the document for changes
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
    
    console.log('Autocomplete disabled for all form elements');
});
