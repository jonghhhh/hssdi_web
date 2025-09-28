// HSSDI 웹사이트 공통 JavaScript

// 페이지 로딩 애니메이션
document.addEventListener('DOMContentLoaded', function() {
    // 페이지 요소들에 페이드인 효과 적용
    const elements = document.querySelectorAll('.card, .hero, .stats');

    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    elements.forEach(element => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(30px)';
        element.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(element);
    });
});

// 네비게이션 활성화 상태 관리
function setActiveNavigation() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav a');

    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === currentPath ||
            (currentPath.startsWith(link.getAttribute('href')) && link.getAttribute('href') !== '/')) {
            link.classList.add('active');
        }
    });
}

// 네비게이션 활성화 스타일 추가
document.addEventListener('DOMContentLoaded', function() {
    setActiveNavigation();

    // 활성화된 네비게이션 스타일
    const style = document.createElement('style');
    style.textContent = `
        .nav a.active {
            color: var(--light-brown) !important;
            font-weight: 600;
            border-bottom: 2px solid var(--light-brown);
            padding-bottom: 0.5rem;
        }
    `;
    document.head.appendChild(style);
});

// 검색 기능 개선
function enhanceSearch() {
    const searchForm = document.querySelector('form[method="GET"]');
    const searchInput = document.querySelector('input[name="search"]');

    if (searchInput) {
        // 검색어 하이라이트
        searchInput.addEventListener('input', function() {
            const query = this.value.toLowerCase();
            if (query.length > 2) {
                highlightSearchTerms(query);
            }
        });
    }
}

// 검색어 하이라이트 함수
function highlightSearchTerms(query) {
    const textElements = document.querySelectorAll('td, p, h1, h2, h3, h4');

    textElements.forEach(element => {
        if (element.children.length === 0) { // 텍스트만 있는 요소
            const text = element.textContent;
            const regex = new RegExp(`(${query})`, 'gi');
            if (regex.test(text)) {
                element.innerHTML = text.replace(regex, '<mark style="background: var(--warning); padding: 0.1rem 0.2rem; border-radius: 2px;">$1</mark>');
            }
        }
    });
}

// 폼 유효성 검사 개선
function enhanceFormValidation() {
    const forms = document.querySelectorAll('form');

    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;

            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    showFieldError(field, '이 필드는 필수입니다.');
                    isValid = false;
                } else {
                    clearFieldError(field);
                }
            });

            if (!isValid) {
                e.preventDefault();
            }
        });
    });
}

// 필드 오류 표시
function showFieldError(field, message) {
    clearFieldError(field);

    field.style.borderColor = 'var(--danger)';

    const errorDiv = document.createElement('div');
    errorDiv.className = 'field-error';
    errorDiv.style.color = 'var(--danger)';
    errorDiv.style.fontSize = '0.8rem';
    errorDiv.style.marginTop = '0.25rem';
    errorDiv.textContent = message;

    field.parentNode.appendChild(errorDiv);
}

// 필드 오류 제거
function clearFieldError(field) {
    field.style.borderColor = '';
    const existingError = field.parentNode.querySelector('.field-error');
    if (existingError) {
        existingError.remove();
    }
}

// 테이블 정렬 기능
function makeTablesSortable() {
    const tables = document.querySelectorAll('.table');

    tables.forEach(table => {
        const headers = table.querySelectorAll('th');

        headers.forEach((header, index) => {
            header.style.cursor = 'pointer';
            header.style.userSelect = 'none';

            header.addEventListener('click', function() {
                sortTable(table, index);
            });
        });
    });
}

// 테이블 정렬 함수
function sortTable(table, columnIndex) {
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));

    rows.sort((a, b) => {
        const aText = a.cells[columnIndex].textContent.trim();
        const bText = b.cells[columnIndex].textContent.trim();

        // 숫자인지 확인
        const aNum = parseFloat(aText);
        const bNum = parseFloat(bText);

        if (!isNaN(aNum) && !isNaN(bNum)) {
            return aNum - bNum;
        }

        // 날짜인지 확인
        const aDate = new Date(aText);
        const bDate = new Date(bText);

        if (!isNaN(aDate) && !isNaN(bDate)) {
            return aDate - bDate;
        }

        // 문자열 비교
        return aText.localeCompare(bText);
    });

    // 정렬된 행들을 다시 추가
    rows.forEach(row => tbody.appendChild(row));
}

// 반응형 테이블
function makeTablesResponsive() {
    const tables = document.querySelectorAll('.table');

    tables.forEach(table => {
        const wrapper = document.createElement('div');
        wrapper.style.overflowX = 'auto';
        wrapper.style.marginBottom = '1rem';

        table.parentNode.insertBefore(wrapper, table);
        wrapper.appendChild(table);

        table.style.minWidth = '600px';
    });
}

// 로딩 상태 관리
function showLoading() {
    const loading = document.createElement('div');
    loading.id = 'loading';
    loading.innerHTML = '<div class="spinner"></div>';
    loading.style.position = 'fixed';
    loading.style.top = '0';
    loading.style.left = '0';
    loading.style.width = '100%';
    loading.style.height = '100%';
    loading.style.background = 'rgba(255, 255, 255, 0.8)';
    loading.style.display = 'flex';
    loading.style.justifyContent = 'center';
    loading.style.alignItems = 'center';
    loading.style.zIndex = '9999';

    document.body.appendChild(loading);
}

function hideLoading() {
    const loading = document.getElementById('loading');
    if (loading) {
        loading.remove();
    }
}

// AJAX 요청 래퍼
function makeRequest(url, options = {}) {
    showLoading();

    return fetch(url, {
        headers: {
            'Content-Type': 'application/json',
            ...options.headers
        },
        ...options
    })
    .then(response => {
        hideLoading();
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .catch(error => {
        hideLoading();
        console.error('Request failed:', error);
        throw error;
    });
}

// 알림 메시지 표시
function showAlert(message, type = 'info') {
    const alert = document.createElement('div');
    alert.className = `alert alert-${type}`;
    alert.textContent = message;
    alert.style.position = 'fixed';
    alert.style.top = '20px';
    alert.style.right = '20px';
    alert.style.zIndex = '10000';
    alert.style.minWidth = '300px';
    alert.style.animation = 'slideInRight 0.3s ease';

    document.body.appendChild(alert);

    setTimeout(() => {
        alert.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => {
            alert.remove();
        }, 300);
    }, 5000);
}

// 애니메이션 CSS 추가
document.addEventListener('DOMContentLoaded', function() {
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideInRight {
            from { transform: translateX(100%); }
            to { transform: translateX(0); }
        }

        @keyframes slideOutRight {
            from { transform: translateX(0); }
            to { transform: translateX(100%); }
        }
    `;
    document.head.appendChild(style);
});

// 초기화
document.addEventListener('DOMContentLoaded', function() {
    enhanceSearch();
    enhanceFormValidation();
    makeTablesSortable();
    makeTablesResponsive();
});

// 유틸리티 함수들
const Utils = {
    formatDate: function(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('ko-KR');
    },

    formatNumber: function(num) {
        return num.toLocaleString('ko-KR');
    },

    truncateText: function(text, maxLength) {
        if (text.length <= maxLength) return text;
        return text.substr(0, maxLength) + '...';
    },

    debounce: function(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
};

// 전역으로 노출
window.HSSDI = {
    Utils,
    showAlert,
    makeRequest,
    showLoading,
    hideLoading
};