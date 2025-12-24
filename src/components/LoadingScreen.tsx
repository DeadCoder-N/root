import { useEffect, useState, useRef } from 'react';

export default function LoadingScreen() {
  const [isVisible, setIsVisible] = useState(true);
  const [progress, setProgress] = useState(0);
  const [currentMessage, setCurrentMessage] = useState(0);
  const [showGlitch, setShowGlitch] = useState(false);
  const audioRef = useRef<HTMLAudioElement | null>(null);

  const bootMessages = [
    'INITIALIZING SECURITY PROTOCOLS...',
    'LOADING PENETRATION TESTING MODULES...',
    'SCANNING VULNERABILITY DATABASE...',
    'ESTABLISHING ENCRYPTED CONNECTION...',
    'ACTIVATING CYBER DEFENSE SYSTEMS...',
    'DEAD CODER INTERFACE READY'
  ];

  useEffect(() => {
    // Create soft ambient loading sound
    const createAmbientSound = () => {
      const audioContext = new (window.AudioContext || (window as any).webkitAudioContext)();
      const gainNode = audioContext.createGain();
      const filterNode = audioContext.createBiquadFilter();
      
      // Create multiple oscillators for rich ambient sound
      const oscillators = [];
      const frequencies = [220, 330, 440]; // Soft harmonic frequencies
      
      for (let i = 0; i < frequencies.length; i++) {
        const oscillator = audioContext.createOscillator();
        const oscGain = audioContext.createGain();
        
        oscillator.frequency.value = frequencies[i];
        oscillator.type = 'sine'; // Soft sine wave
        
        // Very soft volume that fades in
        oscGain.gain.setValueAtTime(0, audioContext.currentTime);
        oscGain.gain.linearRampToValueAtTime(0.02 / frequencies.length, audioContext.currentTime + 0.5);
        
        oscillator.connect(oscGain);
        oscGain.connect(filterNode);
        oscillators.push({ oscillator, gain: oscGain });
      }
      
      // Low-pass filter for warmth
      filterNode.type = 'lowpass';
      filterNode.frequency.value = 800;
      filterNode.connect(gainNode);
      gainNode.connect(audioContext.destination);
      
      // Master volume - very soft
      gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
      
      // Start all oscillators
      oscillators.forEach(({ oscillator }) => {
        oscillator.start(audioContext.currentTime);
      });
      
      return { audioContext, oscillators, gainNode };
    };

    // Create beep sound for interactions
    const createBeepSound = (frequency: number, duration: number) => {
      const audioContext = new (window.AudioContext || (window as any).webkitAudioContext)();
      const oscillator = audioContext.createOscillator();
      const gainNode = audioContext.createGain();
      
      oscillator.connect(gainNode);
      gainNode.connect(audioContext.destination);
      
      oscillator.frequency.value = frequency;
      oscillator.type = 'sine'; // Changed to sine for softer sound
      
      gainNode.gain.setValueAtTime(0.05, audioContext.currentTime); // Reduced volume
      gainNode.gain.exponentialRampToValueAtTime(0.001, audioContext.currentTime + duration);
      
      oscillator.start(audioContext.currentTime);
      oscillator.stop(audioContext.currentTime + duration);
    };

    // Start ambient sound
    let ambientAudio: any = null;
    try {
      ambientAudio = createAmbientSound();
    } catch (error) {
      console.log('Audio context not available');
    }

    // Progress animation
    const progressInterval = setInterval(() => {
      setProgress(prev => {
        if (prev >= 100) {
          clearInterval(progressInterval);
          return 100;
        }
        return prev + 2;
      });
    }, 40);

    // Message cycling
    const messageInterval = setInterval(() => {
      setCurrentMessage(prev => {
        const next = (prev + 1) % bootMessages.length;
        if (ambientAudio) {
          createBeepSound(600 + Math.random() * 200, 0.08); // Softer random beep
        }
        return next;
      });
    }, 300);

    // Glitch effect
    const glitchInterval = setInterval(() => {
      setShowGlitch(true);
      if (ambientAudio) {
        createBeepSound(300, 0.03); // Softer glitch sound
      }
      setTimeout(() => setShowGlitch(false), 100);
    }, 800);

    // Final exit
    const exitTimer = setTimeout(() => {
      if (ambientAudio) {
        // Fade out ambient sound
        ambientAudio.gainNode.gain.linearRampToValueAtTime(0, ambientAudio.audioContext.currentTime + 0.5);
        createBeepSound(880, 0.2); // Softer success sound
        
        // Stop ambient sound after fade
        setTimeout(() => {
          ambientAudio.oscillators.forEach(({ oscillator }: any) => {
            try {
              oscillator.stop();
            } catch (e) {}
          });
        }, 500);
      }
      setTimeout(() => setIsVisible(false), 300);
    }, 2000);

    return () => {
      clearInterval(progressInterval);
      clearInterval(messageInterval);
      clearInterval(glitchInterval);
      clearTimeout(exitTimer);
      
      // Clean up ambient sound
      if (ambientAudio) {
        ambientAudio.oscillators.forEach(({ oscillator }: any) => {
          try {
            oscillator.stop();
          } catch (e) {}
        });
      }
    };
  }, []);

  if (!isVisible) return null;

  return (
    <div className="fixed inset-0 bg-black z-50 overflow-hidden">
      {/* Matrix Rain Background */}
      <div className="matrix-rain">
        {Array.from({ length: 50 }).map((_, i) => (
          <div
            key={i}
            className="matrix-column"
            style={{
              left: `${i * 2}%`,
              animationDelay: `${Math.random() * 2}s`,
              animationDuration: `${2 + Math.random() * 3}s`
            }}
          >
            {Array.from({ length: 20 }).map((_, j) => (
              <span key={j} className="matrix-char">
                {String.fromCharCode(0x30A0 + Math.random() * 96)}
              </span>
            ))}
          </div>
        ))}
      </div>

      {/* Scan Lines */}
      <div className="scan-lines"></div>
      <div className="scan-line-moving"></div>

      {/* Main Content */}
      <div className="relative z-10 flex items-center justify-center min-h-screen">
        <div className="text-center space-y-8">
          
          {/* Hexagonal Progress */}
          <div className="relative w-32 h-32 mx-auto">
            <svg className="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
              {/* Background Hexagon */}
              <polygon
                points="50,5 85,25 85,75 50,95 15,75 15,25"
                fill="none"
                stroke="rgba(6, 182, 212, 0.3)"
                strokeWidth="2"
              />
              {/* Progress Hexagon */}
              <polygon
                points="50,5 85,25 85,75 50,95 15,75 15,25"
                fill="none"
                stroke="#06b6d4"
                strokeWidth="3"
                strokeDasharray="240"
                strokeDashoffset={240 - (progress * 2.4)}
                className="transition-all duration-100 ease-out"
              />
            </svg>
            
            {/* Center Progress Text */}
            <div className="absolute inset-0 flex items-center justify-center">
              <div className="text-center">
                <div className="text-2xl font-bold text-accent-teal font-mono">
                  {Math.round(progress)}%
                </div>
                <div className="w-4 h-4 bg-accent-teal rounded-full mx-auto mt-1 animate-pulse"></div>
              </div>
            </div>
          </div>

          {/* Glitch Logo */}
          <div className="relative">
            <h1 className={`text-4xl font-bold font-mono ${
              showGlitch ? 'glitch-text' : 'text-accent-teal'
            } transition-all duration-100`}>
              DEAD_CODER
            </h1>
            {showGlitch && (
              <>
                <h1 className="absolute top-0 left-0 text-4xl font-bold font-mono text-red-500 opacity-70 transform translate-x-1">
                  DEAD_CODER
                </h1>
                <h1 className="absolute top-0 left-0 text-4xl font-bold font-mono text-blue-500 opacity-70 transform -translate-x-1">
                  DEAD_CODER
                </h1>
              </>
            )}
          </div>

          {/* Boot Messages */}
          <div className="h-16 flex items-center justify-center">
            <p className="text-green-400 font-mono text-sm typewriter-effect">
              {'>'} {bootMessages[currentMessage]}
              <span className="animate-pulse">_</span>
            </p>
          </div>

          {/* System Status */}
          <div className="grid grid-cols-3 gap-4 text-xs font-mono">
            <div className="text-green-400">
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
                <span>FIREWALL: ACTIVE</span>
              </div>
            </div>
            <div className="text-yellow-400">
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-yellow-400 rounded-full animate-pulse"></div>
                <span>SCAN: RUNNING</span>
              </div>
            </div>
            <div className="text-blue-400">
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-blue-400 rounded-full animate-pulse"></div>
                <span>VPN: SECURE</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}