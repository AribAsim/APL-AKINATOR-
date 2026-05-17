import React, { useEffect, useRef } from 'react';
import anime from 'animejs';
import { getMascotImage } from '../utils/getMascotImage';

export const Mascot = ({ loading, confidence, selectedTeam }) => {
  const imgSrc = getMascotImage(selectedTeam);
  const mascotRef = useRef(null);

  useEffect(() => {
    // Idle "breathing" animation
    const breathe = anime({
      targets: mascotRef.current,
      translateY: [-5, 5],
      scale: [1, 1.02],
      duration: 3000,
      direction: 'alternate',
      loop: true,
      easing: 'easeInOutQuad'
    });

    return () => breathe.pause();
  }, []);

  useEffect(() => {
    // React to state changes
    if (mascotRef.current) {
      anime({
        targets: mascotRef.current,
        scale: [1.2, 1],
        rotate: loading ? [0, 5, -5, 0] : 0,
        duration: 500,
        easing: 'easeOutElastic(1, .6)'
      });
    }
  }, [loading, confidence]);

  return (
    <div className="mascot-stage">
      <div className="mascot-glow"></div>
      <img 
        ref={mascotRef}
        src={imgSrc} 
        alt="AI Mascot" 
        className="mascot-img" 
      />
    </div>
  );
};
