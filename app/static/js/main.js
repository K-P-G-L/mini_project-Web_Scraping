const AUTH_API = "/api/v1/auth";
const QUOTE_API = "/api/v1/quotes";
const QUESTION_API = "/api/v1/questions";
const DIARY_API = "/diaries";

// [중요] 토큰을 항상 최신 상태로 가져오기 위한 함수
function getAuthHeader() {
    const token = sessionStorage.getItem("token");
    return token ? { 'Authorization': `Bearer ${token}` } : {};
}

// 전역 변수 초기화
let currentQuoteId = null;
let myBookmarks = [];

window.addEventListener('DOMContentLoaded', () => {
    const token = sessionStorage.getItem("token");
    if (token) {
        showDashboard();
        initDashboard();
    }
});

// --- [인증] 로그인 / 회원가입 ---
function validatePassword() {
    const pwInput = document.getElementById('password');
    const pwHint = document.getElementById('pw-hint');
    const isLoginMode = document.getElementById('auth-title').innerText === "로그인";
    if (!isLoginMode && pwInput.value.length > 0 && pwInput.value.length < 8) {
        pwHint.classList.remove('hidden');
    } else {
        pwHint.classList.add('hidden');
    }
}

function toggleAuth() {
    const isLoginMode = document.getElementById('auth-title').innerText === "로그인";
    document.getElementById('auth-title').innerText = isLoginMode ? "회원가입" : "로그인";
    document.getElementById('auth-switch-text').innerText = isLoginMode ? "이미 계정이 있으신가요?" : "계정이 없으신가요?";
    document.getElementById('auth-switch-link').innerText = isLoginMode ? "로그인하기" : "회원가입";
    document.getElementById('username').classList.toggle('hidden', !isLoginMode);
    document.getElementById('login-btn').classList.toggle('hidden', isLoginMode);
    document.getElementById('signup-btn').classList.toggle('hidden', !isLoginMode);
    document.getElementById('password').value = "";
    document.getElementById('pw-hint').classList.add('hidden');
}

async function login() {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    if (!email || !password) { alert("아이디와 비밀번호를 입력해주세요."); return; }

    const formData = new URLSearchParams();
    formData.append('username', email);
    formData.append('password', password);

    try {
        const res = await fetch(`${AUTH_API}/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: formData
        });

        if (res.ok) {
            const data = await res.json();
            sessionStorage.setItem("token", data.access_token);
            showDashboard();
            initDashboard();
        } else {
            alert("로그인 실패: 정보를 확인하세요.");
        }
    } catch (e) { console.error(e); }
}

async function signup() {
    const userId = document.getElementById('email').value;
    const userName = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    if (!userId || !userName || !password) { alert("모든 필드를 입력해주세요."); return; }
    if (password.length < 8) { alert("비밀번호를 8자 이상으로 설정해주세요."); return; }

    try {
        const res = await fetch(`${AUTH_API}/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user_id: userId, user_name: userName, pwd_hash: password })
        });
        if (res.ok) { alert("회원가입 완료! 로그인해주세요."); toggleAuth(); }
        else { const err = await res.json(); alert("가입 실패: " + (err.detail || "오류 발생")); }
    } catch (e) { console.error(e); }
}

// --- [대시보드] 초기화 및 데이터 로드 ---
async function initDashboard() {
    await fetchBookmarks(); // 북마크 상태를 먼저 알아야함
    await fetchQuote();
    fetchQuestion();
    fetchDiaries();
}

async function fetchQuote() {
    try {
        const res = await fetch(`${QUOTE_API}/random`, { headers: getAuthHeader() });
        if (res.ok) {
            const data = await res.json();
            currentQuoteId = data.id;
            document.getElementById('quote-box').innerText = `${data.content} - ${data.author}`;
            updateBookmarkIconUI();
        } else if (res.status === 401) { logout(); } // 401 뜨면 로그아웃
    } catch (e) { console.error(e); }
}

// --- [북마크] 기능 (401 방지 로직 적용) ---
async function toggleBookmark() {
    if (!currentQuoteId) return;
    const isBookmarked = myBookmarks.some(q => q.id === currentQuoteId);
    if (isBookmarked) {
        await removeBookmark(currentQuoteId);
    } else {
        await addBookmark(currentQuoteId);
    }
}

async function addBookmark(quoteId) {
    try {
        const res = await fetch(`${QUOTE_API}/bookmarks/${quoteId}`, {
            method: 'POST',
            headers: getAuthHeader()
        });
        if (res.ok) await fetchBookmarks();
    } catch (e) { console.error(e); }
}

async function removeBookmark(quoteId) {
    try {
        const res = await fetch(`${QUOTE_API}/bookmarks/${quoteId}`, {
            method: 'DELETE',
            headers: getAuthHeader()
        });
        if (res.ok) await fetchBookmarks();
    } catch (e) { console.error(e); }
}

async function fetchBookmarks() {
    try {
        const res = await fetch(`${QUOTE_API}/bookmarks`, { headers: getAuthHeader() });
        if (res.ok) {
            myBookmarks = await res.json();
            renderBookmarkList();
            updateBookmarkIconUI();
        }
    } catch (e) { console.error(e); }
}

function updateBookmarkIconUI() {
    const icon = document.getElementById('bookmark-icon');
    if (!icon) return;
    const isSaved = myBookmarks.some(q => q.id === currentQuoteId);
    if (isSaved) {
        icon.classList.add('fill-yellow-400', 'text-yellow-400');
        icon.classList.remove('text-gray-400');
    } else {
        icon.classList.remove('fill-yellow-400', 'text-yellow-400');
        icon.classList.add('text-gray-400');
    }
}

function renderBookmarkList() {
    const list = document.getElementById('bookmark-list');
    if (!list) return;
    if (myBookmarks.length === 0) {
        list.innerHTML = `<p class="text-gray-400 italic">저장된 명언이 없습니다.</p>`;
        return;
    }
    list.innerHTML = myBookmarks.map(q => `
        <div class="p-3 bg-white rounded-lg border border-indigo-50 shadow-sm mb-2 group relative">
            <div class="pr-6">
                <p class="text-xs text-gray-700 leading-snug">"${q.content}"</p>
                <p class="text-[10px] text-indigo-400 mt-1 font-bold">- ${q.author}</p>
            </div>
            <button onclick="removeBookmark(${q.id})" class="absolute top-2 right-2 text-gray-300 hover:text-red-500 transition-colors">
                <i data-lucide="x-circle" class="w-4 h-4"></i>
            </button>
        </div>`).join('');
    lucide.createIcons();
}

// --- [일기] 저장 및 목록 (디자인 개선 통합) ---
async function fetchDiaries() {
    try {
        const res = await fetch(DIARY_API, { headers: getAuthHeader() });
        if (res.ok) {
            const diaries = await res.json();
            const list = document.getElementById('diary-list');
            if (diaries.length === 0) {
                list.innerHTML = '<p class="text-center text-gray-400 py-10">첫 일기를 기록해보세요.</p>';
                return;
            }
            list.innerHTML = diaries.map(d => `
                <div class="p-4 border border-gray-100 rounded-xl bg-white group hover:shadow-md transition-all mb-3 relative">
                    <div class="flex justify-between items-start mb-2">
                        <h4 class="font-bold text-gray-800 text-base tracking-tight pr-12 truncate">${d.title}</h4>
                        <div class="flex gap-2 shrink-0">
                            <button onclick='setupEditDiary(${JSON.stringify(d).replace(/'/g, "&apos;")})' class="text-gray-300 hover:text-indigo-500">
                                <i data-lucide="edit-3" class="w-4 h-4"></i>
                            </button>
                            <button onclick="deleteDiary(${d.id})" class="text-gray-300 hover:text-red-400">
                                <i data-lucide="trash-2" class="w-4 h-4"></i>
                            </button>
                        </div>
                    </div>
                    <p class="text-gray-600 text-sm whitespace-pre-wrap leading-relaxed mb-3">${d.content}</p>
                    <div class="flex items-center gap-1 text-[10px] text-gray-300 font-medium tracking-tighter">
                        <i data-lucide="calendar" class="w-3 h-3"></i>
                        <span>${new Date(d.created_at).toLocaleString()}</span>
                    </div>
                </div>`).join('');
            lucide.createIcons();
        }
    } catch (e) { console.error(e); }
}

async function saveDiary() {
    const id = document.getElementById('edit-diary-id').value;
    const title = document.getElementById('diary-title').value;
    const content = document.getElementById('diary-content').value;

    if (!title || !content) { alert("제목과 내용을 모두 입력해주세요."); return; }

    const method = id ? 'PUT' : 'POST';
    const url = id ? `${DIARY_API}/${id}` : DIARY_API;

    try {
        const res = await fetch(url, {
            method,
            headers: { 'Content-Type': 'application/json', ...getAuthHeader() },
            body: JSON.stringify({ title, content })
        });
        if (res.ok) { clearDiaryForm(); await fetchDiaries(); }
        else { alert("저장에 실패했습니다."); }
    } catch (e) { console.error(e); }
}

function setupEditDiary(diary) {
    document.getElementById('diary-form-title').innerText = "일기 수정";
    document.getElementById('edit-diary-id').value = diary.id;
    document.getElementById('diary-title').value = diary.title;
    document.getElementById('diary-content').value = diary.content;
    document.getElementById('save-diary-btn').innerText = "수정 완료";
    document.getElementById('cancel-edit-btn').classList.remove('hidden');
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function clearDiaryForm() {
    document.getElementById('diary-form-title').innerText = "기록하기";
    document.getElementById('edit-diary-id').value = "";
    document.getElementById('diary-title').value = "";
    document.getElementById('diary-content').value = "";
    document.getElementById('save-diary-btn').innerText = "저장하기";
    document.getElementById('cancel-edit-btn').classList.add('hidden');
}

async function deleteDiary(id) {
    if (!confirm("삭제하시겠습니까?")) return;
    const res = await fetch(`${DIARY_API}/${id}`, { method: 'DELETE', headers: getAuthHeader() });
    if (res.ok) fetchDiaries();
}

async function fetchQuestion() {
    try {
        const res = await fetch(`${QUESTION_API}/random`, { headers: getAuthHeader() });
        if (res.ok) {
            const data = await res.json();
            document.getElementById('question-box').innerText = data.question_text;
        }
    } catch (e) { console.error(e); }
}

function showDashboard() {
    document.getElementById('auth-section').classList.add('hidden');
    document.getElementById('main-section').classList.remove('hidden');
    lucide.createIcons();
}

function logout() { sessionStorage.clear(); location.reload(); }