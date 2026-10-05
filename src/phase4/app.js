let currentSessionId = null;
let currentGridData = null;
let pivotCount = 0;

document.getElementById('searchBtn').addEventListener('click', async () => {
    const query = document.getElementById('searchInput').value;
    if (!query) return;

    // Reset UI state
    const initialState = document.getElementById('initialState');
    if(initialState) initialState.classList.add('hidden');
    const promoBanner = document.getElementById('promoBanner');
    if(promoBanner) promoBanner.classList.add('hidden');
    document.getElementById('successState').classList.add('hidden');
    const gridContainer = document.getElementById('choiceGridContainer');
    gridContainer.classList.remove('hidden');
    pivotCount = 0;

    // Show skeletons to mask latency
    setSkeletons();

    try {
        // Call our FastAPI Backend
        const response = await fetch('/api/search', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user_id: 'user_123', query: query })
        });
        
        const data = await response.json();
        
        if (data.type === '2x2_grid') {
            currentSessionId = data.session_id;
            currentGridData = data.grid_data;
            populateGrid(currentGridData);
            if (data.debug_log) {
                renderDebugDashboard(data.debug_log);
            }
        } else if (data.type === 'legacy_list') {
            alert("Specific query detected. Routing to legacy search engine.");
            gridContainer.classList.add('hidden');
        } else {
            alert(data.message || "No results found.");
            gridContainer.classList.add('hidden');
        }
    } catch (error) {
        console.error("Search failed:", error);
        alert("Search failed. Is the server running?");
        gridContainer.classList.add('hidden');
    }
});

async function triggerDynamicPivot() {
    pivotCount++;
    if (pivotCount > 3) {
        alert("Edge Case Mitigation: Pivot limit reached. Falling back to standard search.");
        document.getElementById('choiceGridContainer').classList.add('hidden');
        return;
    }

    if (!currentSessionId || !currentGridData) return;

    // Show skeletons during recalculation
    setSkeletons();

    // Extract the vector embeddings of the 4 images the user just rejected
    const rejectedEmbeddings = currentGridData.map(c => c.embedding);

    try {
        // Call the FastAPI Backend to Pivot
        const response = await fetch('/api/pivot', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                user_id: 'user_123', 
                session_id: currentSessionId,
                rejected_embeddings: rejectedEmbeddings
            })
        });
        
        const data = await response.json();
        
        if (data.type === '2x2_grid') {
            currentGridData = data.grid_data;
            populateGrid(currentGridData);
        } else {
            alert(data.message || "Pivot limit reached or no results.");
            document.getElementById('choiceGridContainer').classList.add('hidden');
        }
    } catch (error) {
        console.error("Pivot failed:", error);
        alert("Pivot failed.");
    }
}

function selectQuadrant(quadrantId) {
    document.getElementById('choiceGridContainer').classList.add('hidden');
    document.getElementById('successState').classList.remove('hidden');
}

function setSkeletons() {
    for (let i = 1; i <= 4; i++) {
        const el = document.getElementById(`quad${i}`);
        el.style.backgroundImage = 'none';
        el.classList.add('skeleton');
    }
}

function populateGrid(gridData) {
    // Dynamically inject the images returned from the ML backend
    for (let i = 1; i <= 4; i++) {
        const el = document.getElementById(`quad${i}`);
        el.classList.remove('skeleton');
        
        if (gridData[i-1]) {
             const filename = gridData[i-1].metadata.filename;
             // Load the image from the /photos/ static route
             el.style.backgroundImage = `url('/photos/${filename}')`;
        }
    }
}

function renderDebugDashboard(log) {
    const dashboard = document.getElementById('debugDashboard');
    if (!dashboard) return;
    
    let html = `<h3>AI Debug Console</h3>`;
    html += `<p><strong>Expanded Query:</strong><br/>"${log.query}"</p>`;
    html += `<p><strong>Abs Cutoff:</strong> ${log.threshold}</p>`;
    html += `<hr style="border-color:#333;"/>`;
    
    html += `<ul style="list-style:none; padding:0; font-size:13px;">`;
    log.results.forEach(res => {
        const color = res.status === "ACCEPTED" ? "#00ff00" : "#ff4444";
        html += `<li style="margin-bottom:8px; border-bottom:1px solid #333; padding-bottom:8px;">
            <span style="color: ${color}">[${res.status}]</span><br/>
            File: ${res.filename}<br/>
            L2 Dist: ${res.distance.toFixed(2)}
        </li>`;
    });
    html += `</ul>`;
    
    dashboard.innerHTML = html;
}
