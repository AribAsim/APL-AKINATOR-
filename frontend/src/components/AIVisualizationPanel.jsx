import { useEffect, useState } from 'react';
import '../styles/AIVisualizationPanel.css';

export default function AIVisualizationPanel({ 
  confidence = 0, 
  topSuspects = [],
  trickDetected = false,
  thinking = false 
}) {
  const [displayConfidence, setDisplayConfidence] = useState(0);
  const [playerImages, setPlayerImages] = useState({});

  useEffect(() => {
    // Animate confidence bar
    const timer = setTimeout(() => {
      setDisplayConfidence(Math.min(confidence * 100, 100));
    }, 100);
    return () => clearTimeout(timer);
  }, [confidence]);

  useEffect(() => {
    // Fetch real-time player photos from Wikipedia search using a robust progressive fallback method
    topSuspects.forEach(async (suspect) => {
      const name = suspect.name;
      if (playerImages[name] !== undefined) return; // Already cached or fetching

      // Mark as loading to avoid duplicate fetches
      setPlayerImages(prev => ({ ...prev, [name]: 'loading' }));

      const tryQuery = async (q) => {
        try {
          const url = `https://en.wikipedia.org/w/api.php?action=query&generator=search&gsrsearch=${encodeURIComponent(q)}&gsrlimit=1&prop=pageimages&pithumbsize=100&format=json&origin=*`;
          const res = await fetch(url);
          const data = await res.json();
          if (data.query && data.query.pages) {
            const pages = data.query.pages;
            const pageId = Object.keys(pages)[0];
            const thumbnail = pages[pageId].thumbnail;
            if (thumbnail && thumbnail.source) {
              return thumbnail.source;
            }
          }
        } catch (e) {
          console.error("Wikipedia query failed for", q, e);
        }
        return null;
      };

      try {
        // Stage 1: Try full name with "ipl"
        let img = await tryQuery(name + " ipl");
        
        // Stage 2: Try full name with "cricket"
        if (!img) {
          img = await tryQuery(name + " cricket");
        }
        
        // Stage 3: Try stripping leading uppercase initials (e.g. "DP Conway" -> "Conway", "AT Rayudu" -> "Rayudu")
        if (!img) {
          const initialsRegex = /^[A-Z\s.-]+(?=[A-Z][a-z])/;
          if (initialsRegex.test(name)) {
            const stripped = name.replace(initialsRegex, "").trim();
            img = await tryQuery(stripped + " cricket");
          }
        }
        
        // Stage 4: Try raw name direct match
        if (!img) {
          img = await tryQuery(name);
        }

        setPlayerImages(prev => ({ ...prev, [name]: img }));
      } catch (err) {
        console.error("Error in player image pipeline for:", name, err);
        setPlayerImages(prev => ({ ...prev, [name]: null }));
      }
    });
  }, [topSuspects, playerImages]);

  const maskName = (name) => {
    return name;
  };

  return (
    <div className="ai-visualization-panel">
      <div className="ai-header">🤖 AI Thinking</div>

      {/* Confidence Bar */}
      <div className="confidence-section">
        <div className="confidence-label">
          <span>Confidence</span>
          <span className="confidence-value">{Math.round(displayConfidence)}%</span>
        </div>
        <div className="confidence-bar-container">
          <div 
            className={`confidence-bar ${
              trickDetected ? 'trick-detected' : ''
            }`}
            style={{ width: `${displayConfidence}%` }}
          />
        </div>
        {trickDetected && (
          <div className="trick-warning">
            ⚠️ Inconsistency detected! The AI noticed something odd...
          </div>
        )}
      </div>

      {/* Top Suspects */}
      <div className="suspects-section">
        <div className="suspects-label">
          {thinking ? '🔍 Analyzing...' : '🎯 Top Suspects'}
        </div>
        
        <div className="suspects-list">
          {topSuspects.length > 0 ? (
            topSuspects.map((suspect, idx) => (
              <div 
                key={idx} 
                className="suspect-item"
                style={{ animationDelay: `${idx * 0.1}s` }}
              >
                <div className="suspect-rank">#{idx + 1}</div>
                <div className="suspect-avatar-container">
                  {playerImages[suspect.name] && playerImages[suspect.name] !== 'loading' ? (
                    <img 
                      src={playerImages[suspect.name]}
                      alt={suspect.name} 
                      className="suspect-avatar real-photo"
                      onError={(e) => {
                        e.target.style.display = 'none';
                        const sibling = e.target.nextSibling;
                        if (sibling) sibling.style.display = 'block';
                      }}
                    />
                  ) : null}
                  <img 
                    src={`https://api.dicebear.com/7.x/initials/svg?seed=${encodeURIComponent(suspect.name)}&radius=50&backgroundColor=0d8abc,00bcd4,3f51b5,2196f3,009688,4caf50,ff9800&fontFamily=monospace&bold=true`}
                    alt={suspect.name} 
                    className="suspect-avatar initials-fallback"
                    style={{ 
                      display: playerImages[suspect.name] && playerImages[suspect.name] !== 'loading' ? 'none' : 'block' 
                    }}
                  />
                </div>
                <div className="suspect-name">{maskName(suspect.name)}</div>
                <div className="suspect-probability">
                  {(suspect.probability * 100).toFixed(0)}%
                </div>
              </div>
            ))
          ) : (
            <div className="suspects-empty">
              Gathering information...
            </div>
          )}
        </div>
      </div>

      {/* Thinking Animation */}
      {thinking && (
        <div className="ai-thinking-animation">
          <div className="dot"></div>
          <div className="dot"></div>
          <div className="dot"></div>
        </div>
      )}
    </div>
  );
}
