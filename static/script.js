/**
 * Cloud Infrastructure Monitoring and Automated Alert System
 * Client-Side Engine: AJAX Auto-Refresh, Canvas Trend Visualization, and Live DOM Updates
 */

// Global auto-refresh configuration
let autoRefreshTimer = null;
let countdownInterval = null;
let remainingSeconds = 5;
const REFRESH_INTERVAL_SECONDS = 5;

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    initAutoRefresh();
    initRangeInputs();
});

/**
 * Initialize auto-refresh timer and countdown indicator
 */
function initAutoRefresh() {
    const toggle = document.getElementById('auto-refresh-toggle');
    const countdownEl = document.getElementById('refresh-countdown');

    if (!toggle || !countdownEl) return;

    function startTimer() {
        remainingSeconds = REFRESH_INTERVAL_SECONDS;
        updateCountdownUI();

        clearInterval(countdownInterval);
        countdownInterval = setInterval(() => {
            remainingSeconds--;
            updateCountdownUI();

            if (remainingSeconds <= 0) {
                remainingSeconds = REFRESH_INTERVAL_SECONDS;
                performMetricsFetch();
            }
        }, 1000);
    }

    function stopTimer() {
        clearInterval(countdownInterval);
        if (countdownEl) countdownEl.textContent = 'Paused';
    }

    function updateCountdownUI() {
        if (countdownEl) {
            countdownEl.textContent = `${remainingSeconds}s`;
        }
    }

    toggle.addEventListener('change', () => {
        if (toggle.checked) {
            startTimer();
        } else {
            stopTimer();
        }
    });

    // Start auto-refresh by default
    if (toggle.checked) {
        startTimer();
    }
}

/**
 * Trigger manual metric refresh via button
 */
function triggerManualRefresh() {
    const btn = document.getElementById('btn-manual-refresh');
    if (btn) btn.classList.add('loading');
    performMetricsFetch().finally(() => {
        if (btn) btn.classList.remove('loading');
        remainingSeconds = REFRESH_INTERVAL_SECONDS;
    });
}

/**
 * Fetch latest metrics from /metrics endpoint and update UI
 */
async function performMetricsFetch() {
    try {
        const response = await fetch('/metrics');
        if (!response.ok) {
            throw new Error(`Metrics API error: ${response.status}`);
        }
        const data = await response.json();

        if (data.status === 'success') {
            updateDashboardUI(data);
        }
    } catch (error) {
        console.warn('[CloudMonitor] Live metrics fetch warning:', error);
    }
}

/**
 * Update Dashboard DOM elements with live metric data
 */
function updateDashboardUI(data) {
    const m = data.metrics;
    if (!m) return;

    // 1. Update CPU card
    const valCpu = document.getElementById('val-cpu');
    const barCpu = document.getElementById('bar-cpu');
    const badgeCpu = document.getElementById('badge-cpu');
    const threshCpuEl = document.getElementById('thresh-cpu-val');
    const cpuThresh = threshCpuEl ? parseFloat(threshCpuEl.textContent) : 80.0;

    if (valCpu) valCpu.textContent = m.cpu_percent;
    if (barCpu) barCpu.style.width = `${Math.min(100, m.cpu_percent)}%`;
    if (badgeCpu) {
        if (m.cpu_percent > cpuThresh) {
            badgeCpu.className = 'card-status-badge badge-danger';
            badgeCpu.textContent = 'High Load';
        } else {
            badgeCpu.className = 'card-status-badge badge-success';
            badgeCpu.textContent = 'Normal';
        }
    }

    // 2. Update Memory card
    const valMem = document.getElementById('val-memory');
    const barMem = document.getElementById('bar-memory');
    const badgeMem = document.getElementById('badge-memory');
    const threshMemEl = document.getElementById('thresh-mem-val');
    const memThresh = threshMemEl ? parseFloat(threshMemEl.textContent) : 80.0;

    if (valMem) valMem.textContent = m.memory_percent;
    if (barMem) barMem.style.width = `${Math.min(100, m.memory_percent)}%`;
    if (badgeMem) {
        if (m.memory_percent > memThresh) {
            badgeMem.className = 'card-status-badge badge-danger';
            badgeMem.textContent = 'High RAM';
        } else {
            badgeMem.className = 'card-status-badge badge-success';
            badgeMem.textContent = 'Normal';
        }
    }

    // 3. Update Disk card
    const valDisk = document.getElementById('val-disk');
    const barDisk = document.getElementById('bar-disk');
    const badgeDisk = document.getElementById('badge-disk');
    const threshDiskEl = document.getElementById('thresh-disk-val');
    const diskThresh = threshDiskEl ? parseFloat(threshDiskEl.textContent) : 85.0;

    if (valDisk) valDisk.textContent = m.disk_percent;
    if (barDisk) barDisk.style.width = `${Math.min(100, m.disk_percent)}%`;
    if (badgeDisk) {
        if (m.disk_percent > diskThresh) {
            badgeDisk.className = 'card-status-badge badge-danger';
            badgeDisk.textContent = 'High Disk';
        } else {
            badgeDisk.className = 'card-status-badge badge-success';
            badgeDisk.textContent = 'Normal';
        }
    }

    // 4. Update Meta Info Bar
    const healthVal = document.getElementById('status-health-val');
    const collectedVal = document.getElementById('status-collected-val');
    const globalStatusBadge = document.getElementById('global-status-badge');

    if (collectedVal && m.collected_at) {
        collectedVal.textContent = m.collected_at;
    }

    if (data.system_health) {
        const h = data.system_health;
        if (healthVal) {
            healthVal.textContent = h;
            healthVal.className = `meta-value health-text health-${h.toLowerCase()}`;
        }
        if (globalStatusBadge) {
            globalStatusBadge.className = `status-indicator status-${h.toLowerCase()}`;
            const label = globalStatusBadge.querySelector('.status-label');
            if (label) label.textContent = h;
        }
    }

    // 5. Prepend new row to Recent Samples table if present
    const tbody = document.getElementById('tbody-recent-samples');
    if (tbody && data.snapshot_id) {
        // Remove empty state placeholder if present
        const emptyRow = tbody.querySelector('.empty-state');
        if (emptyRow) emptyRow.parentElement.remove();

        const tr = document.createElement('tr');
        const exceeded = m.cpu_percent > cpuThresh || m.memory_percent > memThresh || m.disk_percent > diskThresh;
        tr.innerHTML = `
            <td><span class="code-id">#${data.snapshot_id}</span></td>
            <td>${m.collected_at}</td>
            <td><span class="metric-pill ${m.cpu_percent > cpuThresh ? 'pill-danger' : ''}">${m.cpu_percent}%</span></td>
            <td><span class="metric-pill ${m.memory_percent > memThresh ? 'pill-danger' : ''}">${m.memory_percent}%</span></td>
            <td><span class="metric-pill ${m.disk_percent > diskThresh ? 'pill-danger' : ''}">${m.disk_percent}%</span></td>
            <td>${formatSeconds(m.uptime_seconds)}</td>
            <td><span class="badge ${exceeded ? 'badge-warning' : 'badge-success'}">${exceeded ? 'Exceeded' : 'Nominal'}</span></td>
        `;
        tbody.insertBefore(tr, tbody.firstChild);

        // Keep table capped to 10 rows
        while (tbody.children.length > 10) {
            tbody.removeChild(tbody.lastChild);
        }
    }
}

/**
 * Format uptime seconds for dynamic client rows
 */
function formatSeconds(secs) {
    if (!secs) return 'Unavailable';
    const d = Math.floor(secs / 86400);
    const h = Math.floor((secs % 86400) / 3600);
    const m = Math.floor((secs % 3600) / 60);
    const s = secs % 60;
    const parts = [];
    if (d > 0) parts.push(`${d}d`);
    if (h > 0 || d > 0) parts.push(`${h}h`);
    parts.push(`${m}m`);
    parts.push(`${s}s`);
    return parts.join(' ');
}

/**
 * Synchronize settings range sliders with number inputs
 */
function initRangeInputs() {
    ['cpu_threshold', 'memory_threshold', 'disk_threshold'].forEach(id => {
        const numInput = document.getElementById(id);
        if (numInput) {
            numInput.addEventListener('input', function() {
                const slider = this.parentElement.querySelector('.range-slider');
                if (slider) slider.value = this.value;
            });
        }
    });
}

/**
 * Plain HTML5 Canvas Line Chart for Metrics History
 * Crisp HiDPI rendering with zero external libraries
 */
async function renderHistoryChart(limit = 30) {
    const canvas = document.getElementById('trendChartCanvas');
    const emptyMsg = document.getElementById('chart-empty-message');
    if (!canvas) return;

    try {
        const response = await fetch(`/api/history?limit=${limit}`);
        if (!response.ok) throw new Error('Failed to load history');
        const data = await response.json();

        if (!data || data.length === 0) {
            if (emptyMsg) emptyMsg.style.display = 'block';
            return;
        }
        if (emptyMsg) emptyMsg.style.display = 'none';

        drawCanvasChart(canvas, data);
    } catch (err) {
        console.error('[CloudMonitor] Chart render error:', err);
    }
}

function drawCanvasChart(canvas, points) {
    const ctx = canvas.getContext('2d');
    const dpr = window.devicePixelRatio || 1;
    const rect = canvas.getBoundingClientRect();

    canvas.width = rect.width * dpr;
    canvas.height = 280 * dpr;
    ctx.scale(dpr, dpr);

    const width = rect.width;
    const height = 280;
    const padding = { top: 30, right: 30, bottom: 40, left: 50 };
    const chartW = width - padding.left - padding.right;
    const chartH = height - padding.top - padding.bottom;

    ctx.clearRect(0, 0, width, height);

    // Draw background grid lines (0%, 25%, 50%, 75%, 100%)
    ctx.strokeStyle = '#2d3748';
    ctx.lineWidth = 1;
    ctx.fillStyle = '#9ca3af';
    ctx.font = '11px JetBrains Mono, monospace';
    ctx.textAlign = 'right';

    for (let pct = 0; pct <= 100; pct += 25) {
        const y = padding.top + chartH - (pct / 100) * chartH;
        ctx.beginPath();
        ctx.moveTo(padding.left, y);
        ctx.lineTo(width - padding.right, y);
        ctx.stroke();

        ctx.fillText(`${pct}%`, padding.left - 8, y + 4);
    }

    if (points.length < 2) {
        // Draw single point if only 1 sample
        const p = points[0];
        const x = padding.left + chartW / 2;
        drawPoint(ctx, x, padding.top + chartH - (p.cpu_percent / 100) * chartH, '#38bdf8');
        drawPoint(ctx, x, padding.top + chartH - (p.memory_percent / 100) * chartH, '#c084fc');
        drawPoint(ctx, x, padding.top + chartH - (p.disk_percent / 100) * chartH, '#34d399');
        return;
    }

    const stepX = chartW / (points.length - 1);

    // Helper to draw a metric line
    function drawMetricLine(key, color) {
        ctx.strokeStyle = color;
        ctx.lineWidth = 2.5;
        ctx.lineJoin = 'round';
        ctx.beginPath();

        points.forEach((pt, idx) => {
            const x = padding.left + idx * stepX;
            const val = Math.min(100, Math.max(0, pt[key] || 0));
            const y = padding.top + chartH - (val / 100) * chartH;
            if (idx === 0) ctx.moveTo(x, y);
            else ctx.lineTo(x, y);
        });
        ctx.stroke();

        // Draw dots on data points
        points.forEach((pt, idx) => {
            const x = padding.left + idx * stepX;
            const val = Math.min(100, Math.max(0, pt[key] || 0));
            const y = padding.top + chartH - (val / 100) * chartH;
            drawPoint(ctx, x, y, color);
        });
    }

    function drawPoint(c, x, y, color) {
        c.fillStyle = color;
        c.beginPath();
        c.arc(x, y, 3.5, 0, Math.PI * 2);
        c.fill();
    }

    // Draw lines: CPU (Cyan), Memory (Purple), Disk (Green)
    drawMetricLine('cpu_percent', '#38bdf8');
    drawMetricLine('memory_percent', '#c084fc');
    drawMetricLine('disk_percent', '#34d399');

    // Draw bottom timestamp labels (first, middle, last)
    ctx.fillStyle = '#6b7280';
    ctx.textAlign = 'center';
    ctx.font = '10px JetBrains Mono, monospace';

    const indicesToLabel = [0, Math.floor(points.length / 2), points.length - 1];
    indicesToLabel.forEach(idx => {
        if (points[idx] && points[idx].collected_at) {
            const x = padding.left + idx * stepX;
            const timeStr = points[idx].collected_at.split(' ')[1] || points[idx].collected_at;
            ctx.fillText(timeStr, x, height - padding.bottom + 20);
        }
    });
}

/**
 * ==============================================================================
 * Multi-Server Infrastructure Fleet Management & Live Telemetry AJAX Handlers
 * ==============================================================================
 */

// Modal open/close controls
function openAddServerModal() {
    const modal = document.getElementById('modal-add-server');
    if (modal) {
        modal.style.display = 'flex';
        const inputName = document.getElementById('server-name');
        if (inputName) inputName.focus();
    }
}

function closeAddServerModal() {
    const modal = document.getElementById('modal-add-server');
    if (modal) {
        modal.style.display = 'none';
        const form = document.getElementById('form-add-server');
        if (form) form.reset();
    }
}

// Close modal on Escape key or outside click
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeAddServerModal();
});

document.addEventListener('click', (e) => {
    const modal = document.getElementById('modal-add-server');
    if (modal && e.target === modal) {
        closeAddServerModal();
    }
});

/**
 * Submit form to register new monitored server node
 */
async function submitAddServer(event) {
    event.preventDefault();
    const btn = document.getElementById('btn-submit-server');
    const spinner = document.getElementById('btn-submit-spinner');

    const name = document.getElementById('server-name').value.trim();
    const host = document.getElementById('server-host').value.trim();
    const port = document.getElementById('server-port').value.trim();
    const environment = document.getElementById('server-environment').value;
    const jenkins_job = document.getElementById('server-jenkins').value.trim();
    const docker_container = document.getElementById('server-docker').value.trim();

    if (!name || !host) {
        showToast('Please provide both Server Name and Host IP.', 'error');
        return;
    }

    if (btn) btn.disabled = true;
    if (spinner) spinner.style.display = 'inline-block';

    try {
        const response = await fetch('/api/servers/add', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: JSON.stringify({
                name,
                host,
                port: parseInt(port, 10) || 5000,
                environment,
                jenkins_job,
                docker_container
            })
        });

        const data = await response.json();

        if (response.ok && data.status === 'success') {
            closeAddServerModal();
            showToast(data.message || `Server '${name}' registered successfully!`, 'success');
            appendServerToTable(data.server);
            updateFleetCount();
        } else {
            showToast(data.message || 'Failed to register server.', 'error');
        }
    } catch (err) {
        console.error('Error adding server:', err);
        showToast('Network error while registering server.', 'error');
    } finally {
        if (btn) btn.disabled = false;
        if (spinner) spinner.style.display = 'none';
    }
}

/**
 * Append newly created server row into DOM table with animation
 */
function appendServerToTable(s) {
    if (!s) return;
    const tbody = document.getElementById('tbody-servers');
    if (!tbody) return;

    // Remove empty row placeholder if present
    const emptyRow = document.getElementById('empty-servers-row');
    if (emptyRow) emptyRow.remove();

    const tr = document.createElement('tr');
    tr.id = `server-row-${s.id}`;
    tr.style.animation = 'fadeIn 0.4s ease';

    const envClass = (s.environment || 'production').toLowerCase().replace(/\s+/g, '-');

    tr.innerHTML = `
        <td>
            <div class="node-cell">
                <div class="node-avatar">
                    <span class="status-pulse-dot"></span>
                </div>
                <div class="node-details">
                    <strong class="node-name" id="node-name-${s.id}">${escapeHtml(s.name)}</strong>
                    <span class="node-ip font-mono text-muted">${escapeHtml(s.host)}:${s.port}</span>
                </div>
            </div>
        </td>
        <td>
            <span class="badge badge-env-${envClass}">${escapeHtml(s.environment)}</span>
        </td>
        <td>
            <div class="tracking-pill tracking-jenkins">
                <div class="tracking-header">
                    <span class="tracking-badge-icon jenkins-dot">J</span>
                    <a href="http://localhost:8085/job/Cloud-Infrastructure-Monitoring-Pipeline/" target="_blank" class="tracking-title" title="Open Jenkins Pipeline Job">${escapeHtml(s.jenkins_job)}</a>
                </div>
                <div class="tracking-sub">
                    <span class="badge-sub-status text-green">${escapeHtml(s.jenkins_build_status)}</span> &bull; 
                    <span class="text-muted">${escapeHtml(s.jenkins_test_coverage)}</span>
                </div>
            </div>
        </td>
        <td>
            <div class="tracking-pill tracking-docker">
                <div class="tracking-header">
                    <span class="tracking-badge-icon docker-dot">🐳</span>
                    <span class="tracking-title">${escapeHtml(s.docker_container)}</span>
                </div>
                <div class="tracking-sub">
                    <span class="badge-sub-status text-blue">${escapeHtml(s.docker_status)}</span> &bull; 
                    <span class="text-muted font-mono">${escapeHtml(s.docker_port)}</span>
                </div>
            </div>
        </td>
        <td>
            <div class="status-latency-cell">
                <span class="badge badge-success" id="badge-status-${s.id}">
                    <span class="dot-sm"></span> ${escapeHtml(s.status)}
                </span>
                <span class="latency-indicator font-mono" id="latency-${s.id}">
                    ⚡ ${s.latency_ms}ms
                </span>
            </div>
        </td>
        <td>
            <div class="resource-mini-bars">
                <div class="mini-bar-row">
                    <span class="mini-label">CPU:</span>
                    <span class="mini-val font-mono" id="cpu-node-${s.id}">${s.cpu_percent}%</span>
                </div>
                <div class="mini-bar-row">
                    <span class="mini-label">RAM:</span>
                    <span class="mini-val font-mono" id="mem-node-${s.id}">${s.memory_percent}%</span>
                </div>
            </div>
        </td>
        <td>
            <div class="table-actions">
                <button class="btn-icon btn-ping" onclick="pingServer(${s.id})" id="btn-ping-${s.id}" title="Ping and Refresh Node Health">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline></svg>
                    <span>Ping</span>
                </button>
                <button class="btn-icon btn-delete" onclick="deleteServer(${s.id}, '${escapeHtml(s.name)}')" title="Unregister Node">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path></svg>
                </button>
            </div>
        </td>
    `;

    tbody.prepend(tr);
}

/**
 * Ping monitored server node
 */
async function pingServer(serverId) {
    const btn = document.getElementById(`btn-ping-${serverId}`);
    const latencyEl = document.getElementById(`latency-${serverId}`);
    const cpuEl = document.getElementById(`cpu-node-${serverId}`);
    const memEl = document.getElementById(`mem-node-${serverId}`);
    const row = document.getElementById(`server-row-${serverId}`);

    if (btn) btn.classList.add('loading');

    try {
        const response = await fetch(`/api/servers/${serverId}/ping`, {
            method: 'POST',
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        });
        const data = await response.json();

        if (response.ok && data.status === 'success') {
            if (latencyEl) latencyEl.textContent = `⚡ ${data.result.latency_ms}ms`;
            if (cpuEl) cpuEl.textContent = `${data.result.cpu_percent}%`;
            if (memEl) memEl.textContent = `${data.result.memory_percent}%`;
            if (row) {
                row.style.outline = '1px solid #10b981';
                setTimeout(() => { row.style.outline = 'none'; }, 1000);
            }
            showToast(data.message, 'success');
        } else {
            showToast(data.message || 'Ping failed', 'error');
        }
    } catch (err) {
        console.error('Ping error:', err);
        showToast('Error connecting to server node.', 'error');
    } finally {
        if (btn) btn.classList.remove('loading');
    }
}

/**
 * Delete / unregister monitored server node
 */
async function deleteServer(serverId, serverName) {
    if (!confirm(`Unregister server node '${serverName}' from monitoring?`)) {
        return;
    }

    try {
        const response = await fetch(`/api/servers/${serverId}/delete`, {
            method: 'POST',
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        });
        const data = await response.json();

        if (response.ok && data.status === 'success') {
            const row = document.getElementById(`server-row-${serverId}`);
            if (row) {
                row.style.opacity = '0';
                row.style.transform = 'translateX(20px)';
                setTimeout(() => {
                    row.remove();
                    updateFleetCount();
                }, 300);
            }
            showToast(`Server '${serverName}' removed from monitoring fleet.`, 'info');
        } else {
            showToast(data.message || 'Failed to remove server', 'error');
        }
    } catch (err) {
        console.error('Delete error:', err);
        showToast('Network error removing server.', 'error');
    }
}

/**
 * Update total fleet count labels
 */
function updateFleetCount() {
    const tbody = document.getElementById('tbody-servers');
    if (!tbody) return;
    const count = tbody.querySelectorAll('tr:not(#empty-servers-row)').length;
    const countBadge = document.getElementById('fleet-count-badge');
    const totalKpi = document.getElementById('kpi-fleet-total');

    if (countBadge) countBadge.textContent = `${count} Nodes Active`;
    if (totalKpi) totalKpi.textContent = `${count} Servers`;
}

/**
 * Modern floating toast message
 */
function showToast(message, type = 'info') {
    // Remove existing toast if present
    const existing = document.querySelector('.toast-box');
    if (existing) existing.remove();

    const toast = document.createElement('div');
    toast.className = 'toast-box';

    let icon = 'ℹ️';
    let borderColor = '#38bdf8';
    if (type === 'success') { icon = '✅'; borderColor = '#10b981'; }
    else if (type === 'error') { icon = '⚠️'; borderColor = '#ef4444'; }

    toast.style.borderColor = borderColor;
    toast.innerHTML = `<span>${icon}</span><span>${escapeHtml(message)}</span>`;

    document.body.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(10px)';
        setTimeout(() => toast.remove(), 300);
    }, 3500);
}

/**
 * Helper to escape HTML characters
 */
function escapeHtml(text) {
    if (!text) return '';
    return String(text)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}

