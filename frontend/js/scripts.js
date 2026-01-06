// ---------- Config ----------
const API_BASE = "http://127.0.0.1:8000"; // FastAPI backend URL
const USER_ID = 1; // Replace with logged-in user ID

// ---------- Fetch Courses ----------
async function fetchCourses() {
    const res = await fetch(`${API_BASE}/courses`);
    const courses = await res.json();
    return courses;
}

// ---------- Fetch Modules ----------
async function fetchModules(course_id) {
    const res = await fetch(`${API_BASE}/courses/${course_id}/modules`);
    const modules = await res.json();
    return modules;
}

// ---------- Fetch Topics ----------
async function fetchTopics(module_id) {
    const res = await fetch(`${API_BASE}/modules/${module_id}/topics`);
    const topics = await res.json();
    return topics;
}

// ---------- Submit Quiz ----------
async function submitQuiz(topic_id, answers) {
    // Compute score using classical logic (example)
    let score = 0;
    if (answers.q1 && answers.q1.toLowerCase().includes("python")) score += 50;
    if (answers.q2 && parseInt(answers.q2) === 4) score += 50;

    const res = await fetch(`${API_BASE}/quiz/submit`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id: USER_ID, topic_id, score })
    });

    const data = await res.json();
    return { score, data };
}

// ---------- Fetch Recommendations ----------
async function fetchRecommendations() {
    const res = await fetch(`${API_BASE}/recommendations/${USER_ID}`);
    const recommendations = await res.json();
    return recommendations;
}

// ---------- Fetch Weak Topics ----------
async
