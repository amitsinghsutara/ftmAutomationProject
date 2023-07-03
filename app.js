import downloadContent from "./download-content/downloadContent.js";
const mainDiv = document.getElementById("main-div");

async function main() {
  const language = await selectYourLanguage();
  downloadContent(mainDiv, language);
}

function selectYourLanguage() {
  return new Promise((resolve) => {
    const createLanguageInputField = document.createElement("input");
    createLanguageInputField.placeholder = "Enter language you want to create:";
    mainDiv.appendChild(createLanguageInputField);

    createLanguageInputField.addEventListener("keydown", function (event) {
      if (event.keyCode === 13) {
        event.preventDefault(); // Prevent the default Enter key behavior
        const language = createLanguageInputField.value;
        createLanguageInputField.value = "";
        mainDiv.removeChild(createLanguageInputField);
        resolve(language);
      }
    });
  });
}

main();
