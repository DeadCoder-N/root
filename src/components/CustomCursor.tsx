import { useEffect, useRef, useState } from 'react';

export default function CustomCursor() {
  const cursorRef = useRef<HTMLDivElement>(null);
  const trailRef = useRef<HTMLDivElement>(null);
  const [isHovering, setIsHovering] = useState(false);

  useEffect(() => {
    const cursor = cursorRef.current;
    const trail = trailRef.current;
    if (!cursor || !trail) return;

    let mouseX = 0;
    let mouseY = 0;
    let trailX = 0;
    let trailY = 0;

    const updateCursor = (e: MouseEvent) => {
      mouseX = e.clientX;
      mouseY = e.clientY;
      cursor.style.left = mouseX + 'px';
      cursor.style.top = mouseY + 'px';
    };

    const updateTrail = () => {
      trailX += (mouseX - trailX) * 0.1;
      trailY += (mouseY - trailY) * 0.1;
      trail.style.left = trailX + 'px';
      trail.style.top = trailY + 'px';
      requestAnimationFrame(updateTrail);
    };

    const handleMouseEnter = () => setIsHovering(true);
    const handleMouseLeave = () => setIsHovering(false);

    document.addEventListener('mousemove', updateCursor);
    updateTrail();

    // Add hover effects to interactive elements
    const interactiveElements = document.querySelectorAll('a, button, .glass-card, .skill-badge');
    interactiveElements.forEach(el => {
      el.addEventListener('mouseenter', handleMouseEnter);
      el.addEventListener('mouseleave', handleMouseLeave);
    });

    return () => {
      document.removeEventListener('mousemove', updateCursor);
      interactiveElements.forEach(el => {
        el.removeEventListener('mouseenter', handleMouseEnter);
        el.removeEventListener('mouseleave', handleMouseLeave);
      });
    };
  }, []);

  return (
    <>
      <div
        ref={trailRef}
        className={`fixed w-8 h-8 pointer-events-none z-50 transition-all duration-300 ${
          isHovering ? 'scale-150 opacity-30' : 'scale-100 opacity-20'
        }`}
        style={{
          background: 'radial-gradient(circle, #06b6d4 0%, transparent 70%)',
          transform: 'translate(-50%, -50%)',
          borderRadius: '50%',
        }}
      />
      <div
        ref={cursorRef}
        className={`fixed w-2 h-2 pointer-events-none z-50 transition-all duration-150 ${
          isHovering ? 'scale-150' : 'scale-100'
        }`}
        style={{
          background: '#06b6d4',
          transform: 'translate(-50%, -50%)',
          borderRadius: '50%',
          boxShadow: '0 0 10px #06b6d4',
        }}
      />
    </>
  );
}