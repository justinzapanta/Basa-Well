const filter_form = document.querySelector('#filter-form')
const _status = document.querySelector('#status')
const genre = document.querySelector('#genre')
const paginations = document.querySelectorAll('.pagination')

function filter(){
    filter_form.action = `/${_status.value}/${genre.value}/1`
    filter_form.submit()
}


let limit
function pagination(_this) {
    if (limit !== 1){
        window.location.href = `/${_this.textContent}`
    }
    limit = 1
    paginations.forEach(pagin => {
        pagin.removeAttribute('href')
    })
}