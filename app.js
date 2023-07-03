const readline = require("readline");
async function main() {
  const language = await selectYourLanguage();
}

function selectYourLanguage() {
  const language = askQuestion(
    "Enter the language you want your new ftm to be:"
  );
}
async function askQuestion(question) {
  return new Promise((resolve, reject) => {
    const rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout,
    });

    rl.question(question, (answer) => {
      rl.close();
      resolve(answer);
    });
  });
}

main();
