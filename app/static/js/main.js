const AUTH_API = "/api/v1/auth";
const QUOTE_API = "/api/v1/quotes";
const QUESTION_API = "/api/v1/questions";
const DIARY_API = "/diaries";

let accessToken = sessionStorage.getItem("token");
let currentQuoteId = null;
let myBookmarks = [];

window.addEventListener('DOMContentLoaded', () => {
    if (accessToken) {
        showDashboard();
        initDashboard();
    }
});

// --- [추가] 비밀번호 실시간 검증 ---
function validatePassword() {
    const pwInput = document.getElementById('password');
    const pwHint = document.getElementById('pw-hint');
    const isLoginMode = document.getElementById('auth-title').innerText === "로그인";

    // 회원가입 모드일 때만 8자 미만 경고 표시
    if (!isLoginMode && pwInput.value.length > 0 && pwInput.value.length < 8) {
        pwHint.classList.remove('hidden');
    } else {
        pwHint.classList.add('hidden');
    }
}

// --- [추가] 로그인/회원가입 전환 ---
function toggleAuth() {
    const isLoginMode = document.getElementById('auth-title').innerText === "로그인";

    document.getElementById('auth-title').innerText = isLoginMode ? "회원가입" : "로그인";
    document.getElementById('auth-switch-text').innerText = isLoginMode ? "이미 계정이 있으신가요?" : "계정이 없으신가요?";
    document.getElementById('auth-switch-link').innerText = isLoginMode ? "로그인하기" : "회원가입";

    document.getElementById('username').classList.toggle('hidden', !isLoginMode);
    document.getElementById('login-btn').classList.toggle('hidden', isLoginMode);
    document.getElementById('signup-btn').classList.toggle('hidden', !isLoginMode);

    // 폼 초기화
    document.getElementById('password').value = "";
    document.getElementById('pw-hint').classList.add('hidden');
}

// --- 인증 (로그인/회원가입) 기능 ---
async function login() {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    if (!email || !password) {
        alert("아이디와 비밀번호를 입력해주세요.");
        return;
    }

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
            accessToken = data.access_token;
            showDashboard();
            initDashboard();
        } else {
            alert("로그인에 실패했습니다. 정보를 확인해주세요.");
        }
    } catch (e) { console.error(e); }
}

async function signup() {
    const userId = document.getElementById('email').value;
    const userName = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    if (!userId || !userName || !password) {
        alert("모든 필드를 입력해주세요.");
        return;
    }

    // [중요] 8글자 미만일 시 가입 차단 및 안내
    if (password.length < 8) {
        alert("비밀번호를 8자 이상으로 설정해주세요.");
        document.getElementById('password').focus();
        return;
    }

    try {
        const res = await fetch(`${AUTH_API}/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                user_id: userId,
                user_name: userName,
                pwd_hash: password
            })
        });

        if (res.ok) {
            alert("회원가입이 완료되었습니다! 로그인해주세요.");
            toggleAuth();
        } else {
            const err = await res.json();
            alert("가입 실패: " + (err.detail || "오류가 발생했습니다."));
        }
    } catch (e) { console.error(e); }
}

// --- 메인 기능 (명언, 북마크, 일기) ---
async function initDashboard() {
    await fetchBookmarks();
    fetchQuote();
    fetchQuestion();
    fetchDiaries();
}

async function fetchQuote() {
    const headers = { 'Authorization': `Bearer ${accessToken}` };
    try {
        const res = await fetch(`${QUOTE_API}/random`, { headers });
        if (res.ok) {
            const data = await res.json();
            currentQuoteId = data.id;
            document.getElementById('quote-box').innerText = `${data.content} - ${data.author}`;
            updateBookmarkIconUI();
        }
    } catch (e) { console.error(e); }
}

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
    const headers = { 'Authorization': `Bearer ${accessToken}` };
    try {
        const res = await fetch(`${QUOTE_API}/bookmarks/${quoteId}`, { method: 'POST', headers });
        if (res.ok) await fetchBookmarks();
    } catch (e) { console.error(e); }
}

async function removeBookmark(quoteId) {
    const headers = { 'Authorization': `Bearer ${accessToken}` };
    try {
        const res = await fetch(`${QUOTE_API}/bookmarks/${quoteId}`, { method: 'DELETE', headers });
        if (res.ok) await fetchBookmarks();
    } catch (e) { console.error(e); }
}

async function fetchBookmarks() {
    const headers = { 'Authorization': `Bearer ${accessToken}` };
    try {
        const res = await fetch(`${QUOTE_API}/bookmarks`, { headers });
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
        <div class="p-3 bg-white rounded-lg border border-indigo-50 shadow-sm mb- group relative">
            <div class="pr-6">
                <p class="text-xs text-gray-700 leading-snug">"${q.content}"</p>
                <p class="text-[10px] text-indigo-400 mt-1 font-bold">- ${q.author}</p>
            </div>
            <button onclick="removeBookmark(${q.id})" class="absolute top-2 right-2 text-gray-300 hover:text-red-500">
                <i data-lucide="x-circle" class="w-4 h-4"></i>
            </button>
        </div>
    `).join('');
    lucide.createIcons();
}

// --- 일기 및 기타 유틸리티 (이전과 동일) ---
async function fetchDiaries() {
    const res = await fetch(DIARY_API, { headers: { 'Authorization': `Bearer ${accessToken}` } });
    if (res.ok) {
        const diaries = await res.json();
        const list = document.getElementById('diary-list');
        list.innerHTML = diaries.length === 0 ? '<p class="text-center text-gray-400 py-10">첫 일기를 기록해보세요.</p>' :
            diaries.map(d => `
                <div class="p-5 border rounded-xl bg-white group hover:shadow-md transition mb-4">
                    <div class="flex justify-between items-start">
                        <h4 class="font-bold text-gray-800">${d.title}</h4>
                        <div class="flex gap-3 opacity-0 group-hover:opacity-100 transition">
                            <button onclick='setupEditDiary(${JSON.stringify(d).replace(/'/g, "&apos;")})' class="text-blue-500 text-xs font-bold">수정</button>
                            <button onclick="deleteDiary(${d.id})" class="text-red-400 text-xs font-bold">삭제</button>
                        </div>
                    </div>
                    <p class="text-gray-600 mt-2 text-sm whitespace-pre-wrap">${d.content}</p>
                </div>`).join('');
    }
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

async function saveDiary() {
    const id = document.getElementById('edit-diary-id').value;
    const title = document.getElementById('diary-title').value;
    const content = document.getElementById('diary-content').value;
    if (!title || !content) return;
    const method = id ? 'PUT' : 'POST';
    const url = id ? `${DIARY_API}/${id}` : DIARY_API;
    const res = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${accessToken}` },
        body: JSON.stringify({ title, content })
    });
    if (res.ok) { clearDiaryForm(); fetchDiaries(); }
}

async function deleteDiary(id) {
    if (!confirm("삭제하시겠습니까?")) return;
    await fetch(`${DIARY_API}/${id}`, { method: 'DELETE', headers: { 'Authorization': `Bearer ${accessToken}` } });
    fetchDiaries();
}

async function fetchQuestion() {
    const res = await fetch(`${QUESTION_API}/random`, { headers: { 'Authorization': `Bearer ${accessToken}` } });
    if (res.ok) {
        const data = await res.json();
        document.getElementById('question-box').innerText = data.question_text;
    }
}

function showDashboard() {
    document.getElementById('auth-section').classList.add('hidden');
    document.getElementById('main-section').classList.remove('hidden');
    lucide.createIcons();
}

function logout() { sessionStorage.clear(); location.reload(); }