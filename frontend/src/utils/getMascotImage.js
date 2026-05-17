import neutralImg from '../assets/mascot/neutral.svg';
import confidentImg from '../assets/mascot/confident.svg';
import confusedImg from '../assets/mascot/confused.svg';
import thinkingImg from '../assets/mascot/thinking.svg';

export const getMascotImage = (loading, confidence, questionCount) => {
  if (loading) return thinkingImg;
  
  // Confident/Smirking state
  if (confidence > 0.85) return confidentImg;
  
  // Thinking state
  if (confidence > 0.5) return neutralImg;
  
  // Confused/Early game state
  return confusedImg;
};
