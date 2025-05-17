document.addEventListener('DOMContentLoaded', () => {
    const API_URL = 'http://localhost:5000';
    const startButton = document.getElementById('startGame');
    const instructionsButton = document.getElementById('instructions');
    const levelsButton = document.getElementById('levels');
    const instructionsPanel = document.getElementById('instructionsPanel');
    let levelsPanel = null;

    // تهيئة الأزرار
    function initializeButtons() {
        startButton.disabled = false;
        startButton.textContent = 'ابدأ اللعبة';
        
        // إضافة الفئات للأزرار
        [startButton, instructionsButton, levelsButton].forEach(button => {
            button.classList.add('game-button');
        });
    }

    // معالجة بدء اللعبة
    async function handleStartGame() {
        try {
            startButton.disabled = true;
            startButton.textContent = 'جاري بدء اللعبة...';
            
            const response = await fetch(`${API_URL}/start-game`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                }
            });

            if (!response.ok) {
                throw new Error(`خطأ في الاستجابة: ${response.status}`);
            }

            const data = await response.json();
            console.log('تم بدء اللعبة:', data);
            
            // إظهار رسالة نجاح
            showMessage('تم بدء اللعبة بنجاح', 'success');
        } catch (error) {
            console.error('خطأ في بدء اللعبة:', error);
            showMessage('فشل في بدء اللعبة. تأكد من تشغيل الخادم.', 'error');
        } finally {
            initializeButtons();
        }
    }

    // عرض المراحل
    async function handleShowLevels() {
        try {
            const response = await fetch(`${API_URL}/levels`, {
                headers: {
                    'Accept': 'application/json'
                }
            });

            if (!response.ok) {
                throw new Error(`خطأ في تحميل المراحل: ${response.status}`);
            }

            const levels = await response.json();
            
            // إزالة لوحة المراحل السابقة إذا وجدت
            if (levelsPanel) {
                levelsPanel.remove();
            }

            // إنشاء لوحة المراحل الجديدة
            levelsPanel = document.createElement('div');
            levelsPanel.className = 'panel levels-panel';
            levelsPanel.innerHTML = `
                <h2>المراحل المتاحة</h2>
                <div class="levels-list">
                    ${levels.map(level => `
                        <div class="level-item">
                            <h3>المرحلة ${level.id}: ${level.name}</h3>
                            <p class="level-description">${level.description}</p>
                            <div class="level-details">
                                <span>الأعداء: ${level.enemies ? level.enemies.length : 0}</span>
                                <span>المنصات: ${level.platforms ? level.platforms.length : 0}</span>
                            </div>
                        </div>
                    `).join('')}
                </div>
            `;

            document.querySelector('.container').appendChild(levelsPanel);
        } catch (error) {
            console.error('خطأ في تحميل المراحل:', error);
            showMessage('فشل في تحميل المراحل', 'error');
        }
    }

    // إظهار رسالة للمستخدم
    function showMessage(message, type = 'info') {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}`;
        messageDiv.textContent = message;
        
        document.querySelector('.container').appendChild(messageDiv);
        
        // إزالة الرسالة بعد 3 ثواني
        setTimeout(() => {
            messageDiv.remove();
        }, 3000);
    }

    // إضافة مستمعي الأحداث
    startButton.addEventListener('click', handleStartGame);
    instructionsButton.addEventListener('click', () => {
        instructionsPanel.classList.toggle('hidden');
    });
    levelsButton.addEventListener('click', handleShowLevels);

    // تهيئة الواجهة
    initializeButtons();

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
                console.log('Move right');
            } else {
                console.log('Move left');
            }
        }
    }
}); 
