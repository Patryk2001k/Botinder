const questions = document.querySelectorAll('.FAQ-question');

questions.forEach(question => {
  const answer = question.querySelector('.answer');
  question.addEventListener('click', () => {
    toggleAnswer(answer);
  });
});

function toggleAnswer(answer) {
  if (answer.style.maxHeight) {
    answer.style.maxHeight = null;
  } else {
    answer.style.maxHeight = answer.scrollHeight + 'px';
  }
}
