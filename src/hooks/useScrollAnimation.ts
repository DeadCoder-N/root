import { useEffect, useRef } from 'react';

export const useScrollAnimation = (animationType: 'fade-in' | 'fade-in-left' | 'fade-in-right' | 'fade-in-scale' | 'fade-in-stagger' = 'fade-in') => {
  const ref = useRef<HTMLElement>(null);

  useEffect(() => {
    const element = ref.current;
    if (!element) return;

    element.classList.add(animationType);

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('visible');
          } else {
            entry.target.classList.remove('visible');
          }
        });
      },
      {
        threshold: 0.15,
        rootMargin: '-50px 0px -50px 0px'
      }
    );

    observer.observe(element);

    return () => {
      observer.unobserve(element);
    };
  }, [animationType]);

  return ref;
};