# Admin Dashboard HTML with clean styling
def get_admin_dashboard():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Agent Hub - Admin Dashboard</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * { box-sizing: border-box; }
            body { 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0; 
                padding: 20px; 
                background: #f5f5f5;
                min-height: 100vh;
            }
            
            .dashboard { 
                max-width: 1400px; 
                margin: 0 auto;
            }
            
            .header { 
                background: #2196F3;
                color: white; 
                padding: 30px; 
                border-radius: 8px; 
                margin-bottom: 30px; 
                text-align: center;
                box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            }
            
            .header h1 { 
                margin: 0 0 10px 0; 
                font-size: 2.5em;
                font-weight: 300;
            }
            
            .header p { 
                margin: 0; 
                opacity: 0.9; 
                font-size: 1.1em;
                font-weight: 400;
            }
            .grid { 
                display: grid; 
                grid-template-columns: 1fr 1fr; 
                gap: 35px; 
                margin-bottom: 35px; 
            }
            
            .section { 
                background: white; 
                padding: 30px; 
                border-radius: 8px; 
                box-shadow: 0 4px 20px rgba(0,0,0,0.1);
                transition: all 0.3s ease;
            }
            
            .section:hover {
                transform: translateY(-2px);
                box-shadow: 0 8px 30px rgba(0,0,0,0.15);
            }
            
            .full-width { 
                grid-column: 1 / -1; 
            }
            
            .section-header { 
                display: flex; 
                align-items: center; 
                margin-bottom: 25px; 
                padding-bottom: 15px; 
                border-bottom: 2px solid #2196F3;
            }
            
            .section-header h3 { 
                margin: 0; 
                color: #333; 
                font-size: 1.4em;
                font-weight: 500;
            }
            
            .section-header .icon { 
                font-size: 1.5em; 
                margin-right: 15px;
                color: #2196F3;
            }
            .form-group { 
                margin-bottom: 20px;
            }
            
            .form-row { 
                display: grid; 
                grid-template-columns: 1fr 1fr; 
                gap: 15px; 
            }
            
            label { 
                display: block; 
                margin-bottom: 8px; 
                font-weight: 600; 
                color: #333; 
                font-size: 0.9em; 
                text-transform: uppercase; 
                letter-spacing: 0.5px;
            }
            
            input, select, textarea { 
                width: 100%; 
                padding: 15px; 
                border: 2px solid #e0e0e0; 
                border-radius: 4px; 
                font-size: 14px; 
                transition: border-color 0.3s ease;
            }
            
            input:focus, select:focus, textarea:focus { 
                outline: none; 
                border-color: #2196F3;
            }
            
            textarea { 
                resize: vertical; 
                min-height: 120px; 
            }
            
            button { 
                background: #2196F3; 
                color: white; 
                padding: 15px 30px; 
                border: none; 
                border-radius: 4px; 
                cursor: pointer; 
                font-size: 14px; 
                font-weight: 500; 
                text-transform: uppercase; 
                letter-spacing: 0.5px; 
                transition: all 0.3s ease;
            }
            
            button:hover { 
                background: #1976D2;
                transform: translateY(-2px);
            }
            
            button:disabled { 
                background: #bdc3c7; 
                cursor: not-allowed; 
                transform: none;
            }
            .success { color: #27ae60; background: #d5f4e6; padding: 15px; border-radius: 8px; margin: 10px 0; border-left: 4px solid #27ae60; }
            .error { color: #e74c3c; background: #fdf2f2; padding: 15px; border-radius: 8px; margin: 10px 0; border-left: 4px solid #e74c3c; }
            .loading { display: none; color: #666; font-style: italic; text-align: center; padding: 15px; }
            .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-bottom: 25px; }
            .stat-card { background: #f8f9fa; padding: 20px; border-radius: 8px; text-align: center; border: 1px solid #e0e0e0; }
            .stat-number { font-size: 2.2em; font-weight: bold; color: #2196F3; margin-bottom: 5px; }
            .stat-label { color: #666; font-size: 0.9em; text-transform: uppercase; letter-spacing: 0.5px; }
            .tabs { 
                display: flex; 
                margin-bottom: 20px; 
                background: #f8f9fa; 
                border-radius: 8px; 
                padding: 5px;
            }
            
            .tab { 
                flex: 1; 
                padding: 15px 20px; 
                text-align: center; 
                border-radius: 6px; 
                cursor: pointer; 
                transition: all 0.3s ease; 
                font-weight: 500;
                color: #666;
            }
            
            .tab.active { 
                background: #2196F3; 
                color: white;
                box-shadow: 0 2px 8px rgba(33, 150, 243, 0.3);
            }
            .tab-content { display: none; }
            .tab-content.active { display: block; }
            .filter-bar { display: flex; gap: 15px; margin-bottom: 20px; align-items: center; flex-wrap: wrap; }
            .filter-bar input, .filter-bar select { width: auto; min-width: 150px; }
            .data-list { max-height: 600px; overflow-y: auto; }
            .data-item { padding: 15px; margin-bottom: 10px; background: #f8f9fa; border-radius: 8px; border-left: 4px solid #2196F3; }
            .file-upload { border: 2px dashed #e1e8ed; padding: 20px; text-align: center; border-radius: 8px; margin-bottom: 20px; transition: all 0.3s ease; }
            .file-upload:hover { border-color: #2196F3; background: #f8f9fa; }
            .file-upload.dragover { border-color: #2196F3; background: #e3f2fd; }
            @media (max-width: 768px) {
                .grid { grid-template-columns: 1fr; }
                .form-row { grid-template-columns: 1fr; }
                .stats-grid { grid-template-columns: repeat(2, 1fr); }
                .filter-bar { flex-direction: column; align-items: stretch; }
            }
        </style>
    </head>
    <body>
        <div class="dashboard">
            <div class="header">
                <h1>Agent Hub - Admin Dashboard</h1>
                <p>Document Management, Analytics & Employee Tracking</p>
                <div style="margin-top: 15px;">
                    <a href="/" style="color: white; text-decoration: none; background: rgba(255,255,255,0.2); padding: 8px 16px; border-radius: 20px; font-size: 14px;">Back to Home</a>
                </div>
            </div>
            
            <div class="grid">
                <!-- Document Upload Section -->
                <div class="section">
                    <div class="section-header">
                        <span class="icon">📤</span>
                        <h3>Upload New Document</h3>
                    </div>
                    
                    <!-- File Upload -->
                    <div class="file-upload" id="fileUpload">
                        <p>📁 Drop files here or click to select</p>
                        <p style="font-size: 12px; color: #666;">Supported: PDF, DOC, DOCX, TXT</p>
                        <input type="file" id="fileInput" style="display: none;" accept=".pdf,.doc,.docx,.txt" multiple>
                    </div>
                    
                    <form id="uploadForm">
                        <div class="form-group">
                            <label>Document Title</label>
                            <input type="text" id="docTitle" required placeholder="e.g., Employee Handbook 2024">
                        </div>
                        <div class="form-row">
                            <div class="form-group">
                                <label>Category</label>
                                <select id="docCategory">
                                    <option value="policy">Policy</option>
                                    <option value="procedure">Procedure</option>
                                    <option value="guideline">Guideline</option>
                                    <option value="handbook">Handbook</option>
                                    <option value="compliance">Compliance</option>
                                    <option value="general">General</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label>Uploaded By</label>
                                <input type="text" id="uploadedBy" value="admin" placeholder="Admin ID">
                            </div>
                        </div>
                        <div class="form-group">
                            <label>Tags (AI Generated)</label>
                            <input type="text" id="docTags" placeholder="AI will auto-generate tags..." readonly style="background: #f8f9fa;">
                        </div>
                        <div class="form-group">
                            <label>Document Content</label>
                            <textarea id="docContent" required placeholder="Paste content or upload file above..."></textarea>
                        </div>
                        <button type="submit" id="uploadBtn">Upload Document</button>
                    </form>
                    <div id="uploadResult"></div>
                </div>
                
                <!-- Quick Stats Section -->
                <div class="section">
                    <div class="section-header">
                        <span class="icon">📊</span>
                        <h3>System Overview</h3>
                    </div>
                    <div class="stats-grid" id="statsGrid">
                        <div class="stat-card">
                            <div class="stat-number" id="totalDocs">-</div>
                            <div class="stat-label">Total Documents</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number" id="totalEmployees">-</div>
                            <div class="stat-label">Active Employees</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number" id="totalQueries">-</div>
                            <div class="stat-label">Total Queries</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number" id="todayQueries">-</div>
                            <div class="stat-label">Today's Queries</div>
                        </div>
                    </div>
                    <button onclick="refreshStats()">🔄 Refresh Stats</button>
                </div>
            </div>
            
            <!-- Analytics Section -->
            <div class="section full-width">
                <div class="section-header">
                    <span class="icon">📈</span>
                    <h3>Analytics & Employee Tracking</h3>
                </div>
                
                <div class="tabs">
                    <div class="tab active" onclick="showTab('documents')">📚 Documents</div>
                    <div class="tab" onclick="showTab('employees')">👥 Employees</div>
                    <div class="tab" onclick="showTab('queries')">💬 Query History</div>
                    <div class="tab" onclick="showTab('analytics')">📊 Analytics</div>
                </div>
                
                <!-- Documents Tab -->
                <div id="documents-tab" class="tab-content active">
                    <div class="filter-bar">
                        <input type="text" id="docFilter" placeholder="Filter documents..." onkeyup="filterDocuments()">
                        <select id="categoryFilter" onchange="filterDocuments()">
                            <option value="">All Categories</option>
                            <option value="policy">Policy</option>
                            <option value="procedure">Procedure</option>
                            <option value="guideline">Guideline</option>
                            <option value="handbook">Handbook</option>
                            <option value="compliance">Compliance</option>
                            <option value="general">General</option>
                        </select>
                        <button onclick="loadDocuments()">🔄 Refresh</button>
                    </div>
                    <div id="documentsList" class="data-list"></div>
                </div>
                
                <!-- Employees Tab -->
                <div id="employees-tab" class="tab-content">
                    <div class="filter-bar">
                        <input type="text" id="empFilter" placeholder="Filter by Employee ID..." onkeyup="filterEmployees()">
                        <select id="sortEmployees" onchange="sortEmployees()">
                            <option value="queries">Sort by Query Count</option>
                            <option value="recent">Sort by Recent Activity</option>
                            <option value="id">Sort by Employee ID</option>
                        </select>
                        <button onclick="loadEmployeeStats()">🔄 Refresh</button>
                    </div>
                    <div id="employeesList" class="data-list"></div>
                </div>
                
                <!-- Query History Tab -->
                <div id="queries-tab" class="tab-content">
                    <div class="filter-bar">
                        <input type="text" id="queryEmpFilter" placeholder="Filter by Employee ID...">
                        <select id="queryTypeFilter">
                            <option value="">All Query Types</option>
                            <option value="search">Search</option>
                            <option value="summarize">Summarize</option>
                            <option value="question">Question</option>
                        </select>
                        <input type="date" id="queryDateFilter">
                        <button onclick="loadQueryHistory()">🔍 Filter</button>
                        <button onclick="exportQueries()">📥 Export CSV</button>
                    </div>
                    <div id="queryHistoryList" class="data-list"></div>
                </div>
                
                <!-- Analytics Tab -->
                <div id="analytics-tab" class="tab-content">
                    <div class="stats-grid">
                        <div class="stat-card">
                            <div class="stat-number" id="avgQueriesPerEmployee">-</div>
                            <div class="stat-label">Avg Queries/Employee</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number" id="mostPopularDoc">-</div>
                            <div class="stat-label">Most Popular Doc</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number" id="mostActiveEmployee">-</div>
                            <div class="stat-label">Most Active Employee</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number" id="peakHour">-</div>
                            <div class="stat-label">Peak Usage Hour</div>
                        </div>
                    </div>
                    <div style="margin-top: 20px;">
                        <button onclick="generateAnalytics()">📊 Generate Analytics Report</button>
                    </div>
                    <div id="analyticsResults"></div>
                </div>
            </div>
        </div>
        
        <script>
            const API_BASE = window.location.origin;
            
            // Global variables
            let allDocuments = [];
            let allEmployees = [];
            let allQueries = [];
            
            // Initialize dashboard
            window.addEventListener('load', function() {
                refreshStats();
                loadDocuments();
                loadEmployeeStats();
                loadQueryHistory();
                
                // Auto-refresh every 10 seconds
                setInterval(refreshStats, 10000);
                setInterval(loadDocuments, 15000);
                setInterval(loadEmployeeStats, 20000);
                setInterval(loadQueryHistory, 25000);
            });
            
            // File upload handling
            document.getElementById('fileUpload').addEventListener('click', function() {
                document.getElementById('fileInput').click();
            });
            
            document.getElementById('fileInput').addEventListener('change', handleFileSelect);
            
            // Drag and drop
            document.getElementById('fileUpload').addEventListener('dragover', function(e) {
                e.preventDefault();
                this.classList.add('dragover');
            });
            
            document.getElementById('fileUpload').addEventListener('dragleave', function(e) {
                e.preventDefault();
                this.classList.remove('dragover');
            });
            
            document.getElementById('fileUpload').addEventListener('drop', function(e) {
                e.preventDefault();
                this.classList.remove('dragover');
                handleFileSelect({target: {files: e.dataTransfer.files}});
            });
            
            async function handleFileSelect(event) {
                const files = event.target.files;
                if (files.length > 0) {
                    const file = files[0];
                    
                    // Extract text from file
                    let content = '';
                    if (file.type === 'text/plain') {
                        content = await file.text();
                    } else {
                        content = `[Uploaded file: ${file.name} - Content extraction would be implemented here]`;
                    }
                    
                    // Auto-fill form
                    document.getElementById('docTitle').value = file.name.replace(/\\.[^/.]+$/, "");
                    document.getElementById('docContent').value = content;
                    
                    // Generate AI tags
                    await generateTags(content);
                }
            }
            
            async function generateTags(content) {
                try {
                    // Simple tag generation based on content keywords
                    const keywords = content.toLowerCase();
                    let tags = [];
                    
                    if (keywords.includes('policy') || keywords.includes('procedure')) tags.push('policy');
                    if (keywords.includes('employee') || keywords.includes('staff')) tags.push('hr');
                    if (keywords.includes('compliance') || keywords.includes('regulation')) tags.push('compliance');
                    if (keywords.includes('security') || keywords.includes('privacy')) tags.push('security');
                    if (keywords.includes('process') || keywords.includes('workflow')) tags.push('process');
                    if (keywords.includes('guideline') || keywords.includes('standard')) tags.push('guideline');
                    
                    if (tags.length === 0) tags = ['general'];
                    
                    document.getElementById('docTags').value = tags.join(', ');
                } catch (error) {
                    document.getElementById('docTags').value = 'general';
                }
            }
            
            // Tab management
            function showTab(tabName) {
                // Hide all tabs
                document.querySelectorAll('.tab-content').forEach(tab => {
                    tab.classList.remove('active');
                });
                document.querySelectorAll('.tab').forEach(tab => {
                    tab.classList.remove('active');
                });
                
                // Show selected tab
                document.getElementById(tabName + '-tab').classList.add('active');
                event.target.classList.add('active');
            }
            
            // Document upload
            document.getElementById('uploadForm').addEventListener('submit', async function(e) {
                e.preventDefault();
                
                const uploadBtn = document.getElementById('uploadBtn');
                const originalText = uploadBtn.textContent;
                uploadBtn.textContent = '⏳ Uploading...';
                uploadBtn.disabled = true;
                
                const formData = {
                    title: document.getElementById('docTitle').value,
                    content: document.getElementById('docContent').value,
                    category: document.getElementById('docCategory').value,
                    uploaded_by: document.getElementById('uploadedBy').value,
                    tags: document.getElementById('docTags').value.split(',').map(tag => tag.trim()).filter(tag => tag)
                };
                
                try {
                    const response = await fetch(`${API_BASE}/admin/upload-document`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(formData)
                    });
                    
                    const result = await response.json();
                    
                    if (response.ok) {
                        document.getElementById('uploadResult').innerHTML = 
                            `<div class="success">✅ Document uploaded successfully! ID: ${result.id}</div>`;
                        document.getElementById('uploadForm').reset();
                        document.getElementById('docTags').value = '';
                        refreshStats();
                        loadDocuments();
                    } else {
                        document.getElementById('uploadResult').innerHTML = 
                            `<div class="error">❌ Upload failed: ${result.detail}</div>`;
                    }
                } catch (error) {
                    document.getElementById('uploadResult').innerHTML = 
                        `<div class="error">❌ Upload failed: ${error.message}</div>`;
                } finally {
                    uploadBtn.textContent = originalText;
                    uploadBtn.disabled = false;
                }
            });
            
            // Refresh stats
            async function refreshStats() {
                try {
                    const response = await fetch(`${API_BASE}/admin/stats`);
                    const stats = await response.json();
                    
                    document.getElementById('totalDocs').textContent = stats.total_documents;
                    document.getElementById('totalEmployees').textContent = stats.active_employees;
                    document.getElementById('totalQueries').textContent = stats.total_queries;
                    document.getElementById('todayQueries').textContent = stats.today_queries;
                } catch (error) {
                    console.error('Failed to load stats:', error);
                }
            }
            
            // Load documents
            async function loadDocuments() {
                try {
                    const response = await fetch(`${API_BASE}/admin/documents`);
                    allDocuments = await response.json();
                    filterDocuments();
                } catch (error) {
                    document.getElementById('documentsList').innerHTML = 
                        `<div class="error">Failed to load documents: ${error.message}</div>`;
                }
            }
            
            // Filter documents
            function filterDocuments() {
                const filter = document.getElementById('docFilter').value.toLowerCase();
                const categoryFilter = document.getElementById('categoryFilter').value;
                
                let filtered = allDocuments.filter(doc => {
                    const matchesFilter = doc.title.toLowerCase().includes(filter) || 
                                        doc.tags.some(tag => tag.toLowerCase().includes(filter));
                    const matchesCategory = !categoryFilter || doc.category === categoryFilter;
                    return matchesFilter && matchesCategory;
                });
                
                let html = '';
                filtered.forEach(doc => {
                    html += `
                        <div class="data-item">
                            <h4>${doc.title}</h4>
                            <p><strong>ID:</strong> ${doc.id} | <strong>Category:</strong> ${doc.category}</p>
                            <p><strong>Uploaded:</strong> ${doc.uploaded_at || 'N/A'} by ${doc.uploaded_by}</p>
                            <p><strong>Tags:</strong> ${doc.tags.map(tag => `<span style="background: #e8f5e8; padding: 2px 6px; border-radius: 10px; font-size: 11px; margin-right: 5px; color: #2e7d2e; border: 1px solid #c8e6c8;">${tag}</span>`).join('')}</p>
                        </div>
                    `;
                });
                
                document.getElementById('documentsList').innerHTML = html || '<p>No documents found.</p>';
            }
            
            // Load employee statistics
            async function loadEmployeeStats() {
                try {
                    const response = await fetch(`${API_BASE}/admin/employee-stats`);
                    allEmployees = await response.json();
                    filterEmployees();
                } catch (error) {
                    document.getElementById('employeesList').innerHTML = 
                        `<div class="error">Failed to load employee stats: ${error.message}</div>`;
                }
            }
            
            // Filter employees
            function filterEmployees() {
                const filter = document.getElementById('empFilter').value.toLowerCase();
                const filtered = allEmployees.filter(emp => 
                    emp.employee_id.toLowerCase().includes(filter)
                );
                
                let html = '';
                filtered.forEach(emp => {
                    html += `
                        <div class="data-item">
                            <h4>👤 ${emp.employee_id}</h4>
                            <p><strong>Total Queries:</strong> ${emp.query_count}</p>
                            <p><strong>Last Activity:</strong> ${new Date(emp.last_activity).toLocaleString()}</p>
                        </div>
                    `;
                });
                
                document.getElementById('employeesList').innerHTML = html || '<p>No employees found.</p>';
            }
            
            // Sort employees
            function sortEmployees() {
                const sortBy = document.getElementById('sortEmployees').value;
                
                allEmployees.sort((a, b) => {
                    if (sortBy === 'queries') return b.query_count - a.query_count;
                    if (sortBy === 'recent') return new Date(b.last_activity) - new Date(a.last_activity);
                    if (sortBy === 'id') return a.employee_id.localeCompare(b.employee_id);
                });
                
                filterEmployees();
            }
            
            // Load query history
            async function loadQueryHistory() {
                const empFilter = document.getElementById('queryEmpFilter').value;
                const typeFilter = document.getElementById('queryTypeFilter').value;
                const dateFilter = document.getElementById('queryDateFilter').value;
                
                try {
                    let url = `${API_BASE}/admin/query-history?`;
                    if (empFilter) url += `employee_id=${empFilter}&`;
                    if (typeFilter) url += `query_type=${typeFilter}&`;
                    if (dateFilter) url += `date=${dateFilter}&`;
                    
                    const response = await fetch(url);
                    allQueries = await response.json();
                    
                    let html = '';
                    allQueries.forEach(query => {
                        html += `
                            <div class="data-item">
                                <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                                    <strong>👤 ${query.employee_id}</strong>
                                    <span style="font-size: 12px; color: #666;">${new Date(query.timestamp).toLocaleString()}</span>
                                </div>
                                <p><strong>${query.query_type.toUpperCase()}:</strong> ${query.query}</p>
                                ${query.doc_id ? `<p><strong>Document:</strong> ${query.doc_id}</p>` : ''}
                                <p style="font-size: 12px; color: #666;">Query ID: ${query.query_id}</p>
                            </div>
                        `;
                    });
                    
                    document.getElementById('queryHistoryList').innerHTML = html || '<p>No queries found.</p>';
                } catch (error) {
                    document.getElementById('queryHistoryList').innerHTML = 
                        `<div class="error">Failed to load query history: ${error.message}</div>`;
                }
            }
            
            // Generate analytics
            async function generateAnalytics() {
                try {
                    const response = await fetch(`${API_BASE}/admin/analytics`);
                    const analytics = await response.json();
                    
                    document.getElementById('avgQueriesPerEmployee').textContent = analytics.avg_queries_per_employee;
                    document.getElementById('mostPopularDoc').textContent = analytics.most_popular_document;
                    document.getElementById('mostActiveEmployee').textContent = analytics.most_active_employee;
                    document.getElementById('peakHour').textContent = analytics.peak_usage_hour + ':00';
                    
                    // Display detailed analytics
                    let html = '<h4>📊 Detailed Analytics</h4>';
                    html += `<p><strong>Top Documents:</strong> ${analytics.top_documents.join(', ')}</p>`;
                    html += `<p><strong>Query Type Distribution:</strong> ${Object.entries(analytics.query_type_distribution).map(([type, count]) => `${type}: ${count}`).join(', ')}</p>`;
                    html += `<p><strong>Daily Average:</strong> ${analytics.daily_average} queries per day</p>`;
                    
                    document.getElementById('analyticsResults').innerHTML = html;
                } catch (error) {
                    document.getElementById('analyticsResults').innerHTML = 
                        `<div class="error">Failed to generate analytics: ${error.message}</div>`;
                }
            }
            
            // Export queries to CSV
            function exportQueries() {
                if (allQueries.length === 0) {
                    alert('No queries to export. Please load query history first.');
                    return;
                }
                
                let csv = 'Timestamp,Employee ID,Query,Query Type,Document ID,Query ID\\n';
                allQueries.forEach(query => {
                    csv += `"${query.timestamp}","${query.employee_id}","${query.query}","${query.query_type}","${query.doc_id || ''}","${query.query_id}"\\n`;
                });
                
                const blob = new Blob([csv], { type: 'text/csv' });
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `employee_queries_${new Date().toISOString().split('T')[0]}.csv`;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                window.URL.revokeObjectURL(url);
            }
        </script>
    </body>
    </html>
    """