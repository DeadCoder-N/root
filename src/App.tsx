import { useEffect, useState } from 'react';
import Header from './components/Header';
import Hero from './components/Hero';
import About from './components/About';
import Skills from './components/Skills';
import Experience from './components/Experience';
import Projects from './components/Projects';
import CTFShowcase from './components/CTFShowcase';
import SecurityTools from './components/SecurityTools';
import InteractiveTerminal from './components/InteractiveTerminal';
import Blog from './components/Blog';
import Contact from './components/Contact';
import Footer from './components/Footer';
import ParticleSystem from './components/ParticleSystem';
import CustomCursor from './components/CustomCursor';
import AnimatedBackground from './components/AnimatedBackground';
import LoadingScreen from './components/LoadingScreen';

function App() {
  const [isDarkMode, setIsDarkMode] = useState(true);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const timer = setTimeout(() => {
      setIsLoading(false);
    }, 2000);
    return () => clearTimeout(timer);
  }, []);

  useEffect(() => {
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
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
      }
    );

    const animatedElements = document.querySelectorAll('[class*="fade-in"]');
    animatedElements.forEach((el) => observer.observe(el));

    const handleSmoothScroll = (e: Event) => {
      const target = e.target as HTMLAnchorElement;
      if (target.hash) {
        e.preventDefault();
        const element = document.querySelector(target.hash);
        if (element) {
          element.scrollIntoView({ behavior: 'smooth' });
        }
      }
    };

    document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
      anchor.addEventListener('click', handleSmoothScroll);
    });

    return () => {
      const animatedElements = document.querySelectorAll('[class*="fade-in"]');
      animatedElements.forEach((el) => observer.unobserve(el));
      document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
        anchor.removeEventListener('click', handleSmoothScroll);
      });
    };
  }, []);

  useEffect(() => {
    if (isDarkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [isDarkMode]);

  const toggleTheme = () => {
    setIsDarkMode(!isDarkMode);
  };

  return (
    <>
      {isLoading && <LoadingScreen />}
      <div className="min-h-screen bg-primary text-text-primary">
        <AnimatedBackground />
        <ParticleSystem />
        <CustomCursor />
        <Header isDark={isDarkMode} toggleTheme={toggleTheme} />
        <Hero />
        <About />
        <Skills />
        <Experience />
        <Projects />
        <CTFShowcase />
        <SecurityTools />
        <InteractiveTerminal />
        <Blog />
        <Contact />
        <Footer />
      </div>
    </>
  );
}

export default App;
