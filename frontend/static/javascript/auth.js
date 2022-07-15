let element = document.getElementsByClassName("form-field-invalid");
let errorText = document.getElementsByClassName("error-text");

elementArray = [].slice.call(element);
errorTextArray = [].slice.call(errorText);

elementArray.forEach(elem => {
  elem.addEventListener("click", () => {
    elem.classList.remove("form-field-invalid");
    errorText[elementArray.findIndex(() => elem)].remove();
  })
});
