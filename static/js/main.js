document.addEventListener('DOMContentLoaded', () => {
  const body = document.body;
  const htmlElement = document.documentElement;

  const yearSpan = document.getElementById('year');
  if (yearSpan) {
    yearSpan.textContent = new Date().getFullYear();
  }
  const cookiesBanner = document.getElementById('cookies-banner');
  const cookiesAcceptBtn = document.getElementById('cookies-accept');
  const cookiesRejectBtn = document.getElementById('cookies-reject');

  if (cookiesBanner && cookiesAcceptBtn && cookiesRejectBtn) {
    const cookiesKey = 'cookies_accepted';
    const cookiesValue = localStorage.getItem(cookiesKey);
    if (!cookiesValue) {
      setTimeout(() => {
        cookiesBanner.classList.add('show');
      }, 1000);
    }
    cookiesAcceptBtn.addEventListener('click', () => {
      localStorage.setItem(cookiesKey, 'true');
      document.cookie = 'cookies_accepted=true; path=/; max-age=' + (365 * 24 * 60 * 60);
      cookiesBanner.classList.remove('show');
    });
    cookiesRejectBtn.addEventListener('click', () => {
      localStorage.setItem(cookiesKey, 'false');
      cookiesBanner.classList.remove('show');
    });
  }

  const contrastToggle = document.getElementById('contrast-toggle');
  if (contrastToggle) {
    const contrastStorageKey = 'highContrastMode';

    const setContrastMode = (isEnabled) => {
      if (isEnabled) {
        body.classList.add('high-contrast-mode');
        localStorage.setItem(contrastStorageKey, 'true');
      } else {
        body.classList.remove('high-contrast-mode');
        localStorage.setItem(contrastStorageKey, 'false');
      }
    };

    const savedContrastState = localStorage.getItem(contrastStorageKey);
    if (savedContrastState === 'true') {
      setContrastMode(true);
    }

    contrastToggle.addEventListener('click', () => {
      const isEnabled = body.classList.contains('high-contrast-mode');
      setContrastMode(!isEnabled);
    });
  }

  const textIncreaseBtn = document.getElementById('text-increase');
  const textDecreaseBtn = document.getElementById('text-decrease');
  const textResetBtn = document.getElementById('text-reset');
  if (textIncreaseBtn && textDecreaseBtn && textResetBtn) {
    const fontSizeStorageKey = 'fontSize';
    const initialFontSize = 16;

    const setFontSize = (size) => {
      htmlElement.style.fontSize = size + 'px';
      localStorage.setItem(fontSizeStorageKey, size);
    };

    const savedFontSize = localStorage.getItem(fontSizeStorageKey);
    if (savedFontSize) {
      setFontSize(parseFloat(savedFontSize));
    }

    textIncreaseBtn.addEventListener('click', () => {
      let currentSize = parseFloat(window.getComputedStyle(htmlElement).fontSize);
      if (currentSize < 24) {
        setFontSize(currentSize + 1);
      }
    });

    textDecreaseBtn.addEventListener('click', () => {
      let currentSize = parseFloat(window.getComputedStyle(htmlElement).fontSize);
      if (currentSize > 12) {
        setFontSize(currentSize - 1);
      }
    });

    textResetBtn.addEventListener('click', () => {
      setFontSize(initialFontSize);
    });
  }

  const cinemaHall = document.querySelector('.cinema-hall');
  if (cinemaHall) {
    const seatsInput = document.getElementById('selected-seats-input');
    const seatsDisplay = document.getElementById('selected-seats-display');
    const submitButton = document.getElementById('submit-reservation');

    const updateSelection = () => {
      const selectedSeats = cinemaHall.querySelectorAll('.seat.selected');
      const seatIds = Array.from(selectedSeats).map(seat => seat.dataset.seatId);

      seatIds.sort((a, b) => {
        const rowA = a.charAt(0);
        const rowB = b.charAt(0);
        const numA = parseInt(a.substring(1), 10);
        const numB = parseInt(b.substring(1), 10);

        if (rowA < rowB) return -1;
        if (rowA > rowB) return 1;
        return numA - numB;
      });

      if (seatIds.length > 0) {
        seatsDisplay.textContent = seatIds.join(', ');
        seatsInput.value = seatIds.join(',');
        submitButton.disabled = false;
      } else {
        seatsDisplay.textContent = 'Brak';
        seatsInput.value = '';
        submitButton.disabled = true;
      }
    };

    cinemaHall.addEventListener('click', (event) => {
      const seat = event.target.closest('.seat');
      if (seat && !seat.classList.contains('taken')) {
        seat.classList.toggle('selected');
        updateSelection();
      }
    });

    updateSelection();
  }

  const datePickerInput = document.getElementById('date-input-picker');
  const openPickerBtn = document.getElementById('open-date-picker');

  if (datePickerInput) {
    datePickerInput.addEventListener('change', (event) => {
      const selectedDate = event.target.value;
      if (selectedDate) {
        const [year, month, day] = selectedDate.split('-');
        window.location.href = `/seanse/${year}/${month}/${day}/`;
      }
    });
  }

  if (openPickerBtn && datePickerInput) {
    openPickerBtn.addEventListener('click', () => {
      datePickerInput.focus();
      datePickerInput.showPicker();
    });
  }
});
const calendarBox = document.getElementById('custom-calendar');
const openPickerBtn = document.getElementById('open-date-picker');

if (calendarBox && openPickerBtn) {

    let current = new Date();

    const dayNames = ["P", "W", "Ĺš", "C", "P", "S", "N"];

    const renderCalendar = () => {
        calendarBox.innerHTML = "";

        const year = current.getFullYear();
        const month = current.getMonth();

        const firstDay = new Date(year, month, 1).getDay() || 7;
        const daysInMonth = new Date(year, month + 1, 0).getDate();

        const prevMonthDays = new Date(year, month, 0).getDate();
        const header = document.createElement("div");
        header.className = "calendar-header";

        const prevBtn = document.createElement("button");
        prevBtn.textContent = "<";
        prevBtn.onclick = (e) => {
            e.stopPropagation();
            current.setMonth(month - 1);
            renderCalendar();
        };

        const nextBtn = document.createElement("button");
        nextBtn.textContent = ">";
        nextBtn.onclick = (e) => {
            e.stopPropagation();
            current.setMonth(month + 1);
            renderCalendar();
        };

        const title = document.createElement("div");
        title.textContent = current.toLocaleDateString("pl-PL", { month: 'long', year: 'numeric' });

        header.append(prevBtn, title, nextBtn);
        calendarBox.append(header);
        const grid = document.createElement("div");
        grid.className = "calendar-grid";
        dayNames.forEach(d => {
            const el = document.createElement("div");
            el.className = "calendar-day-header";
            el.textContent = d;
            grid.append(el);
        });
        for (let i = 1; i < firstDay; i++) {
            const ghost = document.createElement("div");
            ghost.className = "calendar-day ghost";
            ghost.textContent = prevMonthDays - (firstDay - 1) + i;
            grid.append(ghost);
        }
        for (let day = 1; day <= daysInMonth; day++) {
            const cell = document.createElement("div");
            cell.className = "calendar-day";
            cell.textContent = day;

            cell.onclick = () => {
                const mm = String(month + 1).padStart(2, "0");
                const dd = String(day).padStart(2, "0");
                window.location.href = `/seanse/${year}/${mm}/${dd}/`;
            };

            grid.append(cell);
        }
        let filled = grid.children.length;
        let needed = 49 - filled;
        let c = 1;

        while (needed > 0) {
            const ghost = document.createElement("div");
            ghost.className = "calendar-day ghost";
            ghost.textContent = c++;
            grid.append(ghost);
            needed--;
        }

        calendarBox.append(grid);
    };
    openPickerBtn.addEventListener("click", (e) => {
        e.stopPropagation();
        if (calendarBox.classList.contains("hidden")) {
            renderCalendar();
            calendarBox.classList.remove("hidden");
        } else {
            calendarBox.classList.add("hidden");
        }
    });
    document.addEventListener("click", (e) => {
        if (!calendarBox.contains(e.target) && !openPickerBtn.contains(e.target)) {
            calendarBox.classList.add("hidden");
        }
    });
}
const passwordInput = document.getElementById('id_password1');
const usernameInput = document.getElementById('id_username');
const emailInput = document.getElementById('id_email');
const strengthBar = document.getElementById('strength-bar');
const strengthText = document.getElementById('strength-text');
const submitBtn = document.querySelector('button[type="submit"]');

function updatePasswordStrength() {
    const password = passwordInput.value;
    const username = usernameInput ? usernameInput.value : '';
    const email = emailInput ? emailInput.value : '';
    const requirements = checkRequirements(password);
    updateRequirements(requirements);
    const strength = calculatePasswordStrength(password, requirements, username, email);
    updateStrengthDisplay(strength);
    if (strength.level === 'weak') {
        submitBtn.disabled = true;
        submitBtn.style.opacity = '0.5';
    } else {
        submitBtn.disabled = false;
        submitBtn.style.opacity = '1';
    }
}

if (passwordInput && strengthBar && strengthText) {
    passwordInput.addEventListener('input', updatePasswordStrength);
    if (usernameInput) usernameInput.addEventListener('input', updatePasswordStrength);
    if (emailInput) emailInput.addEventListener('input', updatePasswordStrength);
}

function checkRequirements(password) {
    return {
        length: password.length >= 8,
        uppercase: /[A-Z]/.test(password),
        digit: /\d/.test(password),
        special: /[@$!%*?&]/.test(password)
    };
}

function updateRequirements(reqs) {
    document.getElementById('req-length').classList.toggle('met', reqs.length);
    document.getElementById('req-uppercase').classList.toggle('met', reqs.uppercase);
    document.getElementById('req-digit').classList.toggle('met', reqs.digit);
    document.getElementById('req-special').classList.toggle('met', reqs.special);
}

function calculatePasswordStrength(password, reqs, username, email) {
    let score = 0;
    if (reqs.length) score += 2;
    if (reqs.uppercase) score += 2;
    if (reqs.digit) score += 2;
    if (reqs.special) score += 2;
    if (password.length >= 12) score += 1;
    if (/[a-z]/.test(password)) score += 1;
    if (password.length > 8 && !/(.)\1{2,}/.test(password)) score += 1;

    const commonPasswords = ['password', '123456', 'qwerty', 'admin', 'letmein'];
    if (!commonPasswords.some(common => password.toLowerCase().includes(common))) score += 1;
    const lowerPassword = password.toLowerCase();
    const lowerUsername = username.toLowerCase();
    const emailPrefix = email.split('@')[0].toLowerCase();
    const containsUsername = lowerUsername && lowerPassword.includes(lowerUsername);
    const containsEmail = emailPrefix && lowerPassword.includes(emailPrefix);
    const hasSequentialDigits = /012|123|234|345|456|567|678|789|890|098|987|876|765|654|543|432|321|210/.test(password);

    if (containsUsername || containsEmail) {
        score -= 5;
        if (hasSequentialDigits) {
            score -= 5;
        }
    } else if (hasSequentialDigits) {
        score -= 4;
    }

    let level = 'weak';
    let text = 'Słabe';
    if (score >= 10) {
        level = 'strong';
        text = 'Silne';
    } else if (score >= 5) {
        level = 'medium';
        text = 'Średnie';
    }

    return { score, level, text };
}

function updateStrengthDisplay(strength) {
    strengthBar.innerHTML = `<div class="strength-${strength.level}"></div>`;
    strengthText.textContent = strength.text;
}
document.addEventListener('DOMContentLoaded', () => {
    const stars = document.querySelectorAll('.star');
    const ratingInput = document.getElementById('id_ocena');
    const ratingText = document.querySelector('.rating-text');

    if (stars.length && ratingInput && ratingText) {
        let currentRating = parseFloat(ratingInput.value) || 5.0;
        
        const updateStars = (rating, isPreview = false) => {
            stars.forEach((star, index) => {
                const starValue = index + 1;
                if (isPreview) {
                    star.classList.remove('active', 'half', 'preview-active', 'preview-half');
                } else {
                    star.classList.remove('active', 'half', 'preview-active', 'preview-half');
                }
                
                if (rating >= starValue) {
                    star.classList.add(isPreview ? 'preview-active' : 'active');
                } else if (rating >= starValue - 0.5) {
                    star.classList.add(isPreview ? 'preview-half' : 'half');
                }
            });
            ratingText.textContent = rating.toFixed(1);
            if (!isPreview) {
                ratingInput.value = rating;
                currentRating = rating;
            }
        };

        const previewStars = (rating) => {
            updateStars(rating, true);
        };

        stars.forEach((star, index) => {
            star.addEventListener('click', (e) => {
                const rect = star.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const half = x < rect.width / 2;
                const rating = index + 1 - (half ? 0.5 : 0);
                updateStars(rating, false);
            });

            star.addEventListener('mousemove', (e) => {
                const rect = star.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const half = x < rect.width / 2;
                const rating = index + 1 - (half ? 0.5 : 0);
                previewStars(rating);
            });

            star.addEventListener('mouseleave', () => {
                updateStars(currentRating, false);
            });
        });
        const initialRating = parseFloat(ratingInput.value) || 5.0;
        updateStars(initialRating, false);
    }
    const paginationLinks = document.querySelectorAll('.pagination-controls a');
    if (paginationLinks.length > 0) {
        paginationLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const url = link.href;
                fetch(url, {
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                })
                .then(response => response.text())
                .then(html => {
                    const parser = new DOMParser();
                    const doc = parser.parseFromString(html, 'text/html');
                    const newMoviesList = doc.querySelector('.current-movies-section .movies-list');
                    const oldMoviesList = document.querySelector('.current-movies-section .movies-list');
                    
                    if (newMoviesList && oldMoviesList) {
                        oldMoviesList.innerHTML = newMoviesList.innerHTML;
                    }
                    const newPagination = doc.querySelector('.pagination-controls');
                    const oldPagination = document.querySelector('.pagination-controls');
                    
                    if (newPagination && oldPagination) {
                        oldPagination.innerHTML = newPagination.innerHTML;
                        const newLinks = document.querySelectorAll('.pagination-controls a');
                        newLinks.forEach(newLink => {
                            newLink.addEventListener('click', (e) => {
                                e.preventDefault();
                                const newUrl = newLink.href;
                                
                                fetch(newUrl, {
                                    headers: {
                                        'X-Requested-With': 'XMLHttpRequest'
                                    }
                                })
                                .then(resp => resp.text())
                                .then(newHtml => {
                                    const newDoc = parser.parseFromString(newHtml, 'text/html');
                                    const nextMoviesList = newDoc.querySelector('.current-movies-section .movies-list');
                                    const nextPagination = newDoc.querySelector('.pagination-controls');
                                    
                                    if (nextMoviesList) {
                                        oldMoviesList.innerHTML = nextMoviesList.innerHTML;
                                    }
                                    if (nextPagination) {
                                        oldPagination.innerHTML = nextPagination.innerHTML;
                                    }
                                });
                            });
                        });
                    }
                })
                .catch(error => console.error('Pagination error:', error));
            });
        });
    }
});
