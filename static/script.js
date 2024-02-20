document.getElementById("submitButton").addEventListener('click', function(e) {
    e.preventDefault();

    let form = document.getElementById('new_part_entry');
    let formData = new FormData(form);

    let xhr = new XMLHttpRequest();
    xhr.open(form.method, form.action, true);
    xhr.onload = function () {
        if (xhr.status == 200) {
            console.log(xhr.responseText);
        } else {
            console.error('Request failed' + xhr.status);
        }
    };
    xhr.onerror = function () {
        console.log('Request failed');
    };
    xhr.send(formData)
});