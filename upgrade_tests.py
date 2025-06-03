import os
import re

# Modern CSS content (you can customize this)
CSS_CONTENT = """
/* Modern Design - Mocks Wallah Upgrade */
* { margin: 0; padding: 0; box-sizing: border-box; }

:root {
    --primary: #4361ee;
    --secondary: #3f37c9;
    --success: #4cc9f0;
    --danger: #f72585;
    --warning: #f8961e;
    --light: #f8f9fa;
    --dark: #212529;
}

body {
    font-family: 'Poppins', sans-serif;
    background: #f5f7fa;
    min-height: 100vh;
    color: #2d3436;
    line-height: 1.6;
}

/* Header Styles */
.hdr {
    background: var(--primary);
    color: white;
    padding: 1rem;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    display: flex;
    justify-content: space-between;
    align-items: center;
}

/* Question Card */
.qc {
    background: white;
    border-radius: 12px;
    padding: 1.5rem;
    margin: 1rem auto;
    max-width: 800px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.05);
}

/* Leaderboard Styles */
.leaderboard {
    background: white;
    border-radius: 12px;
    padding: 1.5rem;
    margin: 1rem auto;
    max-width: 800px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.05);
}

/* Responsive Design */
@media (max-width: 768px) {
    .qc, .leaderboard {
        margin: 1rem;
        padding: 1rem;
    }
}
"""

# Leaderboard JavaScript integration
LEADERBOARD_JS = """
// Leaderboard Integration
const SHEET_ID = '1OmdTp2XjSEqljr76X-5Evze9PukVxnzjrsvFvgJBvAE';
const SHEET_NAME = 'Leaderboard';

async function updateLeaderboard() {
    try {
        const response = await fetch(`https://docs.google.com/spreadsheets/d/${SHEET_ID}/gviz/tq?tqx=out:json&sheet=${SHEET_NAME}`);
        const data = await response.text();
        const json = JSON.parse(data.substr(47).slice(0, -2));
        
        const rows = json.table.rows;
        let leaderboardHTML = '<h3>🏆 Top Scores</h3><ol>';
        
        rows.slice(0, 5).forEach(row => {
            const [rank, name, score] = row.c;
            leaderboardHTML += `<li>${name?.v || 'Anonymous'}: ${score?.v || 'N/A'}</li>`;
        });
        
        leaderboardHTML += '</ol>';
        document.getElementById('leaderboard').innerHTML = leaderboardHTML;
    } catch (error) {
        console.error('Leaderboard error:', error);
    }
}

// Initialize leaderboard when page loads
window.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('leaderboard')) {
        updateLeaderboard();
        setInterval(updateLeaderboard, 30000); // Update every 30 seconds
    }
    
    // Save score on test submission
    const originalSub = window.sub;
    window.sub = function() {
        const result = originalSub.apply(this, arguments);
        saveScore();
        return result;
    };
});

async function saveScore() {
    const userName = localStorage.getItem('userName') || 'Anonymous';
    const score = document.getElementById('fs')?.textContent || '0/0';
    
    try {
        await fetch(`https://docs.google.com/forms/d/e/YOUR_FORM_ID/formResponse`, {
            method: 'POST',
            mode: 'no-cors',
            body: new URLSearchParams({
                'entry.1234567890': userName,
                'entry.0987654321': score
            })
        });
    } catch (error) {
        console.error('Score save error:', error);
    }
}
"""

def upgrade_files():
    # Create CSS file
    with open('style.css', 'w') as f:
        f.write(CSS_CONTENT)
    
    # Process each HTML file
    for filename in os.listdir('.'):
        if filename.startswith('day') and filename.endswith('.html'):
            with open(filename, 'r+') as f:
                content = f.read()
                
                # 1. Add CSS link
                content = content.replace('<head>', 
                    '''<head>
    <link rel="stylesheet" href="style.css">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600&display=swap" rel="stylesheet">''')
                
                # 2. Add leaderboard section
                if '<div id="leaderboard"' not in content:
                    content = content.replace('</div> <!-- end main -->', 
                        '''<div class="leaderboard" id="leaderboard">
    <p>Loading leaderboard...</p>
</div>
</div> <!-- end main -->''')
                
                # 3. Add JavaScript
                content = content.replace('</body>', 
                    f'''<script>
    {LEADERBOARD_JS}
</script>
</body>''')
                
                # 4. Update name handling
                content = content.replace('function startTest() {', 
                    '''function startTest() {
    const name = document.getElementById("user-name").value;
    localStorage.setItem('userName', name);''')
                
                # Write changes
                f.seek(0)
                f.write(content)
                f.truncate()
    
    print("Upgrade complete! All files updated with:")
    print("- Modern CSS styles")
    print("- Leaderboard integration")
    print("- Google Sheets connection")

if __name__ == "__main__":
    upgrade_files()
