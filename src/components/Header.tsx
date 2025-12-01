import { useState, useEffect } from 'react';
import { Menu, X, Shield, Moon, Sun } from 'lucide-react';

interface HeaderProps {
  isDark?: boolean;
  toggleTheme?: () => void;
}

export default function Header({ isDark = true, toggleTheme }: HeaderProps) {
  const [isScrolled, setIsScrolled] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 50);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const navItems = [
    { label: 'Home', href: '#home' },
    { label: 'About', href: '#about' },
    { label: 'Skills', href: '#skills' },
    { label: 'Experience', href: '#experience' },
    { label: 'Projects', href: '#projects' },
    { label: 'Blog', href: '#blog' },
    { label: 'Contact', href: '#contact' },
  ];

  return (
    <header
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
        isScrolled ? 'bg-secondary/95 backdrop-blur-md shadow-lg' : 'bg-transparent'
      }`}
    >
      <nav className="container mx-auto px-6 py-4">
        <div className="flex items-center justify-between">
          <a href="#home" className="flex items-center space-x-2 group">
            <Shield className="w-8 h-8 text-accent-teal group-hover:rotate-12 transition-transform" />
            <span className="text-xl font-bold gradient-text">Dead Coder</span>
          </a>

          <div className="hidden md:flex items-center space-x-8">
            {navItems.map((item) => (
              <a
                key={item.href}
                href={item.href}
                className="text-text-secondary hover:text-accent-teal transition-colors duration-300 font-medium relative group"
              >
                {item.label}
                <span className="absolute bottom-0 left-0 w-0 h-0.5 bg-accent-teal group-hover:w-full transition-all duration-300"></span>
              </a>
            ))}
            {toggleTheme && (
              <button
                onClick={toggleTheme}
                className="p-2 rounded-lg bg-tertiary hover:bg-accent-teal/20 transition-colors"
                aria-label="Toggle theme"
              >
                {isDark ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
              </button>
            )}
          </div>

          <button
            className="md:hidden p-2 rounded-lg bg-tertiary hover:bg-accent-teal/20 transition-colors"
            onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
            aria-label="Toggle menu"
          >
            {isMobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </div>

        {isMobileMenuOpen && (
          <div className="md:hidden mt-4 py-4 space-y-4 bg-secondary/95 backdrop-blur-md rounded-lg">
            {navItems.map((item) => (
              <a
                key={item.href}
                href={item.href}
                className="block px-4 py-2 text-text-secondary hover:text-accent-teal hover:bg-tertiary/50 rounded transition-colors"
                onClick={() => setIsMobileMenuOpen(false)}
              >
                {item.label}
              </a>
            ))}
            {toggleTheme && (
              <button
                onClick={() => {
                  toggleTheme();
                  setIsMobileMenuOpen(false);
                }}
                className="w-full px-4 py-2 text-left text-text-secondary hover:text-accent-teal hover:bg-tertiary/50 rounded transition-colors flex items-center space-x-2"
              >
                {isDark ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
                <span>Toggle Theme</span>
              </button>
            )}
          </div>
        )}
      </nav>
    </header>
  );
}
