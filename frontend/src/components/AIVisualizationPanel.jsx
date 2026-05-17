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

  // Comprehensive IPL player name expansion map
  const PLAYER_FULL_NAMES = {
    // India legends
    "MS Dhoni": "Mahendra Singh Dhoni",
    "V Kohli": "Virat Kohli",
    "RG Sharma": "Rohit Sharma",
    "SR Tendulkar": "Sachin Tendulkar",
    "A Kumble": "Anil Kumble",
    "A Chopra": "Aakash Chopra",
    "SC Ganguly": "Sourav Ganguly",
    "VVS Laxman": "VVS Laxman",
    "R Dravid": "Rahul Dravid",
    "Yuvraj Singh": "Yuvraj Singh",
    "Harbhajan Singh": "Harbhajan Singh",
    "Z Khan": "Zaheer Khan",
    "IK Pathan": "Irfan Pathan",
    "YK Pathan": "Yusuf Pathan",
    "S Dhawan": "Shikhar Dhawan",
    "KL Rahul": "KL Rahul",
    "R Ashwin": "Ravichandran Ashwin",
    "RA Jadeja": "Ravindra Jadeja",
    "JJ Bumrah": "Jasprit Bumrah",
    "HH Pandya": "Hardik Pandya",
    "KH Pandya": "Krunal Pandya",
    "SR Watson": "Shane Watson",
    "SK Raina": "Suresh Raina",
    "G Gambhir": "Gautam Gambhir",
    "M Vijay": "Murali Vijay",
    "AT Rayudu": "Ambati Rayudu",
    "PP Chawla": "Piyush Chawla",
    "SP Narine": "Sunil Narine",
    "DJ Bravo": "Dwayne Bravo",
    "Abdur Razzak": "Abdur Razzak",
    "A Badoni": "Ayush Badoni",
    "A Chandila": "Ajit Chandila",
    "A Choudhary": "Ankit Choudhary",
    "A Dananjaya": "Akila Dananjaya",
    "A Kamboj": "Anmolpreet Kamboj",
    "A Mhatre": "Angkrish Mhatre",
    "A Ashish Reddy": "A Ashish Reddy",
    "A Nortje": "Anrich Nortje",
    "A Mishra": "Amit Mishra",
    "A Symonds": "Andrew Symonds",
    "A Flintoff": "Andrew Flintoff",
    "AB de Villiers": "AB de Villiers",
    "AC Gilchrist": "Adam Gilchrist",
    "AD Russell": "Andre Russell",
    "AJ Finch": "Aaron Finch",
    "B Kumar": "Bhuvneshwar Kumar",
    "BA Stokes": "Ben Stokes",
    "CH Gayle": "Chris Gayle",
    "CK Nayudu": "CK Nayudu",
    "DA Warner": "David Warner",
    "DJ Mitchell": "Daryl Mitchell",
    "DP Conway": "Devon Conway",
    "DJ Hussey": "David Hussey",
    "DL Vettori": "Daniel Vettori",
    "DT Christian": "Dan Christian",
    "DS Kulkarni": "Dhawal Kulkarni",
    "EJG Morgan": "Eoin Morgan",
    "F du Plessis": "Faf du Plessis",
    "FA Behardien": "Farhaan Behardien",
    "GB Hogg": "George Hogg",
    "GD McGrath": "Glenn McGrath",
    "GJ Maxwell": "Glenn Maxwell",
    "H Klaasen": "Heinrich Klaasen",
    "HC Brook": "Harry Brook",
    "I Sharma": "Ishant Sharma",
    "IA Healy": "Ian Healy",
    "JC Buttler": "Jos Buttler",
    "JM Bairstow": "Jonny Bairstow",
    "JR Hazlewood": "Josh Hazlewood",
    "JP Faulkner": "James Faulkner",
    "JDP Oram": "Jacob Oram",
    "K Rabada": "Kagiso Rabada",
    "KA Pollard": "Kieron Pollard",
    "KC Sangakkara": "Kumar Sangakkara",
    "KD Karthik": "Dinesh Karthik",
    "KS Williamson": "Kane Williamson",
    "L Ngidi": "Lungi Ngidi",
    "LMP Simmons": "Lendl Simmons",
    "M Morkel": "Morne Morkel",
    "MA Starc": "Mitchell Starc",
    "MEK Hussey": "Mike Hussey",
    "MF Maharoof": "Farveez Maharoof",
    "MG Johnson": "Mitchell Johnson",
    "MJ McClenaghan": "Mitchell McClenaghan",
    "MM Ali": "Moeen Ali",
    "MM Patel": "Munaf Patel",
    "MK Tiwary": "Manoj Tiwary",
    "N Rana": "Nitish Rana",
    "N Pooran": "Nicholas Pooran",
    "NL McCullum": "Nathan McCullum",
    "PA Patel": "Parthiv Patel",
    "PD Collingwood": "Paul Collingwood",
    "PM Nevill": "Peter Nevill",
    "Q de Kock": "Quinton de Kock",
    "R Bhatia": "Rajat Bhatia",
    "R Goyal": "Rahul Goyal",
    "R Parag": "Riyan Parag",
    "R Tewatia": "Rahul Tewatia",
    "R Bishnoi": "Ravi Bishnoi",
    "RD Gaikwad": "Ruturaj Gaikwad",
    "RK Singh": "RP Singh",
    "RR Pant": "Rishabh Pant",
    "RS Gavaskar": "Rohan Gavaskar",
    "S Gill": "Shubman Gill",
    "S Iyer": "Shreyas Iyer",
    "S Samson": "Sanju Samson",
    "SB Wagh": "Shrikant Wagh",
    "SC Ganguly": "Sourav Ganguly",
    "SE Marsh": "Shaun Marsh",
    "SL Malinga": "Lasith Malinga",
    "SM Pollock": "Shaun Pollock",
    "SS Iyer": "Shreyas Iyer",
    "SV Samson": "Sanju Samson",
    "T Natarajan": "T Natarajan",
    "TA Boult": "Trent Boult",
    "TM Head": "Travis Head",
    "TM Srivastava": "Tanmay Srivastava",
    "UT Yadav": "Umesh Yadav",
    "V Shankar": "Vijay Shankar",
    "VR Aaron": "Varun Aaron",
    "W Jaffer": "Wasim Jaffer",
    "WD Parnell": "Wayne Parnell",
    "WP Saha": "Wriddhiman Saha",
    "Y Chahal": "Yuzvendra Chahal",
    "YBK Jaiswal": "Yashasvi Jaiswal",
    "Kartik Sharma": "Kartik Sharma",
  };

  const expandName = (name) => PLAYER_FULL_NAMES[name] || name;

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
                <div className="suspect-name">{expandName(suspect.name)}</div>
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
