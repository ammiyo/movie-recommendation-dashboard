// ─────────────────────────────────────────────
// dashboard.js — Movie Analytics Dashboard
// ─────────────────────────────────────────────

// Shared Chart.js defaults for the dark theme
Chart.defaults.color = "#8b8fa8";
Chart.defaults.borderColor = "rgba(255,255,255,0.07)";
Chart.defaults.font.family = "'Inter', sans-serif";
Chart.defaults.font.size = 12;

// Cinema-themed color palette
const chartColors = {
    primary: "#e50914",  // Netflix red — bar charts
    secondary: "#ffb703",  // amber — highlights
    accent: "#219ebc",  // teal — line charts
    neutral: "#8ecae6",  // light blue — secondary lines
    muted: "#555",
};

// Legacy alias so existing code keeps working
const COLORS = {
    purple: chartColors.primary,
    teal: chartColors.accent,
    coral: "#ff6b6b",
    yellow: chartColors.secondary,
    blue: chartColors.neutral,
    pink: "#f472b6",
    orange: "#fb923c",
    green: "#4ade80",
};
const PALETTE = [
    chartColors.primary, chartColors.secondary, chartColors.accent,
    chartColors.neutral, "#fb923c", "#4ade80", "#f472b6", "#a78bfa",
];

// ── Gradient fill helper ────────────────────────────────────────────────────
function makeGradient(ctx, color) {
    const g = ctx.createLinearGradient(0, 0, 0, 300);
    g.addColorStop(0, color + "55");
    g.addColorStop(1, color + "00");
    return g;
}

// ── Fetch helper ────────────────────────────────────────────────────────────
async function fetchChartData(url) {
    const res = await fetch(url);
    if (!res.ok) throw new Error("API error " + res.status + " on " + url);
    return res.json();
}

// ── KPI Cards ───────────────────────────────────────────────────────────────
async function loadDashboardStats() {
    try {
        const data = await fetchChartData("/api/dashboard-stats");
        document.getElementById("totalMovies").innerText = data.total_movies.toLocaleString();
        document.getElementById("totalRatings").innerText = data.total_ratings.toLocaleString();
        document.getElementById("avgRating").innerText = data.avg_rating;
        document.getElementById("totalUsers").innerText = data.total_users.toLocaleString();
    } catch (e) { console.error("KPI error:", e); }
}

// ── Populate filter dropdowns ─────────────────────────────────────────────
async function loadFilters() {
    try {
        const yearsData = await fetchChartData("/api/movies-per-year");
        const genreData = await fetchChartData("/api/genre-popularity");
        const yearSelect = document.getElementById("yearFilter");
        const genreSelect = document.getElementById("genreFilter");
        yearsData.labels.slice().reverse().forEach(y => {
            const o = document.createElement("option");
            o.value = y; o.textContent = y; yearSelect.appendChild(o);
        });
        genreData.labels.forEach(g => {
            const o = document.createElement("option");
            o.value = g; o.textContent = g; genreSelect.appendChild(o);
        });
    } catch (e) { console.error("Filter error:", e); }
}

// ── Chart: Top Rated Movies ──────────────────────────────────────────────
async function renderTopRatedChart() {
    const data = await fetchChartData("/api/top-rated");
    new Chart(document.getElementById("topRatedChart"), {
        type: "bar",
        data: {
            labels: data.labels,
            datasets: [{
                label: "Avg Rating", data: data.values,
                backgroundColor: chartColors.primary + "cc",
                borderColor: chartColors.primary,
                borderWidth: 1.5, borderRadius: 4
            }]
        },
        options: {
            indexAxis: "y", responsive: true,
            plugins: { legend: { display: false } },
            scales: {
                x: { min: 3.5, grid: { color: "rgba(255,255,255,0.05)" } },
                y: { grid: { display: false } }
            }
        }
    });
}

// ── Chart: Most Rated Movies ─────────────────────────────────────────────
async function renderMostRatedChart() {
    const data = await fetchChartData("/api/most-rated");
    new Chart(document.getElementById("mostRatedChart"), {
        type: "bar",
        data: {
            labels: data.labels,
            datasets: [{
                label: "Rating Count", data: data.values,
                backgroundColor: chartColors.secondary + "cc",
                borderColor: chartColors.secondary,
                borderWidth: 1.5, borderRadius: 4
            }]
        },
        options: {
            indexAxis: "y", responsive: true,
            plugins: { legend: { display: false } },
            scales: {
                x: { grid: { color: "rgba(255,255,255,0.05)" } },
                y: { grid: { display: false } }
            }
        }
    });
}

// ── Chart: Genre Popularity (Doughnut) ───────────────────────────────────
async function renderGenreChart() {
    const data = await fetchChartData("/api/genre-popularity");
    new Chart(document.getElementById("genreChart"), {
        type: "doughnut",
        data: {
            labels: data.labels,
            datasets: [{
                data: data.values,
                backgroundColor: PALETTE.map(c => c + "cc"),
                borderColor: PALETTE, borderWidth: 1.5, hoverOffset: 8
            }]
        },
        options: {
            responsive: true, cutout: "60%",
            plugins: {
                legend: {
                    position: "right",
                    labels: { boxWidth: 12, padding: 10, font: { size: 11 } }
                }
            }
        }
    });
}

// ── Chart: Rating Distribution ───────────────────────────────────────────
async function renderRatingDistribution() {
    const data = await fetchChartData("/api/rating-distribution");
    new Chart(document.getElementById("ratingDistChart"), {
        type: "bar",
        data: {
            labels: data.labels.map(l => "★ " + l),
            datasets: [{
                label: "Number of Ratings", data: data.values,
                backgroundColor: [COLORS.coral + "cc", COLORS.orange + "cc",
                COLORS.yellow + "cc", COLORS.teal + "cc", COLORS.purple + "cc"],
                borderColor: [COLORS.coral, COLORS.orange, COLORS.yellow, COLORS.teal, COLORS.purple],
                borderWidth: 1.5, borderRadius: 6
            }]
        },
        options: {
            responsive: true, plugins: { legend: { display: false } },
            scales: {
                y: { grid: { color: "rgba(255,255,255,0.05)" } },
                x: { grid: { display: false } }
            }
        }
    });
}

// ── Chart: Ratings Over Time ─────────────────────────────────────────────
async function renderRatingsOverTime() {
    const data = await fetchChartData("/api/ratings-over-time");
    const ctx = document.getElementById("ratingsTimeChart");
    new Chart(ctx, {
        type: "line",
        data: {
            labels: data.labels,
            datasets: [{
                label: "Ratings", data: data.values,
                borderColor: chartColors.accent,
                backgroundColor: makeGradient(ctx.getContext("2d"), chartColors.accent),
                borderWidth: 2, pointRadius: 4, pointBackgroundColor: chartColors.accent,
                tension: 0.3, fill: true
            }]
        },
        options: {
            responsive: true, plugins: { legend: { display: false } },
            scales: {
                y: { grid: { color: "rgba(255,255,255,0.05)" } },
                x: { grid: { display: false } }
            }
        }
    });
}

// ── Chart: Top Users ─────────────────────────────────────────────────────
async function renderTopUsersChart() {
    const data = await fetchChartData("/api/top-users");
    new Chart(document.getElementById("topUsersChart"), {
        type: "bar",
        data: {
            labels: data.labels,
            datasets: [{
                label: "Ratings Given", data: data.values,
                backgroundColor: chartColors.secondary + "cc",
                borderColor: chartColors.secondary,
                borderWidth: 1.5, borderRadius: 4
            }]
        },
        options: {
            responsive: true, plugins: { legend: { display: false } },
            scales: {
                y: { grid: { color: "rgba(255,255,255,0.05)" } },
                x: { grid: { display: false }, ticks: { maxRotation: 30 } }
            }
        }
    });
}

// ── Chart: Avg Rating by Genre ───────────────────────────────────────────
async function renderAvgGenreChart() {
    const data = await fetchChartData("/api/avg-rating-genre");
    new Chart(document.getElementById("avgGenreChart"), {
        type: "bar",
        data: {
            labels: data.labels,
            datasets: [{
                label: "Avg Rating", data: data.values,
                backgroundColor: chartColors.primary + "cc",
                borderColor: chartColors.primary,
                borderWidth: 1.5, borderRadius: 4
            }]
        },
        options: {
            indexAxis: "y", responsive: true,
            plugins: { legend: { display: false } },
            scales: {
                x: { min: 3.0, grid: { color: "rgba(255,255,255,0.05)" } },
                y: { grid: { display: false } }
            }
        }
    });
}

// ── Chart: Movies Per Year ───────────────────────────────────────────────
async function renderMoviesPerYearChart() {
    const data = await fetchChartData("/api/movies-per-year");
    const ctx = document.getElementById("moviesYearChart");
    new Chart(ctx, {
        type: "line",
        data: {
            labels: data.labels,
            datasets: [{
                label: "Movies Released", data: data.values,
                borderColor: chartColors.neutral,
                backgroundColor: makeGradient(ctx.getContext("2d"), chartColors.neutral),
                borderWidth: 2, pointRadius: 3, pointBackgroundColor: chartColors.neutral,
                tension: 0.3, fill: true
            }]
        },
        options: {
            responsive: true, plugins: { legend: { display: false } },
            scales: {
                y: { grid: { color: "rgba(255,255,255,0.05)" } },
                x: { grid: { display: false }, ticks: { maxTicksLimit: 12, maxRotation: 45 } }
            }
        }
    });
}

// ── Movie Search ─────────────────────────────────────────────────────────
async function searchMovies() {
    const title = document.getElementById("movieSearch").value.trim();
    const year = document.getElementById("yearFilter").value.trim();
    const genre = document.getElementById("genreFilter").value.trim();

    const params = new URLSearchParams();
    if (title) params.append("title", title);
    if (year) params.append("year", year);
    if (genre) params.append("genre", genre);

    const panel = document.getElementById("searchResultsPanel");
    const body = document.getElementById("searchResultsBody");
    const count = document.getElementById("searchResultCount");
    const noRes = document.getElementById("searchNoResults");
    const table = body.closest("table");

    panel.style.display = "block";
    table.style.display = "table";
    noRes.style.display = "none";
    body.innerHTML = "<tr><td colspan='5' style='text-align:center;padding:24px;color:var(--text-muted);'>" +
        "<i class='bi bi-hourglass-split'></i> Searching...</td></tr>";
    panel.scrollIntoView({ behavior: "smooth", block: "start" });

    try {
        const data = await fetchChartData("/api/search-movies?" + params.toString());
        const movies = data.movies || [];
        count.textContent = movies.length + " result" + (movies.length !== 1 ? "s" : "");

        if (movies.length === 0) {
            table.style.display = "none";
            noRes.style.display = "block";
            body.innerHTML = "";
            return;
        }

        function ratingColor(r) {
            return r >= 4.0 ? "var(--accent-2)" : r >= 3.0 ? "var(--accent-4)" : "var(--accent-3)";
        }

        table.style.display = "table";
        noRes.style.display = "none";
        body.innerHTML = movies.map(function (m) {
            var tags = m.genres.split("|").map(function (g) {
                return "<span style='display:inline-block;background:rgba(108,99,255,.15);color:var(--accent-1);" +
                    "border-radius:4px;padding:2px 7px;font-size:.75rem;margin:2px;'>" + g + "</span>";
            }).join("");
            return "<tr style='border-color:var(--border);'>" +
                "<td style='padding:10px 12px;font-weight:500;'>" + m.title + "</td>" +
                "<td style='padding:10px 12px;'>" + tags + "</td>" +
                "<td style='padding:10px 12px;text-align:center;color:var(--text-muted);'>" + (m.release_year || "—") + "</td>" +
                "<td style='padding:10px 12px;text-align:center;font-weight:600;color:" + ratingColor(m.avg_rating) + ";'>★ " + m.avg_rating + "</td>" +
                "<td style='padding:10px 12px;text-align:center;color:var(--text-muted);'>" + m.rating_count.toLocaleString() + "</td>" +
                "</tr>";
        }).join("");
    } catch (e) {
        body.innerHTML = "<tr><td colspan='5' style='text-align:center;padding:24px;color:var(--accent-3);'>" +
            "<i class='bi bi-exclamation-triangle'></i> Search failed.</td></tr>";
        console.error("Search error:", e);
    }
}

// ── Movie Quick Insight ────────────────────────────────────────────────────
async function fetchInsight() {
    const title = document.getElementById("insightSearch").value.trim();
    if (!title) return;

    const result = document.getElementById("insightResult");
    const notFound = document.getElementById("insightNotFound");
    result.style.display = "none";
    notFound.style.display = "none";

    try {
        const res = await fetch("/api/movie-insight?" + new URLSearchParams({ title }));
        if (res.status === 404) {
            notFound.style.display = "block";
            return;
        }
        const d = await res.json();
        document.getElementById("insightTitle").innerText = d.title;
        document.getElementById("insightAvg").innerText = d.avg_rating + " ★";
        document.getElementById("insightCount").innerText = d.total_ratings.toLocaleString();
        document.getElementById("insightGenres").innerText = d.genres.split("|").join(" | ");
        document.getElementById("insightYear").innerText = d.release_year || "—";
        result.style.display = "block";
    } catch (e) {
        notFound.style.display = "block";
        console.error("Insight error:", e);
    }
}

// ── Filters init ─────────────────────────────────────────────────────────
function initFilters() {
    document.getElementById("searchBtn").addEventListener("click", searchMovies);

    document.getElementById("movieSearch").addEventListener("keydown", function (e) {
        if (e.key === "Enter") searchMovies();
    });
    document.getElementById("closeSearch").addEventListener("click", function () {
        document.getElementById("searchResultsPanel").style.display = "none";
    });
    document.getElementById("resetFilters").addEventListener("click", function () {
        document.getElementById("movieSearch").value = "";
        document.getElementById("yearFilter").value = "";
        document.getElementById("genreFilter").value = "";
        document.getElementById("searchResultsPanel").style.display = "none";
    });
    document.getElementById("insightBtn").addEventListener("click", fetchInsight);
    document.getElementById("insightSearch").addEventListener("keydown", function (e) {
        if (e.key === "Enter") fetchInsight();
    });
}

// ── Entry point ──────────────────────────────────────────────────────────
async function loadDashboard() {
    try {
        // Set last-updated timestamp
        const el = document.getElementById("updateTime");
        if (el) el.innerText = "Last updated: " + new Date().toLocaleString();

        await Promise.all([
            loadDashboardStats(),
            loadFilters(),
            renderTopRatedChart(),
            renderMostRatedChart(),
            renderGenreChart(),
            renderRatingDistribution(),
            renderRatingsOverTime(),
            renderTopUsersChart(),
            renderAvgGenreChart(),
            renderMoviesPerYearChart(),
        ]);
        initFilters();
        console.log("Dashboard loaded successfully.");
    } catch (e) {
        console.error("Dashboard load error:", e);
    }
}

window.onload = loadDashboard;
