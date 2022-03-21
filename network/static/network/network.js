document.addEventListener('DOMContentLoaded', () => {

    // Check that the items exist before adding event listeners to avoid errors
    if (document.querySelectorAll('.edit')){
        document.querySelectorAll('.edit').forEach(item => {
            item.addEventListener('click', (e) => {
                const id = e.target.getAttribute('data-id');
                edit(id);
            })
        })
    }

})

function edit(id) {
    // Target the elements on the page
    const formEl = document.querySelector(`[data-update="${id}"]`);
    const postContentEl = document.querySelector(`[data-content="${id}"]`);

    // Toggle edit
    if (formEl.hidden == true){
        postContentEl.style.display = 'none';
        formEl.hidden = false;
    } else {
        postContentEl.style.display = 'block';
        formEl.hidden = true;
    }

    // Update handled by form submission/Django
}