'use client';

import { Suspense, lazy, useEffect, useState } from 'react';
import type { Application } from '@splinetool/runtime';
const Spline = lazy(() => import('@splinetool/react-spline'));

interface InteractiveRobotSplineProps {
  scene: string;
  className?: string;
}

export function InteractiveRobotSpline({ scene, className }: InteractiveRobotSplineProps) {
  const [isMobile, setIsMobile] = useState(false);

  useEffect(() => {
    const checkMobile = () => setIsMobile(window.innerWidth < 768);
    checkMobile();
    window.addEventListener('resize', checkMobile);
    return () => window.removeEventListener('resize', checkMobile);
  }, []);

  const onLoad = (spline: Application) => {
    if (isMobile) {
      spline.setZoom(0.7);
    }
  };

  return (
    <Suspense
      fallback={
        <div className={`w-full h-full flex items-center justify-center bg-gray-900 text-white ${className}`}>
          <svg className="animate-spin h-5 w-5 text-white mr-3" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l2-2.647z"></path>
          </svg>
        </div>
      }
    >
      <div className="relative w-full h-full pointer-events-none">
        <Spline
          scene={scene}
          className={className}
          onLoad={onLoad}
        />
        <style>{`
          canvas {
            touch-action: none !important;
          }
          #spline-watermark,
          [class*="watermark"],
          [class*="logo"],
          a[href*="spline"],
          a[href*="spline.design"],
          canvas + div,
          canvas ~ div > a,
          div[style*="position: absolute"][style*="bottom"],
          div[style*="z-index"] > a {
            display: none !important;
            opacity: 0 !important;
            visibility: hidden !important;
            pointer-events: none !important;
          }
        `}</style>
        <div className="absolute bottom-0 left-0 right-0 h-14 bg-primary pointer-events-none z-50" />
      </div>
    </Suspense>
  );
}
