function clearInputAndScramble() {
    document.querySelector('input[name=solution_time]').value = ''
}

function validateInput(puzzle) {
    const input = document.querySelector('input[name=solution_time]')
    const regex = new RegExp(/^([1-5]?[0-9]:)?[0-5]?[0-9]([\.,][0-9]{1,3})?$/)

    if ( input.value === '' ) {
        event.preventDefault()
        htmx.ajax('GET', `/scramble?puzzle=${puzzle}`, { target: '#scramble' })
    }

    const isValidInput = regex.test(input.value)

    if (!isValidInput) {
        event.preventDefault()
        //show warning or something
        return
    }
}
