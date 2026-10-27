function updateCharCount() {
    const area = document.getElementById('notes-area');
    const badge = document.getElementById('char-count');
    if (area && badge) {
        badge.textContent = `${area.value.length} characters`;
    }
}

document.addEventListener('input', (e) => {
    if (e.target && e.target.id === 'notes-area') {
        updateCharCount();
    }
});

function switchTab(evt, tabId) {
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabPanes = document.querySelectorAll('.tab-pane');

    tabButtons.forEach(btn => btn.classList.remove('active'));
    tabPanes.forEach(pane => pane.classList.remove('active'));

    evt.currentTarget.classList.add('active');
    const target = document.getElementById(tabId);
    if (target) {
        target.classList.add('active');
    }
}

let answeredTally = 0;

function selectAnswer(button) {
    const card = button.closest('.quiz-card');
    const correctAnswer = card.getAttribute('data-correct').trim();
    const chosenText = button.querySelector('.option-content').textContent.trim();
    const allOptions = card.querySelectorAll('.option-slot');
    const feedback = card.querySelector('.feedback-drawer');
    const statusText = card.querySelector('.feedback-status');

    allOptions.forEach(opt => opt.disabled = true);

    if (chosenText === correctAnswer) {
        button.classList.add('correct');
        statusText.textContent = "Correct assessment";
        statusText.className = "feedback-status correct";
    } else {
        button.classList.add('incorrect');
        statusText.textContent = "Incorrect choice";
        statusText.className = "feedback-status incorrect";

        allOptions.forEach(opt => {
            if (opt.querySelector('.option-content').textContent.trim() === correctAnswer) {
                opt.classList.add('correct');
            }
        });
    }

    feedback.classList.remove('hidden');

    answeredTally++;
    const counter = document.getElementById('answered-counter');
    if (counter) {
        counter.textContent = answeredTally;
    }
}

function resetQuiz() {
    answeredTally = 0;
    const counter = document.getElementById('answered-counter');
    if (counter) counter.textContent = '0';

    document.querySelectorAll('.quiz-card').forEach(card => {
        card.querySelectorAll('.option-slot').forEach(opt => {
            opt.disabled = false;
            opt.classList.remove('correct', 'incorrect');
        });
        const drawer = card.querySelector('.feedback-drawer');
        if (drawer) drawer.classList.add('hidden');
    });
}