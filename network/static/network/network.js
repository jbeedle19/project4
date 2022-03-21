document.addEventListener('DOMContentLoaded', () => {
    // Check that the items exist before adding event listeners to avoid errors

    if (document.querySelectorAll('.edit')) {
        document.querySelectorAll('.edit').forEach(item => {
            item.addEventListener('click', (e) => {
                const id = e.target.getAttribute('data-id');
                edit(id);
            })
        })
    }

    if (document.querySelectorAll('.like')) {
        document.querySelectorAll('.like').forEach(item => {
            item.addEventListener('click', (e) => {
                const id = e.target.getAttribute('data-like');
                like(id);
            })
        })
    }
    if (document.querySelectorAll('.dislike')) {
        document.querySelectorAll('.dislike').forEach(item => {
            item.addEventListener('click', (e) => {
                const id = e.target.getAttribute('data-like');
                dislike(id);
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

function like(id) {
    const likeEl = document.querySelector(`[data-like="${id}"]`);
    const countEl = document.querySelector(`[data-count="${id}"]`);

    if (likeEl.innerHTML === '🤍') {
        // Update the icon and the like count
        let currentCount = countEl.innerHTML;
        currentCount++;
        countEl.innerHTML = currentCount;
        likeEl.innerHTML = '❤️';

        // Make API call with PUT request
        fetch(`/like/${id}`, {
            method: 'PUT',
            body: JSON.stringify({
                liked: true
            })
        });
    } else {
        dislike(id);
    }
}

function dislike(id) {
    const dislikeEl = document.querySelector(`[data-like="${id}"]`);
    const countEl = document.querySelector(`[data-count="${id}"]`);

    if (dislikeEl.innerHTML === '❤️') {
        // Update the icon and the like count
        let currentCount = countEl.innerHTML;
        currentCount--;
        countEl.innerHTML = currentCount;
        dislikeEl.innerHTML = '🤍';

        // Make API call with PUT request
        fetch(`/dislike/${id}`, {
            method: 'PUT',
            body: JSON.stringify({
                liked: false
            })
        });
    } else {
        like(id);
    }
}