import { ArrowDown, Github, Linkedin, Mail, FileText, Terminal } from 'lucide-react';
import { useState, useEffect } from 'react';

export default function Hero() {
  const [typedText, setTypedText] = useState('');
  const roles = ['Cybersecurity Enthusiast', 'Frontend Developer', 'Penetration Tester', 'Ethical Hacker'];
  const [roleIndex, setRoleIndex] = useState(0);

  useEffect(() => {
    const currentRole = roles[roleIndex];
    let currentIndex = 0;
    const typingInterval = setInterval(() => {
      if (currentIndex <= currentRole.length) {
        setTypedText(currentRole.slice(0, currentIndex));
        currentIndex++;
      } else {
        clearInterval(typingInterval);
        setTimeout(() => {
          setRoleIndex((prev) => (prev + 1) % roles.length);
        }, 2000);
      }
    }, 100);

    return () => clearInterval(typingInterval);
  }, [roleIndex]);

  return (
    <section id="home" className="relative min-h-screen flex items-center justify-center overflow-hidden pt-20">
      <div className="blob-container">
        <div className="blob blob-1"></div>
        <div className="blob blob-2"></div>
      </div>

      <div className="container mx-auto px-6 relative z-10">
        <div className="grid md:grid-cols-2 gap-12 items-center">
          <div className="space-y-8 fade-in">
            <div className="inline-flex items-center space-x-2 bg-tertiary/50 backdrop-blur-sm px-4 py-2 rounded-full border border-accent-teal/30">
              <Terminal className="w-4 h-4 text-accent-teal" />
              <span className="text-sm text-text-secondary">Available for opportunities</span>
            </div>

            <h1 className="text-5xl md:text-7xl font-bold leading-tight">
              Hi, I'm <span className="gradient-text">Nitesh</span>
            </h1>

            <div className="flex items-center space-x-3">
              <span className="text-2xl md:text-3xl text-text-secondary">{'<'}</span>
              <h2 className="text-2xl md:text-3xl text-accent-teal font-mono min-h-[2.5rem]">
                {typedText}
                <span className="animate-pulse">|</span>
              </h2>
              <span className="text-2xl md:text-3xl text-text-secondary">{'/>'}</span>
            </div>

            <p className="text-lg text-text-secondary leading-relaxed max-w-xl">
              Computer Engineer specializing in penetration testing, vulnerability assessment, and secure web development.
              Passionate about building secure, scalable applications and identifying security vulnerabilities.
            </p>

            <div className="flex flex-wrap gap-4">
              <a href="#contact" className="btn-primary">
                Get In Touch
              </a>
              <a href="/Nitesh_Sawardekar_Resume.pdf" download className="btn-secondary flex items-center space-x-2">
                <FileText className="w-5 h-5" />
                <span>Download CV</span>
              </a>
            </div>

            <div className="flex items-center space-x-6">
              <a
                href="https://github.com"
                target="_blank"
                rel="noopener noreferrer"
                className="text-text-muted hover:text-accent-teal transition-colors transform hover:scale-110"
              >
                <Github className="w-6 h-6" />
              </a>
              <a
                href="https://linkedin.com"
                target="_blank"
                rel="noopener noreferrer"
                className="text-text-muted hover:text-accent-teal transition-colors transform hover:scale-110"
              >
                <Linkedin className="w-6 h-6" />
              </a>
              <a
                href="mailto:your.email@example.com"
                className="text-text-muted hover:text-accent-teal transition-colors transform hover:scale-110"
              >
                <Mail className="w-6 h-6" />
              </a>
            </div>
          </div>

          <div className="relative fade-in">
            <div className="hero-image-frame">
              <img
                src="/root/IMG_20251008_163230.jpg"
                alt="Nitesh Sawardekar"
                className="w-full h-auto object-cover"
              />
            </div>
            <div className="absolute -bottom-6 -right-6 bg-gradient-to-r from-accent-teal to-accent-purple p-6 rounded-lg shadow-2xl">
              <p className="text-4xl font-bold">5+</p>
              <p className="text-sm text-text-secondary">Projects Completed</p>
            </div>
          </div>
        </div>
      </div>

      <a
        href="#about"
        className="absolute bottom-8 left-1/2 transform -translate-x-1/2 animate-bounce"
      >
        <ArrowDown className="w-8 h-8 text-accent-teal" />
      </a>
    </section>
  );
}
