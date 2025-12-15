// Dream Journal - Main JavaScript Application

const API_BASE = '/api';
let currentEntry = null;
let currentPage = 1;
let allTags = [];

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    console.log('Dream Journal initialized');
    
    // Set default date to now
    const now = new Date();
    now.setMinutes(now.getMinutes() - now.getTimezoneOffset());
    document.getElementById('entry-date').value = now.toISOString().slice(0, 16);
    
    // Sleep quality slider
    document.getElementById('sleep-quality').addEventListener('input', (e) => {
        document.getElementById('sleep-quality-value').textContent = e.target.value;
    });
    
    // Load initial data
    loadDashboard();
    loadTags();
    
    // Search functionality
    document.getElementById('search-entries')?.addEventListener('input', debounce(loadEntries, 500));
    document.getElementById('filter-tag')?.addEventListener('change', loadEntries);
});

// ========== Navigation ==========

function showSection(section) {
    // Hide all sections
    document.querySelectorAll('.content-section').forEach(el => {
        el.style.display = 'none';
    });
    
    // Show selected section
    document.getElementById(`${section}-section`).style.display = 'block';
    
    // Update nav links
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
    });
    event.target.classList.add('active');
    
    // Load section data
    if (section === 'dashboard') {
        loadDashboard();
    } else if (section === 'entries') {
        loadEntries();
    } else if (section === 'insights') {
        loadSummaries();
    }
}

// ========== Dashboard Functions ==========

async function loadDashboard() {
    try {
        // Load overview stats
        const overview = await fetch(`${API_BASE}/analytics/overview?days=30`).then(r => r.json());
        
        document.getElementById('total-entries').textContent = overview.total_entries;
        document.getElementById('avg-sentiment').textContent = overview.avg_sentiment.toFixed(2);
        document.getElementById('dominant-emotion').textContent = 
            overview.dominant_emotion.charAt(0).toUpperCase() + overview.dominant_emotion.slice(1);
        document.getElementById('stress-trend').textContent = 
            overview.stress_trend.charAt(0).toUpperCase() + overview.stress_trend.slice(1);
        
        // Load charts
        await loadCharts();
        
    } catch (error) {
        console.error('Error loading dashboard:', error);
        showNotification('Error loading dashboard', 'danger');
    }
}

async function loadCharts() {
    try {
        // Get timeline data
        const timeline = await fetch(`${API_BASE}/analytics/timeline?days=30`).then(r => r.json());
        
        if (timeline.length > 0) {
            createEmotionTimeline(timeline);
            createStressTrendChart(timeline);
        }
        
        // Get theme data
        const themes = await fetch(`${API_BASE}/analytics/themes?days=90`).then(r => r.json());
        if (themes.themes.length > 0) {
            createThemeChart(themes.themes);
        }
        
        // Get entries for other charts
        const entries = await fetch(`${API_BASE}/entries?per_page=100`).then(r => r.json());
        if (entries.entries.length > 0) {
            createEmotionDistribution(entries.entries);
            createCalendarHeatmap(entries.entries);
        }
        
    } catch (error) {
        console.error('Error loading charts:', error);
    }
}

function createEmotionTimeline(timeline) {
    const emotions = ['joy', 'sadness', 'fear', 'anger', 'surprise', 'disgust', 'trust', 'anticipation'];
    const colors = {
        'joy': '#FFD700',
        'sadness': '#4169E1',
        'fear': '#8B008B',
        'anger': '#DC143C',
        'surprise': '#FF69B4',
        'disgust': '#556B2F',
        'trust': '#00CED1',
        'anticipation': '#FFA500'
    };
    
    const traces = emotions.map(emotion => ({
        x: timeline.map(t => t.date),
        y: timeline.map(t => t.emotions[emotion] || 0),
        name: emotion.charAt(0).toUpperCase() + emotion.slice(1),
        type: 'scatter',
        mode: 'lines+markers',
        line: { color: colors[emotion] },
        opacity: 0.7
    }));
    
    // Add sentiment line
    traces.push({
        x: timeline.map(t => t.date),
        y: timeline.map(t => t.sentiment),
        name: 'Sentiment',
        type: 'scatter',
        mode: 'lines',
        line: { color: 'black', width: 3, dash: 'dash' },
        yaxis: 'y2'
    });
    
    const layout = {
        title: 'Emotion Timeline',
        xaxis: { title: 'Date' },
        yaxis: { title: 'Emotion Score' },
        yaxis2: {
            title: 'Sentiment',
            overlaying: 'y',
            side: 'right'
        },
        hovermode: 'x unified',
        height: 500
    };
    
    Plotly.newPlot('emotion-timeline', traces, layout);
}

function createEmotionDistribution(entries) {
    const emotionTotals = {
        joy: 0, sadness: 0, fear: 0, anger: 0,
        surprise: 0, disgust: 0, trust: 0, anticipation: 0
    };
    
    entries.forEach(entry => {
        if (entry.emotions) {
            Object.keys(entry.emotions).forEach(emotion => {
                if (emotionTotals.hasOwnProperty(emotion)) {
                    emotionTotals[emotion] += entry.emotions[emotion];
                }
            });
        }
    });
    
    const colors = ['#FFD700', '#4169E1', '#8B008B', '#DC143C', '#FF69B4', '#556B2F', '#00CED1', '#FFA500'];
    
    const data = [{
        values: Object.values(emotionTotals),
        labels: Object.keys(emotionTotals).map(e => e.charAt(0).toUpperCase() + e.slice(1)),
        type: 'pie',
        marker: { colors: colors },
        hole: 0.3
    }];
    
    const layout = {
        title: 'Emotion Distribution',
        height: 400
    };
    
    Plotly.newPlot('emotion-distribution', data, layout);
}

function createStressTrendChart(timeline) {
    const data = [{
        x: timeline.map(t => t.date),
        y: timeline.map(t => t.stress),
        name: 'Stress Level',
        type: 'scatter',
        mode: 'markers',
        marker: { color: 'rgba(255, 0, 0, 0.5)', size: 8 }
    }];
    
    // Calculate moving average
    const windowSize = 7;
    const movingAvg = [];
    for (let i = 0; i < timeline.length; i++) {
        const start = Math.max(0, i - windowSize + 1);
        const window = timeline.slice(start, i + 1);
        const avg = window.reduce((sum, t) => sum + t.stress, 0) / window.length;
        movingAvg.push(avg);
    }
    
    data.push({
        x: timeline.map(t => t.date),
        y: movingAvg,
        name: '7-Day Average',
        type: 'scatter',
        mode: 'lines',
        line: { color: 'red', width: 2 }
    });
    
    const layout = {
        title: 'Stress Level Trend',
        xaxis: { title: 'Date' },
        yaxis: { title: 'Stress Level', range: [0, 1] },
        height: 400
    };
    
    Plotly.newPlot('stress-trend-chart', data, layout);
}

function createThemeChart(themes) {
    const data = [{
        x: themes.map(t => t.name),
        y: themes.map(t => t.count),
        type: 'bar',
        marker: { color: 'indianred' }
    }];
    
    const layout = {
        title: 'Top Dream Themes',
        xaxis: { title: 'Theme' },
        yaxis: { title: 'Frequency' },
        height: 400
    };
    
    Plotly.newPlot('theme-chart', data, layout);
}

function createCalendarHeatmap(entries) {
    const dateIntensity = {};
    
    entries.forEach(entry => {
        const date = entry.dream_date.split('T')[0];
        if (!dateIntensity[date] || entry.dream_intensity > dateIntensity[date]) {
            dateIntensity[date] = entry.dream_intensity;
        }
    });
    
    const data = [{
        x: Object.keys(dateIntensity),
        y: Array(Object.keys(dateIntensity).length).fill(1),
        mode: 'markers',
        type: 'scatter',
        marker: {
            size: 20,
            color: Object.values(dateIntensity),
            colorscale: 'YlOrRd',
            showscale: true,
            colorbar: { title: 'Intensity' },
            cmin: 0,
            cmax: 1
        },
        text: Object.entries(dateIntensity).map(([d, i]) => `Date: ${d}<br>Intensity: ${i.toFixed(2)}`),
        hovertemplate: '%{text}<extra></extra>'
    }];
    
    const layout = {
        title: 'Dream Activity Calendar',
        xaxis: { title: 'Date' },
        yaxis: { visible: false },
        height: 200
    };
    
    Plotly.newPlot('calendar-heatmap', data, layout);
}

// ========== Entry Functions ==========

async function loadEntries(page = 1) {
    try {
        currentPage = page;
        const searchTerm = document.getElementById('search-entries')?.value || '';
        const filterTag = document.getElementById('filter-tag')?.value || '';
        
        let url = `${API_BASE}/entries?page=${page}`;
        if (filterTag) url += `&tag=${filterTag}`;
        
        const response = await fetch(url).then(r => r.json());
        const entryList = document.getElementById('entries-list');
        
        if (response.entries.length === 0) {
            entryList.innerHTML = `
                <div class="col-12">
                    <div class="empty-state">
                        <h4>No dream entries yet</h4>
                        <p>Start recording your dreams to unlock insights</p>
                    </div>
                </div>
            `;
            return;
        }
        
        // Filter by search term (client-side)
        let entries = response.entries;
        if (searchTerm) {
            entries = entries.filter(e => 
                (e.title && e.title.toLowerCase().includes(searchTerm.toLowerCase())) ||
                e.content.toLowerCase().includes(searchTerm.toLowerCase())
            );
        }
        
        entryList.innerHTML = entries.map(entry => createEntryCard(entry)).join('');
        
        // Update pagination
        updatePagination(response.pages, currentPage);
        
    } catch (error) {
        console.error('Error loading entries:', error);
        showNotification('Error loading entries', 'danger');
    }
}

function createEntryCard(entry) {
    const date = new Date(entry.dream_date).toLocaleDateString();
    const sentiment = getSentimentLabel(entry.sentiment_score);
    const topEmotion = getTopEmotion(entry.emotions);
    
    return `
        <div class="col-md-6 col-lg-4 mb-3 fade-in">
            <div class="card dream-entry-card" onclick="viewEntry(${entry.id})">
                <div class="dream-entry-header">
                    <h5 class="mb-1">${entry.title || 'Untitled Dream'}</h5>
                    <small>${date}</small>
                </div>
                <div class="dream-entry-content">
                    <p>${entry.content.substring(0, 150)}${entry.content.length > 150 ? '...' : ''}</p>
                    
                    <div class="mb-2">
                        <span class="sentiment-indicator sentiment-${sentiment.class}">
                            ${sentiment.label}
                        </span>
                        ${topEmotion ? `<span class="emotion-badge emotion-${topEmotion}">${topEmotion}</span>` : ''}
                    </div>
                    
                    ${entry.tags && entry.tags.length > 0 ? `
                        <div class="mb-2">
                            ${entry.tags.map(tag => `<span class="tag">${tag}</span>`).join('')}
                        </div>
                    ` : ''}
                    
                    <div class="stress-bar">
                        <div class="stress-fill ${getStressClass(entry.stress_level)}" 
                             style="width: ${(entry.stress_level * 100)}%"></div>
                    </div>
                    <small class="text-muted">Stress: ${(entry.stress_level * 100).toFixed(0)}%</small>
                </div>
            </div>
        </div>
    `;
}

function getSentimentLabel(score) {
    if (score > 0.3) return { label: 'Positive', class: 'positive' };
    if (score < -0.3) return { label: 'Negative', class: 'negative' };
    return { label: 'Neutral', class: 'neutral' };
}

function getTopEmotion(emotions) {
    if (!emotions || Object.keys(emotions).length === 0) return null;
    
    return Object.entries(emotions)
        .filter(([_, score]) => score > 0)
        .sort((a, b) => b[1] - a[1])[0]?.[0];
}

function getStressClass(level) {
    if (level < 0.3) return 'stress-low';
    if (level < 0.7) return 'stress-medium';
    return 'stress-high';
}

function updatePagination(totalPages, current) {
    const pagination = document.getElementById('entries-pagination');
    let html = '';
    
    for (let i = 1; i <= totalPages; i++) {
        html += `
            <li class="page-item ${i === current ? 'active' : ''}">
                <a class="page-link" href="#" onclick="loadEntries(${i}); return false;">${i}</a>
            </li>
        `;
    }
    
    pagination.innerHTML = html;
}

// ========== Entry Modal Functions ==========

function showNewEntryModal() {
    document.getElementById('entry-form').reset();
    document.getElementById('entry-id').value = '';
    document.getElementById('entryModalLabel').textContent = 'New Dream Entry';
    
    const now = new Date();
    now.setMinutes(now.getMinutes() - now.getTimezoneOffset());
    document.getElementById('entry-date').value = now.toISOString().slice(0, 16);
    
    const modal = new bootstrap.Modal(document.getElementById('entryModal'));
    modal.show();
}

async function saveEntry() {
    const entryId = document.getElementById('entry-id').value;
    const title = document.getElementById('entry-title').value;
    const content = document.getElementById('entry-content').value;
    const dreamDate = document.getElementById('entry-date').value;
    const tags = document.getElementById('entry-tags').value.split(',').map(t => t.trim()).filter(t => t);
    const sleepQuality = parseInt(document.getElementById('sleep-quality').value);
    
    if (!content) {
        showNotification('Please enter dream content', 'warning');
        return;
    }
    
    const data = {
        title: title || null,
        content,
        dream_date: dreamDate,
        tags,
        sleep_quality: sleepQuality
    };
    
    try {
        const url = entryId ? `${API_BASE}/entries/${entryId}` : `${API_BASE}/entries`;
        const method = entryId ? 'PUT' : 'POST';
        
        const response = await fetch(url, {
            method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        if (response.ok) {
            showNotification(entryId ? 'Entry updated!' : 'Dream saved & analyzed!', 'success');
            bootstrap.Modal.getInstance(document.getElementById('entryModal')).hide();
            loadEntries(currentPage);
            loadDashboard();
            loadTags();
        } else {
            throw new Error('Failed to save entry');
        }
    } catch (error) {
        console.error('Error saving entry:', error);
        showNotification('Error saving entry', 'danger');
    }
}

async function viewEntry(id) {
    try {
        const entry = await fetch(`${API_BASE}/entries/${id}`).then(r => r.json());
        currentEntry = entry;
        
        document.getElementById('view-entry-title').textContent = entry.title || 'Untitled Dream';
        
        const sentiment = getSentimentLabel(entry.sentiment_score);
        const date = new Date(entry.dream_date).toLocaleString();
        
        let emotionsHtml = '';
        if (entry.emotions) {
            emotionsHtml = Object.entries(entry.emotions)
                .filter(([_, score]) => score > 0)
                .sort((a, b) => b[1] - a[1])
                .map(([emotion, score]) => `
                    <span class="emotion-badge emotion-${emotion}">
                        ${emotion}: ${(score * 100).toFixed(0)}%
                    </span>
                `).join('');
        }
        
        let entitiesHtml = '';
        if (entry.entities) {
            const entityTypes = ['people', 'places', 'symbols'];
            entityTypes.forEach(type => {
                if (entry.entities[type] && entry.entities[type].length > 0) {
                    entitiesHtml += `
                        <div class="mb-2">
                            <strong>${type.charAt(0).toUpperCase() + type.slice(1)}:</strong>
                            ${entry.entities[type].map(e => `<span class="tag">${e}</span>`).join('')}
                        </div>
                    `;
                }
            });
        }
        
        const content = `
            <div class="mb-3">
                <small class="text-muted">${date}</small>
            </div>
            
            <div class="mb-3">
                <h6>Content</h6>
                <p style="white-space: pre-wrap;">${entry.content}</p>
            </div>
            
            <div class="mb-3">
                <h6>Analysis</h6>
                <div class="mb-2">
                    <strong>Sentiment:</strong> 
                    <span class="sentiment-indicator sentiment-${sentiment.class}">
                        ${sentiment.label} (${entry.sentiment_score.toFixed(2)})
                    </span>
                </div>
                
                <div class="mb-2">
                    <strong>Emotions:</strong><br>
                    ${emotionsHtml || 'No significant emotions detected'}
                </div>
                
                <div class="mb-2">
                    <strong>Stress Level:</strong>
                    <div class="stress-bar">
                        <div class="stress-fill ${getStressClass(entry.stress_level)}" 
                             style="width: ${(entry.stress_level * 100)}%"></div>
                    </div>
                    ${(entry.stress_level * 100).toFixed(0)}%
                </div>
                
                <div class="mb-2">
                    <strong>Dream Intensity:</strong> ${(entry.dream_intensity * 100).toFixed(0)}%
                </div>
                
                ${entry.sleep_quality ? `
                    <div class="mb-2">
                        <strong>Sleep Quality:</strong> ${entry.sleep_quality}/10
                    </div>
                ` : ''}
            </div>
            
            ${entitiesHtml ? `
                <div class="mb-3">
                    <h6>Entities</h6>
                    ${entitiesHtml}
                </div>
            ` : ''}
            
            ${entry.themes && entry.themes.length > 0 ? `
                <div class="mb-3">
                    <h6>Themes</h6>
                    ${entry.themes.map(theme => `<span class="tag">${theme}</span>`).join('')}
                </div>
            ` : ''}
            
            ${entry.tags && entry.tags.length > 0 ? `
                <div class="mb-3">
                    <h6>Tags</h6>
                    ${entry.tags.map(tag => `<span class="tag">${tag}</span>`).join('')}
                </div>
            ` : ''}
        `;
        
        document.getElementById('view-entry-content').innerHTML = content;
        
        const modal = new bootstrap.Modal(document.getElementById('viewEntryModal'));
        modal.show();
        
    } catch (error) {
        console.error('Error viewing entry:', error);
        showNotification('Error loading entry', 'danger');
    }
}

function editCurrentEntry() {
    if (!currentEntry) return;
    
    bootstrap.Modal.getInstance(document.getElementById('viewEntryModal')).hide();
    
    document.getElementById('entry-id').value = currentEntry.id;
    document.getElementById('entry-title').value = currentEntry.title || '';
    document.getElementById('entry-content').value = currentEntry.content;
    
    const date = new Date(currentEntry.dream_date);
    date.setMinutes(date.getMinutes() - date.getTimezoneOffset());
    document.getElementById('entry-date').value = date.toISOString().slice(0, 16);
    
    document.getElementById('entry-tags').value = currentEntry.tags ? currentEntry.tags.join(', ') : '';
    document.getElementById('sleep-quality').value = currentEntry.sleep_quality || 5;
    document.getElementById('sleep-quality-value').textContent = currentEntry.sleep_quality || 5;
    
    document.getElementById('entryModalLabel').textContent = 'Edit Dream Entry';
    
    const modal = new bootstrap.Modal(document.getElementById('entryModal'));
    modal.show();
}

async function deleteCurrentEntry() {
    if (!currentEntry || !confirm('Are you sure you want to delete this dream entry?')) return;
    
    try {
        const response = await fetch(`${API_BASE}/entries/${currentEntry.id}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            showNotification('Entry deleted', 'success');
            bootstrap.Modal.getInstance(document.getElementById('viewEntryModal')).hide();
            loadEntries(currentPage);
            loadDashboard();
        } else {
            throw new Error('Failed to delete entry');
        }
    } catch (error) {
        console.error('Error deleting entry:', error);
        showNotification('Error deleting entry', 'danger');
    }
}

// ========== Insights Functions ==========

async function loadSummaries() {
    try {
        const summaries = await fetch(`${API_BASE}/summaries`).then(r => r.json());
        const summariesList = document.getElementById('summaries-list');
        
        if (summaries.length === 0) {
            summariesList.innerHTML = `
                <div class="empty-state">
                    <h4>No summaries generated yet</h4>
                    <p>Generate weekly or monthly summaries to track your progress</p>
                </div>
            `;
            return;
        }
        
        summariesList.innerHTML = summaries.map(summary => createSummaryCard(summary)).join('');
        
    } catch (error) {
        console.error('Error loading summaries:', error);
    }
}

function createSummaryCard(summary) {
    const startDate = new Date(summary.period_start).toLocaleDateString();
    const endDate = new Date(summary.period_end).toLocaleDateString();
    
    return `
        <div class="card summary-card mb-3">
            <div class="card-body">
                <div class="summary-header">
                    <h5>${summary.period_type.charAt(0).toUpperCase() + summary.period_type.slice(1)} Summary</h5>
                    <small class="text-muted">${startDate} - ${endDate}</small>
                </div>
                
                <div class="summary-stats">
                    <div class="summary-stat">
                        <h6>Entries</h6>
                        <p>${summary.total_entries}</p>
                    </div>
                    <div class="summary-stat">
                        <h6>Avg Sentiment</h6>
                        <p>${summary.avg_sentiment.toFixed(2)}</p>
                    </div>
                    <div class="summary-stat">
                        <h6>Dominant Emotion</h6>
                        <p>${summary.dominant_emotion}</p>
                    </div>
                    <div class="summary-stat">
                        <h6>Stress Trend</h6>
                        <p>${summary.stress_trend}</p>
                    </div>
                </div>
                
                ${summary.summary_text ? `<p>${summary.summary_text}</p>` : ''}
                
                ${summary.recurring_themes && summary.recurring_themes.length > 0 ? `
                    <div class="mb-2">
                        <strong>Recurring Themes:</strong><br>
                        ${summary.recurring_themes.map(theme => `<span class="tag">${theme}</span>`).join('')}
                    </div>
                ` : ''}
                
                ${summary.recommendations ? `
                    <div class="recommendations">
                        <i class="fas fa-lightbulb"></i>
                        <{summary.recommendations}
                    </div>
                ` : ''}
            </div>
        </div>
    `;
}

async function generateSummary(periodType) {
    try {
        const response = await fetch(`${API_BASE}/summaries/generate`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ period_type: periodType })
        });
        
        if (response.ok) {
            showNotification(`${periodType.charAt(0).toUpperCase() + periodType.slice(1)} summary generated!`, 'success');
            loadSummaries();
        } else {
            const error = await response.json();
            throw new Error(error.error || 'Failed to generate summary');
        }
    } catch (error) {
        console.error('Error generating summary:', error);
        showNotification(error.message || 'Error generating summary', 'danger');
    }
}

async function exportPDF() {
    try {
        const response = await fetch(`${API_BASE}/export/pdf`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ entry_ids: [] })
        });
        
        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `dream_journal_${new Date().toISOString().split('T')[0]}.pdf`;
            a.click();
            window.URL.revokeObjectURL(url);
            showNotification('PDF exported successfully!', 'success');
        } else {
            throw new Error('Failed to export PDF');
        }
    } catch (error) {
        console.error('Error exporting PDF:', error);
        showNotification('Error exporting PDF', 'danger');
    }
}

// ========== Utility Functions ==========

async function loadTags() {
    try {
        allTags = await fetch(`${API_BASE}/tags`).then(r => r.json());
        const filterTag = document.getElementById('filter-tag');
        if (filterTag) {
            filterTag.innerHTML = '<option value="">All Tags</option>' +
                allTags.map(tag => `<option value="${tag}">${tag}</option>`).join('');
        }
    } catch (error) {
        console.error('Error loading tags:', error);
    }
}

function showNotification(message, type = 'info') {
    // Simple toast notification
    const toast = document.createElement('div');
    toast.className = `alert alert-${type} position-fixed top-0 end-0 m-3`;
    toast.style.zIndex = '9999';
    toast.innerHTML = `
        ${message}
        <button type="button" class="btn-close" onclick="this.parentElement.remove()"></button>
    `;
    document.body.appendChild(toast);
    
    setTimeout(() => toast.remove(), 3000);
}

function debounce(func, wait) {
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
