updateString = (sliderId, stringId) => {
    let slider = document.getElementById(sliderId)
    let sliderValueString = document.getElementById(stringId)
    sliderValueString.textContent = slider.value
}

updateString();
