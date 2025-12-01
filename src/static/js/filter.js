const yearMin = document.getElementById("year-min");
const yearMax = document.getElementById("year-max");
const yearFrom = document.getElementById("year-from");
const yearTo = document.getElementById("year-to");
const selected = document.getElementById("year-color");

function updateValues() {
  const minVal = parseInt(yearMin.value);
  const maxVal = parseInt(yearMax.value);

  if (minVal >= maxVal) { yearMin.value = maxVal - 1; }
  if (maxVal < minVal) { yearMax.value = minVal - 1; }

  yearFrom.value = minVal;
  yearTo.value = maxVal;

  const minPercent = (yearMin.value / yearMin.max) * 100
  const maxPercent = (yearMax.value / yearMax.max) * 100
  selected.style.left = minPercent + "%"
  selected.style.width = (maxPercent - minPercent) + "%"
}

yearMin.addEventListener('input', updateValues);
yearMax.addEventListener('input', updateValues);
yearFrom.addEventListener('input', () => { yearMin.value = yearFrom.value; updateValues(); })
yearTo.addEventListener('input', () => { yearMax.value = yearTo.value; updateValues(); })

updateValues();
