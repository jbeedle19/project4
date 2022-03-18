document.addEventListener('DOMContentLoaded', () => {

    // Check that the items exist before adding event listeners to avoid errors
    if (document.querySelector('#follow')) {
        renderFollowBtn();
        document.querySelector('#follow').addEventListener('click', (e) => {
            const userID = e.target.getAttribute('data-id');
            follow(userID);
        });
        document.querySelector('#unfollow').addEventListener('click', (e) => {
            const userID = e.target.getAttribute('data-id');
            unfollow(userID);
        });
    }
    if (document.querySelectorAll('.edit')){
        document.querySelectorAll('.edit').forEach(item => {
            item.addEventListener('click', (e) => {
                const id = e.target.getAttribute('data-id');
                edit(id);
            })
        })
    }

})

function renderFollowBtn() {
    console.log('This will check if you are following the person or not and render button accordingly');
}

function follow() {
    console.log('Follow this user!');
}

function unfollow() {
    console.log('Unfollow this user!');
}

function edit(id) {
    console.log(`Editing post with id of ${id}`);
}