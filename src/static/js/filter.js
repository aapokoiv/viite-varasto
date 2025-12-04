const yearFrom = document.getElementById("year-from");
const yearTo = document.getElementById("year-to");

function checkValues(text) {
  text.value = text.value.replace(/[^0-9]/g, "");
}

yearFrom.addEventListener('input', () => { checkValues(yearFrom); })
yearTo.addEventListener('input', () => { checkValues(yearTo); })
