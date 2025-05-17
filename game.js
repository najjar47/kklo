document.addEventListener('DOMContentLoaded', () => {
    const startButton = document.getElementById('startGame');
    const instructionsButton = document.getElementById('instructions');
    const levelsButton = document.getElementById('levels');
    const instructionsPanel = document.getElementById('instructionsPanel');

    startButton.addEventListener('click', () => {
        // Start the Python game
        fetch('/start-game', {
            method: 'POST'
        }).then(response => response.json())
          .then(data => {
              console.log('Game started:', data);
          })
          .catch(error => {
              console.error('Error starting game:', error);
          });
    });

    instructionsButton.addEventListener('click', () => {
        instructionsPanel.classList.toggle('hidden');
    });

    levelsButton.addEventListener('click', () => {
        fetch('/levels')
            .then(response => response.json())
            .then(levels => {
                // Show levels information
                const levelsPanel = document.createElement('div');
                levelsPanel.className = 'panel';
                levelsPanel.innerHTML = `
                    <h2>المراحل المتاحة</h2>
                    <ul>
                        ${levels.map(level => `
                            <li>المرحلة ${level.id}: ${level.name}</li>
                        `).join('')}
                    </ul>
                `;
                document.querySelector('.container').appendChild(levelsPanel);
            });
    });

    // Add keyboard controls explanation
    const keyboardControls = {
        'ArrowRight': 'التحرك يمينًا',
        'ArrowLeft': 'التحرك يسارًا',
        'Space': 'القفز',
        'Control': 'إطلاق النار'
    };

    // Add touch controls for mobile devices
    let touchStartX = 0;
    let touchEndX = 0;

    document.addEventListener('touchstart', e => {
        touchStartX = e.changedTouches[0].screenX;
    });

    document.addEventListener('touchend', e => {
        touchEndX = e.changedTouches[0].screenX;
        handleSwipe();
    });

    function handleSwipe() {
        const swipeDistance = touchEndX - touchStartX;
        if (Math.abs(swipeDistance) > 50) {
            if (swipeDistance > 0) {
                // Swipe right
                console.log('Move right');
            } else {
                // Swipe left
                console.log('Move left');
            }
        }
    }
}); 